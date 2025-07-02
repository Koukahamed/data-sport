from sqlalchemy import Table, Column, Date, Integer, Float, String, MetaData
from sqlalchemy import PrimaryKeyConstraint


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
