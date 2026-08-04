# Slide 4 — Einwilligung vs. Informationspflicht

## Kernaussage: Das ist nicht das Gleiche!

Häufiger Irrtum: „Wir brauchen für alles eine Einwilligung." Das ist DSGVO-Denken, nicht DSG-Denken.

---

## 1. Vergleich

| | **Informationspflicht** (Art. 19 DSG) | **Einwilligung** (Art. 6 Abs. 6/7, Art. 31 DSG) |
|---|---|---|
| **Wann?** | **Immer** — bei jeder Datenbearbeitung | Nur bei Persönlichkeitsverletzung (Art. 30) ohne anderen Rechtfertigungsgrund |
| **Inhalt** | Verantwortlicher, Zweck, Empfänger, Auslandsbekanntgabe | Freiwillige, informierte Willensäusserung für bestimmte Bearbeitungen |
| **Form** | Formfrei (DSE, Patienteninfo, Aushang) | Formfrei; bei Gesundheitsdaten: **ausdrücklich** (Art. 6 Abs. 7) |
| **Verzichtbar?** | **Nein** | **Ja** — wenn Vertrag, überwiegendes Interesse oder Gesetz greift |
| **Verstoss** | Persönlichkeitsverletzung; Busse bis CHF 250'000 (Art. 60 DSG) | Rechtswidrige Bearbeitung; zivilrechtliche Ansprüche (Art. 32 DSG) |

---

## 2. Erlaubnisprinzip CH vs. Verbotsprinzip EU

| | **CH DSG** | **EU DSGVO** |
|---|---|---|
| **Prinzip** | Erlaubnisprinzip mit Verbotsvorbehalt | Verbotsprinzip mit Erlaubnisvorbehalt |
| **Bearbeitung** | Grundsätzlich **erlaubt** (Art. 6 + Art. 8 DSG einhalten) | Grundsätzlich **verboten** ohne Rechtsgrundlage |
| **Einwilligung** | Einer von drei Rechtfertigungsgründen — selten nötig | Eine von sechs Rechtsgrundlagen — häufig verwendet |

Art. 6 Abs. 6/7 DSG = **kein allgemeines Einwilligungserfordernis**. Definiert nur Gültigkeitsvoraussetzungen. Auch bei Gesundheitsdaten nicht per se nötig.

Einwilligung wird relevant wenn:
1. Persönlichkeitsverletzung vorliegt (Art. 30 DSG)
2. Kein anderer Rechtfertigungsgrund greift (Art. 31 DSG)

---

## 3. Wann Einwilligung nötig? — Praxisfälle

| Situation | Einwilligung? | Grund |
|---|---|---|
| Patientendaten für Behandlung | **Nein** | Behandlungsvertrag (Art. 31 Abs. 2 lit. a) |
| Bekanntgabe an Versicherer / Abrechnung | **Nein** | Gesetzlich vorgesehen (KVG) |
| Bekanntgabe an zuweisenden Arzt | **Nein** | Überwiegendes Interesse |
| Gesundheitsdaten an behandlungsfremde Dritte | **Ja, ausdrücklich** | Art. 30 Abs. 2 lit. c → Persönlichkeitsverletzung |
| Patientendaten für Forschung (nicht anonymisiert) | **Ja, ausdrücklich** | Zweckänderung; ggf. HFG Art. 7 |
| Patientendaten für KI-Modelltraining | **Ja, ausdrücklich** | Über Behandlungszweck hinaus |
| Automatisierte Einzelentscheidung ohne Mensch | **Ja, ausdrücklich** | Art. 21 Abs. 3 lit. b (Alternative: Vertrag) |
| Auslandsbekanntgabe ohne angemessenes Schutzniveau | **Ja, ausdrücklich** | Art. 17 Abs. 1 lit. a |

---

## 4. Sonderfrage: KI im Behandlungskontext — Rechtsgrundlage

### Zwei Regime: Privat vs. Öffentlich

| | **Private Leistungserbringer** | **Öffentliche Leistungserbringer** (Grundversorgung) |
|---|---|---|
| **Rechtsgrundlage Behandlung** | Privatrechtlicher Behandlungsvertrag | **Gesetz** (kantonale Spital-/Gesundheitsgesetze, KVG). Aufnahmepflicht, kein Vertrag nötig |
| **Rechtsgrundlage Datenbearbeitung** | Erlaubnisprinzip (Art. 6 DSG); Vertrag als Rechtfertigung bei Persönlichkeitsverletzung (Art. 31 Abs. 2 lit. a) | **Legalitätsprinzip**: Datenbearbeitung nur mit gesetzlicher Grundlage. Bei besonders schützenswerten Daten: Grundlage im formellen Gesetz erforderlich |
| **Regime** | Bundes-DSG | **Kantonales Datenschutzgesetz** |
| **KI-Einsatz** | Erlaubt, sofern DSG-Grundsätze eingehalten | Nur mit ausreichender **gesetzlicher Grundlage** + Vorabkontrolle durch kantonalen DSB |

### Kernproblem Private: KI nicht zwingend für Vertrag

KI ist nicht zwingend notwendig für Vertragserfüllung. Arzt kann Befund auch ohne KI erstellen. Greift „Vertragsabwicklung" (Art. 31 Abs. 2 lit. a)?

| Frage | Prüfung |
|---|---|
| **1. Persönlichkeitsverletzung?** | Self-hosted, Daten intern → kaum. Cloud-KI, Daten an Dritten → Art. 30 Abs. 2 lit. c = ja |
| **2. Vertrag als Rechtfertigung?** | Art. 31 Abs. 2 lit. a: „Zusammenhang mit Abwicklung eines Vertrags" — offener als DSGVO. Aber: wenn Vertrag KI nicht erwähnt → angreifbar |
| **3. Vertrag anpassen?** | KI-Klausel im Behandlungsvertrag → Vertragsgrundlage wird tragfähiger |

### Kernproblem Öffentliche: Gesetz deckt KI (noch) nicht

Öffentliche Spitäler bearbeiten Patientendaten gestützt auf kantonale Gesundheits- und Spitalgesetze. Diese Gesetze wurden vor KI geschrieben. Die Frage:

- **Das Gesetz deckt die Behandlung** und die dafür nötige Datenbearbeitung (Diagnose, Dokumentation, Abrechnung)
- **Das Gesetz deckt nicht die Methode KI**. Es sagt nicht: „Die Datenbearbeitung darf mittels KI erfolgen"
- Kantonale DSB stufen KI als **„neue Technologie"** ein → Vorabkontrolle erforderlich
- Massgebend: Ist die bestehende gesetzliche Grundlage ausreichend, um KI-gestützte Datenbearbeitung zu rechtfertigen?

**Konsequenz:** Für öffentliche Organe ist KI-Einsatz **strenger** als im privaten Sektor. Privat gilt Erlaubnisprinzip (erlaubt, sofern keine Persönlichkeitsverletzung). Öffentlich gilt Legalitätsprinzip (nur mit gesetzlicher Grundlage).

### Vertiefung: Reicht die bestehende Rechtsgrundlage für KI?

Aktuell keine explizite KI-Regulierung in CH. Frage: Deckt der gesetzliche Behandlungsauftrag (Grundversorgung) auch KI als Methode ab?

**Argument JA — gleiche Rechtsgrundlage genügt:**
- DSG ist technologieneutral (EDÖB bestätigt). Gesetz schreibt nicht vor *wie* bearbeitet wird
- KI = Werkzeug für denselben Zweck. Wie Ultraschall statt Stethoskop — Gesetz erlaubt Ultraschall nicht explizit, verbietet ihn aber auch nicht
- Zweck ändert sich nicht (Behandlung). Nur Methode ändert sich

**Argument NEIN — reicht nicht:**
- KI bringt neue Risiken, die Gesetzgeber nicht kannte (Datenabfluss, Bias, automatisierte Entscheidungen)
- Kantonale DSB stufen KI als „neue Technologie" ein → Vorabkontrolle impliziert, dass bestehende Grundlage allein nicht selbstverständlich genügt
- Verhältnismässigkeit: Wenn KI nicht *notwendig* für Behandlung, ist Einsatz verhältnismässig?
- Cloud-KI = Daten an Dritte → über das hinaus, was Gesundheitsgesetz bei Erlass vorgesehen hat
- Bei besonders schützenswerten Daten: Grundlage im formellen Gesetz nötig — allgemeiner Behandlungsauftrag evtl. nicht spezifisch genug

**Stand heute:** Kein Gericht hat entschieden. Kantonale DSB lösen es pragmatisch: **Vorabkontrolle = Mechanismus, um zu prüfen, ob bestehende Rechtsgrundlage für den konkreten KI-Einsatz ausreicht.** Ergebnis kann sein: „Ja, genügt für diesen Use Case" oder „Nein, zusätzliche Massnahmen / Einwilligung nötig." Self-hosted (Daten intern) leichter zu rechtfertigen als Cloud-KI.

**Kurzformel:** Rechtsgrundlage bleibt dieselbe (Behandlungsauftrag). Ob sie *ausreicht* für KI, wird fallweise durch Vorabkontrolle geprüft. Genau das ist der Sinn der Vorabkontrolle — nicht neue Rechtsgrundlage schaffen, sondern bestehende auf Tragfähigkeit prüfen.

### Bewertung nach Szenario

| Szenario | Privat | Öffentlich |
|---|---|---|
| Self-hosted KI, Daten intern, Arzt prüft | Wahrsch. **keine Einwilligung nötig** — Informationspflicht genügt | **Vorabkontrolle** durch kantonalen DSB; Rechtsgrundlage dokumentieren |
| Cloud-KI, KI transparent kommuniziert | Vertretbar **ohne Einwilligung** (Vertrag + Info) | Vorabkontrolle **+ Prüfung**, ob gesetzliche Grundlage Cloud-Auslagerung erlaubt |
| Cloud-KI, KI nicht kommuniziert | Eher **Einwilligung nötig** | **Nicht zulässig** — keine Rechtsgrundlage, keine Transparenz |
| Daten für KI-Training / Forschung | **Einwilligung, ausdrücklich** | **Nicht zulässig** ohne spezifische gesetzliche Grundlage |

### Pragmatische Empfehlung

**Private:** Behandlungsverträge um KI-Klauseln ergänzen + transparent informieren. Stärkt Vertragsgrundlage + erfüllt Informationspflicht.

**Öffentliche:** Rechtsgrundlage im kantonalen Gesetz identifizieren und dokumentieren. Vorabkontrolle beim kantonalen DSB einleiten. ISDS-Konzept + DSFA erstellen. Self-hosted KI bevorzugen, wo Rechtsgrundlage für Cloud-Auslagerung unklar.

---

## 5. Gültige Einwilligung (wenn nötig)

**Gewöhnlich** (Art. 6 Abs. 6): freiwillig, informiert, bestimmt, urteilsfähig, vor Bearbeitung.

**Ausdrücklich** (Art. 6 Abs. 7) — bei Gesundheitsdaten, Profiling mit hohem Risiko: aktive Handlung (Unterschrift, Checkbox ankreuzen). Vorausgefüllte Häkchen / Schweigen genügen nicht.

---

## 6. Informationspflicht — Was immer gilt

**Mindestinhalt (Art. 19 DSG):** Verantwortlicher + Kontakt, Zweck, Empfänger, bei Ausland: Zielstaat + Garantien, bei automatisierten Entscheidungen: Hinweis + Recht auf menschliche Überprüfung.

**KI-spezifisch ergänzen:**
- DSE: KI-Tools, Zweck, betroffene Daten
- Patienteninfo: „Wir nutzen KI-gestützte Transkription für Arztberichte"
- Auslandsübermittlung: Zielstaat + Schutzmechanismus

---

## 7. Häufige Fehler

| Fehler | Problem | Besser |
|---|---|---|
| Einwilligung für alles | Widerruf blockiert Behandlung | Vertrag nutzen wo möglich |
| Info vs. Einwilligung verwechselt | Einwilligung geholt, aber nicht informiert | Zuerst informieren (Art. 19), dann ggf. Einwilligung |
| Vorausgefüllte Checkboxen | Ungültige ausdrückliche Einwilligung | Leere Checkbox, aktives Ankreuzen |
| Pauschaleinwilligung | Zu unbestimmt → ungültig | Pro Zweck und Bearbeitungsvorgang |

---

## Quellen

| Nr. | Quelle | URL |
|---|---|---|
| 1.10 | Datenschutztreuhand: Einwilligung nach DSG | https://datenschutztreuhand.ch/grundsaetzliches-zur-einwilligung-nach-dsg/ |
| 1.11 | Online-Kommentar: Art. 6 Abs. 6/7 DSG | https://onlinekommentar.ch/de/kommentare/art6abs6und7 |
| 1.12 | Bratschi AG: KI im Gesundheitswesen | https://www.bratschi.ch/publikationen/rechtliche-anforderungen-an-die-nutzung-von-ki-applikationen-im-gesundheitswesen |
| 1.16 | HIN: nDSG Gesundheitswesen | https://www.hin.ch/de/blog/2023/ndsg-gesundheitswesen-teil-1.cfm |
| 1.17 | Fedlex: DSG Volltext | https://www.fedlex.admin.ch/eli/cc/2022/491/de |
| — | FMH: Musterdokumente nDSG | https://www.fmh.ch/themen/ehealth/datenschutz/neues-datenschutzgesetz-dsg.cfm |
