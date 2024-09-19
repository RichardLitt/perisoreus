import pandas as pd

# Load the dataset (assuming it's a tab-delimited file)
df = pd.read_csv('ebd_sicjay1_relJul-2024.txt', delimiter='\t')

# Extract the 'TRIP COMMENTS' and 'SPECIES COMMENTS' columns
comments_df = df[['TRIP COMMENTS', 'SPECIES COMMENTS']]

# Display the entries in both columns
print(comments_df.dropna(how='all'))  # Drop rows where both columns are NaN

# Save the filtered data to a new file
comments_df.dropna(how='all').to_csv('comments_output.txt', sep='\t', index=False)

