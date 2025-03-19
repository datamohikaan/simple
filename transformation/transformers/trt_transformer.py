import inspect

from utils.utils import (
    read_sheet_as_dataframe,
    create_uri,
    get_column_index,
    capitalize_df,
    lookup_kb_uri_from_code,
    lookup_kdgb_uri_from_naam_kdgb,
    lookup_begrip_uri_from_code,
    find_uri_in_graph,
    get_datastore_endpoint, lookup_kb_naam_from_uri,
)
from datetime import datetime
import uuid
import re
from rdflib import Graph, URIRef, Literal
import pandas as pd
import mde_wrapper.constants.trt_constants as trt_cn
from frontend.ep.config import DATASTORE_ENDPOINT
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, SKOS


class TRTTransformer:
    def __init__(self, file_dir: str, file_name: str, input_xlsx):
        self.file_dir = file_dir
        self.file_name = file_name
        self.file_name_turtle = self.file_name + trt_cn.TURTLE_EXTENSION
        self.input_xlsx = input_xlsx
        self.g = Graph()

        self.uri = None
        self.modelURI = None
        self.advies = None
        self.nummer = None
        self.status = None
        self.toelichting = None

    def transform_trt_xml_to_rdf(self):
        """Main function that needs to be called in order to transform XML to turtle.
        :return: the file name of the created turtle file.
        """
        print("into dze trt_transformer transform_trt_xml_to_rdf" )
        self.process_algemeen()
        self.process_adviezen()
        self.process_meetoordeel()
        self.process_metingen()
        self.process_bevindingen()
        self.process_meetwaarden()
        self.g.serialize(destination=self.file_dir + self.file_name_turtle)

    def set_uri(self):
        """Setting the graph URI"""
        model_file_name = (
                "KG_"
                + self.naam_kb
                + "_-_"
                + self.naam_model
                + "_-_"
                + "v"
                + str(self.versie_num_model_without_snapshot)
                + "_-_"
                + self.versie_datum_model
        )

    def get_uri(self):
        """Returning the graph URI"""
        return self.uri

    def get_file_name_turtle(self):
        """Returning the name of the turtle file"""
        return self.file_name_turtle

    def get_vda_model_name(self):
        if self.naam_kdgb:
            return f"{self.code_kb} {self.naam_kdgb}"
        else:
            return f"{self.naam_kb}"

    def process_algemeen(self):
        """Function that handles the sheet "Algemeen"""

        def handle_naam_model(naam_model: str):
            naam_model_splitted = naam_model.split("-")
            if naam_model_splitted[0] == trt_cn.SM:
                if len(naam_model_splitted) == 2:
                    return naam_model_splitted[1]
                elif (len(naam_model_splitted) > 2) & (
                    naam_model_splitted[1] != self.code_kb
                ):
                    return naam_model
                else:
                    return " ".join(naam_model_splitted[2:])
            else:
                return naam_model

        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=trt_cn.ALGEMEEN,
            index_column=0,
            rename_columns=True,
            column_mapping=trt_cn.ALGEMEEN_COLUMN_MAPPING,
            rename_index=True,
            index_mapping=trt_cn.ALGEMEEN_FIELD_MAPPING,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)
        self.getoetst_model= df.loc[trt_cn.GETOETST_MODEL][trt_cn.WAARDE]
        self.getoetste_versie = df.loc[trt_cn.GETOETSTE_VERSIE][trt_cn.WAARDE]
        self.rapportversie = df.loc[trt_cn.RAPPORTVERSIE][trt_cn.WAARDE]
        self.versiedatum = df.loc[trt_cn.DATUM_RAPPORT][trt_cn.WAARDE].strftime("%Y-%m-%d")
        self.label = str('Toetsingsrapport ' + self.getoetst_model + ' ' + self.getoetste_versie)

        rapport_uuid= create_uri(self.getoetst_model)

        self.g.add((rapport_uuid, RDF.type, trt_cn.NS_TLB.Rapport))
        self.g.add((rapport_uuid, RDFS.label, Literal(self.label)))
        self.g.add((rapport_uuid,trt_cn.NS_MB.versiedatum, Literal(self.versiedatum, datatype=XSD.date)))
        self.g.add((rapport_uuid, trt_cn.NS_MB.versienummer, Literal(self.rapportversie)))



        #return None

        # # Declaring the important fields, not including timestamp and replacing spaces in values with '-'
        # self.versie_datum_model = df.loc[trt_cn.VERSIE_DATUM_MODEL][trt_cn.WAARDEN].strftime(
        #     "%Y-%m-%d"
        # )
        # df.loc[trt_cn.VERSIE_DATUM_MODEL] = self.versie_datum_model
        #
        # #df[sbm_cn.WAARDEN] = df[sbm_cn.WAARDEN].str.replace(" ", "-")
        # self.code_kb = df.loc[trt_cn.CODE_KB][trt_cn.WAARDEN]
        # self.uri_kb = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, self.code_kb)
        # self.naam_kb = lookup_kb_naam_from_uri(DATASTORE_ENDPOINT, self.uri_kb)
        # #self.naam_kb = df.loc[sbm_cn.NAAM_KB][sbm_cn.WAARDEN]
        #
        # self.code_kdgb = df.loc[trt_cn.CODE_KDGB][trt_cn.WAARDEN]
        # opgegeven_naam_kdgb = df.loc[trt_cn.NAAM_KDGB][trt_cn.WAARDEN]
        # if opgegeven_naam_kdgb:
        #     self.uri_kdgb = lookup_kdgb_uri_from_naam_kdgb(DATASTORE_ENDPOINT, opgegeven_naam_kdgb, self.code_kb, self.uri_kb)
        #     self.naam_kdgb = lookup_kb_naam_from_uri(DATASTORE_ENDPOINT, self.uri_kdgb)
        # self.code_kdgb = df.loc[trt_cn.CODE_KDGB][trt_cn.WAARDEN]
        #
        # self.naam_model = handle_naam_model(df.loc[trt_cn.NAAM_MODEL][trt_cn.WAARDEN])
        # self.titel_model = df.loc[trt_cn.NAAM_MODEL][trt_cn.WAARDEN]
        # self.versie_num_model = df.loc[trt_cn.VERSIE_NUM_MODEL][trt_cn.WAARDEN]
        # self.versie_num_model_without_snapshot = self.versie_num_model.split(
        #     "-", maxsplit=1
        # )[0]
        # self.taal_model = df.loc[trt_cn.TAAL_MODEL][trt_cn.WAARDEN]
        # self.taal_model_lower = self.taal_model.lower()
        # if str(df.loc[trt_cn.SECTAAL_MODEL][trt_cn.WAARDEN]) is not "":
        #     self.sec_taal_model = df.loc[trt_cn.SECTAAL_MODEL][trt_cn.WAARDEN]
        #     self.sec_taal_model_lower = self.sec_taal_model.lower()

    def process_adviezen(self):
        """Function that handles the sheet "Algemeen"""
        print("joehoe! we zitten in de functie: " + inspect.currentframe().f_code.co_name)
        # self.set_uri()

        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=trt_cn.ADVIEZEN,
            # index_column=0,
            rename_columns=True,
            column_mapping=trt_cn.ADVIEZEN_COLUMN_MAPPING,
            # rename_index=True,
            # index_mapping=sbm_cn.ADVIEZEN_COLUMN_MAPPING,
        )
        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)
        #return None

        #hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str("testtoetsingsrapport"))
        #self.uri = f"urn:uuid:{hash_uuid}"
        for i in df.itertuples():
            print(i, "Hallo i")
            print(df)
            print(trt_cn.NUMMER)

            self.advies = i[get_column_index(df, trt_cn.NUMMER)]
            object = create_uri(self.advies)
            self.g.add((object, RDFS.label, Literal(self.advies)))


    def process_meetoordeel(self):
        """Function that handles the sheet "Algemeen"""
        print("joehoe! we zitten in de functie: " + inspect.currentframe().f_code.co_name)
        # self.set_uri()

        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=trt_cn.MEETOORDEEL,
            # index_column=0,
            rename_columns=True,
            column_mapping=trt_cn.MEETOORDEEL_COLUMN_MAPPING,
            # rename_index=True,
        )
        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)

    def process_metingen(self):
        """Function that handles the sheet "Algemeen"""
        print("joehoe! we zitten in de functie: " + inspect.currentframe().f_code.co_name)
        # self.set_uri()

        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=trt_cn.METINGEN,
            # index_column=0,
            rename_columns=True,
            column_mapping=trt_cn.METINGEN_COLUMN_MAPPING,
            # rename_index=True,
        )
        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)

    def process_bevindingen(self):
        """Function that handles the sheet "Algemeen"""
        print("joehoe! we zitten in de functie: " + inspect.currentframe().f_code.co_name)
        # self.set_uri()

        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=trt_cn.BEVINDINGEN,
            # index_column=0,
            rename_columns=True,
            column_mapping=trt_cn.BEVINDINGEN_COLUMN_MAPPING,
            # rename_index=True,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)

        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)

        for i in df.itertuples():
            self.nummer = i[get_column_index(df, trt_cn.NUMMER)]
            oordeel = i[get_column_index(df, trt_cn.OORDEEL)]
            self.betreftMTHV = i[get_column_index(df, trt_cn.BETREFT_MTHV)]
            self.bevinding = i[get_column_index(df, trt_cn.BEVINDING)]

            dimensie = i[get_column_index(df, trt_cn.DIMENSIE)]
            self.dimensie = str(trt_cn.NS_TK + dimensie)
            print("oordeel")
            print(oordeel)
            if oordeel == "Kan beter":
                oordeel = "KanBeter"
            self.oordeel = str(trt_cn.NS_TLB + oordeel)

            bevinding_uuid= create_uri(f"{self.nummer}")

            self.g.add((bevinding_uuid, RDF.type, trt_cn.NS_TLB.Bevinding))
            self.g.add((bevinding_uuid, RDFS.label, Literal(self.nummer)))
            self.g.add((bevinding_uuid, trt_cn.NS_TLB.Dimensie, URIRef(self.dimensie)))
            self.g.add((bevinding_uuid, trt_cn.NS_TLB.Oordeel, URIRef(self.oordeel)))
            if self.betreftMTHV != "":
                self.g.add((bevinding_uuid, trt_cn.NS_TLB.BetreftMTHV, Literal(self.betreftMTHV)))
            self.g.add((bevinding_uuid, RDFS.comment, Literal(self.bevinding)))


            #print(self.bevinding)



    def process_meetwaarden(self):
        """Function that handles the sheet "Algemeen"""
        print("joehoe! we zitten in de functie: " + inspect.currentframe().f_code.co_name)
        # self.set_uri()

        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=trt_cn.MEETWAARDEN,
            # index_column=0,
            rename_columns=True,
            column_mapping=trt_cn.MEETWAARDEN_COLUMN_MAPPING,
            # rename_index=True,
        )
        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)







