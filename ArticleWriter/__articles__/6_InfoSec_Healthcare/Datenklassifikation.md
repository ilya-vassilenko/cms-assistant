# Datenklassifikation im Gesundheitswesen (Schweiz)

Übersicht der relevanten Datenkategorien und Geheimnisschutzregime für den KI-Einsatz im Gesundheitswesen. Fokus auf das Schweizer Datenschutzgesetz (DSG), Art. 320 StGB (Amtsgeheimnis) und Art. 321 StGB (Berufsgeheimnis).

---

## 1. Personendaten vs. besonders schützenswerte Personendaten

### Gesetzliche Grundlage: Art. 5 DSG

| Kategorie | Definition | Beispiele im Gesundheitswesen | Rechtsfolgen |
|---|---|---|---|
| **Personendaten** (Art. 5 lit. a DSG) | Alle Angaben, die sich auf eine bestimmte oder bestimmbare natürliche Person beziehen | Name, Adresse, Geburtsdatum, Versichertennummer, Telefonnummer, E-Mail, IP-Adresse, Personalnummer | Bearbeitung grundsätzlich erlaubt bei Einhaltung der Bearbeitungsgrundsätze (Art. 6 DSG); Informationspflicht (Art. 19 DSG) |
| **Besonders schützenswerte Personendaten** (Art. 5 lit. c DSG) | Abschliessend aufgelistete Datenkategorien mit erhöhtem Risiko für Persönlichkeit oder Grundrechte | Siehe Detailtabelle unten | Erhöhte Anforderungen an Sicherheit, Transparenz und Kontrolle; DSFA häufig Pflicht (Art. 22 DSG); bei Einwilligung: ausdrücklich erforderlich |

### Detailtabelle: Besonders schützenswerte Personendaten (Art. 5 lit. c Ziff. 1–6 DSG)

| Ziff. | Kategorie | Beispiele im Gesundheitswesen |
|---|---|---|
| 1 | Religiöse, weltanschauliche, politische oder gewerkschaftliche Ansichten oder Tätigkeiten | Konfessionszugehörigkeit im Patientenstamm (z.B. für Seelsorge); Gewerkschaftsmitgliedschaft von Spitalpersonal |
| 2 | Gesundheit, Intimsphäre, Zugehörigkeit zu einer Rasse oder Ethnie | Diagnosen, Therapien, Medikation, Laborwerte, Operationsberichte, psychische Befunde, Suchterkrankungen, Schwangerschaft, sexuelle Orientierung, ethnische Herkunft |
| 3 | Genetische Daten | Genanalysen, Erbkrankheits-Screenings, pharmakogenetische Profile |
| 4 | Biometrische Daten, die eine Person eindeutig identifizieren | Fingerabdruck für Medikamentenausgabe, Iris-Scan für Zutrittskontrolle, Gesichtserkennung im Spital |
| 5 | Verwaltungs- und strafrechtliche Verfolgungen oder Sanktionen | Strafregisterauszug bei der Anstellung von Gesundheitspersonal; Information über laufende Verfahren gegen Mitarbeitende |
| 6 | Massnahmen der sozialen Hilfe | Sozialhilfebezug eines Patienten (relevant für Abrechnung bei Gemeinde/Kanton); KESB-Massnahmen |

### Typische Daten im Gesundheitswesen und ihre Einordnung

| Datenbeispiel | Personendaten | Besonders schützenswert | Bemerkung |
|---|---|---|---|
| Patientenname, Adresse, Geburtsdatum | Ja | Nein | Allgemeine Personendaten |
| Versichertennummer (AHV-Nr.) | Ja | Nein | Systematische Verwendung nach AHVG geregelt |
| Diagnose, ICD-Code | Ja | **Ja** (Ziff. 2) | Gesundheitsdaten |
| Medikamentenliste | Ja | **Ja** (Ziff. 2) | Rückschluss auf Gesundheitszustand |
| Laborergebnisse, Blutgruppe | Ja | **Ja** (Ziff. 2) | Gesundheitsdaten |
| Operationsbericht | Ja | **Ja** (Ziff. 2) | Gesundheitsdaten |
| Psychologisches Gutachten | Ja | **Ja** (Ziff. 2) | Gesundheit + Intimsphäre |
| Gentest-Ergebnis | Ja | **Ja** (Ziff. 3) | Genetische Daten |
| Fingerabdruck (Zutrittssystem) | Ja | **Ja** (Ziff. 4) | Biometrische Daten |
| Mitarbeiter-Name, Dienstplan | Ja | Nein | Allgemeine Personendaten |
| Mitarbeiter-Krankmeldung mit Diagnose | Ja | **Ja** (Ziff. 2) | Gesundheitsdaten |
| Lohnabrechnung mit Sozialhilfe-Abzug | Ja | **Ja** (Ziff. 6) | Massnahmen der sozialen Hilfe |
| Arzt-Patienten-Gespräch (Transkription) | Ja | **Ja** (Ziff. 2) | Gesundheitsdaten + ggf. Intimsphäre |
| Terminbuchung (ohne Grund) | Ja | Nein | Kein Rückschluss auf Gesundheitszustand |
| Terminbuchung (mit Fachrichtung) | Ja | **Ja** (Ziff. 2) | Rückschluss auf Gesundheitszustand möglich (z.B. Onkologie) |

---

## 2. Amtsgeheimnis vs. Berufsgeheimnis

### Überblick

| | Amtsgeheimnis (Art. 320 StGB) | Berufsgeheimnis (Art. 321 StGB) |
|---|---|---|
| **Geschütztes Gut** | Geheimhaltungsinteresse des Gemeinwesens und der betroffenen Personen | Vertrauensverhältnis zwischen Berufsträger und Klient/Patient |
| **Wer unterliegt?** | Behördenmitglieder, Beamte und Angestellte der öffentlichen Verwaltung, deren Hilfspersonen | Ärzte, Zahnärzte, Chiropraktoren, Apotheker, Hebammen, Psychologen, Pflegefachpersonen, Physiotherapeuten, Ergotherapeuten, Ernährungsberater, Optometristen, Osteopathen — und deren Hilfspersonen |
| **Was ist geschützt?** | Geheimnisse, die in amtlicher oder dienstlicher Stellung anvertraut oder wahrgenommen werden | Geheimnisse, die infolge des Berufes anvertraut werden oder die in dessen Ausübung wahrgenommen werden |
| **Strafrahmen** | Freiheitsstrafe bis 3 Jahre oder Geldstrafe | Freiheitsstrafe bis 3 Jahre oder Geldstrafe |
| **Entbindung** | Schriftliche Einwilligung der vorgesetzten Behörde | Einwilligung des Berechtigten (Patient) ODER schriftliche Bewilligung der Aufsichtsbehörde |
| **Dauer** | Auch nach Beendigung des amtlichen Verhältnisses | Auch nach Beendigung der Berufsausübung |
| **Deliktart** | Echtes Sonderdelikt (nur bestimmte Personen) | Echtes Sonderdelikt (nur bestimmte Berufsgruppen) |

### Wer unterliegt welchem Regime? — Zuordnung im Gesundheitswesen

| Organisation / Rolle | Amtsgeheimnis (Art. 320) | Berufsgeheimnis (Art. 321) | Bemerkung |
|---|---|---|---|
| Kantonales Spital (Angestellte) | **Ja** | Zusätzlich für Gesundheitsfachpersonen | Doppelte Bindung möglich |
| Universitätsklinik (Angestellte) | **Ja** | Zusätzlich für Gesundheitsfachpersonen | Öffentliches Organ |
| Niedergelassener Arzt / Ärztin | Nein | **Ja** | Rein privatrechtlich |
| Privatklinik (Angestellte) | Nein (in der Regel) | **Ja** (für Gesundheitsfachpersonen) | Kantonale Regelungen beachten |
| Krankenkasse (Grundversicherung) | **Ja** (öffentlicher Auftrag) | Nein | Kantonales DSG anwendbar |
| Krankenkasse (Zusatzversicherung) | Nein | Nein | Privatrechtlich, Bundes-DSG |
| Apotheke (privat) | Nein | **Ja** | Art. 321 StGB |
| IT-Dienstleister des Spitals | Ggf. als Hilfsperson | Ggf. als Hilfsperson | Status muss vertraglich geklärt werden |
| KI-Cloud-Anbieter | Ggf. als Hilfsperson | Ggf. als Hilfsperson | Hilfspersonen-Status nur unter strengen Voraussetzungen (funktionale Unterordnung, Weisungsbindung) |
| Spital-Verwaltung (nicht-medizinisch) | **Ja** | Nein | Administratives Personal im öff. Dienst |

### Konsequenzen für den KI-Einsatz

| Szenario | Amtsgeheimnis | Berufsgeheimnis | Massnahme |
|---|---|---|---|
| Cloud-KI für Befundzusammenfassung (kantonales Spital) | Betroffen | Betroffen | Doppelte Prüfung: Behördliche Genehmigung + Patienten-Einwilligung oder Hilfspersonen-Konstruktion; Self-hosted KI prüfen |
| Cloud-KI für Arztbriefe (niedergelassener Arzt) | Nicht betroffen | Betroffen | Patienten-Einwilligung oder Hilfspersonen-Status des Anbieters; Confidential Computing prüfen |
| KI für Abrechnungsoptimierung (Krankenkasse Grundversicherung) | Betroffen | Nicht betroffen | Kantonale Vorabkontrolle; Rechtsgrundlage definieren |
| KI für Marketing-Texte (Privatklinik) | Nicht betroffen | Nicht betroffen (keine Patientendaten) | Allgemeine DSG-Anforderungen genügen |
| Self-hosted KI für Transkription (kantonales Spital) | Betroffen | Betroffen | Daten verlassen die Organisation nicht; Geheimnisschutz einfacher gewährleistbar |

---

## 3. Zusammenfassende Klassifikationsmatrix

| Datenkategorie | Schutzniveau | Anwendbares Recht | Einwilligung | DSFA | KI-Einsatz |
|---|---|---|---|---|---|
| Allgemeine Personendaten (Name, Adresse) | Standard | DSG Art. 6 | Nicht erforderlich (Informationspflicht genügt) | Nur bei hohem Risiko | Grundsätzlich möglich unter DSG-Grundsätzen |
| Besonders schützenswerte Personendaten (Gesundheitsdaten) | Erhöht | DSG Art. 5 lit. c, Art. 6, Art. 22 | Wenn nötig: ausdrücklich | In der Regel Pflicht | Erhöhte Anforderungen; Opt-out für Trainingsdaten; DLP |
| Daten unter Amtsgeheimnis | Hoch | Art. 320 StGB + kantonales DSG | Schriftliche Genehmigung der vorgesetzten Behörde | Pflicht (kantonale Vorabkontrolle) | Rechtsgrundlage zwingend; Vorabkontrolle durch kantonalen DSB |
| Daten unter Berufsgeheimnis | Hoch | Art. 321 StGB + DSG | Einwilligung des Patienten oder Aufsichtsbehörde | In der Regel Pflicht | Self-hosted prüfen; Hilfspersonen-Status klären; Confidential Computing |
| Daten unter Amts- UND Berufsgeheimnis | Höchst | Art. 320 + Art. 321 StGB + kantonales DSG | Behörde + Patient | Pflicht | Strengste Anforderungen; Self-hosted bevorzugt; doppelte Genehmigung |

---

## Quellen

| Nr. | Quelle | URL |
|---|---|---|
| 1 | Fedlex: DSG Volltext (Art. 5) | https://www.fedlex.admin.ch/eli/cc/2022/491/de |
| 2 | activeMind: Personendaten richtig einordnen und schützen | https://www.activemind.ch/blog/personendaten/ |
| 3 | LAW.CH: Checkliste besonders schützenswerte Personendaten | https://law.ch/lawinfo/datenschutzrecht/checklisten/checkliste-besonders-schuetzenswerte-personendaten/ |
| 4 | Datenschutz.law: Besonders schützenswerte Daten | https://datenschutz.law/ratgeber/besonders-schuetzenswerte-daten |
| 5 | Lawbrary: Art. 320 StGB (Amtsgeheimnis) | https://lawbrary.ch/law/art/STGB-v2022.11-de-art-320/ |
| 6 | Lawbrary: Art. 321 StGB (Berufsgeheimnis) | https://lawbrary.ch/law/art/STGB-v2024.07-de-art-321/ |
| 7 | IRM Uni Bern: Ärztliches Berufsgeheimnis | https://www.irm.unibe.ch/weiterbildung/lexikon_der_rechtsmedizin/aerztliches_berufsgeheimnis/index_ger.html |
| 8 | DSB Kanton Zürich: Generative KI für öffentliche Organe | https://www.datenschutz.ch/tb/2024/sichere-kuenstliche-intelligenz |
| 9 | DSB Kanton Zürich: Merkblatt Cloud Computing | https://docs.datenschutz.ch/u/d/publikationen/formulare-merkblaetter/merkblatt_cloud_computing.pdf |
| 10 | Kt. Zürich: Datenschutz, Berufsgeheimnis und die Cloud | https://www.zh.ch/de/wirtschaft-arbeit/wirtschaftsstandort/innovation-sandbox/medizinische-dokumentation/2-datenschutz-berufsgeheimnis-und-die-cloud.html |
| 11 | EDÖB: Leitfaden Personendaten im medizinischen Bereich | https://www.edoeb.admin.ch/dam/en/sd-web/83-BtvM9d98r/leitfaden_fuer_diebearbeitungvonpersonendatenimmedizinischenbere_DE.pdf |
| 12 | ASIP: DSG-Umsetzung — besonders schützenswerte Daten | https://dsg-umsetzung.asip.ch/welche-daten-werden-als-besonders-schuetzenswert |
