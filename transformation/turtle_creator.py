import sys
import os.path
import pandas as pd
import uuid
from mde_wrapper.transformers.sbm_transformer import SBMTransformer
from mde_wrapper.transformers.trt_transformer import TRTTransformer
from mde_wrapper.transformers.ldm_transformer import LDMTransformer
from mde_wrapper.validators.sbm_validator import SBMValidator

from utils.utils import MeldingManager

from rdflib import Graph
from os import path
from frontend.loaderquads import LoaderQuads


class TurtleCreator:
    def __init__(self, gitlab_changed_files, model_type: str):
        self.melding_manager = MeldingManager()
        self.gitlab_changed_files = gitlab_changed_files
        #This method returns the path from the system's root directory.
        self.rootdir = os.getcwd()

        self.file = None
        self.file_dir = None
        self.file_name = None
        self.file_extension = None
        self.file_name_turtle = None
        self.uri = None
        self.yml = None
        self.vda_model_name = None
        self.model_type = model_type

    def create_turtle(self):
        for idx, arg in enumerate(self.gitlab_changed_files[0:], start=0):
            print("Argument #{} is {}".format(idx, arg))
            raw_filename = arg
            self.set_file_info(raw_filename)

            print("hele pad filedir + file=" + self.file_dir + self.file)
            if path.isfile(self.file_dir + self.file):
                self.print_file_info()
                if self.file_extension == ".ttl":
                    self.handle_turtle_file()
                else:
                    self.handle_non_turtle_file()
                LoaderQuads(
                    self.file_dir, self.file_name, self.uri, self.file_name_turtle
                ).load_sparql()

        print(
            "Number of elements excluding the name of the program:", (len(sys.argv) - 1)
        )

    def set_file_info(self, raw_filename):
        #ic(raw_filename)
        self.file = raw_filename.rsplit(os.sep, 1)[-1]
        relative_path = raw_filename.replace(self.file, "")
        self.file_dir = os.path.join(os.getcwd(), relative_path)
        split_filename_extension = os.path.splitext(self.file)
        self.file_name = split_filename_extension[0]
        #ic(self.file_name)
        self.file_extension = split_filename_extension[1]

    def handle_non_turtle_file(self):
        def handle_sbm():
            required_file_extension_start = ".xls"
            if self.file_extension.startswith(required_file_extension_start):
                print("hoi SM nice to see you again!")
                input_xlsx = pd.ExcelFile(self.file_dir + self.file)

                # Model validation
                sbm_validator = SBMValidator(input_xlsx)
                sbm_validator.validate_model()

                # Model transformation
                sbm_transformer = SBMTransformer(self.file_dir, self.file_name, input_xlsx)
                sbm_transformer.transform_sm_xml_to_rdf()
                self.vda_model_name = sbm_transformer.get_vda_model_name()

                # Obtaining the graph uri and name of the turtle file
                self.uri = sbm_transformer.get_uri()
                self.file_name_turtle = sbm_transformer.get_file_name_turtle()
                print("\nuri = " + self.uri)

            else:
                raise ValueError(
                    f"Het formaat van het aangeleverd bestand ({self.file_extension}) voldoet niet. Alleen een Excel conform het SBM formaat ({required_file_extension_start}*) is toegestaan."
                )

        def handle_ldm():
            required_file_extension = ".ldm"
            if self.file_extension == required_file_extension:
                print("hoi ldm nice to see you again!")
                ldm_transformer = LDMTransformer(self.file_dir, self.file, self.file_name, self.model_type)
                ldm_transformer.transform_ldm_xml_to_rdf()
                self.melding_manager += ldm_transformer.melding_manager
                self.vda_model_name = ldm_transformer.get_vda_model_name()

                # Obtaining the graph uri and name of the turtle file
                # self.uri = ldm_transformer.get_model_uri()
                self.uri = ldm_transformer.get_model_version_uri()
                self.file_name_turtle = ldm_transformer.get_file_name_turtle()
                print("\nuri = " + self.uri)
            else:
                raise ValueError(
                    f"Het formaat van het aangeleverd bestand ({self.file_extension}) voldoet niet. Alleen een Powerdesigner LDM bestand ({required_file_extension}) is toegestaan."
                )

        def handle_trt():
            required_file_extension_start = ".xls"
            if self.file_extension.startswith(required_file_extension_start):
                print("hoi TRT toetsingsrapport nice to see you again!")
                input_xlsx = pd.ExcelFile(self.file_dir + self.file)

                # Model validation
                #trt_validator = TRTValidator(input_xlsx)
                #trt_validator.validate_model()

                # Model transformation
                trt_transformer = TRTTransformer(self.file_dir, self.file_name, input_xlsx)
                trt_transformer.transform_trt_xml_to_rdf()
                #self.vda_model_name = trt_transformer.get_vda_model_name()

                # Obtaining the graph uri and name of the turtle file
                hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(self.file_name))
                self.uri = f"urn:uuid:{hash_uuid}"


                #self.uri = trt_transformer.get_uri()
                self.file_name_turtle = trt_transformer.get_file_name_turtle()
                print("\nuri = " + self.uri)

            else:
                raise ValueError(
                    f"Het formaat van het aangeleverde bestand ({self.file_extension}) voldoet niet. Alleen een Excel conform het TRP  formaat ({required_file_extension_start}*) is toegestaan."
                )

        match self.model_type:
            case "TRT":
                handle_trt()
            case "SBM":
                handle_sbm()
            case "CIM":
                handle_ldm()
            case "LGA":
                handle_ldm()
            case "LGG":
                handle_ldm()
            case "LGI":
                handle_ldm()
            case "LGP":
                handle_ldm()

    def handle_turtle_file(self):
        #kennisgebiedenregister_dir = (
        #    self.root_dir + os.sep + "kennisgebiedenregister" + os.sep
        #)

        kennisgebiedenregister_dir = os.path.join(os.getcwd(), "kennisgebiedenregister")
        self.parse_and_serialize_kennisgebiedenregister(kennisgebiedenregister_dir)
        uri = "urn:name:kennisgebiedenregister"
        print(uri)
        file_name_turtle = "sjebang_kennisgebiedenregister.ttl"
        print("file_name_turtle=" + self.file_dir + file_name_turtle)

    def parse_and_serialize_kennisgebiedenregister(self, kennisgebiedenregister):
        # g1 = Graph()
        # g1.parse(kennisgebiedenregister + "affiliatie.ttl")
        #
        # g2 = Graph()
        # g2.parse(kennisgebiedenregister + "domeinen.ttl")
        #
        # g3 = Graph()
        # g3.parse(kennisgebiedenregister + "kennisdeelgebieden.ttl")
        #
        # g4 = Graph()
        # g4.parse(kennisgebiedenregister + "kennisgebieden.ttl")
        #
        # g5 = Graph()
        # g5.parse(kennisgebiedenregister + "wetgeving.ttl")
        #
        # graph = g1 + g2 + g3 + g4 + g5
        graph = Graph()
        # graph.serialize(kennisgebiedenregister + "sjebang_kennisgebiedenregister.ttl", format="turtle")
        graph.serialize(kennisgebiedenregister, format="turtle")

    def get_yml_data(self):
        return self.yml

    def get_vda_model_name(self):
        return self.vda_model_name

    def print_file_info(self):
        if path.isfile(self.file_dir + self.file):
            print("directory = " + self.file_dir)
            print("file_name = " + self.file_name)
            print("file_extension = " + self.file_extension)
            print("Is it File?" + str(path.isfile(self.file_dir + self.file)))
