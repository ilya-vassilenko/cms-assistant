<!-- Source: https://www.bsi.bund.de/DE/Service-Navi/Publikationen/Studien/Office_Telemetrie/telemetrie.html -->

# Evaluierung der Telemetrie von Microsoft Office 365

![Bild-Dokument für das Frontend](https://www.bsi.bund.de/SiteGlobals/Frontend/Images/kopfbereich.png?__blob=normal&v=11)

Büroanwendungen gehören im privaten wie auch im beruflichen Umfeld zu den am häufigsten genutzten Anwendungsprogrammen. Sie umfassen unter anderem Applikationen zur Textverarbeitung, Tabellenkalkulation und Erstellung von Präsentationen. Hersteller sammeln u.a. zur Optimierung ihrer Produkte teilweise umfangreiche Daten über die Nutzung der Software. Diese Daten werden als Telemetrie bezeichnet und können von Versionsangaben und Nutzungsverhalten bis hin zu Absturzberichten inkl. Inhalten von Dokumenten reichen. Bei Microsoft Office 365 übernehmen Telemetriemodule dabei das Sammeln und Senden von Diagnosedaten an von Microsoft verwaltete Serversysteme zum Speichern und Verarbeiten. Neben Telemetrie existieren noch sogenannte "verbundene Erfahrungen". Verbundene Erfahrungen sind Funktionen von Office-Anwendungen, die während des Betriebs mit dem Microsoft-Backend kommunizieren und Daten austauschen können. Im Unterschied zu Telemetrie ist das Ziel verbundener Erfahrungen keine Diagnostik, sondern dem Anwender konkrete Funktionen anzubieten, wie z.B. die Verwendung der Diktierfunktion oder das Übersetzen von Text in eine andere Sprache. Sowohl Office-Anwendungen als auch verbundene Erfahrungen führen zu Diagnoseereignissen, die im Rahmen von Telemetrie möglicherweise an Microsoft gesendet werden.

Microsoft hat eine Reihe von Datenschutzeinstellungen für Office 365 in Form von Gruppenrichtlinieneinstellungen veröffentlicht. Benutzer können beispielsweise die "Stufe der von Office an Microsoft gesendeten Clientsoftware-Diagnosedaten konfigurieren", die Office 365 möglicherweise an das Microsoft-Backend sendet.

Als Einstellungsmöglichkeiten werden 1. "Erforderlich", 2. "Optional" und 3. "Weder noch" angeboten. Selbst bei Konfiguration der dritten Einstellungsmöglichkeit werden weiterhin bestimmte Diagnoseereignisse an Microsoft gesendet. Davon ausgehend hat das Bundesamt für Sicherheit in der Informationstechnik (BSI) die Firma ERNW GmbH beauftragt, die Auswirkungen der Einstellungen von Telemetriedaten in Microsoft Office 365 (i. F. Office genannt) für das Betriebssystem Windows 10 zu analysieren und darauf aufbauend Empfehlungen zu erstellen, wie die Datenübermittlung abgeschaltet oder zumindest reduziert werden kann. Die Motivation Telemetriedaten nicht mit dem Hersteller zu teilen kann sich sowohl aus dem privaten als auch aus dem beruflichen Interesse heraus ergeben. Das teilweise oder vollständige Deaktivieren der Übertragung von Diagnosedaten kann die Möglichkeit des Herstellers einschränken, Probleme bei der Verwendung des Produktes zu erkennen und zu beheben. Beispielsweise können Telemetriedaten auch für eine individuelle Fehlerbehebung genutzt werden. Daher sollte vorab geprüft werden, ob und wo eine Abschaltung der Telemetriedaten im Rahmen der Herstellerunterstützung notwendig ist. So könnte bspw. die Entscheidung für eine Testumgebung anders ausfallen als bei einer Produktivumgebung.

Die Telemetrie der verbundenen Erfahrungen ist nicht konfigurierbar, die Dienste müssten in den Gruppenrichtlinien abgeschaltet werden. Zusätzlich gibt es Abhängigkeiten wie die Lizensierung, Microsoft nennt diese notwendige verbundene Erfahrungen. Sie sind nicht in den Gruppenrichtlinien abschaltbar.

Um die Ausgabe der von Office erstellten Diagnosedaten vollständig zu deaktivieren bzw. weiter zu reduzieren, werden zwei weitere Lösungsansätze, die nicht vom Hersteller beschrieben werden, betrachtet:

- **Blockierung ausgehender Datenströme auf Netzwerkebene:**


Fortgeschrittene Endanwender und IT-Administratoren können ausgehende Diagnosedaten an der Firewall blockieren. Dazu müssen

1. alle Benutzeraktivitäten identifiziert werden, die im Zusammenhang mit den Anwendungen von Office ausgeführt werden können,
2. mittels einem Netzwerksniffer, der als Man-in-the-Middle zwischen der Windowsinstanz auf der Office läuft und dem Microsoft Backend agiert, während der Ausführung der Aktivitäten die Endpunkte des Backends \- an den die Diagnosedaten gesendet werden - beobachtet werden und die beobachteten Endpunkte für die Konfiguration der Firewall verwendet werden.

- **Erstellung eines Wertes in der Systemregistrierung:**


Indem der Systemregistrierungswert

HKEY\_CURRENT\_USER\\Software\\Policies\\Microsoft\\office\\common\\clienttelemetry\\DisableTelemetry

auf 1 gesetzt wird, können die Telemetriemodule deaktiviert werden. Dieser Wert kann nicht in den Gruppenrichtlinieneinstellungen von Office konfiguriert werden, sondern ausschließlich, indem er in der Systemregistrierung angelegt und konfiguriert wird.


Die drei genannten Lösungsansätze unterscheiden sich in ihrer Wirksamkeit (in Bezug auf die Menge der Ausgabe deaktivierter Diagnosedaten), der Komplexität der technischen Umsetzung und den Auswirkungen auf den Betrieb von Office-Anwendungen und den damit verbundenen Erfahrungen, vgl. Tabelle 1. Für eine möglichst umfassende Reduktion der Ausgabemenge mit Hilfe von Bordmitteln sollten daher die Lösungsansätze "Gruppenrichtlinien" sowie "Systemregistrierung" kombiniert werden. Erst eine zusätzliche Blockierung der verbleibenden Datenströme verhindert die vollständige Ausleitung von Telemetriedaten. Für eine nachhaltige Lösung muss der gewählte Ansatz regelmäßig überprüft werden, d.h. das einmalige Umsetzen eines der genannten Lösungsvorschläge reicht nicht aus. Durch Softwareupdates oder Neukonfigurierung der Telemetriemodule können sich beispielsweise die Endpunkte von Microsofts Backend \- zu denen die Telemetriemodule Diagnosedaten senden - über die Zeit ändern. Auch eine Änderung der Konfiguration oder des Verhaltens der Gruppenrichtlinien bzw. der Systemregistrierung ist denkbar.

## Tabelle 1: Relativer Vergleich der Ansätze zur Einschränkung von Telemetriedaten

|  | **Auswirkung auf Ausgabemenge** | **Auswirkung auf die Nutzbarkeit der Funktionen** | **Aufwand für Umsetzung der Maßnahme** | **Erforderliche IT-Fachkenntnisse** |
| --- | --- | --- | --- | --- |
| **Gruppenrichtlinien** |
| Verbundene Erfahrungen | hoch | sehr hoch | gering | gering |
| Office-Anwendungen | hoch | keine | gering | gering |
| **Netzwerkebene** |
| Verbundene Erfahrungen | sehr hoch | sehr hoch | sehr hoch | hoch |
| Office-Anwendungen | sehr hoch | hoch | sehr hoch | hoch |
| **Systemregistrierung** |
| Verbundene Erfahrungen | n/a | n/a | n/a | n/a |
| Office-Anwendungen | hoch | keine | gering | gering |

Das vollständige Ergebnis der Analyse ist in einem [englischsprachigen Bericht](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/Studien/Office_Telemetrie/Office_Telemetrie.html?nn=459634 "Analysis report: Microsoft Office Telemetry") verfügbar.

Kurz-URL:[https://www.bsi.bund.de/dok/14859576](https://www.bsi.bund.de/dok/14859576)
