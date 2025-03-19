# Toetsingskader

## Actualiteit

([ISO25012: Currentness](https://iso25000.com/index.php/en/iso-25000-standards/iso-25012?start=6))

De mate waarin het model de elementen bevat overeenkomstig de tijdsperiode waarvoor het model is beoogd, dwz: of het model actueel is voor het beoogde gebruik.

### ACTU-01 Is duidelijk van welke periode het model de kennis expliciteert? {#ACTU-01}

In hoeverre is duidelijk van welke periode het model de kennis expliciteert? In geval de meetwaarde 'duidelijk' of 'onduidelijk' is, wordt aangegeven (voor zover mogelijk) welke periode dit betreft, bijvoorbeeld: "Belastingjaar 2018".

Mogelijke waarden:
- Duidelijk
- Onduidelijk
- Onbekend

**Meetvoorschrift**

Controleer of in het model eenduidig is beschreven voor welke periode het model de kennis expliciteert. Mocht dit niet eenduidig beschreven zijn, dan is sprake van onduidelijke actualiteit. Dit geldt ook als een eenduidige periodebeschrijving onvolledig is of afhankelijk is van de context (bijvoorbeeld: "vanaf 2018" of "vanaf 2018 tot heden").
Voor de logische gegevensgebruiksmodellen (LGA en LGI) geldt dat deze slechts de afbakening beschrijven van de gebruikte kennis uit het logisch gegevensdefinitiemodel. Voor het LGA en LGI geldt dat voldaan is aan ACTU-01 als eenduidig beschreven is voor welke periode de interactie en administratie van toepassing is.

### ACTU-02 Actueel model voor genoemde periode {#ACTU-02}

In hoeverre is het model een actuele explicitatie van de kennis voor de in het model genoemde periode. In geval van een niet-actuele explicitatie wordt ook kort omschreven voor welke delen van het model dit in ieder geval geldt.

Mogelijke waarden:
- Actueel
- Actualiteit onduidelijk
- Niet actueel

**Meetvoorschrift**

De manier waarop deze meetindicator gemeten kan worden, zal afhangen van het model dat wordt getoetst en hoe de traceerbaarheid in dat model op orde is naar bovenliggende modellen:

|Model|Meetvoorschrift|
|-----|---------------|
|SBM|is de genoemde periode van het model in lijn met de geldigheid van de wet- en regelgeving die is geannoteerd?|
|CIM|is de genoemde periode van het model in lijn met het semantisch model waar dit CIM aan is gerelateerd? Mocht deze relatie onvoldoende duidelijk zijn, dan kan gekeken worden of vanuit het CIM duidelijk is welke wet- en regelgeving is geexpliciteerd. Mocht dit niet duidelijk zijn, dan is de meetwaarde "Actualiteit onduidelijk".|
|LGA, LGI, LGP|deze zijn een "view" op het CIM. De actualiteit van deze modellen is afhankelijk van de actualiteit van het CIM en daarnaast dient ook getoetst te worden of deze view actueel is ten aanzien van het gebruik in respectievelijk de interactie dan wel de administratie. Dit kan getoetst worden in het interview met de kenniscontroleur van het betreffende model.|
### ACTU-03 Waarborgen om actualiteit te borgen bij wijzigingen {#ACTU-03}

In hoeverre is gewaarborgd dat bij wijzigingen van de kennis, het model actueel blijft?

Mogelijke waarden:
- Geborgd in het model
- Geborgd in afspraken
- Stabiele kennis
- Niet geborgd

**Meetvoorschrift**

Gedurende de periode waarvoor het model is bedoeld, kan de kennis wijzigen, bijvoorbeeld door wetswijzigingen. Hiervoor dienen waarborgen aanwezig te zijn. Dit kan op drie verschillende manieren:
1. Het kan geborgd zijn in het model. In zo'n geval kent het model constructies die wijzigingen van de kennis kunnen opvangen in de populatie. Getoetst dient te worden of dergelijke constructies voldoen aan de patronen zoals beschreven in de MTHV's.
2. Het kan geborgd zijn in afspraken, bijvoorbeeld dat bij een wetswijziging een nieuwe versie van het model wordt opgesteld. In een dergelijk geval wordt een beschrijving van deze afspraken verwacht bij het model.
3. Er kan sprake zijn van stabiele kennis, waarvan het niet waarschijnlijk is dat deze wijzigt.

Indien niet vastgesteld kan worden dat één van bovenstaande waarborgen aanwezig is, is sprake van de meetwaarde "niet geborgd".

## Begrijpelijkheid

([ISO25012: Understandability](https://iso25000.com/index.php/en/iso-25000-standards/iso-25012?start=14))

De mate waarin het model correct geïnterpreteerd kan worden, en uitgedrukt is in de passende taal, symbolen en diagrammen. De begrijpelijkheid omvat ook de metadata bij het model.

### BEGR-01 In hoeverre is het model opgesteld in de Nederlandse taal? {#BEGR-01}

In hoeverre is het model opgesteld in de Nederlandse taal?

Mogelijke waarden:
- Meertalig opgesteld, waaronder in de Nederlandse taal
- Correct opgesteld in de Nederlandse taal
- Incorrect opgesteld in de Nederlandse taal
- Slechts gedeeltelijk opgesteld in de Nederlandse taal
- Niet opgesteld in de Nederlandse taal

**Meetvoorschrift**


De meetwaarden zijn zelf afgeleid op basis van meerdere eigenschappen die betrekking hebben op het model:
- Is er wel/niet sprake van de Nederlandse taal in het model?
- Is wel/niet sprake van technische taalconstructies (bijvoorbeeld CamelCase, underscores, niet gebruiken van diacrieten, grammaticaal onjuiste formuleringen)?
- Hebben modelelementen termen die passen bij de Nederlandse taal?
- Is er sprake van een oorspronkelijke niet-Nederlandse taal, en is deze correct vertaald?

Controleer zowel de terminologie die gebruikt is voor de modelelementen als de beschrijvingen van de modelelementen. Er dient sprake te zijn van gebruik van "Normaal Nederlands". Waar sprake is van vakjargon kan daarbij vaktermen gebruikt worden. Merk op dat hierbij niet wordt getoetst of dergelijke termen ook in het domein voorkomen (dat valt niet onder "begrijpelijkheid"), maar wel of een dergelijke term in het Nederlands voor zou kunnen komen.

Indien het model meertalig is opgesteld, dan wordt dit bij de meting vermeld. Het model dient in ieder geval in het Nederlands opgesteld te zijn.

In een enkel geval kan sprake zijn van een model waarvan de oorsprong niet in de Nederlandse taal is gesteld. Zoals bijvoorbeeld een internationale standaard. In dat geval kan sprake zijn van een situatie waarbij de terminologie in de oorspronkelijke taal is. Op zijn minst zal dan echter de uitleg (ook) in het Nederlands gesteld moeten zijn.

### BEGR-02 In hoeverre is gebruik gemaakt van de juiste symbolen en diagrammen? {#BEGR-02}

### BEGR-03 In hoeverre is objectief te begrijpen hoe de kennis is geëxpliciteerd? {#BEGR-03}

### BEGR-04 In hoeverre voldoet de verwoording (terminologie) aan de MTHV's? {#BEGR-04}

### BEGR-05 In hoeverre zijn de modelleringsbeslissingen te begrijpen, in relatie tot de MTHV's? {#BEGR-05}

### BEGR-06 In hoeverre is het model te begrijpen voor de kenniscontroleurs? {#BEGR-06}

## Betrouwbaarheid

De mate waarin het model de correcte weergave is zoals beoogd in de kennisbronnen en ook zo als correct door de domeinexperts wordt gezien.

### BETR-01 Validatie door de juiste kenniscontroleurs {#BETR-01}

### BETR-02 Afbakening kennis overeenkomstig doel {#BETR-02}

### BETR-03 Model conform gestelde business requirements {#BETR-03}

### BETR-04 Voldaan aan kaders van de gegevensarchitectuur {#BETR-04}

### BETR-05 Geschikt voor beoogde use cases {#BETR-05}

### BETR-06 Model is een juiste weergave van de kennis uit de kennisbronnen {#BETR-06}

## Compleetheid

De mate waarin het model alle elementen bevat die noodzakelijk zijn voor het te beschrijven kennisgebied.

### COMP-01 Afbakening kennisgebied(en) duidelijk? {#COMP-01}

### COMP-02 Afbakening kennis(deel)gebied overeenkomstig doel {#COMP-02}

### COMP-03 Verplichte elementen compleet ingevuld {#COMP-03}

## Consistentie

De mate waarin de elementen uit het model vrij zijn van tegenstellingen en in overeenstemming zijn met andere modelelementen binnen en buiten het getoetste model.

### CONS-01 Kennis(deel)gebied consistent afgebakend {#CONS-01}

### CONS-02 Intern consistent? {#CONS-02}

### CONS-03 Verticale consistentie {#CONS-03}

### CONS-04 Horizontale consistentie {#CONS-04}

### CONS-05 Metadata consistent {#CONS-05}

## Herleidbaarheid

De mate waarin de beschrijving van een modelelement herleidbaar is naar de grondslag in wet-, regelgeving en beleid, alsmede de herleidbaarheid van de wijzingen in het model. Dit omvat onder meer een audit trail naar de reden van wijziging en degene die betrokken is bij de wijziging (zoals: verantwoordelijke, uitvoerder, goedkeurder, toetser).

### HERL-01 Gemodelleerde kennisgebieden herleidbaar naar vastgestelde kennisgebieden {#HERL-01}

### HERL-02 Herleidbaar naar juiste kennisbron {#HERL-02}

### HERL-03 Herleidbaarheid naar de juiste begrippen? {#HERL-03}

### HERL-04 Herleidbaarheid naar het bovenliggende model? {#HERL-04}

### HERL-05 Herleidbaarheid wie wijziging heeft doorgevoerd {#HERL-05}

### HERL-06 Herleidbaarheid reden wijziging {#HERL-06}

## Naleving

De mate waarin het model en de voortbrenging conform het beleid van de Belastingdienst tot stand is gekomen, waaronder het toepassen van de juiste MTHV's.

### NALE-01 Volgen top-down aanpak van de VDA {#NALE-01}

### NALE-02 Bottom-up aanpak naleving {#NALE-02}

### NALE-03 SM methoden en technieken gevolgd {#NALE-03}

### NALE-04 SM hulpmiddelen en voorschriften gevolgd {#NALE-04}

### NALE-05 In hoeverre zijn de methoden en technieken correct gevolgd bij het opstellen van het formeel-linguistisch model? {#NALE-05}

### NALE-06 In hoeverre zijn de hulpmiddelen en voorschriften correct gebruikt bij het opstellen van het formeel-linguistisch model? {#NALE-06}

### NALE-07 LGD methoden en technieken gevolgd {#NALE-07}

### NALE-08 LGD hulpmiddelen en voorschriften gevolgd {#NALE-08}

### NALE-09 LGG, LGI, LGA methoden en technieken correct gevolgd {#NALE-09}

### NALE-10 LGG, LGA, LGI hulpmiddelen en voorschriften correct gevolgd {#NALE-10}

### NALE-11 Referentiearchitectuur gevolgd {#NALE-11}

## Nauwkeurigheid

De mate waarin de elementen uit het model op de correcte wijze zijn gebruikt. Syntactische nauwkeurigheid betreft de mate waarin het model conform het metamodel is uitgedrukt en semantische nauwkeurigheid betreft de mate waarin de modelelementen ook correct zijn gebruikt, zoals beoogd in de VDA.

### NASE-01 Afbakening kennisgebieden {#NASE-01}

### NASE-02 Omschrijvingen nauwkeurig {#NASE-02}

### NASE-03 Betekenis nauwkeurig gemodelleerd {#NASE-03}

### NASE-04 annotaties nauwkeurig aangebracht? {#NASE-04}

### NASE-05 Feittypen nauwkeurig gemodelleerd {#NASE-05}

### NASE-06 Contexten nauwkeurig toegepast {#NASE-06}

### NASY-01 SM syntactisch nauwkeurig {#NASY-01}

### NASY-02 Feitmodel syntactisch nauwkeurig {#NASY-02}

### NASY-03 LGD syntactisch nauwkeurig {#NASY-03}

### NASY-04 LGG syntactisch nauwkeurig {#NASY-04}

### NASY-05 LGA syntactisch nauwkeurig {#NASY-05}

### NASY-06 LGI syntactisch nauwkeurig {#NASY-06}

## Precisie

De mate waarin het model voldoende is uitgewerkt in modelelementen zodat de juiste diepgang is bereikt. Met andere woorden: het model is niet abstract, maar precies concreet genoeg.

### PREC-01 Uitwerking annotatie en/of verwijzingen precies genoeg? {#PREC-01}

### PREC-02 Uitwerking begrippen precies genoeg? {#PREC-02}

## Toegankelijkheid

De mate waarin het model en de modelelementen daarbinnen toegankelijk zijn voor zowel mensen als voor machines.

### TOEG-01 Juiste identificeerbare namen? {#TOEG-01}

### TOEG-02 Juiste URI identificatie {#TOEG-02}

### TOEG-03 URI benaderbaar {#TOEG-03}

### TOEG-04 Beschikbaar voor mensen {#TOEG-04}

### TOEG-05 Beschikbaar voor machines {#TOEG-05}

### TOEG-06 Verwijzingen correct {#TOEG-06}

### TOEG-07 Versies duurzaam benaderbaar {#TOEG-07}

### TOEG-08 Versiebeheer correct ingericht {#TOEG-08}

### TOEG-09 Doorzoekbaar model {#TOEG-09}

## Vertrouwelijkheid

De mate waarin het model de vertrouwelijkheid is gewaarborgd van gegevens die met dit model worden vastgelegd of uitgewisseld.

### VERT-01 Privacy wet- en regelgeving meegenomen {#VERT-01}

### VERT-02 Begrippen doelbinding {#VERT-02}

### VERT-03 LGD doelbinding {#VERT-03}

### VERT-04 LGA doelbinding {#VERT-04}

### VERT-05 LGI ontvangen doelbinding {#VERT-05}

### VERT-06 LGI verstrekken doelbinding {#VERT-06}

### VERT-07 Gemodelleerde gegevens in verwerkingsregister {#VERT-07}

### VERT-08 Autorisatie gemodelleerd {#VERT-08}

