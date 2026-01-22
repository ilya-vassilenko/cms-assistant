# Marketing-Überwachung mit dem neuen Microsoft Outlook

Mit dem neuen web-basierten Outlook-Client soll Microsoft Zugangsdaten für Nicht-Microsoft-Emailkonten an eigene Server übertragen und vollständige Kopien aller Emails auf den Microsoft-Servern erstellen. Der Hauptzweck soll Profiling und Werbeverarbeitung sein. Diese Änderung birgt erhöhte Risiken von Datenschutz- und Vertraulichkeitsverletzungen – insbesondere bei sensiblen bzw. besonders schützenswerten Daten. [5][7]

## Wer ist betroffen?

Betroffen sind sowohl Privatkunden, die den neuen Outlook für Nicht-Microsoft-E-Mailkonten nutzen, als auch Enterprise-Kunden, sobald das neue Outlook 2026 in Microsoft 365 (M365) eingeführt wird.

## Was ändert sich im neuen web-basierten Outlook?

Der neue Outlook-Client verlagert zentrale Teile der Datenverarbeitung in die Microsoft-Cloud. Anstatt E-Mails ausschliesslich lokal zu verarbeiten, synchronisiert die Anwendung Inhalte (E-Mails, Kontakte, Kalender) – auch von Fremdanbietern – über Microsoft-Server. [6]

Diese Änderungen stellen einen grundlegenden Paradigmenwechsel dar. Sie fügen sich zudem in Microsofts breitere Strategie ein, das Werbe-/Marketinggeschäft auszubauen: Marktprognosen erwarten für Microsoft Advertising im Jahr 2026 ein Umsatzwachstum von rund 12,2% (auf ca. 19,53 Mrd. USD). [8]

## In welchen Szenarien entstehen welche Risiken?

Die Datenschutz-/Sicherheits-/Compliance-Risiken sind vielfältig:

**Datenübertragung ohne Einwilligung/Transparenz (je nach Region):** Je nach Rechtsraum und Produktkonfiguration können Informations- und Steuerungsmechanismen (Einwilligung vs. Opt-out) deutlich variieren; u.a. wird für die USA/Schweiz ein geringeres Transparenzniveau als in der EU beschrieben. [7]

**Erhöhte Angriffsfläche:** Zusätzliche Speicherung/Synchronisation von Inhalten (neben dem ursprünglichen Mail-Provider) erhöht die potenzielle Angriffsfläche und das Risiko unbefugter Zugriffe. [5]

**Profiling und Datenverwertung:** Hinweise auf Werbepartner/Advertising-Ökosystem und entsprechende Einstellungen deuten darauf hin, dass Profile, welche auf Nutzungs- und Inhaltsdaten basieren, in werberelevanten Kontexten stark verarbeitet werden können - die Analysen sprechen von > 800 Drittanbietern, die von Microsoft Werbedaten erhalten sollen. Für Organisationen mit sensiblen Informationen (z.B. Amtsgeheimnis-, Berufsgeheimnis- oder Gesundheitsdaten) ist das besonders kritisch. [1]

**Compliance-Risiken (insb. öffentliche Organe/Geheimnisträger):** Für Schweizer Behörden/öffentliche Organe wird die Auslagerung besonders schützenswerter oder geheimhaltungspflichtiger Personendaten in SaaS-Lösungen grosser internationaler Anbieter (z.B. M365) in vielen Fällen als unzulässig beurteilt; als zentrale Gegenmassnahme wird echte Ende-zu-Ende-Verschlüsselung genannt, bei der der Anbieter keinen Zugriff auf die Schlüssel hat. Dies lässt sich aber bei Outlook-Produkten nur beschränkt implementieren.

**Regulatorische/politische Reaktionen:** Die Datenschutzbedenken sind so konkret, dass Institutionen wie das EU-Parlament den Einsatz der neuen Outlook-App (bzw. entsprechender Funktionen) aus Datenschutzgründen untersagt bzw. blockiert haben. [2] Auch nach solchen ersten Einschränkungen fordern Abgeordnete im EU-Parlament weitergehende Schritte bis hin zu einem breiteren Verzicht auf Microsoft-Produkte zugunsten digitaler Souveränität. [3][4]

## Was ist die Timeline für die Neuerungen?

Die Einführung des neuen Outlook-Clients läuft bereits. Seit **September 2023** ist die „neue Outlook-App“ für Windows verfügbar; Microsoft plant, Outlook Classic bis **2029** zu ersetzen. Für M365 wird die Umstellung gestaffelt beschrieben (Business früher, Enterprise danach), wobei für Enterprise eine Einführung ab **2026** genannt wird.

## Wie kann man die Risiken adressieren?

Um die Risiken zu minimieren, sollten Nutzer und Unternehmen folgende Massnahmen ergreifen:

**Alternativen prüfen:** Je nach Use Case können alternative Email-Clients und -Services mit besserer Kontrolle über Daten sinnvoll sein.

**Datenverschlüsselung:** Sensible Daten sollten so geschützt werden, dass Cloud-Anbieter keinen Zugriff auf Klartext und Schlüssel erhalten (z.B. Ende-zu-Ende-Verschlüsselung oder Client-seitige Verschlüsselung).

**Regelmässige Schulungen:** Unternehmen sollten Mitarbeitende regelmässig zu Datenschutz und sicherer E-Mail-Nutzung schulen, damit Mitarbeiter Outlook nur konform einsetzen (z.B. nur für nicht geheime Daten).

**Überprüfung der Compliance:** Unternehmen müssen die Konformität von Microsoft’s neuer Lösung für ihren Use Case in Details prüfen - bezüglich Datenschutz, TOMs, sowie Zweck-/Rollenklärungen (Controller/Processor); insbesondere, ob zusätzliche Verarbeitung bei Microsoft rechtlich und vertraglich abgedeckt ist.

## Quellen

[1] [Publikation: Resolution zur Auslagerung von Datenbearbeitungen in die Cloud](https://www.privatim.ch/de/publikation-resolution-zur-auslagerung-von-datenbearbeitungen-in-die-cloud/)

[2] [EU Parliament blocks new Outlook apps over privacy concerns](https://www.networkworld.com/article/935442/eu-parliament-blocks-new-outlook-apps-over-privacy-concerns.html)

[3] [Microsoft vor dem Aus im Europaparlament](https://www.ad-hoc-news.de/boerse/news/ueberblick/microsoft-vor-dem-aus-im-europaparlament/68390726)

[4] [Weg von Microsoft: Abgeordnete fordern digitale Souveränität im EU-Parlament](https://www.heise.de/news/Weg-von-Microsoft-Abgeordnete-fordern-digitale-Souveraenitaet-im-EU-Parlament-11097460.html)

[5] [Datenschutzbedenken zum neuen Outlook von Microsoft](https://www.datenschutzticker.de/2025/04/datenschutzbedenken-zum-neuen-outlook-von-microsoft/)

[6] [Überträgt auch Outlook 365 Classic Zugangsdaten an Microsoft? | Borns IT- und Windows-Blog](https://www.borncity.com/blog/2025/11/27/uebertraegt-auch-outlook-365-classic-zugangsdaten-an-microsoft/)

[7] [Outlook is Microsoft’s new data collection service | Proton](https://proton.me/blog/outlook-is-microsofts-new-data-collection-service)

[8] [Top facts and figures about Microsoft advertising | Embryo](https://embryo.com/blog/top-facts-microsoft-advertising/)
