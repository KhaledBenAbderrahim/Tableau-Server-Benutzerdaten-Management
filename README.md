# Tableau Server Benutzerdaten-Management

![Tableau Data Engine API](https://tableaufans.com/wp-content/uploads/2014/12/679x300_dataengineapi1.jpg)


## 🌟 Über dieses Projekt

Das **Tableau Server Benutzerdaten-Management** Projekt ermöglicht es Tableau Server Administratoren, Benutzerlizenzen effizient zu verwalten. Durch das automatische Abrufen und Bereinigen von Benutzerdaten über verschiedene Sites hinweg, insbesondere das Identifizieren von Benutzern, die sich seit mehr als 90 Tagen nicht angemeldet haben, hilft dieses Tool Unternehmen, ihre Ressourcen optimal zu nutzen.

## 🚀 Hauptfunktionen

- **Anmeldung am Tableau Server**: Automatisches Anmelden mit persönlichen Zugriffstokens.
- **Abrufen aller Sites**: Auflisten aller Sites auf dem Tableau Server.
- **Sammeln von Benutzerinformationen**: Details zu Benutzern extrahieren, einschließlich des letzten Anmeldedatums.
- **Identifizieren inaktiver Benutzer**: Finden von Benutzern, die sich länger als 90 Tage nicht angemeldet haben.
- **Datenbereinigung**: Bereinigen der Daten für die weitere Verarbeitung oder Lizenzverwaltung.

## ✅ Voraussetzungen

- Python 3.6+
- Zugriff auf einen Tableau Server
- Eine MySQL-Datenbank

## 💾 Installation

Zuerst klone das Repository und installiere dann die erforderlichen Abhängigkeiten:

```bash
git clone <Repository-URL>
cd <Repository-Name>
pip install -r requirements.txt
```

## ⚙️ Konfiguration

Erstelle eine `.env` Datei im Wurzelverzeichnis und passe die Umgebungsvariablen an:

```plaintext
SERVER_NAME=dein_tableau_server
VERSION=deine_api_version
PERSONAL_ACCESS_TOKEN_NAME=dein_token_name
PERSONAL_ACCESS_TOKEN_SECRET=dein_token_secret
DB_HOST=dein_db_host
DB_USER=dein_db_user
DB_PASS=dein_db_pass
DB_NAME=dein_db_name
```

## 🚴 Ausführung

Starte den Prozess durch Ausführen des Hauptskripts:

```bash
python main.py
```


## ©️ Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.
