# Importieren der benötigten Module für die Datenbankinteraktion und Datumsverarbeitung

import MySQLdb
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME,DB_SCHEMA
from datetime import datetime,timedelta
from logger import setup_logging

logger = setup_logging()

def is_date_more_than_90_days_ago(last_login):
    """
        Überprüft, ob das übergebene Datum mehr als 90 Tage in der Vergangenheit liegt.

        Args:
            last_login (str): Das Datum des letzten Logins im ISO 8601-Format (YYYY-MM-DDTHH:MM:SSZ).

        Returns:
            bool: True, wenn das Datum mehr als 90 Tage zurückliegt, sonst False.

    """
    if last_login is None:
        return False
    # Entfernen des 'Z' und Parsen des Datums als UTC
    last_login = last_login.rstrip('Z')
    last_login_datetime = datetime.strptime(last_login, "%Y-%m-%dT%H:%M:%S")

    # Vergleich des Datums mit dem aktuellen Datum, um zu überprüfen, ob es mehr als 90 Tage zurückliegt
    return datetime.utcnow() - last_login_datetime > timedelta(days=90)


def create_db_connection():
    """
       Stellt eine Verbindung zur MySQL-Datenbank her basierend auf den Konfigurationsparametern.

       Returns:
           MySQLdb.connections.Connection: Eine Verbindung zum Datenbankserver oder None bei einem Fehler.

    """
    try:
        connection = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASS,
            database=DB_SCHEMA
        )
        print("MySQL Database connection successful")
    except Exception as err:
        print(f"Error: '{err}'")
        connection = None
    return connection

import MySQLdb
from datetime import datetime, timedelta

def update_or_insert_user_data(connection, user_name, last_login, site_role):
    """
        Aktualisiert die Daten eines bestehenden Benutzers oder fügt einen neuen Benutzer in die Datenbank ein.

        Args:
            connection (MySQLdb.connections.Connection): Die Verbindung zur Datenbank.
            user_name (str): Der Name des Benutzers.
            last_login (str): Das letzte Login-Datum des Benutzers im ISO 8601-Format.
            site_role (str): Die Rolle des Benutzers auf der Site.

        Diese Funktion überprüft zunächst, ob ein Benutzer bereits in der Datenbank existiert.
        Wenn ja, wird das letzte Login-Datum aktualisiert, falls das neue Datum neuer ist.
        Existiert der Benutzer noch nicht, wird ein neuer Datensatz mit den Benutzerdaten eingefügt.

    """
    cursor = connection.cursor()

    # Entfernen des 'Z' und Parsen des Datums als UTC, falls last_login nicht None ist
    if last_login:
        last_login = last_login.rstrip('Z')
        last_login_datetime = datetime.strptime(last_login, "%Y-%m-%dT%H:%M:%S")
    else:
        last_login_datetime = None

    # Überprüfen, ob der Benutzer bereits existiert
    check_query = "SELECT lastlogin FROM 0003_01_tableau_user_activity WHERE fullname = %s"
    cursor.execute(check_query, (user_name,))
    result = cursor.fetchone()

    if result:
        # Benutzer existiert, überprüfen Sie das Datum von lastlogin
        existing_last_login = result[0]
        if last_login_datetime and (existing_last_login is None or last_login_datetime > existing_last_login):
            # Aktualisieren lastlogin und siterole, wenn das neue Datum neuer ist
            update_query = "UPDATE 0003_01_tableau_user_activity SET lastlogin = %s, siterole = %s WHERE fullname = %s"
            try:
                cursor.execute(update_query, (last_login_datetime, site_role, user_name))
                connection.commit()
                print(f"Lastlogin und Siterole von Benutzer {user_name} erfolgreich aktualisiert")
                logger.info(f"Lastlogin und Siterole von Benutzer {user_name} erfolgreich aktualisiert.")
            except Exception as err:
                print(f"Error: '{err}'")
                logger.error(f"Aktualisierung von {user_name} fehlgeschlagen: '{err}'")
    else:
        # Benutzer existiert nicht, fügen einen neuen Eintrag hinzu
        insert_query = "INSERT INTO 0003_01_tableau_user_activity (fullname, lastlogin, siterole) VALUES (%s, %s, %s)"
        try:
            cursor.execute(insert_query, (user_name, last_login_datetime, site_role))
            connection.commit()
            print(f"Benutzer {user_name} erfolgreich hinzugefügt")
            logger.info(f"User {user_name} added successfully.")
        except Exception as err:
            print(f"Error: '{err}'")
            logger.error(f"Einfügen von {user_name} fehlgeschlagen: '{err}'")
        finally:
            cursor.close()
