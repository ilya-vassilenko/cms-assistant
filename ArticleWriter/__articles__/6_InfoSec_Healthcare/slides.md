# Wie setze ich KI für Gesundheitsdaten konform ein?

**Slide Deck — InfoSec Healthcare Conference 2026**
Ilya Vasilenko | Senior Security, Compliance and Data Protection Consultant | Arxio AG

---

## Titelfolie

**Wie setze ich KI für Gesundheitsdaten konform ein?**

- Ilya Vasilenko
- Senior Security, Compliance and Data Protection Consultant
- Arxio AG
- InfoSec Healthcare Conference 2026

---

## Slide 1 — Scope: Was ist KI und wo im Unternehmen?

### Betriebsmodell — Wo läuft die KI?

- **Cloud-KI (SaaS)** — Der Anbieter betreibt das Modell; Daten verlassen die Organisation (z.B. ChatGPT, Copilot, Gemini)
- **Self-hosted KI** — Modell läuft lokal oder in der eigenen Infrastruktur; Daten bleiben intern (z.B. Open-Source-LLMs wie Llama, Mistral)
- **Eingebettete KI** — KI ist Bestandteil eines eingekauften Fachprodukts; Betriebsmodell vom Hersteller vorgegeben (z.B. KI-Modul in der Radiologie-Software)

### Einsatzbereiche — Wofür wird KI genutzt?

- **Fachspezifisch im Gesundheitswesen** — Röntgenbild-Analyse, Pathologie-Screening, Transkription von Arzt-Patienten-Gesprächen, klinische Entscheidungsunterstützung, automatisierte Befundung
- **Software Engineering** — Code-Generierung und Code-Review (GitHub Copilot, Cursor)
- **Marketing & Kommunikation** — Texterstellung, Social Media, Übersetzungen
- **HR** — CV-Screening, Interviewzusammenfassungen, Stelleninserateerstellung
- **General Purpose** — E-Mail-Plugins (Copilot für Outlook), Meetingzusammenfassungen, Dokumentensuche

> **Sprechernotizen:**
> Ziel dieser Folie: Den Rahmen setzen. Wir unterscheiden zwei Achsen: Erstens das Betriebsmodell — wo laufen die Daten hin? Cloud-KI bedeutet, dass Patientendaten das Haus verlassen. Self-hosted heisst volle Kontrolle, aber auch voller Betriebsaufwand. Eingebettete KI steckt in Fachprodukten, die man einkauft — da bestimmt der Hersteller das Deployment. Zweitens der Einsatzbereich — wofür wird KI genutzt? Gerade im Gesundheitswesen ist die Bandbreite gross: Von der Röntgenbild-Analyse (potenziell Medizinprodukt) über die Transkription von Arzt-Patienten-Gesprächen (Berufsgeheimnis!) bis hin zu Marketing-Texten (geringes Risiko). Die Kombination aus Betriebsmodell und Einsatzbereich bestimmt das Risikoprofil — und damit die regulatorischen Anforderungen. Die Zahlen zur Einordnung: 57 % der Fachkräfte im Gesundheitswesen begegnen bereits Shadow AI. 97 % der KI-Sicherheitsvorfälle passieren in Organisationen ohne KI-Governance-Richtlinien.

> **Quellen:**
> - Wolters Kluwer: Shadow AI — A Hidden Risk to Healthcare (4.1) — https://www.wolterskluwer.com/en/solutions/uptodate/ai-clinical-decision-support/shadow-ai-report
> - Digital Health Insights: Shadow AI als grösstes Sicherheitsrisiko (4.2) — https://dhinsights.org/blog/shadow-ai-emerges-as-one-of-healthcares-biggest-security-risks/

---

## Slide 2 — Rolle des Unternehmens: Verantwortlicher vs. Auftragnehmer

### Verantwortlicher (Controller)

- Bestimmt **Zweck und Mittel** der Datenbearbeitung
- Trägt die volle Verantwortung gegenüber betroffenen Personen
- Typisch: Spital, Arztpraxis, Versicherung

### Auftragsbearbeiter (Processor)

- Bearbeitet Daten **im Auftrag** des Verantwortlichen
- Eigene Pflichten nach **Art. 9 DSG**: Sicherheit, Weisungsgebundenheit, Unterbeauftragung
- Typisch: KI-Cloud-Anbieter, SaaS-Plattform

### Warum ist das relevant?

- Die Rolle bestimmt, **wer die DSFA durchführt**, wer informiert und wer haftet
- Bei KI-Tools: Vertrag mit dem Anbieter muss klären, ob Daten für eigenes Training verwendet werden

> **Sprechernotizen:**
> Praxisbeispiel: Ein Spital nutzt einen Cloud-KI-Dienst zur Befundzusammenfassung. Das Spital ist Controller — es entscheidet, dass und warum Patientendaten verarbeitet werden. Der KI-Anbieter ist Processor — er darf die Daten nur gemäss Vertrag und Weisung verwenden. Aber: Wenn der Anbieter die Daten auch für Modelltraining nutzt, wird er zum eigenständigen Verantwortlichen für diesen Zweck. Das muss vertraglich klar geregelt sein (Art. 9 DSG).

> **Quellen:**
> - EDÖB: Outsourcing / Auftragsdatenbearbeitung (1.7) — https://www.edoeb.admin.ch/de/outsourcing-auftragsdatenbearbeitung
> - Bratschi AG: Rechtliche Anforderungen an KI-Applikationen im Gesundheitswesen (1.12) — https://www.bratschi.ch/publikationen/rechtliche-anforderungen-an-die-nutzung-von-ki-applikationen-im-gesundheitswesen

---

## Slide 3 — Besonders schützenswerte Daten & Geheimnisse

### Datenkategorien nach DSG

| Kategorie | Beispiel | Relevanz für KI |
|---|---|---|
| Allgemeine Personendaten | Name, E-Mail, Geburtsdatum | Informationspflicht, DSFA bei hohem Risiko |
| **Besonders schützenswerte Personendaten** (Art. 5 lit. c DSG) | **Gesundheitsdaten**, genetische und biometrische Daten | Höhere Anforderungen an Rechtfertigung; ausdrückliche Einwilligung wenn nötig |

### Amtsgeheimnis vs. Berufsgeheimnis

- **Amtsgeheimnis** (Art. 320 StGB) — Betrifft Behörden und öffentliche Einrichtungen (z.B. kantonale Spitäler)
- **Berufsgeheimnis** (Art. 321 StGB) — Betrifft Ärztinnen/Ärzte, Apotheker, Hebammen und deren Hilfspersonen
- Konsequenz: Cloud-KI-Anbieter kann als **Hilfsperson** gelten — aber nur unter strengen Voraussetzungen (funktionale Unterordnung, Weisungsbindung)

> **Sprechernotizen:**
> Gesundheitsdaten sind im DSG immer besonders schützenswert — das ist nicht verhandelbar. Die Frage ist: Unter welches Geheimnisschutzregime fällt die Organisation zusätzlich? Kantonale Spitäler: Amtsgeheimnis. Niedergelassene Ärztinnen und Ärzte: Berufsgeheimnis. Privatkliniken: kommt auf den kantonalen Kontext an. Das Berufsgeheimnis nach Art. 321 StGB ist besonders restriktiv — eine Weitergabe an Cloud-Dienste ist ohne Einwilligung der Patienten oder Hilfspersonen-Status des Anbieters problematisch. Die BFH-Studie zeigt: Self-hosted KI kann hier eine Lösung sein. Der Kanton Zürich hat in seiner Innovation Sandbox hervorragend dargelegt, unter welchen Bedingungen Cloud-KI mit Berufsgeheimnis vereinbar sein kann (Verschlüsselung, Confidential Computing).

> **Quellen:**
> - activeMind: Besonders schützenswerte Personendaten nach DSG (1.9) — https://www.activemind.ch/blog/personendaten/
> - Kanton Zürich: Datenschutz, Berufsgeheimnis und die Cloud (1.5) — https://www.zh.ch/de/wirtschaft-arbeit/wirtschaftsstandort/innovation-sandbox/medizinische-dokumentation/2-datenschutz-berufsgeheimnis-und-die-cloud.html
> - BFH-Studie: Open-Source-KI und Berufsgeheimnis (1.6) — https://www.bfh.ch/dam/jcr:deb88ea7-662d-499a-8a1c-fb83d070f113/Das%20Potenzial%20von%20Open%20Source%20KI%20im%20Kontext%20von%20Datenschutz%20und%20Berufsgeheimnis.pdf

---

## Slide 4 — Einwilligung vs. Informationspflicht

### Das ist nicht das Gleiche!

| | Informationspflicht (Art. 19 DSG) | Einwilligung (Art. 6 Abs. 6/7 DSG) |
|---|---|---|
| **Wann?** | **Immer** — bei jeder Datenbearbeitung | Nur bei Persönlichkeitsverletzung (Art. 30) ohne anderen Rechtfertigungsgrund |
| **Inhalt** | Verantwortlicher, Zweck, Empfänger, Auslandsbekanntgabe | Freiwillige, informierte Willensäusserung für bestimmte Bearbeitungen |
| **Form** | Formfrei (DSE, Patienteninfo, Aushang) | Formfrei; bei Gesundheitsdaten: **ausdrücklich** (Art. 6 Abs. 7) |
| **Verzichtbar?** | **Nein** | **Ja** — wenn Vertrag, überwiegendes Interesse oder Gesetz greift |

### Kernbotschaft

- CH DSG = **Erlaubnisprinzip mit Verbotsvorbehalt** — Bearbeitung grundsätzlich erlaubt
- EU DSGVO = Verbotsprinzip mit Erlaubnisvorbehalt — Bearbeitung grundsätzlich verboten
- **Einwilligung ist im DSG seltener nötig** als unter DSGVO. Auch bei Gesundheitsdaten nicht per se erforderlich
- **Informationspflicht gilt immer** — wer KI einsetzt, muss darüber informieren

### KI-spezifisch: Was jetzt aktualisieren?

- Datenschutzerklärung: KI-Tools, Zweck, betroffene Daten
- Patienteninformation: „Wir nutzen KI-gestützte Transkription für Arztberichte"
- Bei Auslandsübermittlung an KI-Anbieter: Zielstaat + Schutzmechanismus
- Bei automatisierten Entscheidungen: Hinweis + Recht auf menschliche Überprüfung (Art. 21)

> **Sprechernotizen:**
> Häufigster Irrtum in der Praxis: „Wir brauchen für alles eine Einwilligung." Das ist DSGVO-Denken, nicht DSG-Denken. Im CH DSG gilt das Erlaubnisprinzip — Bearbeitung ist erlaubt, sofern Bearbeitungsgrundsätze (Art. 6 DSG) eingehalten werden. Einwilligung braucht es nur bei Persönlichkeitsverletzung ohne anderen Rechtfertigungsgrund. Art. 6 Abs. 6/7 DSG statuieren kein allgemeines Einwilligungserfordernis — sie regeln nur, wann eine Einwilligung gültig ist. Auch bei besonders schützenswerten Personendaten wie Gesundheitsdaten ist keine Einwilligung per se nötig. Was aber immer gilt: Informationspflicht nach Art. 19 DSG. Wer KI einsetzt, muss darüber informieren — unabhängig von der Rechtsgrundlage. Praktischer Tipp: Datenschutzerklärung und Patienteninformation jetzt um KI-Einsatz ergänzen. Das vergessen viele.

> **Quellen:**
> - Datenschutztreuhand: Grundsätzliches zur Einwilligung nach DSG (1.10) — https://datenschutztreuhand.ch/grundsaetzliches-zur-einwilligung-nach-dsg/
> - Online-Kommentar: Art. 6 Abs. 6 und 7 DSG (1.11) — https://onlinekommentar.ch/de/kommentare/art6abs6und7
> - HIN: Neues DSG und Gesundheitswesen (1.16) — https://www.hin.ch/de/blog/2023/ndsg-gesundheitswesen-teil-1.cfm

---

## Slide 5 — Einwilligung vs. Vertrag vs. Gesetz

### Drei Rechtfertigungsgründe bei Persönlichkeitsverletzung (Art. 31 DSG)

| Rechtfertigung | Wann greift sie? | Typisch für |
|---|---|---|
| **1. Einwilligung** | Keine andere Grundlage; bei Gesundheitsdaten: ausdrücklich | Forschung, KI-Modelltraining, Bekanntgabe an behandlungsfremde Dritte |
| **2. Überwiegendes Interesse** (inkl. Vertrag, Art. 31 Abs. 2 lit. a) | KI-Nutzung dient Vertragserfüllung und ist transparent kommuniziert | **Private** Leistungserbringer: Behandlungsvertrag |
| **3. Gesetz** | Gesetzlicher Auftrag zur Leistungserbringung | **Öffentliche** Leistungserbringer: Grundversorgung |

### Privat: Vertrag als Grundlage für KI?

- KI ist nicht zwingend notwendig für Behandlung — Arzt kann auch ohne KI arbeiten
- Art. 31 Abs. 2 lit. a DSG: „Zusammenhang mit Abwicklung eines Vertrags" — offener formuliert als DSGVO
- **Aber:** Wenn Vertrag KI nicht erwähnt → Vertragsgrundlage angreifbar
- **Empfehlung:** Behandlungsvertrag um KI-Klausel ergänzen → Vertragsgrundlage tragfähig

### Öffentlich: Gesetz als Grundlage für KI?

- Grundversorgung basiert auf **Gesetz** (kantonale Spital-/Gesundheitsgesetze), nicht auf Vertrag
- Legalitätsprinzip: Datenbearbeitung nur mit gesetzlicher Grundlage
- Gesundheitsgesetze decken Behandlung — aber **nicht explizit die Methode KI**
- Kantonale DSB: KI = „neue Technologie" → **Vorabkontrolle** prüft, ob bestehende Rechtsgrundlage für konkreten KI-Einsatz ausreicht
- Kein Gericht hat bisher entschieden. Vorabkontrolle = pragmatischer Mechanismus

### Praxisfälle

| Szenario | Privat | Öffentlich |
|---|---|---|
| Self-hosted KI, Arzt prüft Ergebnis | Informationspflicht genügt | Vorabkontrolle; Rechtsgrundlage dokumentieren |
| Cloud-KI, KI im Vertrag/Info transparent | Vertrag + Info = vertretbar | Vorabkontrolle + Prüfung Cloud-Auslagerung |
| KI-Training mit Patientendaten | Einwilligung, ausdrücklich | Nicht zulässig ohne spezifische gesetzliche Grundlage |

> **Sprechernotizen:**
> Diese Folie ist der Kern: Welche Rechtsgrundlage trägt den KI-Einsatz? Drei Optionen — und sie hängen davon ab, ob man privater oder öffentlicher Leistungserbringer ist. Private können sich auf den Behandlungsvertrag stützen, aber nur wenn der Vertrag KI transparent erwähnt. KI ist nicht zwingend nötig für die Behandlung — der Arzt kann auch ohne KI arbeiten. Deshalb muss der Vertrag angepasst werden, sonst ist die Grundlage angreifbar. Öffentliche Spitäler haben es strenger: Kein Vertrag, sondern gesetzlicher Auftrag (Grundversorgung). Problem: Die Gesundheitsgesetze wurden vor KI geschrieben. Sie decken die Behandlung, aber nicht explizit die Methode KI. Die kantonalen Datenschutzbeauftragten lösen das pragmatisch über die Vorabkontrolle: Sie prüfen fallweise, ob die bestehende Rechtsgrundlage für den konkreten KI-Einsatz ausreicht. Das ist genau der Sinn der Vorabkontrolle — nicht neue Rechtsgrundlage schaffen, sondern bestehende auf Tragfähigkeit prüfen. Kein Gericht hat bisher entschieden. Self-hosted KI ist für beide einfacher zu rechtfertigen, weil Daten intern bleiben.

> **Quellen:**
> - Art. 31 DSG: Rechtfertigungsgründe (1.13) — https://datenschutz-grundverordnung.eu/dsg-schweiz/art-31-rechtfertigungsgrunde/
> - Bratschi AG: Rechtliche Anforderungen an KI-Applikationen im Gesundheitswesen (1.12) — https://www.bratschi.ch/publikationen/rechtliche-anforderungen-an-die-nutzung-von-ki-applikationen-im-gesundheitswesen
> - DSB Kanton Zürich: Generative KI für öffentliche Organe (2024) — https://www.datenschutz.ch/tb/2024/sichere-kuenstliche-intelligenz

---

## Slide 6 — Profiling & automatisierte Entscheidungsfindung

### Definitionen

- **Profiling** (Art. 5 lit. f DSG): Automatisierte Bearbeitung von Personendaten zur Bewertung bestimmter Aspekte einer Person (Gesundheit, Verhalten, Aufenthaltsort etc.)
- **Automatisierte Einzelentscheidung** (Art. 21 DSG): Entscheidung, die ausschliesslich auf automatisierter Bearbeitung beruht und mit einer Rechtsfolge oder erheblichen Beeinträchtigung verbunden ist

### Wann wird KI zum Profiling?

- KI-basiertes Risiko-Scoring von Patienten → **Profiling**
- KI-gestützte Triage ohne menschliche Überprüfung → **Automatisierte Einzelentscheidung**
- KI-generierte Zusammenfassung, die ein Arzt prüft → **Keines von beiden**

### Pflichten

- **Informationspflicht**: Die betroffene Person muss darüber informiert werden, dass eine Entscheidung ausschliesslich auf automatisierter Bearbeitung beruht (Art. 21 Abs. 1 DSG)
- **Recht auf menschliche Überprüfung**: Die betroffene Person kann verlangen, dass die automatisierte Entscheidung von einer natürlichen Person überprüft wird (Art. 21 Abs. 2 DSG)
- **DSFA-Pflicht**: Wenn Profiling ein hohes Risiko für die Persönlichkeit oder Grundrechte darstellt, muss vorgängig eine Datenschutz-Folgenabschätzung durchgeführt werden (Art. 22 DSG) — bei KI + Gesundheitsdaten praktisch immer der Fall

> **Sprechernotizen:**
> Hier wird es oft abstrakt — deshalb konkrete Beispiele nutzen. Entscheidend ist die Frage: Trifft die KI eine Entscheidung mit Rechtsfolgen, oder unterstützt sie einen Menschen bei seiner Entscheidung? Wenn ein Arzt die KI-Ausgabe prüft und die Entscheidung selbst trifft, liegt keine automatisierte Einzelentscheidung vor. Wenn aber eine Krankenversicherung per KI automatisch Leistungen ablehnt, ist das eine automatisierte Einzelentscheidung nach Art. 21 DSG — mit Informationspflicht und Recht auf menschliche Überprüfung. Die DSFA-Pflicht nach Art. 22 DSG greift bei KI + Gesundheitsdaten praktisch immer, weil die Kombination ein „hohes Risiko" darstellt.

> **Quellen:**
> - Datenschutz.law: Art. 21 DSG — Automatisierte Einzelentscheidung (1.14) — https://datenschutz.law/revdsg/3-kapitel/art-21
> - Online-Kommentar / Swiss Infosec: Art. 22 DSG — DSFA (1.15) — https://onlinekommentar.ch/de/kommentare/dsg22
> - Bratschi AG: Rechtliche Anforderungen an KI-Applikationen im Gesundheitswesen (1.12) — https://www.bratschi.ch/publikationen/rechtliche-anforderungen-an-die-nutzung-von-ki-applikationen-im-gesundheitswesen

---

## Slide 7 — KI als Medizingerät vs. KI als Assistenz

### Abgrenzung

| | KI als Medizinprodukt | KI als Assistenz |
|---|---|---|
| **Bestimmungszweck** | Diagnose, Therapie, Überwachung einer Krankheit | Dokumentation, Verwaltung, allgemeine Effizienz |
| **Beispiele** | Radiologie-KI zur Tumorerkennung, KI-basierte Triage | Spracherkennung für Arztberichte, Terminplanung |
| **Regulierung** | MDR/MepV + ab Aug. 2027: EU AI Act Art. 6(1) | DSG, ggf. allgemeine AI-Act-Pflichten |
| **Konformität** | CE-Kennzeichnung, Konformitätsbewertung, QMS | Datenschutz-Compliance, Informationssicherheit |

### Schweizer Kontext

- **Swissmedic**: Übernimmt EU-Rahmen weitgehend, aber kein automatisches MRA-Update
- **MepV-Übergangsfristen**: Registrierungspflicht ab Juli 2026
- **Duale Konformität ab 2027**: KI-Medizinprodukte müssen sowohl MDR/MepV als auch AI Act erfüllen

> **Sprechernotizen:**
> Die Frage „Ist unsere KI ein Medizinprodukt?" ist für viele Organisationen die erste Weichenstellung. Faustregel: Wenn die KI einen medizinischen Zweck verfolgt (Diagnose, Therapie, Prognose), ist sie ein Medizinprodukt — unabhängig davon, ob sie nur „unterstützt". Ein KI-Tool, das Röntgenbilder analysiert und Befundvorschläge macht, ist ein Medizinprodukt. Ein KI-Tool, das Arztbriefe diktiert, ist es in der Regel nicht. Ab August 2027 kommt die Doppelbelastung: KI-Medizinprodukte der Risikoklasse IIa und höher fallen automatisch unter die Hochrisiko-Kategorie des EU AI Act (Art. 6 Abs. 1). Die MDCG 2025-6 Guidance klärt die Details. Für die Schweiz: Swissmedic orientiert sich am EU-Rahmen, aber das MRA ist noch nicht aktualisiert — also Auffangmassnahmen beachten.

> **Quellen:**
> - MDCG 2025-6: Interplay MDR/IVDR und AI Act (2.1) — https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en?filename=mdcg_2025-6_en.pdf
> - quickbird medical: AI Act Guidelines für Medizinproduktehersteller (2.3) — https://quickbirdmedical.com/en/ai-act-medical-devices-mdr/
> - Swissmedic: Rahmenbedingungen für KI (2.4) — https://www.swissmedic.ch/swissmedic/de/home/humanarzneimittel/authorisations/artificiel-intelligence.html
> - BAG: Medizinprodukterecht Schweiz (2.5) — https://www.bag.admin.ch/de/medizinprodukterecht

---

## Slide 8 — Ausgewählte Sicherheitsmassnahmen

### Leitprinzip: Lösungen anbieten, bevor verbieten

- **57 %** der Fachkräfte begegnen Shadow AI im Gesundheitswesen
- **86 %** der IT-Executives berichten von Shadow-IT-Fällen mit KI
- **80 %** der Policy-Verstösse betreffen geschützte Gesundheitsdaten (PHI)
- **$ 7,42 Mio.** durchschnittliche Kosten eines Datenschutzvorfalls im Gesundheitswesen
- → Verbote allein funktionieren nicht. Mitarbeitende brauchen sichere Alternativen.

### Internationaler Datentransfer

- **Staatenliste des BJ** (Anhang 1 DSV): Staaten mit angemessenem Datenschutzniveau
- **Swiss-U.S. Data Privacy Framework**: USA auf der Liste — aber nur für zertifizierte Unternehmen
- **Standardvertragsklauseln (SCCs)**: Fallback für Länder ohne Angemessenheit
- **Self-hosted KI**: Eliminiert Datentransfer-Problem komplett — besonders relevant bei Berufsgeheimnis

> **Sprechernotizen:**
> Diese Folie hat zwei Kernbotschaften. Erstens: Wer KI verbietet, ohne Alternativen anzubieten, züchtet Shadow AI. Die Zahlen von Wolters Kluwer und Digital Health Insights zeigen das deutlich. Mitarbeitende nutzen ChatGPT über private Geräte, kopieren Patientendaten in nicht genehmigte Tools — weil sie ihre Arbeit effizienter erledigen wollen. Die Lösung: Genehmigte, sichere KI-Tools bereitstellen. Zweitens: Internationaler Datentransfer. Die meisten KI-Anbieter sitzen in den USA. Seit dem Swiss-U.S. Data Privacy Framework stehen die USA auf der Staatenliste — aber nur für DPF-zertifizierte Unternehmen (Microsoft, Google, OpenAI sind zertifiziert). Für alle anderen: SCCs. Und bei Berufsgeheimnis ist Self-hosted KI oft die einzige saubere Lösung.

> **Quellen:**
> - Wolters Kluwer: Shadow AI Report (4.1) — https://www.wolterskluwer.com/en/solutions/uptodate/ai-clinical-decision-support/shadow-ai-report
> - Digital Health Insights: Shadow AI (4.2) — https://dhinsights.org/blog/shadow-ai-emerges-as-one-of-healthcares-biggest-security-risks/
> - BJ: Staatenliste — Internationaler Datentransfer (1.8) — https://www.bj.admin.ch/bj/de/home/staat/datenschutz/internationales/anerkennung-staaten.html
> - BFH-Studie: Open-Source-KI und Berufsgeheimnis (1.6) — https://www.bfh.ch/dam/jcr:deb88ea7-662d-499a-8a1c-fb83d070f113/Das%20Potenzial%20von%20Open%20Source%20KI%20im%20Kontext%20von%20Datenschutz%20und%20Berufsgeheimnis.pdf

---

## Slide 9 — Umsetzung: Technische Governance

### SSO (Single Sign-On)

- Zentrale Identität für alle KI-Tools — keine separaten Logins
- Ermöglicht zentrale Zugriffskontrolle und Audit-Trail
- Verhindert Schatten-Accounts

### Trainingsdaten

- **Opt-out sicherstellen**: Vertraglich und technisch regeln, dass Patientendaten nicht ins Modelltraining fliessen
- API-Nutzung statt Consumer-Versionen (z.B. OpenAI API mit Opt-out vs. ChatGPT Free)

### Zugriffsberechtigungen

- **Rollenbasiert** (RBAC): Wer darf welche KI-Tools mit welchen Daten nutzen?
- **Least Privilege**: Nur die Berechtigungen, die für die Aufgabe nötig sind
- **Audit-Logs**: Nachvollziehbarkeit aller KI-Interaktionen mit Personendaten

### DLP (Data Loss Prevention)

- Verhindern, dass Gesundheitsdaten unkontrolliert an externe KI-Dienste fliessen
- Technische Massnahmen: Content Inspection, Endpoint Controls, API-Gateway mit Filterregeln
- Organisatorische Massnahmen: Genehmigte Tools, klare Richtlinien, Schulung

> **Sprechernotizen:**
> Hier kommen wir von der Theorie in die Praxis. Vier Umsetzungsaspekte, die sofort angegangen werden können. SSO ist die Grundlage — ohne zentrale Identität kann man KI-Nutzung nicht steuern. Trainingsdaten sind ein heisses Thema: Die meisten Consumer-KI-Tools nutzen Eingabedaten standardmässig fürs Training. Über die API lässt sich das deaktivieren — aber es muss vertraglich abgesichert sein. Zugriffsberechtigungen: Nicht jede Abteilung braucht Zugang zu allen KI-Tools, und nicht jedes Tool braucht Zugang zu allen Daten. DLP ist die letzte Verteidigungslinie: Wenn trotz allem jemand versucht, Patientendaten in ein nicht genehmigtes Tool zu kopieren, sollte DLP das erkennen und blockieren.

> **Quellen:**
> - HealthTech Magazine: How to Address Shadow AI in Healthcare (4.3) — https://healthtechmagazine.net/article/2026/03/how-address-shadow-ai-healthcare
> - NIST AI Risk Management Framework (3.1) — https://www.nist.gov/itl/ai-risk-management-framework
> - ISO/IEC 42001:2023 — AI Management System (3.2) — https://www.iso.org/standard/42001
> - KPMG CH: ISO/IEC 42001 für AI Governance (3.3) — https://kpmg.com/ch/en/insights/artificial-intelligence/iso-iec-42001.html

---

## Slide 10 — Wrap-up: 5 erste Schritte zum Handeln

### Jetzt starten — nicht perfekt, aber strukturiert

1. **Risiken eruieren — von Nichtstun und von falschem Tun.** Zwei Seiten der Medaille: Wer KI ignoriert, riskiert Wettbewerbsnachteile (Konkurrenz arbeitet schneller, günstiger, qualitativ besser) bis hin zum Kundenverlust. Wer KI unkontrolliert einsetzt, riskiert Datenabfluss durch Shadow AI, Compliance-Verstösse und Reputationsschäden. Beides auf Stufe Unternehmensstrategie bewerten — nicht nur auf Tool-Ebene.

2. **Bestandsaufnahme** — Alle KI-Tools im Unternehmen inventarisieren, inkl. Shadow AI. Wer nutzt was, mit welchen Daten, in welchem Betriebsmodell? Die Tool-Inventur ist die Grundlage — aber erst nachdem die strategischen Risiken klar sind.

3. **Risikoklassifikation pro Tool** — Jedes inventarisierte Tool nach Datenkategorie (allgemeine vs. besonders schützenswerte Personendaten), Einsatzbereich (Medizinprodukt vs. Assistenz) und Betriebsmodell (Cloud vs. Self-hosted) bewerten. Priorisierung nach Risiko und Nutzen.

4. **Sichere Alternativen bereitstellen & Richtlinien erstellen** — Genehmigte KI-Tools mit SSO, DLP und Opt-out anbieten. Praxisorientierte KI-Policy mit Do's und Don'ts. Behandlungsverträge und Datenschutzerklärungen um KI-Klauseln ergänzen. Lösungen vor Verboten — sonst entsteht Shadow AI.

5. **DSFA durchführen** — Für alle Hochrisiko-Anwendungen. Bei Gesundheitsdaten + KI ist eine DSFA nach Art. 22 DSG praktisch immer Pflicht.

### Arxio unterstützt Sie dabei

- Strukturierter KI-Framework-Ansatz — von der Bestandsaufnahme bis zur Umsetzung
- Analyse, Priorisierung, Richtlinien, Enablement und Solution Design

**Kontakt:** ilya.vasilenko@arxio.ch | [LinkedIn](https://www.linkedin.com/in/ilya-vasilenko-09a93b7b/)

> **Sprechernotizen:**
> Die Schlussfolie soll Mut machen und Handlungsfähigkeit erzeugen. Die Botschaft: Man muss nicht alles auf einmal lösen, aber man muss anfangen. Schritt 1 ist bewusst strategisch: Bevor man einzelne Tools bewertet, muss man die Unternehmensrisiken durch KI verstehen — in beide Richtungen. Nichtstun ist ein Risiko: Konkurrenten, die KI effektiv einsetzen, arbeiten schneller und günstiger — das kann Kundschaft kosten, Revenue und im Extremfall die Existenz. Falsches Tun ist ebenfalls ein Risiko: Unkontrollierte KI-Nutzung führt zu Datenabfluss, Compliance-Verstössen und Reputationsschäden. Erst wenn diese strategische Einordnung steht, lohnt sich die Tool-Inventur (Schritt 2) und die detaillierte Risikobewertung pro Tool (Schritt 3). Schritte 4 und 5 sind dann die operative Umsetzung. Beim Abschluss: Visitenkarten bereithalten, QR-Code zur LinkedIn-Seite einblenden. Fragen aus dem Publikum aktiv einladen.

> **Quellen:**
> - HealthTech Magazine: How to Address Shadow AI in Healthcare (4.3) — https://healthtechmagazine.net/article/2026/03/how-address-shadow-ai-healthcare
> - KPMG CH: ISO/IEC 42001 für AI Governance (3.3) — https://kpmg.com/ch/en/insights/artificial-intelligence/iso-iec-42001.html
> - HealthTech Magazine: What Healthcare Organizations Can Learn from NIST AI RMF (3.4) — https://healthtechmagazine.net/article/2026/03/what-healthcare-organizations-can-learn-nists-ai-risk-management-framework
