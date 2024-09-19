def sort_names_by_last_name(names):
    # Split each name by space and sort by the last word (last name)
    sorted_names = sorted(names, key=lambda name: name.split()[-1])
    return sorted_names

# Read names from a newline-delimited file
with open('names.txt', 'r') as file:
    names = [line.strip() for line in file.readlines()]

# Call the function and get sorted names
sorted_names = sort_names_by_last_name(names)

# Print the sorted names in comma-delimited format
print(", ".join(sorted_names))
