from dotenv import load_dotenv
import os
import psycopg2
from datetime import datetime

# Importation des varaiables d'environnement
load_dotenv(r'../../.env')
path_donnees = os.getenv("PATH_DONNEES")
nom_base_de_donnees = os.getenv("NOM_BASES_DONNEES")
utilisateur = os.getenv("USERAZURE")
mot_de_passe = os.getenv("PASSWORD")   
host = os.getenv("HOST")
port = os.getenv("PORT")

def connect_to_db():
    """Connecte à la base de données."""
    try:
        connexion = psycopg2.connect(
            dbname=nom_base_de_donnees,
            user=utilisateur,
            password=mot_de_passe,
            host=host,
            port=port
        )
        print("Connexion réussie à la base de données")
        return connexion
    except psycopg2.Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        return None
    
def create_schema(connexion, schema_name):
    '''Crée un schéma dans la base de données s'il n'existe pas.'''
    try:
        curseur = connexion.cursor()
        curseur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        connexion.commit()
        curseur.close()
        print(f"Schéma '{schema_name}' créé (ou déjà existant).")
    except psycopg2.Error as e:
        print(f"Erreur lors de la création du schéma '{schema_name}': {e}")
    except Exception as e:
        print(f"Erreur inconnue lors de la création du schéma '{schema_name}': {e}")
    finally:
        if 'curseur' in locals():
            curseur.close()

def create_table_logs(connexion, schema_name):
    '''Crée une table dans la base de données.'''
    table_name = "logs"
    try:
        curseur = connexion.cursor()
        # Définir le schéma
        curseur.execute(f"SET search_path TO {schema_name}")
        # Création de la table si elle n'existe pas
        curseur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id SERIAL PRIMARY KEY,
            level TEXT,
            message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        connexion.commit()
        curseur.close()
        print(f"Table '{table_name}' créée (ou déjà existante) dans le schéma '{schema_name}'.")
    except psycopg2.Error as e:
        print(f"Erreur lors de la création de la table '{table_name}': {e}")
    except Exception as e:
        print(f"Erreur inconnue lors de la création de la table '{table_name}': {e}")
    finally:
        if 'curseur' in locals():
            curseur.close()

def write_msg_DB(level, message, schema_name="vocalweather"):
    """Enregistre un message de log dans la base de données."""
    connexion = connect_to_db()
    curseur = connexion.cursor()
    
    create_schema(connexion, schema_name)
    create_table_logs(connexion, schema_name)
    
    # Définir le schéma
    curseur.execute(f"SET search_path TO {schema_name}")
    
    # Insertion du log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    curseur.execute("INSERT INTO logs (level, message, timestamp) VALUES (%s, %s, %s)", 
                   (level, message, timestamp))
    
    connexion.commit()
    curseur.close()
    connexion.close()


#if __name__ == "__main__":
    #Utilisation de la fonction write_msg_DB
    #write_msg_DB("INFO", "Démarrage du programme")
