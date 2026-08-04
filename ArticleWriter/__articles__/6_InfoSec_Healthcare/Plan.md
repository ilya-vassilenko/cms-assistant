# InfoSec Healthcare Conference 2026 -- Slide Deck

## Datei

- Ziel: `[ArticleWriter/__articles__/6_InfoSec_Healthcare/slides.md](ArticleWriter/__articles__/6_InfoSec_Healthcare/slides.md)`
- Sprache: Deutsch (Schweizer Kontext)
- Format pro Folie: Slide-Titel, Bullet Points, Sprechernotizen, Quellenverweise

## Slide-Struktur (10 + Titelfolie)

### Titelfolie (extra, nicht gezaehlt)

- Titel: "Wie setze ich KI fuer Gesundheitsdaten konform ein?"
- Referent, Funktion, Firma, Konferenz, Datum

### Slide 1 -- Scope: Was ist KI und wo im Unternehmen?

- Drei KI-Typen: Self-hosted, generelle Cloud-KI, fachspezifische Services
- Einsatzbereiche: KI im Produkt, Software Engineering, Marketing, HR, General Purpose Text, E-Mail-Plugins
- **Kernbotschaft:** Rahmen abstecken, damit das Publikum weiss, wovon wir heute sprechen
- Quellen: Wolters Kluwer Shadow AI Report (4.1) fuer Statistiken zu unkontrolliertem KI-Einsatz

### Slide 2 -- Rolle des Unternehmens: Verantwortlicher vs. Auftragnehmer

- Controller-Rolle: Bestimmt Zweck und Mittel der Datenbearbeitung
- Processor-Rolle: Bearbeitet im Auftrag, eigene Pflichten nach DSG Art. 9
- Praxisbeispiel: Spital als Controller, KI-Cloud-Anbieter als Processor
- Quellen: EDOEB Outsourcing / Auftragsdatenbearbeitung (1.7)

### Slide 3 -- Besonders schuetzenswerte Daten & Geheimnisse

- Abgrenzung: Allgemeine Personendaten vs. besonders schuetzenswerte Personendaten (Art. 5 lit. c DSG) -- Gesundheitsdaten sind immer besonders schuetzenswert
- Amtsgeheimnis (Art. 320 StGB) vs. Berufsgeheimnis (Art. 321 StGB): Wer unterliegt welchem?
- Implikation fuer KI: Hoehere Anforderungen an Rechtfertigung, DSFA-Pflicht, Verschluesselung
- Quellen: activeMind (1.9), Kt. Zuerich (1.5), BFH-Studie (1.6)

### Slide 4 -- Einwilligung vs. Informationspflicht

- Kernaussage: Das ist nicht das Gleiche!
- Informationspflicht (Art. 19 DSG): Gilt immer, unabhaengig von der Rechtsgrundlage
- Einwilligung: Im CH-DSG seltener noetig als in der DSGVO (Erlaubnisprinzip mit Verbotsvorbehalt)
- Bei Gesundheitsdaten: Wenn Einwilligung noetig, dann ausdruecklich
- Quellen: Datenschutztreuhand (1.10), Online-Kommentar Art. 6 (1.11), HIN (1.16)

### Slide 5 -- Einwilligung vs. Vertrag

- Wann Einwilligung? Wenn keine andere Rechtsgrundlage greift und Persoenlichkeitsverletzung vorliegt
- Wann Vertrag? Art. 31 Abs. 2 lit. a DSG -- Vertragsabwicklung als ueberwiegendes Interesse
- Praxisbezug KI: Patientenvertrag kann KI-Nutzung abdecken, wenn transparent informiert
- Quellen: Art. 31 DSG (1.13), Bratschi AG (1.12)

### Slide 6 -- Profiling & automatisierte Entscheidungsfindung

- Definition Profiling (Art. 5 lit. f DSG) und automatisierte Einzelentscheidung (Art. 21 DSG)
- Wann ist KI-Einsatz Profiling? Wann automatisierte Entscheidung?
- Pflichten: Informationspflicht, Recht auf menschliche Ueberpruefung, DSFA bei hohem Risiko
- Quellen: Datenschutz.law Art. 21 (1.14), Online-Kommentar Art. 22 DSFA (1.15), Bratschi AG (1.12)

### Slide 7 -- KI als Medizingeraet vs. KI als Assistenz

- Abgrenzung: Medizinprodukt (MDR/MepV) wenn bestimmungsgerecht zur Diagnose/Therapie vs. Assistenztool (Dokumentation, Verwaltung)
- Regulatorische Konsequenz: Medizinprodukt = Konformitaetsbewertung + ab 2027 AI Act Art. 6(1)
- Schweizer Kontext: Swissmedic, MepV-Uebergangsfristen, Registrierungspflicht ab Juli 2026
- Quellen: MDCG 2025-6 (2.1), quickbird medical (2.3), Swissmedic (2.4), BAG (2.5)

### Slide 8 -- Ausgewaehlte Sicherheitsmassnahmen

- Leitprinzip: "Loesungen anbieten, bevor verbieten" -- Shadow AI als Warnung (57% begegnen Shadow AI, $7.42 Mio. durchschnittliche Breach-Kosten)
- Internationaler Datentransfer: Staatenliste BJ (Anhang 1 DSV), Swiss-U.S. DPF, SCCs als Fallback
- Self-hosted KI als Alternative bei Berufsgeheimnis
- Quellen: Wolters Kluwer (4.1), DH Insights (4.2), BJ Staatenliste (1.8), BFH-Studie (1.6)

### Slide 9 -- Umsetzung: Technische Governance

- SSO: Zentrale Identitaet, keine separaten KI-Tool-Logins
- Trainingsdaten: Opt-out sicherstellen, vertragliche Regelung mit Anbietern
- Zugriffsberechtigungen: Rollenbasiert, Least Privilege, Audit-Logs
- DLP (Data Loss Prevention): Verhindern, dass Gesundheitsdaten unkontrolliert an KI-Dienste fliessen
- Quellen: HealthTech Shadow AI (4.3), NIST AI RMF (3.1), ISO 42001 (3.2/3.3)

### Slide 10 -- Wrap-up: 5 erste Schritte zum Handeln

- 5 priorisierte, sofort umsetzbare Handlungsschritte (konkrete Vorschlaege)
- Referenz auf Arxio-Dienstleistungen (dezent, als "wir helfen dabei")
- Kontaktdaten
- Quellen: HealthTech (4.3), KPMG ISO 42001 (3.3), HealthTech NIST-Praxis (3.4)

## Offener Vorschlag: Inhalt der "5 ersten Schritte"

Basierend auf dem Kontext des Vortrags und den Quellen schlage ich vor:

1. **Bestandsaufnahme:** Alle KI-Tools im Unternehmen inventarisieren (inkl. Shadow AI)
2. **Risikoklassifikation:** Jedes Tool nach Datenkategorie und Einsatzbereich bewerten
3. **Sichere Alternativen bereitstellen:** Genehmigte KI-Tools mit SSO, DLP und Opt-out anbieten
4. **Richtlinien erstellen:** Praxisorientierte KI-Policy mit Do's und Don'ts
5. **DSFA durchfuehren:** Fuer alle Hochrisiko-Anwendungen (Gesundheitsdaten + KI = immer)

Diese 5 Schritte koennen im Umsetzungsprozess angepasst werden.

## Annex: Oeffentliche Organe und kantonale Vorabkontrolle

### Kontext

Oeffentliche Organe — darunter Krankenkassen im oeffentlichen Auftrag der Grundversicherung, kantonale Spitaeler, Universitaetskliniken — unterliegen nicht (nur) dem Bundes-DSG, sondern den **kantonalen Datenschutzgesetzen**. Das hat direkte Konsequenzen fuer den KI-Einsatz.

### KI als "Neue Technologie" — Vorabkontrolle

- Kantonale Datenschutzbeauftragte stufen KI in der Regel als **"Neue Technologie"** ein
- Daraus ergibt sich eine **Vorabkontrollpflicht** vor dem produktiven Einsatz
- Einzureichende Dokumente (typisch): ISDS-Konzept, Datenschutz-Folgenabschaetzung (DSFA), Rechtsgrundlagenanalyse, ggf. weitere kantonsspezifische Unterlagen

### Kantonale Unterschiede

- **Vorlagen:** Einige Kantone haben eigene Vorlagen; mehrere Kantone verwenden die Vorlagen des Datenschutzbeauftragten des Kantons Zuerich als Referenz
- **Pilotprojekte:**
  - Einige Kantone erlauben **Piloten ohne eingereichte Vorabkontrolle** (empfehlen aber, die Unterlagen intern zu erstellen)
  - Andere Kantone verlangen die **Vorabkontrolle auch fuer Pilotprojekte** (kleine Benutzergruppen, eingeschraenkte Use Cases mit kleinem Risiko)
- Definition Pilot: Kleine User-Gruppen, eingeschraenkte Use Cases, bewusst reduziertes Risikoprofil

### Kernaspekt: Rechtsgrundlage

- Massgebend bei der Vorabkontrolle ist die **Definition der Rechtsgrundlage**: Aus welchem Grund wuerde das oeffentliche Organ KI fuer einen bestimmten Zweck einsetzen?
- Ohne klare gesetzliche Grundlage fuer die KI-gestuetzte Bearbeitung ist der Einsatz fuer oeffentliche Organe nicht zulaessig — unabhaengig von technischen Sicherheitsmassnahmen