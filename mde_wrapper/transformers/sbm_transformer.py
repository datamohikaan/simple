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
from rdflib import Graph, URIRef, Literal, BNode
import pandas as pd
import mde_wrapper.constants.sbm_constants as sbm_cn
from frontend.ep.config import DATASTORE_ENDPOINT
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, SKOS, FOAF


class SBMTransformer:
    def __init__(self, file_dir: str, file_name: str, input_xlsx):
        self.file_dir = file_dir
        self.file_name = file_name
        self.file_name_turtle = self.file_name + sbm_cn.TURTLE_EXTENSION
        self.input_xlsx = input_xlsx
        self.g = Graph()
        self.naam_model = None
        self.titel_model = None

        self.naam_kb = None
        self.code_kb = None
        self.uri_kb = None
        self.naam_kdgb = None
        self.code_kdgb = None
        self.uri_kdgb = None

        self.versie_num_model = None
        self.versie_num_model_without_snapshot = None
        self.versie_datum_model = None
        self.taal_model = None
        self.taal_model_lower = None
        self.sec_taal_model = None
        self.sec_taal_model_lower = None
        self.uri = None
        self.modelURI = None

    def transform_sm_xml_to_rdf(self):
        """Main function that needs to be called in order to transform XML to turtle.
        :return: the file name of the created turtle file.
        """
        self.process_algemeen()
        self.set_uri()
        self.create_namespace_graph()
        self.process_kennisbronnen()
        self.process_begrippen()
        if sbm_cn.TERMVORMEN in self.input_xlsx.sheet_names:
            self.process_termvormen()
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
        hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(model_file_name))
        self.uri = f"urn:uuid:{hash_uuid}"

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

    def create_namespace_graph(self):
        """Creates the Namespace graph with the specified namespaces.
        :return: returns the created Namespace Graph.
        """
        # Creating and adding custom namespaces
        self.g.bind("mb", sbm_cn.NS_MB)
        self.g.bind("kgr", sbm_cn.NS_KGR)
        self.g.bind("skos", SKOS)
        self.g.bind("skosxl", sbm_cn.NS_SKOSXL)
        self.g.bind("rdfs", RDFS)
        self.g.bind("dcterms", DCTERMS)
        self.g.bind("sm", sbm_cn.NS_SM)

        # Defining names

        if self.naam_kdgb is not None:
            self.modelURI = create_uri(f"{self.code_kb}/{self.naam_kdgb.lower()}")
            self.modelversieURI = create_uri(f"{self.code_kb}/{self.naam_kdgb.lower()}-{self.versie_num_model_without_snapshot}")
        else:
            print('UUID generate')
            #self.naam_kb =self.naam_kb.lower()
            print(self.code_kb)
            self.modelURI = create_uri(f"{self.code_kb}/{self.naam_kb.lower()}")
            print(self.modelURI)
            print(f"{self.code_kb}/{self.naam_kb.lower()}-{self.versie_num_model_without_snapshot}")
            self.modelversieURI = create_uri(f"{self.code_kb}/{self.naam_kb.lower()}-{self.versie_num_model_without_snapshot}")


        registratie_moment = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.model_name_version = self.get_vda_model_name() + ' ' + self.versie_num_model_without_snapshot

        # Look up
        lookup_code_kb = self.code_kb  # EXM
        kennisgebiedURI = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, lookup_code_kb)

        self.g.add((self.modelURI, RDF.type, SKOS.ConceptScheme))
        self.g.add((self.modelURI, RDF.type, sbm_cn.NS_MB.Model))
        self.g.add((self.modelURI, DCTERMS.title, Literal(self.naam_model, lang = self.taal_model)))
        self.g.add((self.modelURI, RDFS.label, Literal(self.get_vda_model_name())))
        self.g.add((self.modelURI, sbm_cn.NS_KGR.kennisgebied, URIRef(kennisgebiedURI)))
        self.g.add((self.modelversieURI, RDF.type, sbm_cn.NS_MB.Modelversie))
        self.g.add((self.modelversieURI, sbm_cn.NS_MB.versieVan, self.modelURI))
        self.g.add(
            (
                self.modelversieURI,
                sbm_cn.NS_MB.versiedatum,
                Literal(self.versie_datum_model, datatype=XSD.date),
            )
        )
        self.g.add(
            (self.modelversieURI, sbm_cn.NS_MB.versienummer, Literal(self.versie_num_model))
        )
        self.g.add(
            (
                self.modelversieURI,
                RDFS.label,
                Literal(self.model_name_version)
            )
        )
        self.g.add((self.modelversieURI, sbm_cn.NS_MB.status, sbm_cn.NS_MB.Finaal))
        self.g.add(
            (
                self.modelversieURI,
                sbm_cn.NS_MB.registratiemoment,
                Literal(registratie_moment, datatype=XSD.dateTime),
            )
        )
        if self.uri_kdgb:
            self.g.add(
                (self.modelURI, sbm_cn.NS_KGR.kennisdeelgebied, URIRef(self.uri_kdgb))
            )

    def process_algemeen(self):
        """Function that handles the sheet "Algemeen"""

        def handle_naam_model(naam_model: str):
            naam_model_splitted = naam_model.split("-")
            if naam_model_splitted[0] == sbm_cn.SM:
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
            sheet_name=sbm_cn.ALGEMEEN,
            index_column=0,
            rename_columns=True,
            column_mapping=sbm_cn.ALGEMEEN_COLUMN_MAPPING,
            rename_index=True,
            index_mapping=sbm_cn.ALGEMEEN_FIELD_MAPPING,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
        df = capitalize_df(df, capitalize_index=True, capitalize_columns=True)

        # Declaring the important fields, not including timestamp and replacing spaces in values with '-'
        self.versie_datum_model = df.loc[sbm_cn.VERSIE_DATUM_MODEL][sbm_cn.WAARDEN].strftime(
            "%Y-%m-%d"
        )
        df.loc[sbm_cn.VERSIE_DATUM_MODEL] = self.versie_datum_model

        #df[cn.WAARDEN] = df[cn.WAARDEN].str.replace(" ", "-")
        self.code_kb = df.loc[sbm_cn.CODE_KB][sbm_cn.WAARDEN]
        self.uri_kb = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, self.code_kb)
        self.naam_kb = lookup_kb_naam_from_uri(DATASTORE_ENDPOINT, self.uri_kb)
        #self.naam_kb = df.loc[cn.NAAM_KB][cn.WAARDEN]

        self.code_kdgb = df.loc[sbm_cn.CODE_KDGB][sbm_cn.WAARDEN]
        opgegeven_naam_kdgb = df.loc[sbm_cn.NAAM_KDGB][sbm_cn.WAARDEN]
        if opgegeven_naam_kdgb:
            self.uri_kdgb = lookup_kdgb_uri_from_naam_kdgb(DATASTORE_ENDPOINT, opgegeven_naam_kdgb, self.code_kb, self.uri_kb)
            self.naam_kdgb = lookup_kb_naam_from_uri(DATASTORE_ENDPOINT, self.uri_kdgb)
        self.code_kdgb = df.loc[sbm_cn.CODE_KDGB][sbm_cn.WAARDEN]

        self.naam_model = handle_naam_model(df.loc[sbm_cn.NAAM_MODEL][sbm_cn.WAARDEN])
        self.titel_model = df.loc[sbm_cn.NAAM_MODEL][sbm_cn.WAARDEN]
        self.versie_num_model = df.loc[sbm_cn.VERSIE_NUM_MODEL][sbm_cn.WAARDEN]
        self.versie_num_model_without_snapshot = self.versie_num_model.split(
            " ", maxsplit=1)[0]
        self.taal_model = df.loc[sbm_cn.TAAL_MODEL][sbm_cn.WAARDEN]
        self.taal_model_lower = self.taal_model.lower()
        if str(df.loc[sbm_cn.SECTAAL_MODEL][sbm_cn.WAARDEN]) is not "":
            self.sec_taal_model = df.loc[sbm_cn.SECTAAL_MODEL][sbm_cn.WAARDEN]
            self.sec_taal_model_lower = self.sec_taal_model.lower()

    def process_kennisbronnen(self):
        """Function that handles the sheet "Kennisbronnen" """
        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.KENNISBRONNEN,
            rename_columns=True,
            column_mapping=sbm_cn.KENNISBRONNEN_COLUMN_MAPPING,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
        df = capitalize_df(df, capitalize_columns=True)

        for i in df.itertuples():
            print("kennisbronnenUri")
            print(f"doc/{str(i[get_column_index(df, sbm_cn.CITEERTITEL)]).lower()}")
            grondslagURI = create_uri(f"doc/{str(i[get_column_index(df, sbm_cn.CITEERTITEL)]).lower()}")
            self.g.add((grondslagURI, RDF.type, DCTERMS.BibliographicResource))

            if str(i[get_column_index(df, sbm_cn.CITEERTITEL)]) is not "":
                # self.g.add(
                #     (
                #         grondslagURI,
                #         RDFS.label,
                #         Literal(i[get_column_index(df, cn.BRONNAAM)]),
                #     )
                # ).
                self.g.add(
                    (
                        grondslagURI,
                        DCTERMS.alternative,
                        Literal(i[get_column_index(df, sbm_cn.CITEERTITEL)]),
                    )
                )
                #commenten wanneer ispartof nodig is
          #  if str(i[get_column_index(df, cn.ONDERDEELVAN)]) is not "":
           #     if (
            #        i[get_column_index(df, cn.ONDERDEELVAN)]
             #       in df[cn.CITEERTITEL].unique()
              #  ):
                    #self.g.add(
                     #   (
                      #      grondslagURI,
                       #     DCTERMS.isPartOf,
                        #    create_uri(f"doc/{i[get_column_index(df, cn.ONDERDEELVAN)].lower()}"),
                        #)
                    #)
            # if str(i[get_column_index(df, cn.BRONNAAM)]) is not "":
            #     self.g.add(
            #         (
            #             grondslagURI,
            #             DCTERMS.title,
            #             Literal(i[get_column_index(df, cn.BRONNAAM)]),
            #         )
            #     )
            if str(i[get_column_index(df, sbm_cn.BRONLOCATIE)]) is not "":
                if str(i[4][:4]) == sbm_cn.HTTP:
                    self.g.add(
                        (
                            grondslagURI,
                            FOAF.page,
                            URIRef(i[get_column_index(df, sbm_cn.BRONLOCATIE)]),
                        )
                    )
                if str(i[4][:4]) != sbm_cn.HTTP:
                    self.g.add(
                        (
                            grondslagURI,
                            FOAF.page,
                            Literal(i[get_column_index(df, sbm_cn.BRONLOCATIE)]),
                        )
                    )

    def process_begrippen(self):
        """Function that handles the sheet "Begrippen" """
        df_begrippen = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.BEGRIPPEN,
            rename_columns=True,
            column_mapping=sbm_cn.BEGRIPPEN_COLUMN_MAPPING,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)

        df_kennisbronnen = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.KENNISBRONNEN,
            rename_columns=True,
            column_mapping=sbm_cn.KENNISBRONNEN_COLUMN_MAPPING,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)

        df_begrippen = capitalize_df(df_begrippen, capitalize_columns=True)
        df_kennisbronnen = capitalize_df(df_kennisbronnen, capitalize_columns=True)
        lookup_code_kb = self.code_kb
        lookedup_kg_uri = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, lookup_code_kb)
        self.naam_kb = lookup_kb_naam_from_uri(DATASTORE_ENDPOINT, lookedup_kg_uri)

        for i in df_begrippen.itertuples():

            lookup_code_kb = self.code_kb
            lookedup_kg_uri = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, lookup_code_kb)
            self.naam_kb = lookup_kb_naam_from_uri(DATASTORE_ENDPOINT, lookedup_kg_uri)

            if self.naam_kdgb is not None:
                print(f"{self.code_kb}/{self.naam_kdgb}/{i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)].lower()}")
                subject = create_uri(
                f"{self.code_kb}/{self.naam_kdgb}/{i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)].lower()}")
            else:
                print(f"{self.code_kb}/{i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)].lower()}")
                subject = create_uri(
                    f"{self.code_kb}/{self.naam_kb.lower()}/{i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)].lower()}")

            self.g.add((subject, RDF.type, SKOS.Concept))
            self.g.add((subject, SKOS.inScheme, self.modelURI))
            self.g.add((subject, sbm_cn.NS_KGR.kennisgebied, URIRef(lookedup_kg_uri)))

            # Voorkeursterm
            print("hallo voorkeursterm")
            print(subject)
            print(i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)])
            print(Literal(i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)]))
            self.g.add(
                (
                    subject,
                    RDFS.label,
                    Literal(
                        i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)],
                        lang=self.taal_model_lower,
                    ),
                )
            )
            self.g.add(
                (
                    subject,
                    SKOS.prefLabel,
                    Literal(
                        i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM)],
                        lang=self.taal_model_lower,
                    ),
                )
            )

            # Bovenliggend begrip
            if str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]) is not "":
                if str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]).count(".") == 1:

                    parts = str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]).split('.')
                    begrip = str(parts[1]).strip("]")
                    code_kb= str(parts[0]).strip("[")
                    lookedup_kg_uri = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, code_kb)

                    extern_begrip_uri=create_uri(f"{code_kb}/{begrip.lower()}")
                    self.g.add((subject, SKOS.broader, extern_begrip_uri))
                    self.g.add((extern_begrip_uri, RDF.type, SKOS.Concept))
                    self.g.add((extern_begrip_uri, RDFS.label, Literal(begrip, lang = self.taal_model.lower())))
                    self.g.add((extern_begrip_uri, sbm_cn.NS_KGR.Kennisgebied, URIRef(lookedup_kg_uri)))

                else:
                    df_termvormen = df = read_sheet_as_dataframe(
                        xls_file=self.input_xlsx,
                        sheet_name=sbm_cn.TERMVORMEN,
                        rename_columns=True,
                        column_mapping=sbm_cn.TERMVORMEN_COLUMN_MAPPING,
                    ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
                    capitalize_df(df_termvormen, capitalize_columns=True)

                    predicate = SKOS.broader

                    if str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]) in df_begrippen[sbm_cn.VOORKEURSTERM].values:

                        if self.naam_kdgb is not None:
                            object = create_uri(f"{self.code_kb}/{self.naam_kdgb.lower()}/{i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)].lower()}")
                        else:
                            object = create_uri(
                                f"{self.code_kb}/{self.naam_kb.lower()}/{i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)].lower()}")
                        self.g.add((subject, predicate, object))

                    elif str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]) in df_termvormen[sbm_cn.MEERVOUD].values:

                        voorkeursterm = str(df_termvormen.iloc[k][sbm_cn.VOORKEURSTERM].values[0])

                        if self.naam_kdgb is not None:
                            meervoud_uri = create_uri(f"{self.code_kb}/{self.naam_model.lower()}/{str(voorkeursterm).lower()}")
                        else:
                            meervoud_uri = create_uri(f"{self.code_kb}/{str(voorkeursterm).lower()}")
                        self.g.add((subject, predicate, meervoud_uri))

                    elif str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]) in df_termvormen[sbm_cn.AFKORTING].values:

                        k = df_termvormen.index[
                            df_termvormen[sbm_cn.AFKORTING].str.lower() == str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)])]

                        voorkeursterm = str(df_termvormen.iloc[k][sbm_cn.VOORKEURSTERM].values[0])


                        if self.naam_kdgb is not None:
                            afkorting_uri = create_uri(f"{self.code_kb}/{self.naam_model.lower()}/{str(voorkeursterm).lower()}")
                        else:
                            afkorting_uri = create_uri(f"{self.code_kb}/{str(voorkeursterm).lower()}")
                        self.g.add((subject, predicate, afkorting_uri))

                    elif str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)])in df_termvormen[sbm_cn.ENKELVOUD].values:
                        k = df_termvormen.index[
                            df_termvormen[sbm_cn.ENKELVOUD].str.lower() == str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)])]

                        voorkeursterm = str(df_termvormen.iloc[k][sbm_cn.VOORKEURSTERM].values[0])


                        if self.naam_kdgb is not None:
                            enkelvoud_uri = create_uri(f"{self.code_kb}/{self.naam_model.lower()}/{str(voorkeursterm).lower()}")
                        else:
                            enkelvoud_uri = create_uri(f"{self.code_kb}/{str(voorkeursterm).lower()}")
                        self.g.add((subject, predicate, enkelvoud_uri))

                    else:

                        onbekend_bovenliggend = BNode()
                        self.g.add((subject, SKOS.broader, onbekend_bovenliggend))
                        self.g.add((onbekend_bovenliggend, RDFS.label, Literal(str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]))))

            ##meervoudsvorm hiddenlabel
#            self.g.add((subject, SKOS.hiddenLabel, meervoud_uri))
            # Definitie
            if str(i[get_column_index(df_begrippen, sbm_cn.DEFINITIE)]) is not "":
                predicate = SKOS.definition
                object = Literal(
                    i[get_column_index(df_begrippen, sbm_cn.DEFINITIE)],
                    lang=self.taal_model_lower,
                )
                self.g.add((subject, predicate, object))

                # Verwijzing van begrippen https://jira.belastingdienst.nl/browse/GVG-4800
                bovenliggend = ("[" + str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]) + "]")

                resDefinitie = re.findall(
                    r"\[.*?\]", i[get_column_index(df_begrippen, sbm_cn.DEFINITIE)]
                )
                verwijzingen=[]
                for verwijzing in resDefinitie:
                    if verwijzing == bovenliggend:
                        print(verwijzing, 'is bovenliggend')
                    else:
                        verwijzingen.append(verwijzing)


                for begrip_bron in verwijzingen:
                    print("Hallo begrip_bron2")
                    print(begrip_bron)
                    begrip_bron=str(begrip_bron)[1:-1]
                    begrip_bron_lower=begrip_bron.lower()
                    #print("resDefinitie akte",[resDefinitie[1]])
                    if begrip_bron.count(".") == 1:
                        print("extern begrip")

                        parts = str(begrip_bron).split('.')
                        begrip = str(parts[1]).strip("]")
                        code_kb = str(parts[0]).strip("[")
                        lookedup_kg_uri = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, code_kb)
                        print(f"{code_kb}/{self.naam_kb.lower()}/{begrip.lower()}")
                        extern_begrip_uri = create_uri(f"{code_kb}/{begrip.lower()}")
                        self.g.add((subject, SKOS.related, extern_begrip_uri))

                        self.g.add((extern_begrip_uri, RDF.type, SKOS.Concept))
                        self.g.add((extern_begrip_uri, RDFS.label, Literal(begrip, lang = self.taal_model)))
                        self.g.add((extern_begrip_uri, sbm_cn.NS_KGR.Kennisgebied, URIRef(lookedup_kg_uri)))


                    else:
                        df_termvormen = read_sheet_as_dataframe(
                        xls_file=self.input_xlsx,
                        sheet_name=sbm_cn.TERMVORMEN,
                        rename_columns=True,
                        column_mapping=sbm_cn.TERMVORMEN_COLUMN_MAPPING,
                        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
                        capitalize_df(df_termvormen, capitalize_columns=True)

                        predicate2 = SKOS.related
                        voorkeurstermen =  [s.lower() for s in df_begrippen[sbm_cn.VOORKEURSTERM].values]
                        if begrip_bron.casefold() in voorkeurstermen:
                            print(type(df_begrippen[sbm_cn.VOORKEURSTERM].values))
                            print("Hallo waarden")
                            print(begrip_bron.casefold())
                            print(self.code_kb)
                            print(self.naam_kb)


                            if self.naam_kdgb is not None:
                                object2 = create_uri(
                                    f"{self.code_kb}/{self.naam_kdgb.lower()}/{str(begrip_bron.lower())}")
                            else:
                                object2 = create_uri(
                                    f"{self.code_kb}/{self.naam_kb.lower()}/{str(begrip_bron).lower()}")
                            self.g.add((subject, predicate2, object2))
                        elif begrip_bron.count(".") == 1:

                            parts = str(i[get_column_index(df_begrippen, sbm_cn.BOVENLIGGEND_BEGRIP)]).split('.')
                            begrip = str(parts[1]).strip("]")
                            code_kb = str(parts[0]).strip("[")
                            #lookedup_kg_uri = lookup_kb_uri_from_code(DATASTORE_ENDPOINT, code_kb)
                            extern_begrip_uri = create_uri(f"{code_kb}/{begrip.lower()}")
                            self.g.add((subject, SKOS.related, extern_begrip_uri))

                        elif begrip_bron.casefold() in df_termvormen[sbm_cn.MEERVOUD].values:

                            k = df_termvormen.index[
                                df_termvormen[sbm_cn.MEERVOUD].str.lower() == begrip_bron]
                            voorkeursterm=str(df_termvormen.iloc[k][sbm_cn.VOORKEURSTERM].values[0])

                            if self.naam_kdgb is not None:
                                meervoud_uri=create_uri(
                                    f"{self.code_kb}/{self.naam_kdgb.lower()}/{str(voorkeursterm).lower()}")
                            else:
                                meervoud_uri = create_uri(
                                    f"{self.code_kb}/{self.naam_kb.lower()}/{str(voorkeursterm).lower()}")
                            if voorkeursterm in df_begrippen[sbm_cn.VOORKEURSTERM].values:
                                self.g.add((subject,predicate2,meervoud_uri))
                            else:
                                begrip_niet_gevonden = BNode()
                                self.g.add((subject, SKOS.related, begrip_niet_gevonden))
                                self.g.add((begrip_niet_gevonden, RDFS.label,
                                            Literal(begrip_bron, lang=self.taal_model.lower())))
                        elif begrip_bron.casefold() in df_termvormen[sbm_cn.AFKORTING].values:

                            k = df_termvormen.index[
                                df_termvormen[sbm_cn.AFKORTING].str.lower() == begrip_bron]

                            voorkeursterm = str(df_termvormen.iloc[k][sbm_cn.VOORKEURSTERM].values[0])

                            if self.naam_kdgb is not None:
                                afkorting_uri = create_uri(
                                    f"{self.code_kb}/{self.naam_kdgb.lower()}/{str(voorkeursterm).lower()}")
                            else:
                                afkorting_uri = create_uri(
                                    f"{self.code_kb}/{self.naam_kb.lower()}/{str(voorkeursterm).lower()}")
                            self.g.add((subject, predicate2, afkorting_uri))
                        elif begrip_bron.casefold() in df_termvormen[sbm_cn.ENKELVOUD].values:
                            k = df_termvormen.index[
                                df_termvormen[sbm_cn.ENKELVOUD].str.lower() == begrip_bron]

                            voorkeursterm = str(df_termvormen.iloc[k][sbm_cn.VOORKEURSTERM].values[0])

                            if self.naam_kdgb is not None:
                                enkelvoud_uri = create_uri(
                                    f"{self.code_kb}/{self.naam_kdgb.lower()}/{str(voorkeursterm).lower()}")
                            else:
                                enkelvoud_uri=create_uri(
                                    f"{self.code_kb}/{self.naam_kb.lower()}/{str(voorkeursterm).lower()}")
                            self.g.add((subject, predicate2, enkelvoud_uri))
                        else:

                            begrip_niet_gevonden=BNode()
                            self.g.add((subject, SKOS.related, begrip_niet_gevonden))
                            self.g.add((begrip_niet_gevonden, RDFS.label, Literal(begrip_bron, lang= self.taal_model.lower())))


            # Toelichting
            if str(i[get_column_index(df_begrippen, sbm_cn.TOELICHTING)]) is not "":
                self.g.add(
                    (
                        subject,
                        SKOS.scopeNote,
                        Literal(
                            str(i[get_column_index(df_begrippen, sbm_cn.TOELICHTING)]),
                            lang=self.taal_model_lower,
                        ),
                    )
                )

            # Redactionele opmerking
            if sbm_cn.REDACTIONELE_OPMERKING in df_begrippen.columns:
                if str(i[get_column_index(df_begrippen, sbm_cn.REDACTIONELE_OPMERKING)]) is not "":
                    self.g.add(
                        (
                            subject,
                            SKOS.editorialNote,
                            Literal(
                                str(
                                    i[
                                        get_column_index(
                                            df_begrippen, sbm_cn.REDACTIONELE_OPMERKING
                                        )
                                    ]
                                ),
                                lang=self.taal_model_lower,
                            ),
                        )
                    )

            # Alternatieve Term(en)
            if str(i[get_column_index(df_begrippen, sbm_cn.ALTERNATIEVE_TERMEN)]) is not "":
                self.g.add(
                    (
                        subject,
                        SKOS.altLabel,
                        Literal(
                            i[get_column_index(df_begrippen, sbm_cn.ALTERNATIEVE_TERMEN)],
                            lang=self.taal_model_lower,
                        ),
                    )
                )

            # Kennisbron(nen)
            if str(i[get_column_index(df_begrippen, sbm_cn.BEGRIPPEN_KENNISBRONNEN)]) is not "":
                kennisbronnen = (
                    i[get_column_index(df_begrippen, sbm_cn.BEGRIPPEN_KENNISBRONNEN)]
                    .replace("; ", ";")
                    .replace(", jo.", " jo.")
                    .replace(" jo.", ";")
                    .split(";")
                )
                if len(kennisbronnen) == 1:
                    kennisbronnen = kennisbronnen[0].split("\n")

                for begrip_bron in kennisbronnen:
                    trimmed_begrip_bron = begrip_bron.strip()
                    print("halllo getrimde bron")
                    print(trimmed_begrip_bron)
                    onderdeelvanUri=create_uri(f"doc/{trimmed_begrip_bron.lower()}")
                    # self.g.add((onderdeelvanUri,RDFS.label, Literal(trimmed_begrip_bron)))
                    # self.g.add((onderdeelvanUri, DCTERMS.title, Literal(trimmed_begrip_bron)))

                    #  self.g.add((subject, cn.NS_MB["grondslag"], kennisbron_uri))
                    #self.g.add(
                    #    (kennisbron_uri, RDF.type, DCTERMS.BibliographicResource)
                    #)
                    #if len(trimmed_begrip_bron.split()) > 1:
                        # begrip_bron_one_word = trimmed_begrip_bron.split()[::-1][0]
                        # begrip_bron_two_words = " ".join(begrip_bron.split()[-2:])
                        #
                        # determine_grondslag_uri = lambda bron: (
                        #     find_uri_in_graph(self.g, Literal(bron))
                        #     if find_uri_in_graph(self.g, Literal(bron))
                        #     else create_uri(bron)
                        # )
                        # print("grondslag uri=", determine_grondslag_uri)
                        #
                        # begrip_bron_uri = (
                        #     determine_grondslag_uri(begrip_bron_one_word)
                        #     if begrip_bron_one_word
                        #     in df_kennisbronnen[cn.CITEERTITEL].values
                        #     else (
                        #         determine_grondslag_uri(begrip_bron_two_words)
                        #         if begrip_bron_two_words
                        #         in df_kennisbronnen[cn.CITEERTITEL].values
                        #         else None
                        #     )
                        # )
                        # df_kennisbronnen = read_sheet_as_dataframe(
                        #     xls_file=self.input_xlsx,
                        #     sheet_name=cn.KENNISBRONNEN,
                        #     rename_columns=True,
                        #     column_mapping=cn.KENNISBRONNEN_COLUMN_MAPPING,
                        # )
                        #
                        # df_kennisbronnen = capitalize_df(df_kennisbronnen, capitalize_columns=True)
                        # bronnaam = i[get_column_index(df_kennisbronnen, cn.BRONNAAM)]
                        # self.g.add((kennisbron_uri, RDFS.label, Literal(bronnaam)))
                        # self.g.add((kennisbron_uri, DCTERMS.title, Literal(bronnaam)))

                        # if begrip_bron_uri:
                        #     if begrip_bron_uri != kennisbron_uri:
                        #         self.g.add(
                        #             (kennisbron_uri, DCTERMS.isPartOf, begrip_bron_uri)
                        #         )



                    relevante_citeertitels = []

                    def add_citeertitel_kennisbron_combi(citeertitel):
                        print("kennisbronnen")

                        k = df_kennisbronnen.index[
                            df_kennisbronnen[sbm_cn.CITEERTITEL].str.lower() == citeertitel
                            ]

                        found_uri = find_uri_in_graph(self.g, Literal(begrip_bron))
                        self.bron_taal= df_kennisbronnen[sbm_cn.TAAL].values[k][0]
                        grondslag_uri = (
                            found_uri
                            if found_uri
                            else create_uri(str(df_kennisbronnen.iloc[k][sbm_cn.BRONNAAM]).lower())
                        )

                        kennisbron_uri = create_uri(f"doc/{citeertitel.lower()}")
                        #self.g.add((onderdeelvanUri, DCTERMS.isPartOf, kennisbron_uri))
                        bronnaam = str(df_kennisbronnen[sbm_cn.BRONNAAM].values[k][0])
                        print(bronnaam)
                        self.g.add((subject, DCTERMS.source, onderdeelvanUri))
                        self.g.add((subject, sbm_cn.NS_MB["grondslag"], onderdeelvanUri))

                        print("kennisbron_uri vs onderdeelvanuri")
                        self.g.add((kennisbron_uri, RDFS.label, Literal(bronnaam, lang = self.bron_taal)))
                        self.g.add((kennisbron_uri, DCTERMS.title, Literal(bronnaam, lang = self.bron_taal)))

                        if onderdeelvanUri != kennisbron_uri:
                            self.g.add((onderdeelvanUri, RDF.type, DCTERMS.BibliographicResource))
                            print(trimmed_begrip_bron)
                            a=len(citeertitel)
                            b=len(trimmed_begrip_bron)
                            print(len(citeertitel))
                            print(len(trimmed_begrip_bron))
                            c=b-a
                            bron_zonder_citeertitel = trimmed_begrip_bron[0:c].strip()
                            print(bron_zonder_citeertitel)
                            self.g.add((onderdeelvanUri, RDFS.label, Literal(trimmed_begrip_bron)))
                            self.g.add((onderdeelvanUri, DCTERMS.title, Literal(bron_zonder_citeertitel, lang = self.taal_model.lower())))
                            self.g.add((onderdeelvanUri, DCTERMS.isPartOf, kennisbron_uri))
                            self.g.add((subject, DCTERMS.source, onderdeelvanUri))
                            self.g.add((subject, sbm_cn.NS_MB["grondslag"], onderdeelvanUri))
                        else:
                            self.g.add((subject, DCTERMS.source, kennisbron_uri))
                            self.g.add((subject, sbm_cn.NS_MB["grondslag"], kennisbron_uri))


                    relevante_citeertitels = [
                        citeertitel for citeertitel in
                        df_kennisbronnen[sbm_cn.CITEERTITEL]
                        .str.lower()
                        .values
                        if begrip_bron.lower().endswith(citeertitel)
                    ]

                    if relevante_citeertitels:
                        # do actions
                        [add_citeertitel_kennisbron_combi(citeertitel) for citeertitel in relevante_citeertitels]

                    else:
                        # er is geen kennisbron gevonden

                        kennisbron = BNode()
                        self.g.add((subject, DCTERMS.source, kennisbron))
                        self.g.add((kennisbron, RDFS.label, Literal(trimmed_begrip_bron)))

                        # kennisbron2 = BNode()
                        # self.g.add((subject, cn.NS_MB["grondslag"], kennisbron2))
                        # self.g.add((kennisbron2, RDFS.label, Literal(trimmed_begrip_bron)))

            # Voorbeelden

            if str(i[get_column_index(df_begrippen, sbm_cn.VOORBEELDEN)]) is not "":
                self.g.add(
                    (
                        subject,
                        SKOS.example,
                        Literal(i[get_column_index(df_begrippen, sbm_cn.VOORBEELDEN)]),
                    )
                )

            if sbm_cn.VOORKEURSTERM_SECUNDAIRE_TAAL in df_begrippen.columns:
                if str(i[get_column_index(df_begrippen, sbm_cn.VOORKEURSTERM_SECUNDAIRE_TAAL)]) is not "":
                    self.g.add(
                        (
                            subject,
                            SKOS.prefLabel,
                            Literal(
                                i[
                                    get_column_index(
                                        df_begrippen, sbm_cn.VOORKEURSTERM_SECUNDAIRE_TAAL
                                    )
                                ],
                                lang=self.sec_taal_model_lower,
                            ),
                        )
                    )

            if sbm_cn.DEFINITIE_SECUNDAIRE_TAAL in df_begrippen.columns:
                if str(i[get_column_index(df_begrippen, sbm_cn.DEFINITIE_SECUNDAIRE_TAAL)]) is not "":
                    self.g.add(
                        (
                            subject,
                            SKOS.definition,
                            Literal(
                                i[
                                    get_column_index(
                                        df_begrippen, sbm_cn.DEFINITIE_SECUNDAIRE_TAAL
                                    )
                                ],
                                lang=self.sec_taal_model_lower,
                            ),
                        )
                    )

    def process_termvormen(self):
        """Function that handles the sheet "Termvormen" """
        df = read_sheet_as_dataframe(
            xls_file=self.input_xlsx,
            sheet_name=sbm_cn.TERMVORMEN,
            rename_columns=True,
            column_mapping=sbm_cn.TERMVORMEN_COLUMN_MAPPING,
        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
        capitalize_df(df, capitalize_columns=True)
        df_begrippen = read_sheet_as_dataframe(
                        xls_file=self.input_xlsx,
                        sheet_name=sbm_cn.BEGRIPPEN,
                        rename_columns=True,
                        column_mapping=sbm_cn.BEGRIPPEN_COLUMN_MAPPING,
                        ).applymap(lambda x: x.strip().replace('  ', ' ') if isinstance(x, str) else x)
        capitalize_df(df_begrippen, capitalize_columns=True)




        for i in df.itertuples():
            enkelvoud_uri = create_uri(f"term/{str(i[get_column_index(df, sbm_cn.ENKELVOUD)]).lower()}")
            meervoud_uri = create_uri(f"term/{str(i[get_column_index(df, sbm_cn.MEERVOUD)]).lower()}")
            afkorting_uri = create_uri(f"term/{str(i[get_column_index(df, sbm_cn.AFKORTING)]).lower()}")

            # Enkelvoud
            if str(i[get_column_index(df, sbm_cn.ENKELVOUD)]) is not "":
                self.g.add(
                    (
                        enkelvoud_uri,
                        sbm_cn.NS_SKOSXL.literalForm,
                        Literal(str(i[get_column_index(df, sbm_cn.ENKELVOUD)])),
                    )
                )
                self.g.add((enkelvoud_uri, RDF.type, sbm_cn.NS_SKOSXL.Label))
                self.g.add((enkelvoud_uri, sbm_cn.NS_SM.meervoud, meervoud_uri))
                self.g.add((enkelvoud_uri, sbm_cn.NS_SKOSXL.hiddenLabel, meervoud_uri))

            # Meervoud
            if str(i[get_column_index(df, sbm_cn.MEERVOUD)]) is not "":
                self.g.add(
                    (
                        meervoud_uri,
                        sbm_cn.NS_SKOSXL.literalForm,
                        Literal(str(i[get_column_index(df, sbm_cn.MEERVOUD)])),
                    )
                )
                self.g.add((meervoud_uri, RDF.type, sbm_cn.NS_SKOSXL.Label))
                self.g.add((meervoud_uri, sbm_cn.NS_SM.enkelvoud, enkelvoud_uri))


                if self.naam_kdgb is not None:
                    print(
                        f"{self.code_kb}/{self.naam_kdgb}/{i[get_column_index(df, sbm_cn.VOORKEURSTERM)].lower()}")
                    subject = create_uri(
                        f"{self.code_kb}/{self.naam_kdgb}/{i[get_column_index(df, sbm_cn.VOORKEURSTERM)].lower()}")
                else:
                    print(f"{self.code_kb}/{i[get_column_index(df, sbm_cn.VOORKEURSTERM)].lower()}")
                    subject = create_uri(
                        f"{self.code_kb}/{self.naam_kb.lower()}/{i[get_column_index(df, sbm_cn.VOORKEURSTERM)].lower()}")
                print("hiddenlabel")
                if i[get_column_index(df, sbm_cn.VOORKEURSTERM)] in df_begrippen[sbm_cn.VOORKEURSTERM].values:
                    print("voeg hiddenlabel toe")
                    print(f"{self.code_kb}/{i[get_column_index(df, sbm_cn.VOORKEURSTERM)].lower()}")
                    self.g.add((subject, SKOS.hiddenLabel, Literal(str(i[get_column_index(df, sbm_cn.MEERVOUD)]), lang= self.taal_model.lower())))

                ##toevoegen hiddenlabel bij begrip
#                self.g.add((suject, SKOS.hiddenLabel, Literal(str(i[get_column_index(df, cn.MEERVOUD)]))))


            # Afkorting
            if str(i[get_column_index(df, sbm_cn.AFKORTING)]) is not "":
                self.g.add(
                    (
                        afkorting_uri,
                        sbm_cn.NS_SKOSXL.literalForm,
                        Literal(str(i[get_column_index(df, sbm_cn.AFKORTING)])),
                    )
                )
                self.g.add((afkorting_uri, RDF.type, sbm_cn.NS_SKOSXL.Label))
                self.g.add((afkorting_uri, sbm_cn.NS_SM.afkorting, enkelvoud_uri))
                self.g.add((afkorting_uri, sbm_cn.NS_SKOSXL.hiddenLabel, enkelvoud_uri))