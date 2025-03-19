import os.path
import sys
from dataclasses import dataclass, field, MISSING
from enum import Enum
from typing import Optional, Iterator
import numpy as np
from flask import jsonify

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import os
import uuid
import ssl
import pandas as pd
from SPARQLWrapper import SPARQLWrapper2
from rdflib import URIRef, Graph
from utils.sparql_queries import query_code_kennisgebieden, query_code_begrippen, query_naam_kennisdeelgebieden, \
    query_naam_kennisgebieden, query_naam_administratie, query_naam_interactie, query_naam_proces, \
    query_uri_kennisgebieden, query_uri_architectuurmodel, query_uri_toetsingslogboek


# TODO: Mag eventueel eruit als er geen environment variabelen nodig zijn
def get_environment():
    if os.getenv("CI_ENVIRONMENT_NAME"):
        return os.getenv("CI_ENVIRONMENT_NAME")
    else:
        return "ontwikkeling"


# TODO: Mag eventueel eruit als er geen environment variabelen nodig zijn
def get_datastore_endpoint():
    return os.getenv("DATASTORE")


def read_sheet_as_dataframe(
    xls_file: pd.ExcelFile,
    sheet_name: str,
    index_column: int = None,
    rename_columns: bool = False,
    rename_index: bool = False,
    column_mapping: dict = None,
    index_mapping: dict = None,
):
    """Reads sheet from an Excel file where the choice can be made to rename the columns to a generic name
    :param xls_file: the respective Excel sheet that need to be read in
    :param sheet_name: the corresponding sheet name
    :param index_column: optional argument, in case one would like to specify an index column
    :param rename_columns: optional argument, flag to indicate whether one would like to rename the column names
    and provide generic names
    :param rename_index: optional argument, flag to indicate whether one would like to rename the index names
    and provide generic names
    :param column_mapping: optional argument, the column mapping needed for the column renaming
    :param index_mapping: optional argument, the index mapping needed for the index renaming
    :return: created dataframe with potentially specified index column and generic column names
    """
    df = pd.read_excel(xls_file, sheet_name, index_col=index_column)

    if rename_columns:
        for generic_name, column_names in column_mapping.items():
            actual_columns = [col for col in df.columns if col in column_names]
            if actual_columns:
                df.rename(columns={actual_columns[0]: generic_name}, inplace=True)

    if rename_index:
        for generic_name, index_names in index_mapping.items():
            actual_index = [index for index in df.index if index in index_names]
            if actual_index:
                df.rename(index={actual_index[0]: generic_name}, inplace=True)

    df_stripped = df.applymap(lambda x: x.strip() if isinstance(x, str) else x) # strip all trailing spaces from all string values

    return df_stripped.replace(np.nan, '', regex=True)  # remove nan values


def create_uri(name: str) -> URIRef:
    """Each cononical uri has the following structure according to RFC4122.

    :param name: name of the namespace
    :return: the created uri
    """
    uuidstr = uuid.uuid5(uuid.NAMESPACE_URL, name)
    return URIRef(f"urn:uuid:{uuidstr}")


def get_column_index(df: pd.DataFrame, column: str):
    """Returns the column index number of a dataframe - the number does not start at zero, but is corrected with plus one
    :param df: the dataframe of which the index number is desired
    :param column: the column name
    :return: the column index number
    """
    return df.columns.get_loc(column) + 1


def capitalize_df(
    df: pd.DataFrame, capitalize_index: bool = False, capitalize_columns: bool = False
):
    """
    :param df: the input dataframe
    :param capitalize_index: flag whether we want to  capitalize the index names
    :param capitalize_columns: flag whether to capitalize the column names
    :return: the dataframe with the capitalized names
    """
    if capitalize_index:
        df.index = [str(index).upper() for index in df.index]

    if capitalize_columns:
        df.columns = [str(column).upper() for column in df.columns]

    return df


def lookup_kb_uri_from_code(lookup_endpoint: str, lookup_code_kb: str):
    """Looks up the uris from Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_code_kb: the respective code to be looked up, either a kb code or a kdgb code
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_code_kennisgebieden(lookup_code_kb))
    uri = []
    for result in sparql.query().bindings:
        uri.append(result["kennisgebied"].value)
    if not uri:
        raise ValueError(
            f"Het kennisgebied met code {lookup_code_kb} komt niet voor in het kennisgebiedenregister."
        )
    else:
        return uri[0]


def lookup_kdgb_uri_from_code(lookup_endpoint: str, lookup_code_kdgb: str):
    """Looks up the uris from Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_code_kdgb: the respective code to be looked up, either a kb code or a kdgb code
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_code_kennisgebieden(lookup_code_kdgb))
    uri = []
    for result in sparql.query().bindings:
        uri.append(result["kennisgebied"].value)
    if not uri:
            raise ValueError(
                f"Het kennisdeelgebied met code {lookup_code_kdgb} komt niet voor in het kennisgebiedenregister."
            )
    else:
        return uri[0]


def lookup_kdgb_uri_from_naam_kdgb(lookup_endpoint: str, lookup_naam_kdgb: str, lookup_code_kb:str, lookup_uri_kb:str):
    """Looks up the uris from Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_naam_kdgb: the respective code to be looked up, either a kb code or a kdgb code
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_naam_kennisdeelgebieden(lookup_naam_kdgb=lookup_naam_kdgb, lookup_uri_kb=lookup_uri_kb))
    uri_kdgb = []
    for result in sparql.query().bindings:
        uri_kdgb.append(result["kennisgebied"].value)
    if not uri_kdgb:
        raise ValueError(
            f"Het kennisdeelgebied met naam {lookup_naam_kdgb} bij kennisgebied met code {lookup_code_kb} bestaat niet in het kennisgebiedenregister"
        )

    else:
        return uri_kdgb[0]


def lookup_kb_uri_from_naam(lookup_endpoint: str, lookup_naam_kgb: str):
    """Looks up the uris from Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_naam_kgb: the respective code to be looked up, either a kb code or a kdgb code
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    lookup_naam_kgb_formatted = f"\"{lookup_naam_kgb}\""

    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_naam_kennisgebieden(lookup_naam_kgb=lookup_naam_kgb))
    uri_kgb = []
    for result in sparql.query().bindings:
        uri_kgb.append(result["kennisgebied"].value)
    if not uri_kgb:
        raise ValueError(
            f"Het kennisgebied met naam {lookup_naam_kgb} bestaat niet in het kennisgebiedenregister"
        )

    else:
        return uri_kgb[0]


def lookup_begrip_uri_from_code(lookup_endpoint: str, lookup_code_kb: str, lookup_begrip: str):
    """Looks up the uris from Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_code_kb: the respective code to be looked up, either a kb code or a kdgb code
    :param lookup_begrip: "begrip" to be looked up
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_code_begrippen(lookup_code_kb, lookup_begrip))
    uri = []
    for result in sparql.query().bindings:
        uri.append(result["begrip"].value)
    if not uri:
        print(
            f'Het begrip "{lookup_begrip}" komt niet voor in het kennisgebiedenregister {lookup_code_kb}.'
        )
    else:
        return uri[0]


def lookup_administratie_uri_from_naam(lookup_endpoint: str, lookup_naam_administratie: str):
    """Looks up the uris from Architectuurmodel (BES)
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_naam_administratie: the respective name to be looked up
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_naam_administratie(lookup_naam_administratie=lookup_naam_administratie))
    administratie_uri = []
    for result in sparql.query().bindings:
        administratie_uri.append(result["administratie_uri"].value)
    if not administratie_uri:
        raise ValueError(
            f"De administratie met naam {lookup_naam_administratie} bestaat niet in het Architectuurmodel (BES)"
        )

    else:
        return administratie_uri[0]


def lookup_interactie_uri_from_naam(lookup_endpoint: str, lookup_naam_interactie: str):
    """Looks up the uris from Architectuurmodel (BES)
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_naam_interactie: the respective name to be looked up
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_naam_interactie(lookup_naam_interactie=lookup_naam_interactie))
    interactie_uri = []
    for result in sparql.query().bindings:
        interactie_uri.append(result["interactie_uri"].value)
    if not interactie_uri:
        raise ValueError(
            f"De interactie met naam {lookup_naam_interactie} bestaat niet in het Architectuurmodel (BES)"
        )

    else:
        return interactie_uri[0]


def lookup_proces_uri_from_naam(lookup_endpoint: str, lookup_naam_proces: str):
    """Looks up the uris from Architectuurmodel (BES)
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_naam_proces: the respective name to be looked up
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_naam_proces(lookup_naam_proces=lookup_naam_proces))
    proces_uri = []
    for result in sparql.query().bindings:
        proces_uri.append(result["proces_uri"].value)
    if not proces_uri:
        raise ValueError(
            f"Het proces met naam {lookup_naam_proces} bestaat niet in het Architectuurmodel (BES)"
        )

    else:
        return proces_uri[0]


def lookup_kb_naam_from_uri(lookup_endpoint: str, lookup_kb_uri: str):
    """Looks up the naam from a given uri in Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_kb_uri: the respective uri to be looked up
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_uri_kennisgebieden(lookup_kb_uri=lookup_kb_uri))
    uri_kgb = []
    for result in sparql.query().bindings:
        uri_kgb.append(result["label"].value)
    if not uri_kgb:
        raise ValueError(
            f"Het kennisgebied met uri {lookup_kb_uri} bestaat niet in het kennisgebiedenregister"
        )
    else:
        return uri_kgb[0]


def lookup_bes_naam_from_uri(lookup_endpoint: str, lookup_bes_uri: str):
    """Looks up the naam from a given uri in Kennisgebiedenregister
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_kb_uri: the respective uri to be looked up
    :param is_kg: flag to specify whether the code is kb (True) or kdgb (False)
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_uri_architectuurmodel(lookup_bes_uri=lookup_bes_uri))
    uri_kgb = []
    for result in sparql.query().bindings:
        uri_kgb.append(result["label"].value)
    if not uri_kgb:
        raise ValueError(
            f"Het Architectuurmodel(BES)-object met uri {lookup_bes_uri} bestaat niet in het kennisgebiedenregister"
        )
    else:
        return uri_kgb[0]


def lookup_model_uri_from_modelverzoek_uri(lookup_endpoint: str, lookup_modelverzoek_uri: str):
    """Looks up the named_graph/model_uri from a given modelverzoek_uuid in Toetsingslogboek
    :param lookup_endpoint: the end point reference from the the look-up should be done
    :param lookup_modelverzoek_uri: the respective modelverzoek uuid to be looked up
    :return: list containing the uris
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    sparql = SPARQLWrapper2(lookup_endpoint)
    sparql.setQuery(query_uri_toetsingslogboek(lookup_modelverzoek_uri=lookup_modelverzoek_uri))
    uri_kgb = []
    for result in sparql.query().bindings:
        uri_kgb.append(result["model_uri"].value)
    if not uri_kgb:
        raise ValueError(
            f"Het modelverzoek met met uuid '{lookup_modelverzoek_uri}' bevat geen modelversie in het toetsingslogboek"
        )
    else:
        return uri_kgb[0]


def find_uri_in_graph(g: Graph, filters):
    """Returns the uri of a triple of the respective graph
    :param g: the respecive Graph
    :param filters: item to look for in the graph, no type is passed to have it generic
    :return: uri of the item
    """
    for s, p, o in g:
        if o == filters:
            return s


class MeldingSoort(str, Enum):
    WARNING = 'WARNING'
    INFO = 'INFO'
    ERROR = 'ERROR'
    SUCCESS = 'INFO'


class StandaardMeldingBericht(str, Enum):
    WARNING = 'Waarschuwing'
    INFO = 'Actie Succesvol'
    ERROR = 'Er is een onbekende fout opgetreden'


@dataclass(frozen=True)
class Melding:
    """
    Een gebruiksvriendelijke melding na een actie.

    frozen=True Makes the object immutable after creation

    Attrs:
        soort: The type of message (INFO, WARNING, ERROR).
            Type: MeldingSoort
            Default: MeldingSoort.INFO

        melding: The content of the message. Defaults to StandaardMeldingBericht corresponding with `soort`
            Type = (Optional[str])
            Default = StandaardMeldingBericht[self.soort.name]

    """
    soort: MeldingSoort = MeldingSoort.INFO
    melding: Optional[str] = None

    def __post_init__(self):
        """If melding wasn't provided, compute it based on the soort.
        """
        if self.melding is None:
            default_message = StandaardMeldingBericht[self.soort.name]
            object.__setattr__(self, 'melding', default_message)

    def __str__(self):
        return f"{self.soort.name}: {self.melding}"


@dataclass(frozen=True, kw_only=True)
class AttribuutMelding(Melding):
    """Een melding voor een specifieke attribuut in een formulier.
    Overerft gedrag van Melding

        frozen=True     Makes the object immutable after creation
        kw_only=True    Requires the values in this object to be specifically assigned through a keyword.
                            Voorbeeld:
                            >    AttribuutMelding('sparql_query') -> Error
                            >    AttribuutMelding(attribuut='sparql_query') -> Succes

    Usage:
        AttribuutMelding(MeldingSoort.ERROR, attribuut='model_naam')
        AttribuutMelding(MeldingSOORT.INFO, '', attribuut='sparql_query')
        AttribuutMelding(MeldingSOORT.INFO, 'Document met naam: {name} succesvol geupload' attribuut='sparql_query')
    """
    attribuut: str = field(default=MISSING)

    def __post_init__(self):
        super().__post_init__()
        # Optionally, add further processing for AttribuutMelding if needed.


class MeldingManager(list):
    def __init__(self):
        super().__init__()
        self.meldingen: list[Melding] = []

    def meld(self, soort: MeldingSoort = MeldingSoort.SUCCESS, melding: Optional[str] = None, attribuut: Optional[str] = None):
        """Appends a meld to the meldingen list"""
        if attribuut:
            melding = AttribuutMelding(soort=soort, melding=melding, attribuut=attribuut)
        else:
            melding = Melding(soort=soort, melding=melding)
        self.meldingen.append(melding)

    def contains(self, melding_soort: MeldingSoort):
        # returns first item
        return any(melding.soort == melding_soort for melding in self.meldingen)

    # List-like behavior
    def __getitem__(self, index):
        return self.meldingen[index]

    def __setitem__(self, index, value):
        self.meldingen[index] = value

    def __delitem__(self, index):
        del self.meldingen[index]

    def __len__(self):
        return len(self.meldingen)

    def __iter__(self):
        return iter(self.meldingen)

    def __contains__(self, item):
        return item in self.meldingen

    def append(self, item):
        self.meldingen.append(item)

    def extend(self, iterable):
        self.meldingen.extend(iterable)

    def insert(self, index, item):
        self.meldingen.insert(index, item)

    def remove(self, item):
        self.meldingen.remove(item)

    def pop(self, index=-1):
        return self.meldingen.pop(index)

    def clear(self):
        self.meldingen.clear()

    def index(self, item, *args):
        return self.meldingen.index(item, *args)

    def count(self, item):
        return self.meldingen.count(item)

    def reverse(self):
        self.meldingen.reverse()

    def sort(self, *args, **kwargs):
        self.meldingen.sort(*args, **kwargs)

    def __repr__(self):
        return repr(self.meldingen)

    def __iadd__(self, other):
        if isinstance(other, MeldingManager):
            self.meldingen.extend(other.meldingen)
        else:
            self.meldingen.extend(other)
        return self

    def to_str(self):
        return "\n".join(str(melding) for melding in self.meldingen)



class ReturnHandler(dict):
    def __init__(self):
        super().__init__()
        self.return_variables: dict[Melding] = {}

    def meld(self, soort: MeldingSoort, melding: Optional[str] = None, attribuut: Optional[str] = None):
        """Appends a meld to the meldingen list"""
        if attribuut:
            melding = AttribuutMelding(soort=soort, melding=melding, attribuut=attribuut)
        else:
            melding = Melding(soort=soort, melding=melding)
        self.return_variables.append(melding)

    def __getitem__(self, key):
        if key == "meldingen":
            return self.return_variables
        raise KeyError(f"Key '{key}' not found")

    def __setitem__(self, key, value):
        if key == "meldingen":
            if isinstance(value, list):
                self.return_variables = value
            else:
                raise TypeError("Value must be a list")
        else:
            raise KeyError("Only 'meldingen' key is allowed")

    def __delitem__(self, key):
        if key == "meldingen":
            self.return_variables.clear()
        else:
            raise KeyError("Only 'meldingen' key is allowed")

    def keys(self):
        return ["meldingen"]

    def values(self):
        return [self.return_variables]

    def items(self):
        return [("meldingen", self.return_variables)]

    def __iter__(self):
        return iter(["meldingen"])

    def __contains__(self, key):
        return key == "meldingen"

    def __repr__(self):
        return f"{{'meldingen': {self.return_variables}}}"
