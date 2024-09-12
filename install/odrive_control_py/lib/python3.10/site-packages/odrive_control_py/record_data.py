import zipfile
import os
import sqlite3
import pandas as pd

# Define the path to the uploaded zip file and extraction directory
zip_file_path = '~/gaitlab_ws/my_talker_bag1.zip'
extraction_dir = '~/gaitlab_ws/my_talker_bag1'

# Extract the contents of the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_dir)

# List the extracted files to understand the contents
extracted_files = os.listdir(extraction_dir)

# The extracted directory contains a subdirectory named 'my_talker_bag1'
# Let's list the contents of this subdirectory
subdir_path = os.path.join(extraction_dir, 'my_talker_bag1')
subdir_files = os.listdir(subdir_path)

# Define the path to the .db3 file and the output CSV file
db3_file_path = os.path.join(subdir_path, 'my_talker_bag1_0.db3')
csv_file_path = '/mnt/data/my_talker_bag1.csv'

# Connect to the SQLite database and read the messages table
conn = sqlite3.connect(db3_file_path)
query = "SELECT * FROM messages"
df = pd.read_sql(query, conn)

# Save the dataframe to a CSV file
df.to_csv(csv_file_path, index=False)

# Close the database connection
conn.close()

# Output the path to the CSV file
csv_file_path
