import pandas as pd
import os

# Path to the folder containing the files
folder_path = '/path/to/your/folder'

# List of columns you want to extract from the files
columns_to_extract = ['column1', 'column2', 'column3']

# Function to load and filter data from a file
def load_and_filter_data(file_path, columns):
    # Determine the file type and load accordingly
    if file_path.endswith('.json'):
        df = pd.read_json(file_path)
    elif file_path.endswith('.jsonl'):
        df = pd.read_json(file_path, lines=True)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xml'):
        df = pd.read_xml(file_path)
    else:
        print(f"Unsupported file format for file: {file_path}")
        return

    # Filter the DataFrame to only include specified columns
    df = df[columns]

    # Save the filtered data back to JSON
    new_file_path = os.path.splitext(file_path)[0] + '_filtered.json'
    df.to_json(new_file_path, orient='records', lines=True)
    print(f"Filtered data saved to {new_file_path}")

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        load_and_filter_data(file_path, columns_to_extract)