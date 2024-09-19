import os
import sys
import re
import pandas as pd

def get_unique_recordists_from_file(csv_file):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Compile regex patterns
        patterns = ['mimic', 'imitat']
        regex_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

        # List to store matching recordists
        matching_recordists = []

        # Iterate through each row in the DataFrame
        for _, row in df.iterrows():
            mlno = row.get('ML Catalog Number', '')
            media_notes = row.get('Media notes', '')
            checklist_notes = row.get('Observation Details', '')
            checklist_id = row.get('eBird Checklist ID', '')
            recordist = row.get('Recordist', None)

            matched_term = None

            # Check if any pattern matches the media_notes
            for regex in regex_patterns:
                if regex.search(str(media_notes)):  # Ensure media_notes is treated as a string
                    matched_term = regex.pattern
                    break  # Stop after the first match

            # If matched term and the same term does NOT match in checklist_notes
            if matched_term and checklist_id and not re.search(matched_term, str(checklist_notes), re.IGNORECASE):
                if recordist:
                    matching_recordists.append(recordist)

        return matching_recordists

    except Exception as e:
        print(f"Error processing file {csv_file}: {e}")
        return []

def get_unique_recordists_from_directory(directory):
    # Set to store unique recordists across all files (deduplicates automatically)
    unique_recordists_set = set()

    # Loop through all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")

            # Get unique recordists from the current file
            recordists = get_unique_recordists_from_file(file_path)

            # Add the unique recordists to the set (to deduplicate across all files)
            unique_recordists_set.update(recordists)

    return unique_recordists_set

def sort_recordists_by_last_name(recordists_set):
    # Helper function to extract the last name from the full name
    def get_last_name(name):
        return name.split()[-1] if isinstance(name, str) else ""

    # Sort recordists by their last name
    return sorted(recordists_set, key=get_last_name)

if __name__ == "__main__":
    # Get the directory from the command line argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory")
        sys.exit(1)

    # Get unique recordists from all files in the directory
    unique_recordists_set = get_unique_recordists_from_directory(directory_path)

    # Sort the recordists by last name
    sorted_recordists = sort_recordists_by_last_name(unique_recordists_set)

    # Print the deduplicated and sorted recordists
    print("Deduplicated and Sorted Unique Recordists:")
    for recordist in sorted_recordists:
        print(recordist)
