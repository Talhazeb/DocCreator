# DocCreator App mit Webservice und Schlüsselgenerierung

## 1. Überblick
Die DocCreator App ist ein System bestehend aus einer Desktop-Anwendung, einem Webservice zur Verifizierung und einem Skript zur Schlüsselgenerierung. Es ermöglicht das Ausfüllen von Word-Vorlagen, die Konvertierung in PDFs, digitale Signierung und optionalen Upload auf Nextcloud und die öffentliche Überprüfung, ob die Datei echt und integer ist.

## 2. Komponenten

### 2.1 Desktop-Anwendung

#### 2.1.1 Konfiguration
- Lesen der Hauptkonfiguration aus `config.ini`
- Konfigurierbare Einstellungen:
  - Pfad zum Vorlagenverzeichnis
  - Pfad zum Verzeichnis für Autoren (Signer) Daten
  - Pfad zur öffentlichen Schlüsseldatei für PDF-Signatur
  - Pfad zur geheimen Schlüseldatei für PDF Signatur
  - Archiv (optional) 
    - Nextcloud-Zugangsdaten 
    - Upload-Einstellung (true/false)
    - Dateinamen-Pattern für Upload (Standard: Vorlagenname-YYYY-MM-DD-ZZZ-NameKlient-Unterschreiber.pdf)

#### 2.1.2 Vorlagenmanagement
- Auslesen von Word-Vorlagen (.docx) aus dem konfigurierten Vorlagenverzeichnis
- Für jede Vorlage existiert eine zugehörige .ini-Datei mit:
  - Dokumentsprache
  - Variablen mit zugehörigen Fragen, um diese in der Word-Vorlage einzusetzen.

#### 2.1.3 Autorenverwaltung (Signer)
- Anlage eines Autors (Signer) mit folgenden Informationen:
  - Vollständiger Name {{SignerFullName}}
  - KurzName {{SignerShortName}}
  - E-Mail Adresse {{SignerEmail}}
  - Telefonnummer {{SignerPhone}}
  - Handynummer {{SignerMobilePhone}}
  - Role {{SignerRole}}
  - ExtraInfo1 {{SignerExtraInfo1}}
  - ExtraInfo2 {{SignerExtraInfo2}}
  - ExtraInfo3 {{SignerExtraInfo3}}
  - ExtraInfo4 {{SignerExtraInfo4}}
  - ExtraInfo5 {{SignerExtraInfo5}}
  - Unterschrift Passwort
- Upload einer PNG-Datei als Unterschrift
- Überprüfung, ob die PNG-Datei einen transparenten Hintergrund hat; Ablehnung bei fehlendem transparenten Hintergrund
- Verschlüsselung der Unterschrift-PNG mit dem angegebenen Passwort
- Speicherung der Autoreninformationen in `Signer-KurzName.ini` im konfigurierten Verzeichnis
- Speicherung der verschlüsselten Unterschrift als `Signer-KurzName-Signatur.png` im konfigurierten Verzeichnis
- Löschen eines Autors und seiner Daten nach Eingabe des korrekten Passworts (Überprüfung ob verschlüsselte PNG-Datei mit Unterschrift entschlüsselt wird und eine valide PNG Datei erstellt wurde. Falls nicht, werden die Daten nicht gelöscht und es wird eine Fehlermeldung ausgegeben.)

#### 2.1.4 PDF-Erstellung und Signierung
- Ausfüllen der ausgewählten Word-Vorlage mit den Benutzereingaben
- Erstellen einer Fingerprint String des Dokumentes, der als {{Fingerprint}} zur Verfügung steht
- Ersetzen der Variable {{VerificationURL}} in der Word-Vorlage mit der URL zur PDF-Verifikation
- Ersetzen der Variable {{SignerSignature}} in der Word-Vorlage mit der entschlüsselten Unterschrift-PNG
- Ersetzen der Variable {{CurrentDate}} in der Word-Vorlage mit dem aktuellen Datum. Das Format wird in der Vorlagen .ini Datei mit "current_date = DD.MM.YYYY" als Standard angegeben. Nutze die bekannte Platzhalter dafür.
- Ersetzen aller Signer-bezogenen Variablen ({{SignerFullName}}, {{SignerShortName}}, etc.) mit den entsprechenden Werten
- Konvertierung des ausgefüllten Word-Dokuments in PDF (ohne Word-Installation)
- Digitale Signierung des PDFs mit dem öffentlichen Schlüssel

#### 2.1.5 PDF Integritätscheck
- Überprüfung, ob das hochgeladene PDF nach der Signierung verändert wurde
- Überprüfung, ob das hochgeladene PDF mit unserem System erstellt wurde

#### 2.1.6 Nextcloud-Integration (optional)
- Upload des signierten PDFs auf Nextcloud, wenn in config.ini aktiviert
- Verwendung des konfigurierten Dateinamen-Patterns
- Dies dient als ein elektronisches Archiv

#### 2.1.7 Logging
- Implementierung von Logging mit den Levels DEBUG, INFO, WARNING, ERROR
- Ausgabe in Log-Datei und Standard Output
- DEBUG: Ausgabe aller Variablen
- INFO: Ausgabe der einzelnen Verarbeitungsschritte
- WARNING und ERROR für entsprechende Situationen

#### 2.1.8 Formulardaten-Speicherung
- Möglichkeit, den Inhalt des Formulars zu speichern mit dem Namen des Formulars
- Neuer Menüpunkt "Vorheriges Dokument weiter bearbeiten" bei vorhandenen gespeicherten Daten
- wenn altes Dokument gespeichert wurde gibt es auch den Menu Ounkt "Daten vorheriges Dokuemtn löschen", was die temporären Datein des vorherigen Formulars löscht.

### 2.2 Webservice zur PDF-Verifikation
- Python-Skript, das beim Aufruf ohne POST Daten eine HTML-Datei ausliefert, die als .thtml Datei in der config.ini konfiguriert wird. Diese HTML Datei soll eine Aufforderung zum PDF-Upload enthalten, um die Integrität und Unterschrift des PDF Dokument zu überprüfen.
- Verarbeitung des PDF-Uploads und Durchführung der Verifikation
- Konfiguration des Pfads zum geheimen Schlüssel in config.ini
- Strikte Überprüfung aller Eingaben auf möglichen Missbrauch
- Rückgabe des Verifizierungsergebnisses an den Web-Benutzer
- Darstellung der Verifizierungsergebnisse:
  - Klare, leicht verständliche Anzeige des Ergebnisses (z.B. "Verifizierung erfolgreich" oder "Verifizierung fehlgeschlagen")
  - Bei erfolgreicher Verifizierung: Anzeige relevanter Dokumentinformationen (z.B. Erstellungsdatum, Autor)
  - Bei fehlgeschlagener Verifizierung: Anzeige möglicher Gründe für den Fehlschlag
- Führen einer separaten Log-Datei für den Webservice:
  - Logging aller inhaltlich wichtigen Informationen: Datum, Uhrzeit, Dokumentenname, Verifizierungsergebnis
  - Konfigurierbarkeit des Log-Pfads in der config.ini
- Sicherheitshinweis: Der Webservice speichert zu keinem Zeitpunkt die hochgeladene PDF-Datei. Dies muss deutlich auf der HTML-Seite kommuniziert werden.

### 2.3 Skript zur Schlüsselgenerierung
- Generierung von asymmetrischen Schlüsselpaaren für die PDF-Signatur
- Speicherung des öffentlichen und privaten Schlüssels an dem in config.ini spezifizierten Ort

## 3. Benutzeroberfläche der Desktop-Anwendung

### 3.1 Hauptmenü
- Dokument (führt zur Autoren(Signer)- und Vorlagenauswahl und Formular)
- Autor (führt zur Autoren(Signer) Anlage, Bearbeitung, Löschung)
- Vorheriges Dokument weiter bearbeiten (nur wenn gespeicherte Daten vorhanden)
- Daten vorheriges Dokument löschen (nur wenn gespeicherte Daten vorhanden)

### 3.2 Dokument
- Dropdown-Menü zur Auswahl des Autors (Signer)
- Dropdown-Menü zur Auswahl der Vorlage
- Dynamisch generierte Eingabefelder basierend auf der ausgewählten Vorlage
- Passwortabfrage zur Entschlüsselung der Unterschrift
- Überprüfung der Unterschrift (Entschlüsselung der PNG)
- Möglichkeit das Dokument zu speicher, z.B. falls Passwort falsch war
- Button "PDF erstellen und signieren"
- Dialog zum Speichern des erstellten PDFs

### 3.3 Autor
- Dropdown-Menü zur Auswahl des Autors (Signer) zum Bearbeiten oder Löschen
- Knopf zur Neuanlage eines Autors (Signer)
- Bei Auswahl eines Autors (Signers) werden die Veränderungen erst gespeichert, wenn das Passwort richtig eingegeben wurde
- Bei Auswahl den Autor (Signer) zu löschen, wird erst gelöscht, wenn das Passwort richtig eingegeben wurde.

### 3.3 Dialoge
- Dialog zum Erstellen, Verädnern und Löschen eines Autors (Signer)
- Bestätigungsdialoge für wichtige Aktionen

## 4. Workflow Desktop App
1. Anzeige Hauptmenü
2. Bei Auswahl "Dokument": Weiter zu Autorauswahl, Vorlagenauswahl und Formular
3. Bei "Autor": Dialog zur Anlage, Bearbeitung und Löschung aller Autorendaten und Unterschrift-Upload, Überprüfung auf transparenten Hintergrund
5. Bei "Vorheriges Dokument weiter bearbeiten": Laden der gespeicherten temporären Formulardaten
6. Bei "Daten vorheriges Dokument löschen": Löschen der gespeicherten temporären Formulardaten
7. Bei "Beenden": das Programm beenden

## 5. Sicherheit
- Verschlüsselung der Unterschrift-PNG: Nur das korrekte Passwort entschlüsselt die Datei zu einer gültigen PNG
- Verwendung von asymmetrischer Verschlüsselung für die PDF-Signatur
- Sichere Handhabung des privaten Schlüssels für die PDF-Signatur
- Überprüfung aller Eingaben im Webservice auf möglichen Missbrauch

## 6. Erweiterbarkeit
- Modularer Aufbau für einfache Erweiterung um zusätzliche Funktionen
- Möglichkeit zur Implementierung zusätzlicher Cloud-Speicher-Integrationen

## 7. Technische Anforderungen
- Entwicklung in Python
- Verwendung von PyQt5 für die Desktop-Anwendung
- Nutzung von docx2pdf oder ähnlicher Bibliothek für Word-zu-PDF Konvertierung ohne Word-Installation
- Implementierung des Webservices mit einem Python-Web-Framework (z.B. Flask)
- Verwendung sicherer Kryptographie-Bibliotheken für Verschlüsselung und Signierung

### 8. Lieferumfang
- Desktop-Anwendung (ausführbare Datei oder Python-Skript mit Abhängigkeiten)
- Webservice zur PDF-Verifikation (Python-Skript)
- Skript zur Schlüsselgenerierung
- Dokumentation zur Installation und Nutzung (README.md)
- Beispiel-Konfigurationsdateien (config.ini, Vorlagen-ini)
- Changelog-Datei zur Dokumentation von Änderungen und Versionshistorie

## 9. Testanforderungen
- Unit-Tests für kritische Funktionen (Verschlüsselung, Signierung, PDF-Generierung)
- Integrationstests für den gesamten Workflow
- Sicherheitstests, insbesondere für den Webservice

## 10. Wartung und Support
- Regelmäßige Updates zur Behebung von Sicherheitslücken
- Dokumentation für zukünftige Erweiterungen und Anpassungen

### 11. Changelog
- Einführung einer Changelog-Datei (CHANGELOG.md) im Projektverzeichnis
- Dokumentation aller Änderungen, neuen Features und Fehlerbehebungen
- Verwendung des "Keep a Changelog" Formats (https://keepachangelog.com/)
- Versionierung nach Semantic Versioning 2.0.0 (https://semver.org/)
- Aktualisierung des Changelogs bei jedem Release oder signifikanten Update
