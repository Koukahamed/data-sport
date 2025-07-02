import psycopg2
from psycopg2 import OperationalError


def create_connection(db_url):
    connection = None
    try:
        connection = psycopg2.connect(db_url)
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


# Remplacez le mot de passe dans l'URL par le vrai mot de passe
db_url = "postgresql://postgres.rmleutpuvrtumkpzsigy:uqn8mkOzxt743NTO@aws-0-eu-west-3.pooler.supabase.com:5432/postgres"

connection = create_connection(db_url)

# Exemple d'exécution d'une requête simple
if connection:
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    # N'oubliez pas de fermer la connexion
    cursor.close()
    connection.close()
