# This file can be used together with Macaulay Library data to get all instances of audio that has comments
# which match certain substrings. This is useful for when you want media comments that are not in the
# eBird checklist or the normally exported database.
# You need to export the information from ML first.

import csv
import glob
import re

# Path pattern for the CSV files
# Change this as needed for your own file export.
file_pattern = 'ML__2024-09-11T0*_gryjay_audio.csv'

patterns = ['mimic', 'imitat', ' [A_Z]{4} ', 'call', 'goshawk']
regex_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

checklist_data = {}

# Iterate through all files matching the pattern
for file_name in glob.glob(file_pattern):
    print(f"Processing file: {file_name}")

    with open(file_name, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV file
        for row in reader:
            mlno = row.get('\ufeffML Catalog Number', '')
            media_notes = row.get('Media notes', '')
            checklist_notes = row.get('Observation Details', '')
            checklist_id = row.get('eBird Checklist ID', '')

            matched_term = None

            # Check if any pattern matches the media_notes and capture the matching term
            for regex in regex_patterns:
                if regex.search(media_notes):
                    matched_term = regex.pattern
                    break  # Stop after the first match

            # If a term is matched and the same term does NOT match in checklist_notes
            if matched_term and checklist_id and not re.search(matched_term, checklist_notes, re.IGNORECASE):
                # Store checklist_id and media_notes in the dictionary
                if checklist_id not in checklist_data:
                    checklist_data[checklist_id] = {
                        "Media notes": [],
                        "ML Catalog Number": []
                    }
                checklist_data[checklist_id]['Media notes'].append(media_notes)
                print(row)
                checklist_data[checklist_id]['ML Catalog Number'].append(mlno)

# Write the checklist_id and corresponding media_notes to a CSV file
with open('checklist_media_notes.csv', mode='w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['Checklist ID', 'ML Catalog Number', 'Media Notes'])

    # Write each checklist_id and its associated ML Catalog Number and media_notes
    for checklist_id, data in checklist_data.items():
        ml_catalog_numbers = data['ML Catalog Number']
        media_notes_list = data['Media notes']

        # Zip through ML Catalog Numbers and Media Notes for each checklist_id
        for mlno, note in zip(ml_catalog_numbers, media_notes_list):
            writer.writerow([checklist_id, mlno, note])

print("Done.")

