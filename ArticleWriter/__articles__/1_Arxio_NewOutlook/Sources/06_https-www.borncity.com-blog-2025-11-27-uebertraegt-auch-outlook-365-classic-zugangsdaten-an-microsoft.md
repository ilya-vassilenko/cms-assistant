<!-- Source: https://www.borncity.com/blog/2025/11/27/uebertraegt-auch-outlook-365-classic-zugangsdaten-an-microsoft/ -->

[Zum Inhalt springen](https://borncity.com/blog/2025/11/27/uebertraegt-auch-outlook-365-classic-zugangsdaten-an-microsoft/#content)

# Überträgt auch Outlook 365 Classic Zugangsdaten an Microsoft?

Veröffentlicht am [27\. November 2025](https://borncity.com/blog/2025/11/27/uebertraegt-auch-outlook-365-classic-zugangsdaten-an-microsoft/ "08:18") von[Günter Born](https://borncity.com/blog/author/guenni/ "Alle Beiträge von Günter Born anzeigen")

![](https://borncity.com/blog/wp-content/uploads/2012/07/Office1.jpg)Dass die Outlook New-App Zugangsdaten von Mail-Konten an Microsoft überträgt, ist längst bekannt. Nun gibt es einen Bericht, dass auch neuere Versionen von Outlook Classic (also wohl Outlook 365) ihre kompletten Zugangsdaten für Konten an Microsoft übertragen.

Admin-Passwörter schützen mit Windows LAPS. [eBook jetzt herunterladen »](https://www.windowspro.de/landing-page/kostenloses-ebook-admin-passwoerter-schuetzen-windows-laps-registrierung?utm_source=bornitblog) (Sponsored by IT Pro)

## Rückblick: Der Outlook-New-Fall

![](https://vg04.met.vgwort.de/na/18c62fadb4fa404b8f69863e978b6a5d)Seit September 2023 stellt Microsoft die sogenannte "Neue Outlook-App" für Windows bereit, die bis 2029 auch Microsoft Classic ersetzen soll. Kurz nach Freigabe der App wurde dann bekannt, dass diese alle Zugangsdaten für konfigurierte Mail- und Kalenderkonten an Microsoft überträgt. Die Microsoft-Server speichern die Zugangsdaten, ziehen sich die Konteninhalte und stellen diese der Outlook New-App zum Abruf bereit.

Das Verhalten ist von Microsoft-Anwendungen bekannt. Bereits im Februar 2015 hatte ich im Blog-Beitrag [Outlook-App: Im EU-Parlament wegen IT-Sicherheit blockiert](https://borncity.com/blog/2015/02/07/outlook-app-im-eu-parlament-wegen-it-sicherheit-blockiert/) eine sicherheitstechnische Bombe beschrieben. Die IT des EU-Parlaments hatte die Outlook-App aus Sicherheitsgründen für eine Verwendung durch Mitglieder und Mitarbeiter des EU-Parlaments gesperrt. Hintergrund war, dass die App alle Anmeldedaten sowie dann auch die Inhalte gegenüber Microsoft offen legt.

Ebenfalls bekannt war, dass die Outlook-Apps für Android und iOS die Passwörter der Benutzerkonten in der Microsoft Cloud speichern und Inhalte analysiert werden. Microsoft kann diese Daten dann für KI-Auswertungen oder weitere Zwecke nutzen.

Und es war seit 2023 bekannt, dass die Outlook New-App für Windows die Inhalte von Mail- und Kalenderkonten über Microsoft-Server synchronisiert, dort also die Zugangsdaten für die Konten hinterlegt. Der Sachverhalt wurde von mir im Beitrag [Neue Outlook-App überträgt Zugangsdaten an Microsoft](https://borncity.com/blog/2023/11/10/neue-outlook-app-bertrgt-zugangsdaten-an-microsoft/) näher erläutert, wobei ich dort auch darauf hinwies, dass diese Praxis bereits bei den Microsoft Apps für Android und iOS seit Jahren der Fall ist.

Microsoft hatte sich gegenüber heise dann zu diesem letztgenannten Thema erklärt (siehe [Neue Outlook-App: Microsoft äußert sich zu übertragenen Zugangsdaten](https://borncity.com/blog/2023/11/16/neue-outlook-app-microsoft-uert-sich-zu-bertragenen-zugangsdaten/)) und einige Aussagen getroffen. Fazit war: Wer die neue Outlook-App verwendet, für den lassen wir alle Mails und Termine von den konfigurierten Konten über die Microsoft-Server wandern.

## Zeigt auch Outlook Classic (neuerdings) dieses Verhalten?

Bisher war die Hoffnung der Outlook-Protagonisten, dass Outlook Classic die Zugangsdaten lokal speichert und die Inhalte von externen Mail-und Kalenderkonten selbst abholt. Nur Konten bei Microsoft selbst (Microsoft 365, Exchange Online) werden eh auf deren Servern geführt, da ist es nicht so tragisch, wenn die Zugangsdaten auch noch dort liegen.

Kritische Geister zeigten sich von der Möglichkeit, dass Inhalte im Outlook Client durch CoPilot & Co. ausgewertet werden beunruhigt. Aber so schlimm wird es nicht werden, scheint die Hoffnung zu sein. Gestern hat mich ein ungenannt bleiben wollender Leser per E-Mail unter dem Betreff "Interessante Beobachtung zu MS Exchange" auf eine neue Fundstelle im Web hingewiesen.

[![Passwortklau durch Outlook?](https://i.postimg.cc/mDM1WrRV/image.png)](https://www.youtube.com/watch?app=desktop&v=cX6rBoegaMg)

Ein YouTuber, der unter dem Kanal _IT an der Bar_ Inhalte veröffentlicht, hat sich Outlook und die übertragenen Daten näher angesehen. Hintergrund ist, dass der Mann eine IT-Firma betreibt und bei einem seiner E-Mail-Server fehlerhafte Anmeldedaten erhielt, die von Microsoft kamen. Also hat er das Ganze analysiert und aufgedröselt.

Die Erkenntnisse zeigt er in geraffter Form in seinem YouTube-Video. Dazu hat er einen frischen Mail-Server bei Hetzner eingerichtet, dann unter Outlook New für Windows die Zugangsdaten für dieses Konto eingetragen. Gleichzeitig hat er den Datenverkehr unter Outlook aufgebrochen und analysiert, was passiert.

Die Erkenntnis, die sich aus dem Video ergibt: Er zeigt, dass die Zugangsdaten von Outlook New unter Windows diese an Microsoft weiter reicht. Das ist aber nicht neu, ich hatte oben bereits darauf hingewiesen. Die klare Aussage des Youtubers im Video lautet aber: Er hat das Ganze auch unter Outlook Classic und der Outlook-App für Android getestet und die Zugangsdaten für dieses Testkonto dort eingetragen. Die Analyse, so die Aussage, zeigte, dass der Datenverkehr unter Outlook über Microsoft-Server läuft. Die Aussage im Video (ab 7:40) lautet: Outlook New, bestimmte Versionen von Outlook Classic für Windows sowie die Outlook-App für Android übertragen die Zugangsdaten für das Konto an Microsoft. Bei Outlook New für Windows sowie bei der Outlook-App für Android war das längst bekannt. iOS konnte der YouTuber mangels Apple-Gerät nicht testen.

Neu für mich ist die Aussage, wenn ich es richtig verstanden habe, dass auch bestimmte Builds (imho neue Fassungen) von Outlook Classic (mutmaßlich also Outlook 365) die Kontendaten an Microsoft Server übertragen. Schaut euch dazu das [Video auf YouTube](https://www.youtube.com/watch?app=desktop&v=cX6rBoegaMg) an.

## Das Fazit

So ganz überraschend war dieser "Move Microsofts" für mich nicht. Es ist naheliegend, dass der Code, der für Outlook New für Windows verwendet wird, irgendwann auch in aktuelle Versionen von Outlook Classic für Windows (und macOS) einfließt. Die Überschrift des Themas lautet ja langfristig: "Outlook ist der Client für Exchange Online" .

Wer in Firmenumgebungen oder im Privatbereich ausschließlich auf Exchange Online und/oder Outlook.com als Dienst setzt, hat seine Inhalte und Zugangsdaten längst Microsoft übereignet. Kollateralschaden sind dann die Fälle, in denen externe E-Mail- und Kalender-Konten über Microsoft Outlook eingebunden werden.

Unabhängig von der Frage, ob der oben skizzierte Sachverhalt immer stimmt – beim "querschauen des Videos" habe ich nicht vernommen, dass der YouTuber eine konkrete Outlook-Build für Windows angibt, ab der die Zugangsdaten an Microsoft überträgt: Es ist in meinen Augen an der Zeit, endlich auf alternative E-Mail-Clients zu wechseln und das Outlook-Zeugs links liegen zu lassen. Hier mache ich jedenfalls drei Kreuze, 2009, nach einem Test, den Verzicht auf Microsoft Outlook getroffen und auf den Thunderbird als Client gesetzt zu haben.
