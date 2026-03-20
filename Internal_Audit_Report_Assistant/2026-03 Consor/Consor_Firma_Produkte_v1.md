# Consor (Consor AG) — Firmen- & Produktbeschreibung (für ISO 27001 Kontext)

## 1) Kurzprofil
Consor ist ein in Zürich ansässiges Softwareunternehmen (gegründet 2001), das sich auf Lösungen für Versicherungsgesellschaften spezialisiert. Der Fokus liegt auf Underwriting- und Policy-Management-Software für Industrie-, Unternehmens-, Individual- und Spezialversicherungen im deutschsprachigen Raum. Das Kernprodukt ist **Consor Universal**, eine **Low-Code-Plattform** zur Modellierung und Automatisierung von Underwriting-, Policierungs- und Vertragsänderungsprozessen. Consor bietet Consor Universal sowohl als **klassische Softwarelösung** als auch als **Cloud-Service (SaaS)** an und übernimmt im SaaS-Modell Betrieb und Support.

**Positionierung / Markt**
- Consor positioniert Consor Universal als führende Underwriting-Software im Segment Industrie-/Unternehmensversicherung.
- Fokus auf Industrie-, Individual- und Spezialversicherung sowie Corporate-/Commercial-Lines im deutschsprachigen Raum.

## 2) Zielkunden & Einsatzdomäne
**Zielgruppe**
- Komposit-/P&C-Versicherer, Corporate-/Industrial-Lines-Einheiten, Specialty Lines
- Underwriting-Organisationen inkl. Risikoingenieure, Firmenkundenberater, Underwriter, Produktmanagement
- Versicherer in der Schweiz und Deutschland

**Typische Anwendungsfälle**
- Risikoanalyse & Risikobewertung (qualitativ/quantitativ)
- Angebotserstellung/Quoting, Policierung, Vertragsänderungen/Mutationen
- Abbildung komplexer Vertragskonstrukte (z. B. Kollektiv-, Rahmenverträge, internationale Programme)
- Unterstützung von Embedded-Insurance-Ansätzen (als Vertrags-/Produktvariante)

## 3) Produkte & Produktbausteine

### 3.1 Consor Universal (Kernprodukt)
**Beschreibung**
- End-to-end Underwriting- und Policy-Management-Lösung: von Risikoanalyse über Angebot/Policy Issuance bis Policy Changes/Mutationen.
- Low-Code/Design-Engine-Ansatz: Fachbereiche (Business Analysts) können **Produkte, Prozesse und Schriftstücke/Dokumente** modellieren, statt zu programmieren.

**Hauptnutzen (Value Proposition)**
- Kürzere Time-to-Market für Produkt-/Tarif-/Prozessänderungen
- Nachvollziehbare, steuerbare End-to-end-Prozesse
- Automatisierung von Routineaufgaben im Underwriting
- Hoher Individualisierungsgrad für komplexe Industrie-/Spezialsparten

**Typische Funktionsbereiche**
- Underwriting-Workflow (Bearbeitung, Freigaben, Dokumentation)
- Produkt-/Tarif- und Regelmodellierung (fachliche Logik)
- Dokumente/Schriftstücke (z. B. Offerten, Policen, Nachträge) inkl. Generierung
- Vertragskonstrukte: Einzel-/Rahmen-/Kollektivverträge; Mutationen/Änderungen

**Unterstützte Sparten (Beispiele)**
- Industrie-Sach, Technische Versicherungen, Haftpflicht, Transport
- Financial Lines, Kommunalversicherungen/öffentliche Einrichtungen
- Cyber, Rechtsschutz, Spezialitäten (z. B. Kunst, Luftfahrt)

**Unterstützte Vertragsarten**
- Einzelverträge, Kollektivverträge, Rahmenverträge, internationale Programme
- Mechanismen wie „Vererbung" von Konditionen aus Rahmenverträgen/Masterpolicen

### 3.2 Design Engine / Product Modelling (funktionaler Kern von Low-Code)
**Beschreibung**
- Modellierung von Benutzeroberflächen, Workflows, Dokumenten/Schriftstücken, Tarifierungen/Logik ohne (oder mit minimaler) Programmierung.
- Wiederverwendbare Bausteine („out-of-the-box components") zur schnelleren Umsetzung.

**Relevanz für ISO 27001**
- Änderungen werden (teilweise) durch Fachbereiche konfiguriert → Governance/Change-Management, Rollen & Berechtigungen, Test-/Freigabeprozesse sind besonders wichtig.

### 3.3 Consor Universal Cloud Service (SaaS)
**Beschreibung**
- Browserbasierter Zugriff auf eine dedizierte Kundeninstanz, betrieben durch Consor.
- Consor übernimmt Installation, Betrieb, Updates/Upgrades (Terminierung in Abstimmung mit Kunden) sowie Support.
- Betrieb „nach Best Practices" auf AWS; Datenspeicherung für CH-Kunden physisch in der Schweiz, für DE-Kunden in Deutschland.

**Typische SaaS-Mehrwerte**
- Planbare Kosten (OPEX statt CAPEX)
- Entlastung interne IT
- Regelmässige Updates, hohe Verfügbarkeit (gemäss Anbieter: „Always up to date")

**Hintergrund (aus CISO-Interview)**
- Die Umstellung auf SaaS war ein grosser Schritt: Consor wurde damit Betreiber von Software und übernahm Verantwortung für Kundendaten und -systeme. Das gesamte betriebliche Zugriffs- und Berechtigungskonzept wurde aus der Sicherheitsperspektive überarbeitet und neu konzipiert.

### 3.4 Schulungen & Enablement
- Trainings für Kunden (v. a. Business Analysts/Customizers) zur selbstständigen Modellierung von Produkten/Prozessen in der Design Engine.
- Optional individualisierte Schulungsinhalte.

### 3.5 Customizing- und Implementierungsdienstleistungen
- Unterstützung bei Implementierung und (optional) Modellierung/Customizing von Versicherungsprodukten.
- Zusammenarbeit/Implementierungspartner: **BearingPoint** (langjährig, gemeinsame Umsetzung von Consor-Universal-Projekten im deutschsprachigen Raum).
- Integrationen mit Partnerlösungen:
  - **BSI Customer Suite** (CRM/Customer Interaction, Schweizer Softwarehersteller)
  - **Skribble** (elektronische Signatur, nahtlos integriert mit Consor Universal)
  - Plus API-basierte Integration in bestehende Systemlandschaften

### 3.6 Integrationsbild (High-Level)
- Integration in die Systemlandschaft des Versicherers via Schnittstellen/APIs (z. B. CRM, eSignatur, weitere Kernsysteme je nach Kunde).

## 4) Technische Architektur (High-Level, aus Anbieterangaben)
- Webbasierte Anwendung, vollständig in **Java** entwickelt.
- Modulare Architektur; Integration über **APIs** und Schnittstellentechnologie in bestehende Systemlandschaften.

## 5) Security, Datenschutz & Compliance

### 5.1 ISMS/ISO-27001 Scope-Kontext

**Interner Scope (bestätigt)**
- **ISO-27001 Scope gilt für die gesamte Consor** (unternehmensweit, alle Funktionen/Standorte/Prozesse).

**Öffentlich dokumentierter Zertifikatsscope**
- Zertifikate nennen als Scope u. a. „**Entwicklung und Betrieb der Plattform Consor Universal**".
- Hinweis: Für die ISO-Arbeit intern zählt die Vorgabe „gesamte Consor"; das Zertifikat ist als extern kommunizierter Scope/Statement zu behandeln und ggf. zu reconciliieren.

**Zertifizierungshistorie**
- ISO 27001 zertifiziert seit 2023.
- Zertifizierungsprojekt startete März 2023, Abschluss innerhalb von sechs Monaten.
- Beratungspartner: **Secfix** (Startup für automatisierten Zertifizierungsprozess).
- Zertifizierungsstelle: **Certivation**.
- CISO: **Florian Haid** (seit 2023, verantwortlich für alle Security-Themen, Funktion über alle Firmenbereiche hinweg).

### 5.2 Anbieter-Claims (öffentlich kommuniziert)
- **GDPR-konform**, jährliche unabhängige Audits zur DSGVO-Compliance.
- Verschlüsselung: RSA4096, SHA256, AES256; TLS für Daten in Transit; End-to-End-Verschlüsselung at rest, in transit und in Cloud Storage.
- Alle Services laufen in Cloud-Umgebungen; keine eigenen physischen Netzwerk-/Serverkomponenten (Router/Load Balancer/DNS/Server).
- AWS-basierter Betrieb nach Best Practices; Datenresidenz CH/DE nach Kundendomizil.
- Cloud-Provider unterliegen unabhängigen Reviews nach ISO/IEC 27001, ISO/IEC 27017, SOC 1/2/3, PCI DSS, HIPAA, CSA Star, FedRAMP u. a.

### 5.3 Secure Software Development
- Secure Software Development Life Cycle (S-SDLC).
- SAST/DAST zur Identifikation von Sicherheitslücken.
- Regelmässige externe Penetrationstests in Produktionsumgebungen.
- Regelmässige Updates der Backend-Infrastruktur und Software; Prüfung auf bekannte Vulnerabilities.
- Security-Frameworks als Referenz: OWASP Top 10, SANS Top 25, ATT&CK.
- Entwickler-Sicherheitstrainings (regelmässig).
- **Renovate Bot** aktiv für automatisierte Aktualisierung von Drittpartei-Bibliotheken.
- Regelmässige automatisierte Schwachstellenscans (kontinuierlich verbessert und ausgeweitet).

### 5.4 Monitoring & Incident Response
- Application Security Monitoring und Protection:
  - Logs/Audit Trails der Applikationsaktivitäten
  - Exception- und Anomalie-Erkennung
  - Angriffserkennung und Reaktion auf Datenverletzungen
- Runtime Protection System (Echtzeit-Erkennung und Blockierung von Web-Attacken und Business-Logic-Angriffen).
- Security Headers zum Schutz der Nutzer.

### 5.5 Netzwerksicherheit
- Mehrere Sicherheitszonen, überwacht und geschützt mit Firewalls inkl. IP-Adressfilterung.
- Intrusion Detection/Prevention (IDS/IPS) zur Überwachung und Blockierung potentiell bösartiger Pakete.
- DDoS-Mitigation-Services (branchenführende Lösung).

### 5.6 Responsible Disclosure
- Kontakt: security@consor.ch.

### 5.7 Wichtig für ISO 27001 Vorbereitung
- Abgrenzung Geltungsbereich (Scope) zwischen:
  - Produktentwicklung (Software Engineering, Release/Build/Deploy)
  - SaaS-Betrieb (Cloud Operations, Monitoring, Incident Mgmt, BC/DR)
  - Kundenprojekte/Customizing/Schulungen (Projektsecurity, Customer Data Handling)
- Lieferketten-/Provider-Risiken: AWS und weitere Tooling-/Partnerintegrationen (je nach Deployment), inkl. Datenflüsse und Vertrags-/DPA-Setup.

## 6) Operative Annahmen & Input für ISO-Dokumente (interne Faktenbasis)
Diese Punkte wurden intern vorgegeben und sollten als „Known Facts" in ISMS-Artefakten verwendet werden:

1. **ISMS Scope**: gesamtes Unternehmen (alle Funktionen/Standorte/Prozesse der Consor).
2. **Subprocessor-Management**: Subprocessors werden durch Consor in **SecFix** verwaltet. Hosting-Provider: AWS.
3. **Datenkategorien**: Consor verarbeitet **Geschäftsdaten der Kunden** (weitere Datenkategorien aktuell unbekannt).
4. **SLA**: gemäss individuellen Kundenverträgen.
5. **Regulatorik**: Anforderungen gemäss intern gepflegter Liste; in den ISO-Massnahmen berücksichtigt.

## 7) Referenzen / Marktpositionierung (öffentlich kommuniziert)
- Öffentlich genannte Referenzen umfassen u. a. Versicherer in CH/DE (z. B. AXA, Helvetia, Die Mobiliar, Zurich; zusätzlich weitere in DE/AT/CH je nach Sparte/Tochter).

## 8) Organisations- & Standortinformationen (öffentlich)
- Sitz/Adresse: Wengistrasse 7, 8004 Zürich, Schweiz.
- Gegründet: 2001.

**Management Team**
| Rolle | Name |
|---|---|
| CEO | Ruedi Wipf |
| CTO | Andrea Rezzonico |
| Leiterin Kundenprojekte | Bettina Niklaus |
| Head of Business Development | Martin Nokes |
| Leiter Softwareentwicklung | Marco Regniet |
| CISO | Florian Haid (seit 2023) |

**Verwaltungsrat**
| Rolle | Name | Hintergrund |
|---|---|---|
| Verwaltungsratspräsident | Marcel Nickler | Seit 2018; ehem. Partner bei BearingPoint |
| Verwaltungsrat | Stefan Wengi | Unternehmensberater, digitaler Unternehmer |
| Verwaltungsrätin | Désirée Mettraux | Beraterin in Insurtech Start-ups und Versicherungen |
| Beratender Beirat (DE-Markt) | Dr. Christopher Lohmann | Ehem. CEO Allianz Commercial; > 24 J. Erfahrung als Vorstand (u. a. HDI, Gothaer) |

## 9) ISO-27001-relevante Besonderheiten und Implikationen
> Dieser Abschnitt ist als Startpunkt für den LLM-Agent gedacht und muss mit internen Fakten verifiziert werden.

### 9.1 Low-Code/Design-Engine → Governance & Change Control
- Erhöhte Anforderungen an Rollen-/Rechtekonzept, Segregation of Duties (SoD) und Freigabeprozesse.
- Change-/Release-Management muss Konfigurationsänderungen (nicht nur Code) abdecken: Testkonzept, Freigaben, Audit Trails, Rollback.
- Dev/Test/Prod-Trennung besonders wichtig.

### 9.2 SaaS auf AWS → Cloud Controls & Supplier Management
- Supplier Management/A.5.19ff bzw. 27001:2022 Annex A (und ggf. 27017/27018-Referenzen) für AWS und weitere Subprocessor.
- Logging/Monitoring, Incident Response, BC/DR (RTO/RPO), Backup/Restore, Vulnerability & Patch Mgmt als Kernkontrollen.
- Datenresidenz, Mandantentrennung, Zugriffskontrollen, Secrets/Key Management (je nach AWS-Design).

### 9.3 Unklarer Datenumfang → Data Mapping als Top-Priority
- Da aktuell „Geschäftsdaten" bekannt sind, braucht es ein strukturiertes Data Inventory:
  - Welche Datenobjekte (Underwriting-Daten, Vertragsdaten, ggf. Personenbezug)?
  - In welchen Umgebungen (Prod/Non-Prod), in welchen Speichersystemen, welche Retention?
  - Welche Transfers zu/zwischen Subprocessors?

### 9.4 Kundenprojekte & Customizing
- Projekt-/Delivery-Prozesse mit Security Gates
- Umgang mit Kundendaten in Implementierungsprojekten
- Dokumentierte Support-/Ticket-Prozesse und SLA/OLA (falls angeboten)

### 9.5 Scope-Reconciliation
- „Unternehmensweiter Scope" (intern) vs. öffentliches Zertifikats-Statement „Entwicklung und Betrieb der Plattform Consor Universal" (falls erforderlich für Kommunikation/Audit-Storyline).

## 10) Offene Punkte zur internen Klärung
1. **Datenklassifikation**: Welche Datenkategorien (inkl. möglicher personenbezogener Daten) werden tatsächlich verarbeitet? Wie sehen die Datenflüsse aus?
2. **Mandantentrennung und Zugriffsmodell**: Wie ist die Trennung zwischen Kundeninstanzen umgesetzt? Welche Zugriffe hat Consor Ops/Support auf Kundendaten?
3. **Toolchain als Supplier-Liste**: Welche Cloud-Accounts/Regionen und Sub-Processor/Tools werden im Betrieb und in der Entwicklung tatsächlich genutzt (CI/CD, Monitoring, Ticketing, SAST/DAST, Secrets)? → In SecFix zu pflegen.
4. **SLA/BCDR-Ziele**: Welche Support-/Betriebszeiten, BC/DR-Ziele (RTO/RPO) gelten pro Kundensegment/Service-Tier?
5. **Regulatorik**: Welche regulatorischen Anforderungen sind für die Zielkunden relevant (z. B. FINMA-Rundschreiben, BaFin/VAIT, DORA), und inwiefern übernimmt Consor Anforderungen vertraglich?
6. **Scope-Reconciliation**: Abgleich „unternehmensweiter Scope" vs. öffentliches Zertifikats-Statement – ist ein Update des externen Statements geplant/erforderlich?
