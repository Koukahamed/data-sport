"""
Module sqlachemy table
"""

from sqlalchemy import (Column, Date, Float, Integer, MetaData,
                        PrimaryKeyConstraint, String, Table)

metadata = MetaData()

seances_musculation_table = Table(
    "seances_musculation",
    metadata,
    Column("date", Date, nullable=False),
    Column("exercice", String, nullable=False),
    Column("series", Integer, nullable=False),
    Column("repetitions", Integer, nullable=False),
    Column("poids_kg", Float, nullable=False),
    PrimaryKeyConstraint("date", "exercice"),
)

# test