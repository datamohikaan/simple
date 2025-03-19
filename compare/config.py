ENV = "LOC"  # TODO: VOOR HET PUSHEN, VERANDER DIT NAAR "ONT", VOOR LOKAAL TESTEN, VERANDER NAAR "LOC"

##################### CONTAINER PLATFORM ENDPOINTS #####################
if ENV == "LOC":
    #DATASTORE_ENDPOINT = "https://mbieb2.ont.belastingdienst.nl/modellenbibliotheek"
    #DATASTORE_ENDPOINT = "https://mbieb.tst.belastingdienst.nl/modellenbibliotheek"
    #DATASTORE_ENDPOINT = "http://mbk-fuseki:3030/modellenbibliotheek"
    DATASTORE_ENDPOINT = "https://mbk-fuseki-boscp08-dev.apps.rm3.7wse.p1.openshiftapps.com/modellenbibliotheek"

    DB_CONFIG = {
    "dbname": "database1",
    "user": "user1",
    "password": "password1",
    "host": "mbk-postgres",
    "port": "5432",
    }

   # DB_CONFIG = {
   #    "dbname": "postgres",
   #     "user": "postgres",
   #     "password": "postgres",
   #     "host": "localhost",
   #     "port": "5432",
   # }

elif ENV in ["ONT", "TST", "ACC", "PROD"]:
    DATASTORE_ENDPOINT = "http://mbk-fuseki:3030/modellenbibliotheek"
    DB_CONFIG = {
        "dbname": "database1",
        "user": "user1",
        "password": "password1",
        "host": "mbk-postgres",
        "port": "5432",
    }
DATASTORE_LOOKUP_ENDPOINT = DATASTORE_ENDPOINT + "/sparql"

##################### SINGLE SIGN ON #####################
PRODUCTION_BASE_URL = "https://fibi1.belastingdienst.nl"
BASE_URL = "https://fibi2.acc.belastingdienst.nl"
REDIRECT_URL = "https://modellenbibliotheek.ont.belastingdienst.nl/authorized"
AUTHORIZATION_URL = BASE_URL + "/as/authorization.oauth2"
TOKEN_URL = BASE_URL + "/as/token.oauth2"
USERINFO_URL = BASE_URL + "/idp/userinfo.openid"
CLIENT_ID = "7cb623f1-ddec-4541-a13d-9f2bcbe74647"
CLIENT_KEY = "F5udJRW2s9QnLvs77nqQni7xy7jf6I2AiaBjSkwWpl8="
SCOPE = "openid profile"

##################### FLASK ENDPOINTS #####################
SECRET = "test"
QUERY_ROUTE = "/querier"
UPLOAD_ROUTE = "/upload"
SSO_ROUTE = "/authorized"
DOWNLOAD_ROUTE = "/download"
QUERYDIENST_ROUTE = "/rapportage_query/uitvoeren_query"
FUSEKI_RESTORE = "/fuseki_restore"
TOEVOEGEN_GEBRUIKERS = "/toevoegen_gebruikers"

PUBLIC_PAGES = [
    "",
    "/authorized",
    "domeinen",
    "kennisbronnen",
    "kennisgebiedenregister",
    "registerwijzigingen",
    "kennisbanken",
    "toetsingslogboek",
    "dashboard",
    "dashboard2",
]

PROTECTED_PAGES_MAPPING = {
    "mau": [
        "upload",
        "querydienst",
        "magazijn",
        "toetsingslogboek_",
        "modelverzoeken",
        "rapportage_query/wijzigen_pagina",
        "rapportage_query/create_pagina",
    ],
    "das": [
        "upload",
        "modelverzoeken",
    ],
    "mod": [
        "upload",
        "modelverzoeken",
    ],
    "beh": [
        "querydienst",
        "magazijn",
        "fuseki_restore",
        "fuseki_herstel",
        "toevoegen_gebruikers"
    ],
    "dflt": [],
    "loc": [
        "upload",
        "querydienst",
        "magazijn",
        "fuseki_restore",
        "fuseki_herstel",
        "modelverzoeken",
    ],
    "pow": [
        "upload",
        "querydienst",
        "magazijn",
        "fuseki_restore",
        "fuseki_herstel",
        "modelverzoeken",
        "toevoegen_gebruikers",
        "toetsingslogboek_",
        "rapportage_query/wijzigen_pagina",
        "rapportage_query/create_pagina",
    ],
    "cnrp": [
        "upload",
        "querydienst",
        "rapportage_query/wijzigen_pagina",
        "rapportage_query/create_pagina",
        "magazijn",
        "toetsingslogboek_",
        "modelverzoeken",
    ],
}

# Create a set to hold all protected pages for all roles
PROTECTED_PAGES_SET = set()
for role, extensions in PROTECTED_PAGES_MAPPING.items():
    PROTECTED_PAGES_SET.update(extensions)

PROTECTED_ENDPOINTS_MAPPING = {
    "mau": [
        'update_modelverzoek',
    ],
    "das": [
        'update_modelverzoek',
    ],
    "mod": [
        'update_modelverzoek',
    ],
    "beh": [
    ],
    "dflt": [
    ],
    "loc": [
        'update_modelverzoek',
    ],
    "pow": [
        'update_modelverzoek',
    ],
}

# Create a set to hold all protected pages for all roles
PROTECTED_ENDPOINTS_SET = set()
for role, extensions in PROTECTED_ENDPOINTS_MAPPING.items():
    PROTECTED_ENDPOINTS_SET.update(extensions)



##################### FUNCTIONAL ENDPOINTS #####################
TOETSINGSLOGBOEK_ENDPOINT = DATASTORE_ENDPOINT + "?graph=urn:name:toetsingslogboek"
