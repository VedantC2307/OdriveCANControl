import h5py
import pandas as pd
import numpy as np
import os
import argparse
import glob
import sys

def convert_h5_to_csv(input_file, output_file=None, verbose=False):
    """
    Convert HDF5 file to CSV
    
    Args:
        input_file: Path to HDF5 file
        output_file: Path to output CSV file (optional)
        verbose: Whether to print detailed information
    """
    if output_file is None:
        # Create output filename based on input filename
        output_file = os.path.splitext(input_file)[0] + '.csv'
    
    print(f"Converting {input_file} to {output_file}")
    
    try:
        with h5py.File(input_file, "r") as h5_file:
            # If verbose, print the file structure
            if verbose:
                print("HDF5 file structure:")
                def print_attrs(name, obj):
                    print(f"  {name} ({type(obj).__name__})")
                    if hasattr(obj, 'attrs'):
                        for key, val in obj.attrs.items():
                            print(f"    Attribute: {key} = {val}")
                    if hasattr(obj, 'shape') and isinstance(obj, h5py.Dataset):
                        print(f"    Shape: {obj.shape}, Dtype: {obj.dtype}")
                
                h5_file.visititems(print_attrs)
            
            group_name = "TrialData"  # The group containing datasets
            data_dict = {}
            
            # First check if the expected group exists
            if group_name not in h5_file:
                print(f"Error: Group '{group_name}' not found in {input_file}")
                if verbose:
                    print("Available groups/datasets:")
                    for name in h5_file:
                        print(f"  {name}")
                return False

            # Get the datasets from the group
            datasets = list(h5_file[group_name].keys())
            
            if verbose:
                print(f"Found datasets: {datasets}")
                
            if not datasets:
                print(f"Warning: No datasets found in group '{group_name}'")
                return False

            for dataset_name in datasets:
                try:
                    dataset = h5_file[f"{group_name}/{dataset_name}"]
                    
                    if verbose:
                        print(f"Reading dataset: {dataset_name}, shape: {dataset.shape}, dtype: {dataset.dtype}")
                    
                    # Check if dataset is empty
                    if dataset.shape[0] == 0:
                        print(f"Warning: Dataset '{dataset_name}' is empty")
                        continue
                        
                    data = dataset[:]
                    
                    # Check if the dataset is multi-dimensional
                    if data.ndim > 1:
                        # Flatten the data
                        data = data.reshape(data.shape[0], -1)  # Convert to 2D (if not already)

                        # Create separate columns for multi-dimensional arrays
                        for i in range(data.shape[1]):
                            data_dict[f"{dataset_name}_{i}"] = pd.Series(data[:, i])
                    else:
                        data_dict[dataset_name] = pd.Series(data)  # Store as pandas Series
                        
                except Exception as e:
                    print(f"Error reading dataset '{dataset_name}': {str(e)}")
                    continue

            # Make sure the data dictionary isn't empty after processing
            if not data_dict:
                print(f"Error: No data could be read from group '{group_name}' in {input_file}")
                return False
                
            # Check data lengths for consistency
            data_lengths = {k: len(v) for k, v in data_dict.items()}
            if len(set(data_lengths.values())) > 1:
                print("Warning: Inconsistent data lengths across datasets")
                for k, v in data_lengths.items():
                    print(f"  {k}: {v} records")
                
            # Convert to Pandas DataFrame
            df = pd.DataFrame(data_dict)
            
            if verbose:
                print(f"DataFrame created with shape: {df.shape}")
                print(f"Columns: {df.columns.tolist()}")
                if not df.empty:
                    print("First few rows:")
                    print(df.head())
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

            # Save to CSV
            df.to_csv(output_file, index=False, float_format='%.6f')
            
            # Verify the CSV was created successfully
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"CSV saved as {output_file} ({file_size} bytes)")
                if file_size < 100:  # Arbitrary small file size that might indicate only headers
                    print("Warning: CSV file is very small, might contain only headers")
            else:
                print(f"Error: Failed to create CSV file {output_file}")
                return False
                
            return True
    except Exception as e:
        print(f"Error processing {input_file}: {str(e)}")
        return False

def main():
    # Create command-line argument parser
    parser = argparse.ArgumentParser(description='Convert HDF5 file to CSV')
    parser.add_argument('input', nargs='?', help='Input HDF5 file or directory containing HDF5 files')
    parser.add_argument('-o', '--output', help='Output CSV file or directory')
    parser.add_argument('-a', '--all', action='store_true', help='Convert all H5 files in directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed information')
    parser.add_argument('-d', '--default', action='store_true', 
                       help='Use default data directory from data_recording_node')
    
    args = parser.parse_args()
    
    # Default data directory - match with data_recording_node.py
    default_data_dir = '/home/vedant/odrivecontrol/src/data_logging/data_logging/subject1'
    
    # If using default directory or no input provided
    if args.default or not args.input:
        if os.path.exists(default_data_dir):
            print(f"Using default data directory: {default_data_dir}")
            args.input = default_data_dir
            if not args.output:
                args.output = default_data_dir  # Save CSVs in same directory as H5 files
            if not args.all and os.path.isdir(args.input):
                args.all = True  # Process all files when using default directory
        else:
            # Try to find where data might be stored
            print(f"Default data directory {default_data_dir} does not exist.")
            possible_dirs = [
                '/home/vedant/odrivecontrol/src/data_logging/data_logging/data/subject1',
                '/home/vedant/odrivecontrol/src/data_logging/data/subject1',
                '/home/vedant/data/subject1'
            ]
            
            for dir_path in possible_dirs:
                if os.path.exists(dir_path):
                    print(f"Found alternative data directory: {dir_path}")
                    args.input = dir_path
                    if not args.output:
                        args.output = dir_path
                    args.all = True
                    break
            else:
                print("Error: Could not find data directory. Please specify input file or directory.")
                sys.exit(1)
    
    # Handle directory with -a/--all flag
    if args.all and os.path.isdir(args.input):
        input_dir = args.input
        output_dir = args.output if args.output else input_dir
        
        # Find all .h5 files
        h5_files = glob.glob(os.path.join(input_dir, '**', '*.h5'), recursive=True)
        
        if not h5_files:
            print(f"No HDF5 files found in {input_dir}")
            return
            
        print(f"Found {len(h5_files)} HDF5 files to convert")
        for h5_file in h5_files:
            # Create equivalent output path
            rel_path = os.path.relpath(h5_file, input_dir)
            output_path = os.path.join(output_dir, rel_path)
            output_path = os.path.splitext(output_path)[0] + '.csv'
            
            convert_h5_to_csv(h5_file, output_path, args.verbose)
    
    # Handle single file
    elif os.path.isfile(args.input):
        convert_h5_to_csv(args.input, args.output, args.verbose)
    
    # Special case for default behavior - look in the default data directory
    elif not os.path.exists(args.input):
        print(f"Error: Input path {args.input} does not exist")
    else:
        print(f"Error: Input path {args.input} exists but is not a file or directory")

if __name__ == "__main__":
    main()
