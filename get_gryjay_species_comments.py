import pandas as pd

# Load the data into a pandas DataFrame
# Change this as needed for your own file export from eBird
file_path = 'ebd_gryjay_smp_relJul-2024.txt'

# Reading the text file (assuming it's tab-separated)
df = pd.read_csv(file_path, sep='\t')

# Count the number of rows where SPECIES COMMENTS is not empty
comments_count = df[['SPECIES COMMENTS', 'TRIP COMMENTS']].apply(lambda x: x.str.strip().notna() & (x.str.strip() != ''), axis=1).any(axis=1).sum()

print(f"Number of rows with text in the 'SPECIES COMMENTS' field: {species_comments_count}")

