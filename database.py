import MySQLdb
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_SCHEMA

def create_db_connection():
    """Stellt eine Verbindung zur Datenbank her."""
    try:
        connection = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            db=DB_NAME
        )
        print("Datenbankverbindung erfolgreich hergestellt.")
        return connection
    except MySQLdb.Error as err:
        print(f"Fehler beim Herstellen der Datenbankverbindung: {err}")
        return None


from datetime import datetime

def update_or_insert_user_data(connection, user_name, last_login, site_role):
    """Aktualisiert oder fügt Benutzerdaten in die Datenbank ein, basierend auf den angegebenen Bedingungen."""
    cursor = connection.cursor()
    # Überprüfen, ob der Benutzer bereits existiert
    check_query = """
    SELECT lastlogin FROM tableau_user_data WHERE fullname = %s
    """
    cursor.execute(check_query, (user_name,))
    result = cursor.fetchone()

    if result:
        # Benutzer existiert, überprüfen Sie das Datum von lastlogin
        existing_last_login = result[0]
        if last_login and (existing_last_login is None or datetime.strptime(last_login, "%Y-%m-%d %H:%M:%S") > existing_last_login):
            # Aktualisieren Sie lastlogin und siterole, wenn das neue Datum neuer ist
            update_query = """
            UPDATE tableau_user_data SET lastlogin = %s, siterole = %s WHERE fullname = %s
            """
            try:
                cursor.execute(update_query, (last_login, site_role, user_name))
                connection.commit()
                print(f"User {user_name}'s lastlogin and siterole updated successfully.")
            except Exception as err:
                print(f"Error: '{err}'.")
    else:
        # Benutzer existiert nicht, fügen Sie einen neuen Eintrag hinzu
        insert_query = """
        INSERT INTO tableau_user_data (fullname, lastlogin, siterole)
        VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (user_name, last_login, site_role))
            connection.commit()
            print(f"User {user_name} added successfully.")
        except Exception as err:
            print(f"Error: '{err}'.")
        finally:
            cursor.close()
