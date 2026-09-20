import pandas as pd

class AnimeDataLoader:
    def __init__(self, original_csv: str, processed_csv: str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        # 1. Read the CSV and drop empty rows
        df = pd.read_csv(self.original_csv, encoding='utf-8', on_bad_lines='skip').dropna()

        # 2. Check if the required columns exist
        required_cols = {'Name', 'Genres', 'sypnopsis'}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError("Missing column in CSV File")
        
        # 3. Combine the text into one clean column
        df['combined_info'] = (
            "Title: " + df["Name"] + " Overview: " + df["sypnopsis"] + " Genres: " + df["Genres"]
        )

        # 4. Save the cleaned data to a new file
        df[['combined_info']].to_csv(self.processed_csv, index=False, encoding='utf-8')
        return self.processed_csv
