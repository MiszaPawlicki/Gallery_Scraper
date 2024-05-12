import csv

def read_unique_values(csv_file):
    unique_values = set()  # Using a set to store unique rows

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            unique_values.add(tuple(row))  # Convert row to tuple to ensure uniqueness

    return unique_values

# Example usage:
csv_file = r"C:\Users\misza\OneDrive\Documents\Work\Personal Projects\Gallery Scraper\ML\training_data\exhibition_href_training.csv"  # Replace with the path to your CSV file
unique_rows = read_unique_values(csv_file)
for row in unique_rows:
    print(f"{row[0]}, {row[1]}")
