# import h5py

# # Open the HDF5 file in read mode
# file_path = "/home/vedant/data/subject_1/trial_1.h5"  # Replace with your file path
# with h5py.File(file_path, "r") as h5_file:
#     # List all top-level groups and datasets
#     print("Contents of the HDF5 file:")
#     def print_structure(name, obj):
#         print(name, ":", "Group" if isinstance(obj, h5py.Group) else "Dataset")
    
#     h5_file.visititems(print_structure)


# with h5py.File(file_path, "r") as h5_file:

#     dataset_name = "TrialData/elapsed_time"  # Replace with actual dataset name
#     if dataset_name in h5_file:
#         data = h5_file[dataset_name][:]
#         print(f"Data from {dataset_name}:")
#         print(data)
#     else:
#         print(f"Dataset {dataset_name} not found!")



# import h5py
# import pandas as pd
# import numpy as np

# # Open HDF5 file
# file_path = "/home/vedant/data/subject_1/trial_1.h5"  # Replace with your actual file path
# csv_path = "/home/vedant/data/subject_1/output.csv"  # Output CSV file

# with h5py.File(file_path, "r") as h5_file:
#     group_name = "TrialData"  # The group containing datasets
#     data_dict = {}

#     for dataset_name in h5_file[group_name]:
#         data = h5_file[f"{group_name}/{dataset_name}"][:]

#         # Check if the dataset is multi-dimensional
#         if data.ndim > 1:
#             # Flatten the data
#             data = data.reshape(data.shape[0], -1)  # Convert to 2D (if not already)
            
#             # Create separate columns for multi-dimensional arrays
#             for i in range(data.shape[1]):
#                 data_dict[f"{dataset_name}_{i}"] = data[:, i]
#         else:
#             data_dict[dataset_name] = data  # 1D array, store as is

#     # Convert to Pandas DataFrame
#     df = pd.DataFrame(data_dict)

#     # Save to CSV
#     df.to_csv(csv_path, index=False)

# print(f"CSV saved as {csv_path}")


import h5py
import pandas as pd
import numpy as np

# Open HDF5 file
file_path = "/home/vedant/data/subject_1/trial_1.h5"  # Replace with your actual file path
csv_path = "/home/vedant/data/subject_1/output.csv"  # Output CSV file

with h5py.File(file_path, "r") as h5_file:
    group_name = "TrialData"  # The group containing datasets
    data_dict = {}

    for dataset_name in h5_file[group_name]:
        data = h5_file[f"{group_name}/{dataset_name}"][:]

        # Check if the dataset is multi-dimensional
        if data.ndim > 1:
            # Flatten the data
            data = data.reshape(data.shape[0], -1)  # Convert to 2D (if not already)

            # Create separate columns for multi-dimensional arrays
            for i in range(data.shape[1]):
                data_dict[f"{dataset_name}_{i}"] = pd.Series(data[:, i]) # Store as pandas Series
        else:
            data_dict[dataset_name] = pd.Series(data)  # Store as pandas Series

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data_dict)

    # Save to CSV
    df.to_csv(csv_path, index=False)

print(f"CSV saved as {csv_path}")
