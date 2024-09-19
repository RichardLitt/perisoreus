import os
from ebird.api import get_checklist

api_key = os.getenv('EBIRD_API_TOKEN')

checklist_ids = [
    'S77522054', 'S77728438', 'S80020866', 'S78579896', 'S80641001', 'S121352287', 
    'S101638638', 'S127871973', 'S144271103', 'S154688994', 'S150770854', 'S63054451', 
    'S64174869', 'S69803293', 'S70117454', 'S119840822', 'S125620691', 'S146571313', 
    'S139737673', 'S149394444', 'S152239877'
]

# Set to store unique user names
user_names = set()

# Loop through the checklist IDs
for checklist_id in checklist_ids:
    # Fetch the checklist details using the eBird API
    checklist = get_checklist(api_key, checklist_id)

    # Check if 'userDisplayName' exists in the checklist and store it
    if 'userDisplayName' in checklist:
        # Capitalize the name and add to set (ensures uniqueness)
        user_names.add(checklist['userDisplayName'].title())  # Capitalizes each word in the name

# Convert the set back to a list for sorting
sorted_user_names = sorted(user_names, key=lambda name: name.split()[-1])

# Print the comma-delimited list of names
print(', '.join(sorted_user_names))


# Jason Beason, Ferenc Domoki, Anthony Glenesk, Jacob Grover, William Kirsch, Alan Knue, Kim  Selbee, Brian Shulist