"""
ETL module to create muscu table
"""

import os
import re
from datetime import date

import pandas as pd
from pg_helpers.db_manager import DBManager

from .model import seances_musculation_table


class ETLSeanceMuscu:
    """
    Classe pour exécuter un ETL sur des séances de musculation.
    """

    def __init__(self, db_url):
        self.db_manager = DBManager(db_url, verbose=True)

    def extract(self):
        """Lit le fichier CSV et retourne le DataFrame et son nom de fichier."""

        path = "musculation/resources/seances_juin25.csv"
        # Essayez de spécifier l'encodage si nécessaire
        df = pd.read_csv(path, sep=",", encoding="utf-8")
        print(f"Extracted {len(df)} rows")
        print(f"Columns found: {list(df.columns)}")
        return df, os.path.basename(path)

    def transform(self, df: pd.DataFrame, file_name: str) -> pd.DataFrame:
        """Transforme les données brutes du CSV en données nettoyées et typées."""

        # Extraire mois et année depuis le nom du fichier
        match = re.search(r"seances_(\w+)(\d{2})", file_name)
        if not match:
            raise ValueError(
                "Le nom du fichier ne respecte pas le format attendu 'seances_moisAA.csv'"
            )
        mois_str = match.group(1).lower()  # ex: "juin"
        annee_suffix = match.group(2)  # ex: "25"

        mois_dict = {
            "janvier": 1,
            "fevrier": 2,
            "mars": 3,
            "avril": 4,
            "mai": 5,
            "juin": 6,
            "juillet": 7,
            "aout": 8,
            "septembre": 9,
            "octobre": 10,
            "novembre": 11,
            "decembre": 12,
        }

        if mois_str not in mois_dict:
            raise ValueError(f"Mois '{mois_str}' non reconnu")

        mois = mois_dict[mois_str]
        annee = 2000 + int(annee_suffix)

        df_clean = df.dropna()

        # Construire la vraie date (colonne "Date" dans ton CSV)
        df_clean["date"] = df_clean["Date"].apply(lambda d: date(annee, mois, int(d)))

        df_clean = df_clean.rename(
            columns={
                "Exercice": "exercice",
                "Séries": "series",
                "Répétitions": "repetitions",
                "Poids (kg)": "poids_kg",
            }
        )

        df_clean = df_clean[["date", "exercice", "series", "repetitions", "poids_kg"]]

        df_clean["series"] = df_clean["series"].astype(int)
        df_clean["repetitions"] = df_clean["repetitions"].astype(int)
        df_clean["poids_kg"] = df_clean["poids_kg"].astype(float)

        print(
            f"Transformed dataframe with {len(df_clean)} rows, month={mois}, year={annee}"
        )
        return df_clean

    def load(self, df: pd.DataFrame) -> None:
        """Charge les données dans la base de données PostgreSQL."""

        if not self.db_manager.table_exists(seances_musculation_table):
            self.db_manager.create_table(seances_musculation_table)
        self.db_manager.insert_in_table(seances_musculation_table, df)


if __name__ == "__main__":
    DB_URL = (
        "postgresql://postgres.rmleutpuvrtumkpzsigy:uqn8mkOzxt743NTO"
        "@aws-0-eu-west-3.pooler.supabase.com:5432/postgres"
    )
    etl = ETLSeanceMuscu(DB_URL)
    # testons encore
    extracted_df, filename = etl.extract()
    df_transform = etl.transform(extracted_df, filename)
    etl.load(df_transform)
