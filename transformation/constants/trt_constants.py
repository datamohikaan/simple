from utils.constants import *

######################################################################################################################
# TOETSINGSRAPPORT TRT  #
######################################################################################################################

##Namespaces
NS_TLB = Namespace("http://modellenbibliotheek.belastingdienst.nl/def/tlb#")
NS_TK = Namespace("http://modellenbibliotheek.belastingdienst.nl/def/tk#")

# Algemeen
# TRT Template Sheet Names
ALGEMEEN = "Algemeen"
ADVIEZEN = "Adviezen"
MEETOORDEEL = "Meetoordeel"
METINGEN = "Metingen"
BEVINDINGEN = "Bevindingen"
CALCULATIE = "Calculatie"
TOETSINGSKADER = "Toetsingskader"
MEETWAARDEN = "Meetwaarden"

# Sheet Algemeen
## Invoervelden
RAPPORTVERSIE = "Rapportversie"
DATUM_RAPPORT = "Datum rapport"
BETREFT = "Betreft"
KWALITEITSLABEL = "Kwaliteitslabel"
TOELICHTING = "Toelichting"
DATUM_TOETSING = "Datum toetsing"
GEBRUIKTE_TOETSKADERS = "Gebruikte toetskaders"

## Column names
WAARDE = (
    "WAARDE"  # corresponds to the column "In te vullen waarden / IN TE VULLEN WAARDEN"
)

## Should-velden, zou er moeten zijn en anders warning
GETOETST_MODEL = "GETOETST MODEL"
GETOETSTE_VERSIE = "GETOETSTE VERSIE"
RAPPORTVERSIE = "RAPPORTVERSIE"
DATUM_RAPPORT = "DATUM RAPPORT"


ALGEMEEN_FIELD_MAPPING = {
    RAPPORTVERSIE: ["Rapportversie"],
    DATUM_RAPPORT: ["Datum rapport"],
    BETREFT: ["Betreft"],
    KWALITEITSLABEL: ["Kwaliteitslabel"],
    TOELICHTING: ["Toelichting"],
    DATUM_TOETSING: ["Datum toetsing"],
    GEBRUIKTE_TOETSKADERS: ["Gebruikte toetskaders"],
    GETOETST_MODEL: ["Getoetst model"],
    GETOETSTE_VERSIE: ["Getoetste versie"],
}

ALGEMEEN_MANDATORY_FIELDS = {
    RAPPORTVERSIE,
    DATUM_RAPPORT,
    BETREFT,
    KWALITEITSLABEL,
    TOELICHTING,
    DATUM_TOETSING,
    GEBRUIKTE_TOETSKADERS
}

ALGEMEEN_OPTONAL_FIELDS = []

# These fields should exist, if not, give a warning but continue the transformation
ALGEMEEN_WARNING_FIELDS = [GETOETST_MODEL, GETOETSTE_VERSIE]


ALGEMEEN_COLUMN_MAPPING = {
    WAARDE: ["Waarde", "WAARDE"],
}

# Sheet Adviezen column names
NUMMER = "NUMMER"
ADVIES = "ADVIES"
STATUS = "STATUS"
TOELICHTING = "TOELICHTING"
VERWACHT_RESULTAAT = "VERWACHT_RESULTAAT"

ADVIEZEN_COLUMN_MAPPING = {
    NUMMER: ["Nummer", "NUMMER"],
    ADVIES: ["Advies", "ADVIES"],
    STATUS: ["Status", "STATUS"],
    TOELICHTING: ["Toelichting", "TOELICHTING"],
    VERWACHT_RESULTAAT: ["Verwacht resultaat", "VERWACHT_RESULTAAT"],
}


# Sheet Meetoordeel column names
DIMENSIE = "Dimensie"
SCORE = "Score"
OORDEEL = "Oordeel"
Toelichting = "Toelichting"

MEETOORDEEL_COLUMN_MAPPING = {
    DIMENSIE: ["Dimensie", "DIMENSIE"],
    SCORE: ["Score", "SCORE"],
    OORDEEL: ["Oordeel", "OORDEEL"],
    TOELICHTING: ["Toelichting", "TOELICHTING"],
}


# Sheet Metingen column names
DIMENSIE = "Dimensie"
MEETINDICATOR = "Meetindicator"
GEMETEN_WAARDE = "Gemeten waarde"
Toelichting = "Toelichting"

METINGEN_COLUMN_MAPPING = {
    DIMENSIE: ["Dimensie", "DIMENSIE"],
    MEETINDICATOR: ["Meetindicator", "MEETINDICATOR"],
    GEMETEN_WAARDE: ["Gemeten waarde", "GEMETEN_WAARDE"],
    TOELICHTING: ["Toelichting", "TOELICHTING"],
}

# Sheet Bevindingen column names
NUMMER = "NUMMER"
DIMENSIE = "DIMENSIE"
STATUS = "STATUS"
OORDEEL = "OORDEEL"
BEVINDING = "BEVINDING"
BETREFT_MTHV = "BETREFT MTHV"

BEVINDINGEN_COLUMN_MAPPING = {
    NUMMER: ["Nummer", "NUMMER"],
    DIMENSIE: ["Dimensie", "DIMENSIE"],
    STATUS: ["Status", "STATUS"],
    OORDEEL: ["Oordeel", "OORDEEL"],
    BEVINDING: ["Bevinding", "BEVINDING"],
    BETREFT_MTHV: ["Betreft MTHV", "BETREFT_MTHV"],
}

# Sheet Meetwaarden column names
MEETWAARDE = "Meetwaarde"
CODE = "Code"

MEETWAARDEN_COLUMN_MAPPING = {
    MEETWAARDE: ["Meetwaarde", "MEETWAARDE"],
    CODE: ["Code", "CODE"],
}
