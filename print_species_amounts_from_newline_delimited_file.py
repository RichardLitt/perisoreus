import pandas as pd

# Read the entire dataset
df = pd.read_csv('strings.csv', header=None)

strings = df[0].astype(str).str.split(',', expand=True).stack().str.strip()

# Count the frequencies
frequency = strings.value_counts()

# Print the frequencies
print(frequency)


# Format the output
formatted_output = ', '.join(f"{value} ({count})" for value, count in frequency.items())

# Print the formatted output
print(formatted_output)