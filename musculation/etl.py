import os

import pandas as pd
from model import seances_musculation_table
from pg_helpers.db_manager import DBManager
from sqlalchemy import MetaData, Table


class ETLSeanceMuscu:
    def __init__(self, db_url):
        self.db_manager = DBManager(db_url, verbose=True)

    def extract(self):
        path = "musculation/resources/seances.csv"
        df = pd.read_csv(path)
        print(f"Extracted {len(df)} rows")
        return df

    def transform(self, df):
        df_clean = df.dropna()
        print(f"Transformed dataframe to {len(df_clean)} rows after cleaning")
        return df_clean

    def load(self, df):
        # Crée la table si elle n'existe pas
        seances_musculation_table.metadata.create_all(self.db_manager.pg_engine)
        success = self.db_manager.insert_in_table(seances_musculation_table, df)
        if success:
            print(f"Loaded {len(df)} rows into database")
        else:
            print("Failed to load data")


if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    etl = ETLSeanceMuscu(db_url)
    df = etl.extract()
    df = etl.transform(df)
    etl.load(df)
