 
"""
Hauptskript für die Interaktion mit der Tableau Server REST API.

Dieses Skript steuert den Prozess der Anmeldung am Tableau Server, das Abrufen aller Sites und das Sammeln von Benutzerinformationen,
einschließlich des letzten Logins. Benutzer, die sich seit mehr als 90 Tagen nicht angemeldet haben, werden identifiziert,
und ihre Daten werden für weitere Aktionen ausgegeben.

"""

from tableau_api import tableau_sign_in, get_all_sites, get_users_and_last_login
from config import *
from logger import setup_logging
from datetime import datetime, timedelta
import base64
from database import create_db_connection, update_or_insert_user_data

logger = setup_logging()

def is_more_than_90_days(last_login_date):
    """
        Überprüft, ob das Datum des letzten Logins mehr als 90 Tage zurückliegt.

        :param last_login_date: Das Datum des letzten Logins im Format "YYYY-MM-DDTHH:MM:SSZ".
        :return: True, wenn das Datum mehr als 90 Tage zurückliegt oder kein Datum vorhanden ist, sonst False.

    """
    try:
        if not last_login_date:
            return True  # Kein lastLogin vorhanden, Benutzer einschließen
        last_login_datetime = datetime.strptime(last_login_date, "%Y-%m-%dT%H:%M:%SZ")
        return datetime.now() - last_login_datetime > timedelta(days=90)
    except Exception as e:
        logger.error(f"Fehler bei der Überprüfung des Datums: {e}")
        return False

def tableau_server_login():
    """Meldet den Benutzer am Tableau Server an und gibt das Token zurück."""
    try:
        token, _ = tableau_sign_in(SERVER_NAME, VERSION, PERSONAL_ACCESS_TOKEN_NAME, PERSONAL_ACCESS_TOKEN_SECRET)
        return token
    except Exception as e:
        logger.error(f"Fehler bei der Anmeldung am Tableau Server: {e} , prüfen die Gültigkeit von PERSONAL_ACCESS_TOKEN_SECRET ")
        return None

def fetch_all_sites(token):
    """Ruft alle Sites vom Tableau Server ab."""
    try:
        sites = get_all_sites(SERVER_NAME, VERSION, token)
        return sites
    except Exception as e:
        logger.error(f"Fehler beim Abrufen aller Sites: {e}")
        return []

def process_users_for_site(site, token):
    """Verarbeitet Benutzer für eine gegebene Site."""
    try:
        logger.info(f"Versuche, sich bei Site anzumelden: {site['name']}")
        site_token, site_id = tableau_sign_in(SERVER_NAME, VERSION, PERSONAL_ACCESS_TOKEN_NAME, PERSONAL_ACCESS_TOKEN_SECRET, site['contentUrl'])
        users = get_users_and_last_login(SERVER_NAME, VERSION, site_token, site_id)
        return users
    except Exception as e:
        logger.error(f"Fehler bei der Verarbeitung von Benutzern für Site {site['name']}: {e}")
        return []

def filter_and_update_user_data(users, user_data, site):
    """Filtert und aktualisiert Benutzerdaten basierend auf dem letzten Login."""
    for user in users:
        user_name = user['name']
        last_login = user.get('lastLogin')
        site_role = user['siteRole']
        if is_more_than_90_days(last_login) or last_login is None:
            if user_name not in user_data:
                user_data[user_name] = {'name': user_name, 'lastLogin': last_login, 'sites': [site['name']], 'siteRole': site_role}
            else:
                user_data[user_name]['sites'].append(site['name'])
                if last_login and (not user_data[user_name]['lastLogin'] or last_login > user_data[user_name]['lastLogin']):
                    user_data[user_name]['lastLogin'] = last_login
    return user_data

def insert_users_into_database(sorted_users):
    """Fügt sortierte Benutzer in die Datenbank ein."""
    connection = create_db_connection()
    if connection:
        for user in sorted_users:
            update_or_insert_user_data(connection, user['name'], user['lastLogin'], user['siteRole'])
        connection.close()

def main():
    """Hauptfunktion, die den Prozess steuert."""
    try:
        token = tableau_server_login()
        sites = fetch_all_sites(token)
        user_data = {}
        for site in sites:
            users = process_users_for_site(site, token)
            user_data = filter_and_update_user_data(users, user_data, site)

        sorted_users = sorted(user_data.values(), key=lambda x: (x['lastLogin'] is None, x['lastLogin']), reverse=True)
        insert_users_into_database(sorted_users)

        # Ausgabe der sortierten Benutzerdaten
        for user in sorted_users:
            print(f"Name: {user['name']}, Letzter Login: {user['lastLogin']}, Site-Rolle beim letzten Login: {user['siteRole']}")
        print(f"Anzahl einzigartiger Benutzer: {len(sorted_users)}")

    except Exception as e:
        logger.error(f"Ein Fehler ist aufgetreten: {e}")
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()




