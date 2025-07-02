"""
Model module defining the seances_musculation table for musculation sessions.
"""

from sqlalchemy import Column, Float, Integer, MetaData, String, Table

metadata = MetaData(schema="public")

seances_musculation_table = Table(
    "seances_musculation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, comment="Primary key"),
    Column("exercice", String, comment="Exercise name"),
    Column("series", Integer, comment="Number of series"),
    Column("repetitions", Integer, comment="Number of repetitions"),
    Column("poids_kg", Float, comment="Weight in kilograms"),
    comment="Table to store musculation session details",
)
