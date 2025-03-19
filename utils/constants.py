import json
import os

from rdflib import Namespace, URIRef
import pandas as pd

PATH = "path"
MAPPING = "mapping"
CREATE_QUERY = 'create_query'
READ_QUERY = 'read_query'
INSERT_QUERY = "insert_query"
UPDATE_QUERY = "update_query"
DELETE_QUERY = "delete_query"
ADDITIONAL_COLUMNS = "additional_columns"
PRIMARY_KEYS = "primary key"
ATTRIBUTES = "attributes"
KOLOMMEN = "kolommen"

NAMED_GRAPH_URI_PLACEHOLDER = "GRAPH"

mb_json_options = json.load(
    open(
        os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
        + os.sep
        + "frontend"
        + os.sep
        + "ep"
        + os.sep
        + "mb-json-options.json"
    )
)
#mb_json_options = pd.read_json('ep/mb-json-options.json')

POSTGRES_MAPPING = {
    "domeinen": {
        PATH: "id/domein",
        MAPPING: {
            #"uri": "subject",
            "naam": "http://www.w3.org/2000/01/rdf-schema#label",
            "ketenvoorzitter": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#verantwoordelijke",
            #"laatste_wijziging": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#laatste_wijziging",
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Domeinen (uri varchar(120), naam varchar(150), ketenvoorzitter varchar(150), laatste_wijziging TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO Domeinen (uri, naam, ketenvoorzitter, laatste_wijziging) VALUES (%s, %s, %s, %s)",
        UPDATE_QUERY: "UPDATE Domeinen "
                      "SET naam = %s, ketenvoorzitter = %s, laatste_wijziging = %s "
                      "WHERE uri = %s",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "naam": {
                "type": "input",
                "label": "Naam",
                "waarde": ""
            },
            "ketenvoorzitter": {
                "type": "input",
                "label": "Ketenvoorzitter",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "display",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        }
    },
    "kennisgebieden": {
        PATH: "kennisgebied",
        MAPPING: {
            #"uri": "uri?",
            "naam": "http://www.w3.org/2000/01/rdf-schema#label",
            "code": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#code",
            "domein": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#domein",
            "type_kennisgebied": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#soortKennis",
            "status": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#status",
            "afbakeningstype": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#afbakeningstype",
            "verantwoordelijk_organisatieonderdeel": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#belegdBij",
            "primaire_datasteward": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#datasteward",
            "aanvullende_informatie": "http://www.w3.org/2000/01/rdf-schema#seeAlso",
            #"laatste_wijziging": "laatste_wijziging?"
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Kennisgebieden (uri varchar(120), naam varchar(150), code varchar(100), domein varchar(150), type_kennisgebied varchar(150), status varchar(150), afbakeningstype varchar(150), verantwoordelijk_organisatieonderdeel varchar(150), primaire_datasteward varchar(250), aanvullende_informatie varchar(150), laatste_wijziging timestamp, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO Kennisgebieden (uri, naam, code, domein, type_kennisgebied, status, afbakeningstype, verantwoordelijk_organisatieonderdeel, primaire_datasteward, aanvullende_informatie, laatste_wijziging) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        UPDATE_QUERY: "UPDATE Kennisgebieden "
                      "SET naam = %s, "
                      "code = %s, "
                      "domein = %s, "
                      "type_kennisgebied = %s, "
                      "status = %s, "
                      "afbakeningstype = %s, "
                      "verantwoordelijk_organisatieonderdeel = %s, "
                      "primaire_datasteward = %s, "
                      "aanvullende_informatie = %s, "
                      "laatste_wijziging = %s "
                      "WHERE uri = %s",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "naam": {
                "type": "input",
                "label": "Naam",
                "waarde": ""
            },
            "code": {
                "type": "input",
                "label": "Code",
                "waarde": ""
            },
            "domein": {
                "type": "link",
                "label": "Domein",
                "waarde": ""
            },
            "type_kennisgebied": {
                "type": "input",  # change to select?
                "label": "Type Kennisgebied",
                "waarde": ""
            },
            "status": {
                "type": "input",
                "label": "Status",
                "waarde": ""
            },
            "afbakeningstype": {
                "type": "input",
                "label": "Afbakeningstype",
                "waarde": ""
            },
            "verantwoordelijk_organisatieonderdeel": {
                "type": "input",
                "label": "Verantwoordelijk Organisatieonderdeel",
                "waarde": ""
            },
            "primaire_datasteward": {
                "type": "input",
                "label": "Primaire Datasteward",
                "waarde": ""
            },
            "aanvullende_informatie": {
                "type": "textarea",
                "label": "Aanvullende Informatie",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "datetime",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        }
    },
    "kennisdeelgebieden": {
        PATH: "kennisgebied",
        MAPPING: {
            #"uri": "uri?",
            "naam": "http://www.w3.org/2000/01/rdf-schema#label",
            "code": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#code",
            "kennisgebied": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#onderdeelVan",
            "toelichting": "http://www.w3.org/2000/01/rdf-schema#comment",
            #"laatste_wijziging": "laatste_wijziging?"
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Kennisdeelgebieden (uri varchar(120), naam varchar(150), code varchar(100), kennisgebied varchar(150), toelichting varchar(500), laatste_wijziging timestamp, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO Kennisdeelgebieden (uri, naam, code, kennisgebied, toelichting, laatste_wijziging) VALUES (%s, %s, %s, %s, %s, %s)",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "naam": {
                "type": "input",
                "label": "Naam",
                "waarde": ""
            },
            "code": {
                "type": "input",
                "label": "Code",
                "waarde": ""
            },
            "kennisgebied": {
                "type": "link",
                "label": "Kennisgebied",
                "waarde": ""
            },
            "toelichting": {
                "type": "textarea",
                "label": "Toelichting",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "datetime",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        },
    },
    "medewerkers": {
        PATH: "/id/medewerker/",
        MAPPING: {
            #"uri": "uri?",
            "naam": "http://www.w3.org/2000/01/rdf-schema#label",
            "userid": "http://modellenbibliotheek.belastingdienst.nl/def/mb#username",
            "rol": "http://www.w3.org/ns/org#member",
            "onderdeel_van": "http://www.w3.org/ns/org#memberOf",
            #"toegewezen_kennisgebied": "toegewezen_kennisgebied?",
            #"laatste_wijziging": "laatste_wijziging?"
        },
        ADDITIONAL_COLUMNS: [""],
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Medewerkers (uri varchar(200), naam varchar(150), userid varchar(100), rol varchar(100), onderdeel_van varchar(150), toegewezen_kennisgebied varchar(120), laatste_wijziging timestamp, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO Medewerkers (uri, naam, userid, rol, onderdeel_van, toegewezen_kennisgebied, laatste_wijziging) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "naam": {
                "type": "input",
                "label": "Naam",
                "waarde": ""
            },
            "userid": {
                "type": "input",
                "label": "User ID",
                "waarde": ""
            },
            "rol": {
                "type": "input",
                "label": "Rol",
                "waarde": ""
            },
            "onderdeel_van": {
                "type": "link",
                "label": "Onderdeel van",
                "waarde": ""
            },
            "toegewezen_kennisgebied": {
                "type": "link",
                "label": "Toegewezen Kennisgebied",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "datetime",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        },
    },
    "organisatieonderdeel": {
        PATH: "/id/organisatie/",
        MAPPING: {
            #"uri": "uri?",
            "naam": "http://www.w3.org/2000/01/rdf-schema#label",
            "onderdeeltype": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "voorzitter": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#voorzitter",
            #"laatste_wijziging": "laatste_wijziging?"
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Organisatieonderdeel (uri varchar(200), naam varchar(150), onderdeeltype varchar(150), voorzitter varchar(100), laatste_wijziging timestamp, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO Organisatieonderdeel (uri, naam, onderdeeltype, voorzitter, laatste_wijziging) VALUES (%s, %s, %s, %s, %s)",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "naam": {
                "type": "input",
                "label": "Naam",
                "waarde": ""
            },
            "onderdeeltype": {
                "type": "input",
                "label": "Onderdeeltype",
                "waarde": ""
            },
            "voorzitter": {
                "type": "input",
                "label": "Voorzitter",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "datetime",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        },
    },
    "kennisbronnen": {
        PATH: "id/regeling",
        MAPPING: {
            #"uri": "uri?",
            "naam": "http://www.w3.org/2000/01/rdf-schema#label",
            "titel": "http://purl.org/dc/terms/title",
            "kennisgebied": "http://purl.org/dc/terms/isPartOf",
            "vindplaats": "http://purl.org/dc/terms/bibliographicCitation",
            #"laatste_wijziging": "laatste_wijziging?"
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Kennisbronnen (uri varchar(200), naam varchar(150), titel varchar(150), kennisgebied varchar(150), vindplaats varchar(700), laatste_wijziging timestamp, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO Kennisbronnen (uri, naam, titel, kennisgebied, vindplaats, laatste_wijziging) VALUES (%s, %s, %s, %s, %s, %s)",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "naam": {
                "type": "input",
                "label": "Naam",
                "waarde": ""
            },
            "titel": {
                "type": "input",
                "label": "Titel",
                "waarde": ""
            },
            "kennisgebied": {
                "type": "link",
                "label": "Kennisgebied",
                "waarde": ""
            },
            "vindplaats": {
                "type": "input",
                "label": "Vindplaats",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "datetime",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        }
    },
    "registerwijzigingen": {
        PATH: "id/wijziging",
        MAPPING: {
            #"uri": "uri?",
            "titel": "http://www.w3.org/2000/01/rdf-schema#label",
            "omschrijving": "http://www.w3.org/2000/01/rdf-schema#comment",
            "datum_wijziging": "http://modellenbibliotheek.belastingdienst.nl/def/kgr#datumWijziging",
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS RegisterWijzigingen (uri varchar(200), titel varchar(150), omschrijving varchar(2500), datum_wijziging varchar(100), laatste_wijziging timestamp, PRIMARY KEY (uri));",
        INSERT_QUERY: "INSERT INTO RegisterWijzigingen (uri, titel, omschrijving, datum_wijziging, laatste_wijziging) VALUES (%s, %s, %s, %s, %s)",
        PRIMARY_KEYS: ["uri"],
        ATTRIBUTES: {
            "uri": {
                "type": "link",
                "label": "Bron",
                "waarde": ""
            },
            "titel": {
                "type": "input",
                "label": "Titel",
                "waarde": ""
            },
            "omschrijving": {
                "type": "textarea",
                "label": "Omschrijving",
                "waarde": ""
            },
            "datum_wijziging": {
                "type": "input",
                "label": "Datum wijziging",
                "waarde": ""
            },
            "laatste_wijziging": {
                "type": "datetime",
                "label": "Laatste wijziging",
                "waarde": "",
                "format": "DD-MM-YYYY HH:MM"
            }
        },
    },
    "modelverzoeken": {
        PATH: "id/verzoek",
        MAPPING: {
            "file_id": "subject",
            #"file_id": "http://modellenbibliotheek.belastingdienst.nl/id/verzoek/",
            #"model_name": "model_name?",
            #"vda_model_name": "vda_model_name?",
            #"binary_data": "binary_data?",
            #"file_extension": "file_extension?",
            "named_graph": "http://modellenbibliotheek.belastingdienst.nl/def/tlb#betreft",
            "upload_moment": "http://modellenbibliotheek.belastingdienst.nl/def/tlb#datumVerzoek",
            "bd_user": "http://modellenbibliotheek.belastingdienst.nl/def/tlb#ingediendDoor",
            #"domain": "domain?",
            "title_request": "http://www.w3.org/2000/01/rdf-schema#label",
            "request_type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            #"model_type": "model_type?",
            "jira_number": "http://modellenbibliotheek.belastingdienst.nl/def/mb#code",
            "jira_link": "http://modellenbibliotheek.belastingdienst.nl/def/tlb#jiraLink",
            #"extra_modellers": "http://modellenbibliotheek.belastingdienst.nl/def/tlb#betrokken", #todo: dont retrieve, DO put
            #"remarks": "remarks?",
            "model_status": "http://modellenbibliotheek.belastingdienst.nl/def/tlb#status"
        },
        ADDITIONAL_COLUMNS: None,
        # todo: toekomst CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Modelverzoeken (file_id varchar(100), model_name varchar(100), vda_model_name varchar(100), binary_data bytea, file_extension varchar(5), named_graph varchar(1000), upload_moment timestamp, bd_user varchar(7), domain varchar(100), title_request varchar(100), request_type varchar(100), model_type varchar(100), model_status varchar(100), jira_number varchar(10), extra_modellers varchar(100), remarks varchar(5000), laatste_wijziging timestamp, PRIMARY KEY(jira_number, file_extension));",
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS Modelverzoeken (file_id varchar(100), model_name varchar(100), vda_model_name varchar(100), binary_data bytea, file_extension varchar(5), named_graph varchar(1000), upload_moment timestamp, bd_user varchar(7), domain varchar(100), title_request varchar(100), request_type varchar(1000), model_type varchar(100), model_status varchar(100), jira_number varchar(10), jira_link varchar(1000), extra_modellers varchar(100), remarks varchar(5000), laatste_wijziging timestamp, modelverzoek_status varchar(100);",
        INSERT_QUERY: "INSERT INTO modelverzoeken (file_id, named_graph, upload_moment, bd_user , title_request, request_type, jira_number, jira_link, model_status, laatste_wijziging, modelverzoek_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        #INSERT_QUERY: "INSERT INTO modelverzoeken (file_id, model_name, vda_model_name, binary_data, file_extension, named_graph, upload_moment, bd_user, domain , title_request, request_type, model_type, model_status, jira_number, jira_link, extra_modellers, remarks, laatste_wijziging) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        PRIMARY_KEYS: ["file_id", "named_graph"],
        ATTRIBUTES: {
            "file_id": {
                "type": "hide",
                "label": "Bestand id",
                "waarde": ""
            },
            "model_name": {
                "type": "hide",
                "label": "Modelnaam",
                "waarde": ""
            },
            "vda_model_name": {
                "type": "hide",
                "label": "VDA Modelnaam",
                "waarde": ""
            },
            "file_extension": {
                "type": "hide",
                "label": "bestand-extensie",
                "waarde": ""
            },
            "named_graph": {
                "type": "hide",
                "label": "Uri",
                "waarde": ""
            },
            "bd_user": {
                "type": "input-text",
                "label": "Eigen user ID",
                "waarde": "",
                "verplicht": "required",
                "regex": "^[a-z]{5}\\\d{2}$",
                "regexplanation": "Een gebruikersnaam bestaande uit 5 kleine letters gevolgd door 2 cijfers",
                "position": 4,
            },
            "upload_moment": {
                "type": "display",
                "label": "Datum verzoek",
                "waarde": "",
                "position": 3
            },
            "domain": {
                "type": "hide",
                "label": "Domein actief",
                "waarde": "",
                "position": 99
            },
            "title_request": {
                "attribuut": "title_request",
                "type": "input-text",
                "label": "Titel van het verzoek",
                "waarde": "",
                "position": 1
            },
            "request_type": {
                "type": "select",
                "label": "Soort verzoek",
                "waarde": "",
                "opties": [mb_json_options["soortVerzoek"]["options"][option] for option in mb_json_options["soortVerzoek"]["options"]],
                "position": 6
            },
            "model_type": {
                "type": "display",
                "label": "Soort model",
                "waarde": "",
                "opties": [mb_json_options["soortModel"]["options"][option] for option in mb_json_options["soortModel"]["options"]],
                "position": 7
            },
            "model_status": {
                "type": "hide",
                "label": "Model Status",
                "waarde": "",
                "opties": [mb_json_options["modelStatus"]["options"][option] for option in mb_json_options["modelStatus"]["options"]],
                "position": 99
            },
            "modelverzoek_status": {
                "type": "select",
                "label": "Modelverzoek Status",
                "waarde": "",
                "opties": [mb_json_options["modelVerzoekStatus"]["options"][option] for option in mb_json_options["modelVerzoekStatus"]["options"]],
                "position": 8
            },
            "jira_number": {
                "type": "input-text",
                "label": "Service desk Jira nummer",
                "waarde": "",
                "verplicht": "required",
                "regex": "^SDGGD-\\\d{3}$",
                "regexplanation": "Een Jira-ticket beginnend met SDGGD- gevolgd door 3 cijfers",
                "position": 2
            },
            "jira_link": {
                "type": "hide",
                "label": "Jira URL",
                "waarde": ""
            },
            "extra_modellers": {
                "type": "input-text",
                "label": "Extra modelleurs",
                "waarde": "",
                "regex": "^$|^([a-z]{5}\\\d{2})([ ,]+[a-z]{5}\\\d{2})*$",
                "regexplanation": "Een komma-gescheiden lijst van gebruikersnamen bestaande uit 5 kleine letters gevolgd door 2 cijfers",
                "position": 5
            },
            "remarks": {
                "type": "input-text",
                "label": "Opmerkingen",
                "waarde": "",
                "position": 9
            },
            "binary_data": {
                "type": "input-file",
                "label": "Model",
                "waarde": "",
                "position": 10
            },
            "laatste_wijziging": {
                "type": "hide",
                "label": "",
                "waarde": ""
            },
        }
    },
    "toetsingsrapport": {
        PATH: "id/toetsingsrapport",
        MAPPING: {
            "named_graph": "named_graph?",
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"DROP TABLE IF EXISTS Toetsingsrapport; CREATE TABLE IF NOT EXISTS Toetsingsrapport (named_graph varchar(100), binary_data bytea, name varchar(100), PRIMARY KEY(named_graph));", #TODO: REMOVE DROP TABLE WHEN MOVING TO DEVELOP
        INSERT_QUERY: "INSERT INTO toetsingsrapport (named_graph, binary_data, name) VALUES (%s, %s, %s) ON CONFLICT (named_graph) DO UPDATE SET binary_data = EXCLUDED.binary_data;",
        READ_QUERY: "SELECT name FROM toetsingsrapport WHERE named_graph = %s",

        PRIMARY_KEYS: ["named_graph"],
        ATTRIBUTES: {
            "named_graph": {
                "type": "hide",
                "label": "modelversie (named_graph)",
                "waarde": ""
            },
            "binary_data": {
                "type": "input-file",
                "verplicht": "required",
                "label": "Upload toetsingsrapport",
                "waarde": "Geen"
            },
            "name": {
                "type": "hide",
                "label": "naam van toetsingsrapport",
                "waarde": ""
            }
        }
    },
    "rapportage_query": {
        PATH: "id/query",
        MAPPING: {
            "query_id": "query_id?",
        },
        ADDITIONAL_COLUMNS: None,
        CREATE_QUERY: f"CREATE TABLE IF NOT EXISTS rapportage_query (rapportage_query_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), sparql_query TEXT, naam VARCHAR(100), beschrijving TEXT, modeltype VARCHAR(5));",
        INSERT_QUERY: "INSERT INTO rapportage_query (sparql_query, naam, beschrijving, modeltype) VALUES (%s, %s, %s, %s);",
        UPDATE_QUERY: "UPDATE rapportage_query SET sparql_query = %s, naam = %s, beschrijving = %s, modeltype = %s WHERE rapportage_query_id = %s;",
        DELETE_QUERY: "DELETE FROM rapportage_query WHERE rapportage_query_id = %s;",
        PRIMARY_KEYS: ["rapportage_query_id"],
        ATTRIBUTES: {
            "rapportage_query_id": {
                "type": "hide",
                "label": "Query ID",
                "waarde": ""
            },
            "model": {
                "type": "select",
                "verplicht": "required",
                "label": "Kies een Model",
                "waarde": "",
                "opties": ["Kies een model", "ModelPlaceHolder1", "ModelPlaceHolder2", "ModelPlaceHolder3", "ModelPlaceHolder4"],
                "position": 1
            },
            "sparql_query": {
                "type": "input-textarea",
                "verplicht": "required",
                "label": "Query",
                "waarde": "SELECT * WHERE\n{\n\tGRAPH <@" + NAMED_GRAPH_URI_PLACEHOLDER + "@> \n\t{\n\t\t?subject ?predicate ?object\n\t}\n}\n",
                "buttons": {
                    "querytest": "/rapportage_query/uitvoeren_query"
                },
                "position": 2
            },
            "naam": {
                "type": "input-text",
                "verplicht": "required",
                "label": "Naam",
                "waarde": "Hier komt de naam van de query",
                "position": 4
            },
            "beschrijving": {
                "type": "input-text",
                "verplicht": "required",
                "label": "Beschrijving",
                "waarde": "Beschrijving van de query",
                "position": 5
            },
            "modeltype": {
                "type": "select",
                "verplicht": "required",
                "label": "Modeltype",
                "waarde": "",
                "opties": mb_json_options["soortModel"]["options"],
                "position": 6
            }
        },
        KOLOMMEN: {
            "kolom 1": "Naam Query",
            "kolom 2": "Beschrijving",
            "kolom 3": "Modeltype"
        }
    }
}

######################################################################################################################
# GENERAL #
######################################################################################################################
# Namespaces URFs
URF_MB = "http://modellenbibliotheek.belastingdienst.nl/def/mb#"
URF_KGR = "http://modellenbibliotheek.belastingdienst.nl/def/kgr#"

# Custom Namespaces
NS_MB = Namespace(URF_MB)
NS_KGR = Namespace(URF_KGR)
NS_SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")
NS_SM = Namespace("http://modellenbibliotheek.belastingdienst.nl/def/sm#")
NS_LGD = Namespace("http://modellenbibliotheek.belastingdienst.nl/def/lgd#")
NS_TLB = Namespace("http://modellenbibliotheek.belastingdienst.nl/def/tlb#")

# Extensions
TURTLE_EXTENSION = ".ttl"
XLSX_EXTENSION = ".xlsx"
LDM_EXTENSION = ".ldm"
XML_EXTENSION = ".xml"
HTTP = "http"

# Request Header
turtle_headers = {"Content-Type": "text/turtle;charset=utf-8"}

# Prefixes
LM_PREFIX = URIRef("http://modellenbibliotheek.belastingdienst.nl/lm/")

GET_FUSEKI_MODELS_SPARQL_QUERY = f"""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix mb: <http://modellenbibliotheek.belastingdienst.nl/def/mb#>
select ?modelversie ?modelversie_label
where {{
  graph ?modelversie {{
    ?modelversie a mb:Modelversie.
    ?modelversie rdfs:label ?modelversie_label.
    ?modelversie mb:versieVan ?model.
    ?modelversie mb:versiedatum ?datum
  }}
  FILTER NOT EXISTS {{
    graph ?nieuwer {{
      ?nieuwer mb:versieVan ?model.
      ?nieuwer mb:versiedatum ?ndatum.
      FILTER (?ndatum>?datum)
    }}
  }}
}}
order by ?modelversie_label
"""
