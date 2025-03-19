# Introductie

De modelautoriteit gebruikt het toetsingskader bij het toetsen of conform de VDA richtlijnen is gewerkt (proceskwaliteit) en of de modellen die daarbij worden geproduceerd kwalitatief voldoende zijn om opgenomen te kunnen worden in de modelrepository (productkwaliteit).

## Toetsingsdimensies, meetindicatoren en meetvoorschriften

Voor de opzet van de toetsing en voor het toetsingskader zelf is gebruik gemaakt van de [DQV best-practice](https://www.w3.org/TR/vocab-dqv/). Het toetsingskader is opgebouwd uit toetsdimensies. Dit zijn de "hoofdonderwerpen" van het toetsingskader. Elke toetsdimensie is vervolgens uitgewerkt in één of meerdere meetindicatoren.

Een meetindicator is een zelfstandig meetbare indicator over een bepaald kwaliteitsaspect van de uitgevoerde werkwijze dan wel het resulterende model. Een meetindicator hoort bij precies één toetsdimensie. Op basis van de meetindicatoren van één toetsdimensie kan worden vastgesteld wat het oordeel is over deze ene toetsdimensie.

Bij elke meetindicator hoort precies één meetvoorschrift, waarin is uitgewerkt hoe de modelautoriteit concreet de meetindicator toetst.

## Modellen, modelversies en modelelementen

Het toetsingskader toetst een afzonderlijke modelversie. Een modelversie betreft een specifieke versie van een model van een bepaald modeltype. Bijvoorbeeld de modelversie van het semantisch begrippenmodel van de Vliegbelasting met versienummer 1.0.0 snapshot 5. Zo kunnen er meerdere versies zijn van één model. Er wordt altijd een snapshot-versie getoetst. Na toetsing kan deze gepubliceerd worden onder het versienummer zonder het snapshotnummer. Dit noemen we dan het releasenummer. In dit voorbeeld is dit dan releasenummer 1.0.0. Het toetsingkader passen we op dit moment toe op de volgende modeltypen:

- Kennismodellen:
  - Semantisch begrippenmodel (SBM);
  - Conceptueel informatiemodel (CIM);
- Gebruiksmodellen:
  - Logische gegevensgebruiksmodellen (LGG of LGx):
    - Logisch gegevensadministratiemodel (LGA);
    - Logisch gegevensinteractiemodel (LGI);
    - Logisch gegevensgebruiksmodel van een proces (LGP)
- Implementatiemodellen

Elke toetsingsdimensie is in beginsel van toepassing op elk type model. Een uitzondering hierop is de implementatie: hiervan wordt alleen getoetst in hoeverre het implementatiemodel correct is verbonden met de overige modellen. Zo kun je voor elke modelversie de kwaliteit benoemen. Modellen mogen gelijktijdig aangeboden worden, maar zullen na elkaar worden getoetst, in de volgorde die hierboven staat vermeld.

## Oordeel per toetsdimensie

Het oordeel per toetsingsdimensie is een eenvoudige schaal van 3 punten. Dit maakt het eenvoudig om de essentie van de toets te communiceren. Eventuele details kunnen per meetindicator bekeken worden:

- **Onvoldoende**: de kwaliteit van het model of de voortbrenging daarvan is voor deze toetsdimensie onvoldoende. Het model kan niet opgenomen worden in de modelrepository zonder dat aanvullende maatregelen zijn genomen en ook zijn aanvullende maatregelen nodig om de dataschuld voldoende te reduceren.
- **Voldoende**: de kwaliteit van het model of de voortbrenging daarvan is voor deze toetsdimensie voldoende. Het model kan (voor zover deze toetsdimensie) worden opgenomen in de modelrepository. Aanvullende maatregelen zijn nodig om de dataschuld voldoende te reduceren.
- **Goed**: de kwaliteit van het model of de voortbrenging daarvan is voor deze toetsdimensie goed. Het model kan (voor zover deze toetsdimensie) worden opgenomen in de modelrepository. Er zijn geen aanvullende maatregelen nodig.

Op basis van de beoordeling per toetsdimensie volgt een kwaliteitslabel voor het betreffende model. We onderkennen op dit moment de kwaliteitslabels A, B, C en D.
Indien een toetsdimensie niet als goed is beoordeeld, dan zal de Modelautoriteit met aanbevelingen komen welke aanvullende maatregelen genomen moeten worden.

> Voorbeelden van dergelijke aanbevelingen zijn:
>
> - De betrouwbaarheid van het model is onvoldoende: we hebben niet kunnen vaststellen of, en zo ja: door wie het model is geverifieerd. Laat het model geverifiëren door de domeineigenaar en neem expliciet op wie het model op welk moment heeft geverifieerd;
> - De nauwkeurigheid van het model is onvoldoende: je hebt niet gebruik gemaakt van de juiste stereotypes bij de entiteittypen. Controleer de stereotypes in model, zie ook voorschrift X uit het handboek;
> - De compliance van het model is onvoldoende: je hebt de voorschriften uit het handboek met betrekking tot tijdslijnen niet goed toegepast. Dien een verzoek in bij de consultancydienst om jou te helpen deze voorschriften correct toe te passen.

Degenen aan wie het toetsingsrapport is gesteld, geven terugkoppeling wat ze van plan zijn te doen met de aanbevelingen van de Modelautoriteit.

## Kwaliteitslabel

*Het kwaliteitslabel geeft een totaaloordeel over het model.*

Het kwaliteitslabel geeft een indruk wat het risico is als het model, of onderdelen daaruit, wordt gebruikt door een ander dan de opsteller van het model: hoe lager het kwaliteitslabel, hoe groter het risico. Daarnaast geeft het kwaliteitslabel aan wat het advies van de Modelautoriteit was t.a.v. vrijgave van het model ter publicatie.

De Modelautoriteit zal elk model dat getoetst is en vrijgegeven is door de kennisverantwoordelijke publiceren, conform het publicatieproces.
Echter, indien de Modelautoriteit geadviseerd heeft om dit niet te doen, dan is dit zichtbaar uit het gegeven kwaliteitslabel. Onderstaande tabel geeft dit weer.

|Kwaliteitslabel|Modelkwalificatie|Risico voor hergebruik|Vrijgaveadvies|
|---------------|-----------------|----------------------|--------------|
|**A**|Een *voorbeeldig* model|Het model is uitstekend te gebruiken door anderen|Positief|
|**B**|Een *goed* model voor hergebruik|Het model is te gebruiken door anderen, maar hier kleven wel risico's aan. Aanbevolen wordt om het toetsingsrapport te lezen en zo nodig mitigerende maatregelen te nemen.|Positief|
|**B***||De modelautoriteit heeft niet kunnen vaststellen of het model te gebruiken is door anderen, maar ook niet vast kunnen stellen dat het niet geschikt is voor hergebruik. Deze speciale situatie kan optreden op het moment dat vanuit het gebruik een kennismodel is gemodelleerd (vanuit een gegevensstroom- of gegevensbrongedreven aanpak). Aanbevolen wordt om het toetsingsrapport te lezen en zo nodig mitigerende maatregelen te nemen. Ook wordt aanbevolen om zelf te beoordelen of het kennismodel wel te gebruiken is. Mocht het kennismodel in deze andere gebruikscontext niet bruikbaar zijn, dan zal het kwaliteitslabel van B* naar C verschuiven.|Positief|
|**C**|Een model voor *eigen* gebruik|Het model is niet geschikt voor hergebruik. Het model is goed te gebruiken door de oorspronkelijke opsteller (verticaal hergebruik binnen hetzelfde kennisgebied), maar hergebruik door anderen wordt afgeraden (horizontaal hergebruik tussen verschillende kennisgebieden).|Positief|
|**D**|Een *proef*model|Het model is niet geschikt voor hergebruik. Aanpassingen aan het model zijn nodig voordat anderen verder modelleren op basis van dit model (zowel horizontaal als verticaal).|Negatief|

Het kwaliteitslabel wordt bepaald op basis van de beoordeling per toetsdimensie:

- Om kwaliteitslabel A te verkrijgen mogen maximaal 2 toetsdimensies de beoordeling "Voldoende" hebben en dienen de overige toetsdimensies de beoordeling "Goed" te hebben. Daarbij geldt bovendien dat de toetsdimensies "Begrijpelijkheid" en "Herleidbaarheid" in ieder geval de beoordeling "Goed" moeten hebben.

## Rapportage

Bij een concrete toetsing, zal voor elke meetindicator een meetwaarde worden bepaald. Daarbij wordt vastgelegd welke versie van het model is getoetst en welke personen zijn geïnterviewd voor het toetsen van de proceskwaliteit. Daarbij wordt er vanuit gegaan dat de voortbrenging wordt getoetst van de betreffende versie van het model. Vervolgens bevat de rapportage de samenvatting per toetsdimensie en tenslotte een kwaliteitslabel voor het gehele model alsmede een overzicht van de aanbevelingen.

## Overzicht toetsdimensies

Voor de toetsingsdimensies sluiten we aan bij de [ISO/IEC 25012 standaard](https://iso25000.com/index.php/en/iso-25000-standards/iso-25012), het Data Quality Model. We passen deze standaard toe op het model dat we toetsen:

- De **[actualiteit](#actualiteit)** is belangrijk om zeker te zijn dat de Belastingdienst op basis van de actuele regels data verwerkt. Als de actualiteit niet op orde is, dan bestaat het risico dat de Belastingdienst gebruik maakt van verouderde definities en regels en daarmee niet wendbaar kan inspringen op (inmiddels) gewijzigde wet- en regelgeving.
- De **[begrijpelijkheid](#begrijpelijkheid)** is belangrijk om zeker te zijn dat medewerkers van de Belastingdienst de juiste data verwerken en daarbij ook de kennis op de juiste wijze toepassen. Als de begrijpelijkheid niet op orde is, dan bestaat het risico dat de Belastingdienst de data die zij verwerkt op de verkeerde wijze interpreteert.
- De **[betrouwbaarheid](#betrouwbaarheid)** is belangrijk om zeker te zijn dat de kennis zoals vastgelegd in het model ook daadwerkelijk overeen komt met hetgeen in de wet- en regelgeving is beoogd en als zodanig door de beleidsmakers van de Belastingdienst is uitgewerkt.
Als de betrouwbaarheid niet op orde is, dan bestaat het risico dat medewerkers van de Belastingdienst zich niet bewust zijn van het feit dat zij data op een mogelijk verkeerde manier verwerken, wanneer zij netjes de kennis uit het model volgen, terwijl die kennis zelf incorrect is.
- De **[compleetheid](#compleetheid)** is belangrijk om zeker te zijn dat alle kennis is vastgelegd die noodzakelijk is voor het specifieke doel waarvoor het model is beoogd. Als de compleetheid niet op orde is, dan bestaat het risico dat kennis ontbreekt die wel noodzakelijk is voor het correct verwerken van gegevens voor dit specifieke doel.
- De **[naleving](#naleving) is belangrijk om zeker te zijn dat het model tot stand is gekomen volgens de afspraken die binnen de Belastingdienst zijn gemaakt.
Als de naleving niet op orde is, dan bestaat het risico dat niet goed getoetst kan worden of het model wel van voldoende kwaliteit is en daarmee het risico dat verwerken van gegevens op basis van dit model niet correct zal plaatsvinden.
- De **[consistentie](#consistentie)** is belangrijk om zeker te zijn dat het model in de praktijk ook bruikbaar is, zonder dat er inconsistenties gaan ontstaan bij het verwerken van gegevens volgens dit model. Als de consistentie niet op orde is, dan bestaat het risico dat de Belastingdienst gegevens gaat verwerken die leiden tot inconsistente beslissingen.
Als deze inconsistenties kennisdomeinoverstijgend zijn, bestaat het risico dat een dergelijke inconsistentie zich verspreid over meerdere kennisdomeinen heen, met als gevolg dat ook andere kennisdomeinen te maken krijgen met inconsistente gegevensverwerking.
- De **[herleidbaarheid](#herleidbaarheid)** is belangrijk om zeker te zijn dat het model de kennis bevat die toetsbaar terug te herleiden is naar de wet-, regelgeving en uitvoeringsbeleid en om te kunnen toetsen wie welke wijzigingen op het model heeft gemaakt en om welke reden.
Als de herleidbaarheid niet op orde is, dan bestaat het risico dat niet goed getoetst kan worden of het model wel de kennis uit de wet-, regelgeving en beleid bevat. Ook kan niet goed getoetst worden of wijzigingen wel conform de gemaakte afspraken door de daartoe bevoegde functionarissen zijn gemaakt.
- De **[nauwkeurigheid](#nauwkeurigheid)** is belangrijk om zeker te zijn dat de kennis uit het kennisdomein op de juiste wijze is geëxpliciteerd in de modelconstructies en patronen die zijn voorgeschreven.
Als de nauwkeurigheid niet op orde is, dan bestaat het risico dat de Belastingdienst slordig omgaat met de verwerking van gegevens en daarmee onvoldoende kan aantonen dat deze verwerking volgens de wet- en regelgeving verloopt.
- De **[precisie](#precisie)** is belangrijk om zeker te zijn dat de kennis uit het kennisdomein voldoende gedetailleerd is uitgewerkt. Als de precisie niet op orde is, dan bestaat het risico dat kennis ontbreekt die wel noodzakelijk is voor het correct verwerken van gegevens.
- De **[toegankelijkheid](#toegankelijkheid)** is belangrijk om zeker te zijn dat de kennis uit het kennisdomein ook toegankelijk is voor anderen dan de oorspronkelijke modelleurs. Als de toegankelijkheid niet op orde is, dan bestaat het risico dat eenmalig vastgelegde gegevens niet op een correcte wijze hergebruikt kunnen worden.
- De **[vertrouwelijkheid](#vertrouwelijkheid)** is belangrijk om zeker te zijn dat bij de vertrouwelijkheid van gegevens al bij het expliciteren van de kennis is meegenomen. Als de vertrouwelijkheid niet op orde is, dan bestaat het risico dat hiermee niet voldaan is aan de wettelijke vereiste van privacy by design.