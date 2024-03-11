 
"""
tableau_api.py

Dieses Modul enthält Funktionen zur Interaktion mit der Tableau Server REST API. Es ermöglicht das Anmelden mit einem persönlichen Zugriffstoken, das Abrufen aller Sites auf dem Server und das Abrufen von Benutzerinformationen für eine bestimmte Site.

Verfügbare Funktionen:
- tableau_sign_in(server, version, pat_name, pat_secret, site_url_id=''): Meldet einen Benutzer am Tableau Server an und holt ein Authentifizierungstoken sowie die Site-ID.
- get_all_sites(server, version, token): Ruft eine Liste aller Sites auf dem Tableau Server ab.
- get_users_and_last_login(server, version, token, site_id): Ruft Informationen zu allen Benutzern einer bestimmten Site ab, einschließlich des letzten Logins.

"""


import requests
from config import SERVER_NAME, VERSION, PERSONAL_ACCESS_TOKEN_NAME, PERSONAL_ACCESS_TOKEN_SECRET
from logger import setup_logging

logger = setup_logging()

def tableau_sign_in(server, version, pat_name, pat_secret, site_url_id=''):
    """
        Meldet einen Benutzer am Tableau Server an und holt ein Authentifizierungstoken sowie die Site-ID.

        :param server: Der Hostname oder die IP-Adresse des Tableau Servers.
        :param version: Die Version der Tableau Server REST API.
        :param pat_name: Der Name des persönlichen Zugriffstokens.
        :param pat_secret: Das Geheimnis des persönlichen Zugriffstokens.
        :param site_url_id: Die URL-ID der Site, bei der sich der Benutzer anmelden möchte (optional).
        :return: Ein Tuple bestehend aus dem Authentifizierungstoken und der Site-ID.
        :raises requests.exceptions.HTTPError: Wenn der Anmeldeversuch fehlschlägt.

    """
    try:
        signin_url = f"http://{server}/api/{version}/auth/signin"
        payload = {
            "credentials": {
                "personalAccessTokenName": pat_name,
                "personalAccessTokenSecret": pat_secret,
                "site": {"contentUrl": site_url_id}
            }
        }
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        response = requests.post(signin_url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()
        token = data["credentials"]["token"]
        site_id = data["credentials"]["site"]["id"]
        logger.info(f"Der Benutzer hat sich erfolgreich bei Tableau Server unter {server} angemeldet.")
        return token, site_id
    except requests.exceptions.HTTPError as e:
        logger.error(f"Anmeldung bei Tableau Server auf {server} fehlgeschlagen: {e}")
        raise


def get_all_sites(server, version, token):
    """
        Ruft eine Liste aller Sites auf dem Tableau Server ab.

        :param server: Der Hostname oder die IP-Adresse des Tableau Servers.
        :param version: Die Version der Tableau Server REST API.
        :param token: Das Authentifizierungstoken, das von `tableau_sign_in` zurückgegeben wurde.
        :return: Eine Liste von Dictionaries, die Informationen zu jeder Site enthalten.
        :raises requests.exceptions.HTTPError: Wenn die Anfrage fehlschlägt.

    """
    try:
        sites_url = f"http://{server}/api/{version}/sites"
        headers = {
            'X-Tableau-Auth': token,
            'accept': 'application/json'
        }
        response = requests.get(sites_url, headers=headers, verify=False)
        response.raise_for_status()
        sites_data = response.json()
        sites = sites_data["sites"]["site"]
        logger.info(f"Alle Sites erfolgreich vom Tableau Server bei {server} abgerufen.")
        return sites
    except requests.exceptions.HTTPError as e:
        logger.error(f"Fehler beim Abrufen aller Sites vom Tableau Server bei {server}: {e}")
        raise

def get_users_and_last_login(server, version, token, site_id):
    """
        Ruft Informationen zu allen Benutzern einer bestimmten Site ab, einschließlich des letzten Logins.

        :param server: Der Hostname oder die IP-Adresse des Tableau Servers.
        :param version: Die Version der Tableau Server REST API.
        :param token: Das Authentifizierungstoken, das von `tableau_sign_in` zurückgegeben wurde.
        :param site_id: Die ID der Site, für die Benutzerinformationen abgerufen werden sollen.
        :return: Eine Liste von Benutzer-Dictionaries, die Informationen zu jedem Benutzer enthalten.
        :raises requests.exceptions.HTTPError: Wenn die Anfrage fehlschlägt.

    """
    users_url = f"http://{server}/api/{version}/sites/{site_id}/users"
    headers = {
        'X-Tableau-Auth': token,
        'accept': 'application/json'
    }
    response = requests.get(users_url, headers=headers, verify=False)
    response.raise_for_status()
    users_data = response.json()
    if 'user' in users_data.get('users', {}):
        users = users_data["users"]["user"]
    else:
        users = []  # Eine leere Liste zurückgeben, wenn kein 'user' Schlüssel vorhanden ist
    logger.info(f"Benutzerinformationen für Site-ID {site_id} erfolgreich vom Tableau Server bei {server} abgerufen.")
    return users
