from datetime import datetime
import frontend.ep.config as config
from utils.utils import *


"""https://jira.belastingdienst.nl/browse/GVG-6055
Validatie functie CIM/LGG/LGA/LGI modellen (powerdesigner ldm)
Het model wordt niet getransformeerd en niet opgeslagen in de (PostgreSQL) database 
zolang er fouten zitten in de validatie.
Validatie betreft alleen hetgeen nodig is om het model te kunnen transformeren. 
Als de transformatie kan slagen, dan moet de validatie ook slagen.
et is geen inhoudelijke validatie van het model. 
Het is alleen een validatie op formaliteiten. 
Dus als een model technisch gezien voldoet, dan moet het ingeladen kunnen worden. 
In beginsel geldt dat als het een powerdesigner LDM bestand is in XML formaat 
(dus niet het binaire formaat), dan is het bestand in te laden, mits de koppeling 
naar het kennisgebied kan worden gemaakt en de juiste XEMs zijn gebruikt.

"""


class LDMValidator:
    def __init__(self, input_json, input_file_dir, input_xml_file):
        self.kdgb_uri = None
        self.proces = None
        self.proces_uri = None
        self.interactie = None
        self.interactie_uri = None
        self.administratie_uri = None
        self.administratie = None
        self.json = input_json
        self.naam_kb = None
        self.naam_kdgb = None
        self.code_kb = None
        self.kb_uri = None
        self.melding_manager = MeldingManager()

    def validate_argument_0(self, input_json, input_file_dir, input_xml_file):
        """first parnass Function that reads the model name  and prints the necessary information input_json """

        print(
            "VALIDATIE MDE_OUTPUT_DIR= " + input_file_dir)  # var/folders/bf/rf8kmqkd2s3d1jkzr03_9ggw0000gr/T/tmprdtdrww6/
        print("VALIDATIE INPUT_FILE= " + input_xml_file)

        if self.json["model"]["entities"] is not None:
            print("VALIDATIE AANTAL_ENTITEITEN=" + str(len(self.json["model"]["entities"])))

        if self.json["model"]["relationships"] is not None:
            print("VALIDATIE AANTAL_RELATIES=" + str(len(self.json["model"]["relationships"])))
        if self.json["model"]["relationships"] is None:
            print("VALIDATIE AANTAL_RELATIES= 0")

        if self.json["model"]["domains"] is not None:
            print("VALIDATIE AANTAL_DOMAIN_AND_SHORTCUTS=" + str(len(self.json["model"]["domains"])))

        if len(self.json["model"]["entities"]) < 1:
            print("VALIDATIE AANTAL_ENTITEITEN=" + str(len(self.json["model"]["entities"])))
            raise ValueError(
                f" er zijn minder dan 1 entiteiten"
            )

        # print(input_json)
        # print json to screen with human-friendly formatting
        # pprint.pprint(input_json, compact=True)
        # https://medium.com/@murungaephantus/validating-xml-with-python-a-step-by-step-guide-53d4a4b9716b
        # input_file_dir= /tmp/tmpr0ejlmdp /
        # input_xml_file=LGD_EXM_Ander_kennisgebied_Kern.ldm

    def validate_model_name(self, input_json, input_file_dir, input_xml_file, model_type):
        """first parnass Function that reads the model name  and prints the necessary information input_json """

        model_name = input_json["model"]["name"]

        print("https://confluence.belastingdienst.nl/display/GVG/Powerdesigner+%28LDM%29+export")
        print("hoi " + str(model_name) + "  , nice to see you again!")

        """ #00 URI < urn: uuid:{o: Model / a: ObjectID} > """
        self.mde_model_uuid = self.json["model"]["uuid"]
        self.mde_model_version = self.json["model"]["version"]
        self.mde_model_file_name = self.mde_model_uuid + self.mde_model_version
        hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(self.mde_model_file_name))
        self.model_uri = URIRef(f"urn:uuid:{hash_uuid}")
        self.mde_repositoryfilename = self.json["model"]["repositoryfilename"]
        self.mde_modificationdate = self.json["model"]["modificationdate"]
        dt_object = datetime.fromtimestamp(int(self.mde_modificationdate))
        self.mde_versie_datum_model = (str(dt_object.year) + "-" + str(dt_object.month) + "-" + str(dt_object.day))

        """#01 Model	type	altijd lgd:LogischGegevensdefinitieModel 
       Let op: de {o:Model/a:Name} moet beginnen met "CIM", anders foutmelding.
       Je kunt bij Modelverzoeken alleen CIM aangeven, LGD is niet meer mogelijk. 
       Mocht iemand toch een model uploaden waarbij in het “name” veld van Powerdesigner toch nog “LGD” staat, 
       dan moet dit afgekeurd worden. 
       """
        model_name_splitted = model_name.split(' ')
        print("model_name_splitted: " + str(model_name_splitted))

        if model_type not in ["CIM", "LGA", "LGI", "LGP"]:
            raise ValueError(f"⁉️ modeltype '{model_type}' bestaat niet")

        if model_type != model_name_splitted[0]:
            raise ValueError(f"naam van het model begint met '{model_name_splitted[0]}'-, dit komt niet overeen met gekozen modeltype: {model_type}")

        match model_type:
            case "CIM":
                try:
                    # STAP 1: valideer naam_kb in geval van vda_model_name = {naam_kb}
                    potentieel_naam_kennisgebied = " ".join(model_name_splitted[1:])
                    self.kb_uri = lookup_kb_uri_from_naam(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_naam_kgb=potentieel_naam_kennisgebied)
                    self.naam_kb = lookup_kb_naam_from_uri(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_kb_uri=self.kb_uri)
                except ValueError:
                    try:
                        # STAP 2.1: valideer code_kb in geval van vda_model_name = {code_kb naam_kdgb}
                        potentieel_code_kennisgebied = model_name_splitted[1]
                        potentieel_naam_kennisdeelgebied = " ".join(model_name_splitted[2:])
                        self.kb_uri = lookup_kb_uri_from_code(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_code_kb=potentieel_code_kennisgebied)
                        self.code_kb = potentieel_code_kennisgebied

                        # STAP 2.2: valideer naam_kdgb in geval van vda_model_name = {code_kb naam_kdgb}
                        self.kdgb_uri = lookup_kdgb_uri_from_naam_kdgb(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_naam_kdgb=potentieel_naam_kennisdeelgebied, lookup_code_kb=self.code_kb, lookup_uri_kb=self.kb_uri)
                        self.naam_kdgb = lookup_kb_naam_from_uri(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_kb_uri=self.kdgb_uri)
                    except ValueError as v:
                        raise ValueError(v)
            case "LGA":
                try:
                    potentieel_naam_administratie = " ".join(model_name_splitted[1:])
                    self.administratie_uri = lookup_administratie_uri_from_naam(lookup_endpoint=config.DATASTORE_ENDPOINT,
                                                                                lookup_naam_administratie=potentieel_naam_administratie)
                    self.administratie = lookup_bes_naam_from_uri(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_bes_uri=self.administratie_uri)
                except ValueError as v:
                    self.melding_manager.meld(MeldingSoort.WARNING, str(v))
                    # raise ValueError(v)

            case "LGI":
                try:
                    potentieel_naam_interactie = " ".join(model_name_splitted[1:])
                    self.interactie_uri = lookup_interactie_uri_from_naam(lookup_endpoint=config.DATASTORE_ENDPOINT,
                                                                          lookup_naam_interactie=potentieel_naam_interactie)
                    self.interactie = lookup_bes_naam_from_uri(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_bes_uri=self.interactie_uri)

                except ValueError as v:
                    self.melding_manager.meld(MeldingSoort.WARNING, str(v))
                    # raise ValueError(v)

            case "LGP":
                try:
                    potentieel_naam_proces = " ".join(model_name_splitted[1:])
                    self.proces_uri = lookup_proces_uri_from_naam(lookup_endpoint=config.DATASTORE_ENDPOINT,
                                                                  lookup_naam_proces=potentieel_naam_proces)
                    self.proces = lookup_bes_naam_from_uri(lookup_endpoint=config.DATASTORE_ENDPOINT, lookup_bes_uri=self.proces_uri)

                except ValueError as v:
                    self.melding_manager.meld(MeldingSoort.WARNING, str(v))
                    # raise ValueError(v)


        # HIERONDER OUDE CODE DIE DIE DOET WAT LINES 100-120 NU DOEN
        # """#02 Model	kennisgebied	{o:Model/a:Name} bevat na "CIM"
        # ófwel de -code- van het kennisgebied gevolgd door de naam van het kennisdeelgebied.
        # Óf de -volledige naam- van het kennisgebied
        # De URI hiervan is de waarde van deze VDA-eigenschap.
        # Mocht deze code niet voorkomen in het kennisgebiedenregister, dan foutmelding.
        # """
        # naam_kennisgebied = model_name_splitted[1:]
        # # model_name = "VDA Context en attribuutdomeinen"
        # # Split a string only by first space in python [duplicate]
        # naam_kennisgebied_split = naam_kennisgebied.split(None, 1)
        # # print(naam_kennisgebied_split)
        # # print(naam_kennisgebied_split[0])
        # # print(naam_kennisgebied_split[1])
        # # naam_kennisgebied ="Akten"
        # naam_kennisgebied = naam_kennisgebied_split[0]  # VDA
        # naam_kennisgebied_quoted = (f'"{naam_kennisgebied}"')
        # query = Literal(
        #     "SELECT ?subject WHERE {GRAPH <urn:name:kennisgebiedenregister> {  ?subject ?predicate " + naam_kennisgebied_quoted + "}}")
        # # print (f"{query}") # gaat niet lekker maar sparql lijkt gevuld.
        #
        # response = requests.post(
        #     config.DATASTORE_LOOKUP_ENDPOINT, data={"query": query}, verify=False
        # )
        # if response.status_code == 200:
        #     response_json = str(response.json())
        #     # substring = "kennisgebied/"+naam_kennisgebied
        #     substring = naam_kennisgebied
        #     if response_json.find(substring) != -1:
        #         print(f"🐢kennisgebied='{substring}' jeuh, want komt voor in het kennisgebiedenregister.")
        #     else:
        #         raise ValueError(
        #             f"Error ⛔❌ kennisgebied='{substring}' komt helaas niet voor in het kennisgebiedenregister"
        #         )
        #         sys.exit(1)
        #
        # else:
        #     return jsonify("Query niet correct.")
        #
        # """#02 Model	kennisdeelgebied	{o:Model/a:Name} bevat na "CIM"
        #         de code van het kennisdeelgebied. De URI hiervan is de waarde van deze VDA-eigenschap.
        #         Mocht deze code niet voorkomen in het kennisdeelgebiedenregister, dan foutmelding.
        #         """
        #
        # # naam_kennisdeelgebied ="Context en attribuutdomeinen"
        # naam_kennisgebied = model_name[4:]
        # # model_name = "VDA Context en attribuutdomeinen"
        # # Split a string only by first space in python [duplicate]
        # naam_kennisgebied_split = naam_kennisgebied.split(None, 1)
        # # print(naam_kennisgebied_split)
        # # print(naam_kennisgebied_split[0]) #VDA
        # # print(naam_kennisgebied_split[1]) #Context en attribuutdomeinen
        # naam_kennisgebied_split.append("kennisdeelgebied is leeg")
        # naam_kennisdeelgebied = naam_kennisgebied_split[1]
        #
        # naam_kennisdeelgebied_quoted = (f'"{naam_kennisdeelgebied}"')
        # query = Literal(
        #     "prefix kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> select  ?kennisdeelgebied where { graph <urn:name:kennisgebiedenregister> { ?kennisdeelgebied a kgr:Kennisdeelgebied. ?kennisdeelgebied rdfs:label ?naam.  FILTER (lcase(?naam)=lcase(" + naam_kennisdeelgebied_quoted + "))}}")
        # # print (f"{query}") # gaat niet lekker maar sparql lijkt gevuld.
        #
        # response = requests.post(
        #     config.DATASTORE_LOOKUP_ENDPOINT, data={"query": query}, verify=False
        # )
        # if response.status_code == 200:
        #     response_json = str(response.json())
        #     substring = "kennisgebied/"  #
        #     # substring = naam_kennisdeelgebied
        #
        #     if response_json.find(substring) != -1:
        #         print(
        #             f"🐢kennisdeelgebied='{naam_kennisdeelgebied}' jeuh, want komt voor in het kennisgebiedenregister.")
        #     else:
        #         print(
        #             f"⁉️ kennisdeelgebied='{naam_kennisdeelgebied}' komt helaas niet voor in het kennisgebiedenregister")
        #
        #     # else:
        #     #    raise ValueError(
        #     #        f"⁉️ kennisdeelgebied='{naam_kennisdeelgebied}' komt helaas niet voor in het kennisgebiedenregister"
        #     #    )
        #     # sys.exit(1)
        #
        # else:
        #     return jsonify("Query niet correct.")

        """#03 model	naam	{o:Model/a:Name} bevat na de code van het kennisgebied de naam van het model."""
        print("#03 Model naam=" + model_name)

        """#04 Model	titel	Gelijk aan {o:Model/a:Name}"""
        print("#04 Modeltitel=" + model_name)

        """#05 Model	kennisdeelgebied	Indien de naam van het Model niet gelijk 
       aan de naam van het kennisgebied, dan is sprake van een kennisdeelgebied 
       en dient de naam van het kennisdeelgebied opgezocht te worden 
       uit het kennisdeelgebiedenregister. Mocht deze niet gevonden worden, dan waarschuwing geven."""

        print("#05 model kennisdeelgebied  ..TODO.. ") #TODO

        """ #06 label	Gelijk aan de titel"""
        print("#01 Model titel= " + model_name)

        """#07 Modelversie	URI	UUID5 met als input het UUID van het Model, 
       aangevuld met het versienummer (zonder snapshot, formaat 1.0.0)"""
        print("#07 modelversie= " + self.mde_model_uuid + self.mde_model_version)

        """#08 modelversie	versieVan	URI van het model"""
        model_version = input_json["model"]["version"]
        print("#08 modelversie " + model_version)

        """#09 Modelversie	naam	De naam van het model, aangevuld met het (volledige) versienummer"""
        print("#09 model versie naam" + model_name + model_version)

        """#10 Modelversie	titel	De titel van het model, aangevuld met het (volledige) versienummer"""
        print("#09 model versie titel aangevuld met versienummer=" + model_name + model_version)

        """#11 Modelversie	status	Gelijk aan mb:Uitgewerkt"""
        print("#11 model versie status=")

        """ #12 Modelversie	versiedatum	De datum van de meest recent {a:ModificationDate} van alle objecten in het bestand"""
        print("#12 modelversie versiedatum=" + self.mde_versie_datum_model)

        """#13 Modelversie	versienummer	{o:Model/a:Version}"""
        print("#13 model versie naam=" + model_version)

        """ #14 Label	Gelijk aan de titel"""
        print("#14 label=" + model_name)
