import os
import re
import uuid
import shutil
import json

from datetime import datetime
from timeit import default_timer as timer

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS, SKOS, XSD

from striprtf.striprtf import rtf_to_text

import mde_wrapper.constants.ldm_constants as ldm_cn
from utils.utils import create_uri, MeldingManager

from mde_wrapper.mde import xml_extractor, ldm2json
from mde_wrapper.mde.pd_ldm_preprocessor import PowerDesignerLDMPreprocessor
from mde_wrapper.validators.ldm_validator import LDMValidator


class LDMTransformer:
    def __init__(self, file_dir: str, file: str, file_name: str, model_type: str):
        self.melding_manager = MeldingManager()
        self.file_dir = file_dir
        self.file = file
        self.file_name = file_name
        self.file_path = file_dir + file
        self.file_name_turtle = self.file_name + ldm_cn.TURTLE_EXTENSION
        self.model_type = model_type

        self.yaml = None
        self.json_data = None
        self.g = Graph()
        self.versie_num_model = None
        self.model_uri = None
        self.naam_model = None
        self.logisch_model = None
        self.versie_datum_model = None

        self.naam_kb = None
        self.naam_kdgb = None
        self.code_kb = None
        self.code_kdgb = None
        self.kb_uri = None

        self.administratie = None
        self.interactie = None
        self.proces = None

        self.administratie_uri = None
        self.interactie_uri = None
        self.proces_uri = None

        # TODO: Beneden zijn de MDE variabelen - refactor de namen als de transformatie compleet is
        # MDE
        self.mde_model_uuid = None
        self.mde_model_code = None
        self.mde_model_name = None
        self.mde_repositoryfilename = None
        self.mde_modificationdate = None
        self.mde_versie_datum_model = None
        self.mde_model_version = None
        self.mde_model_file_name = None

    def generate_json(self):
        """Generates the json files needed for the mde_wrapper to turtle. Code is obtained from the MDE."""
        #MDE_ROOT_DIR = os.path.join(os.getcwd(), "mde_wrapper", "mde")
        dubbel_uit_directory = ".." + os.sep + ".."
        GIT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), dubbel_uit_directory))
        MDE_ROOT_DIR = os.path.join(GIT_DIR, "mde_wrapper", "mde")
        MDE_OUTPUT_DIR = os.path.join(self.file_dir, "output")
        if os.path.isdir(MDE_OUTPUT_DIR):
            shutil.rmtree(MDE_OUTPUT_DIR)

        # Recreate output directory
        os.mkdir(MDE_OUTPUT_DIR)
        # Run preprocessor here we go, hope the run will be okay
        preprocessor: PowerDesignerLDMPreprocessor = PowerDesignerLDMPreprocessor()
        preprocessor.preprocess_ldm(self.file_path)

        # Runs dze extractor
        xml_extractor.extract(
            self.file_path.replace(".ldm", "_preprocessed.ldm"),
            os.path.join(MDE_ROOT_DIR, "mde_utils" + os.sep + "powerdesigner-extractor-config.yml"),
            MDE_OUTPUT_DIR,
        )

        # Run JSON convertor
        # print("into ldm2json")
        ldm2json.generate_json(
            source_path=MDE_OUTPUT_DIR,
            target_file=self.file_path.replace(".ldm", ".yml"),
        )  # target file wordt niet gebruikt bij json productie
        with open(f"{MDE_OUTPUT_DIR}/ldm.json", "r") as json_file:
            self.json = json.load(json_file)

        # print(self.json)  # TODO: Verwijder na refactoring
        # self.mde_model_uuid = self.json['model']['uuid']
        # self.mde_model_version = self.json['model']['version']
        # self.mde_model_file_name = self.mde_model_uuid + self.mde_model_version
        # hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(self.mde_model_file_name))
        # self.model_uri = URIRef(f'urn:uuid:{hash_uuid}')

    def validate_powerdesigner_model(self, input_json, input_file_dir, input_xml_file):
        # Run validator
        """Validates the LDM https://jira.belastingdienst.nl/browse/GVG-6055
         :return:.
        """
        ldm_validator = LDMValidator(input_json, input_file_dir, input_xml_file)
        # 🙏🙏🙏👇
        ldm_validator.validate_model_name(input_json, input_file_dir, input_xml_file, model_type=self.model_type)
        ldm_validator.validate_argument_0(input_json, input_file_dir,
                                          input_xml_file)  # validator validate_argument_0 /var/folders/bf/rf8kmqkd2s3d1jkzr03_9ggw0000gr/T/tmprdtdrww6/

        self.melding_manager += ldm_validator.melding_manager

        self.code_kb = ldm_validator.code_kb
        self.naam_kb = ldm_validator.naam_kb
        self.naam_kdgb = ldm_validator.naam_kdgb
        self.kb_uri = ldm_validator.kb_uri

        self.administratie = ldm_validator.administratie
        self.administratie_uri = ldm_validator.administratie_uri

        self.interactie = ldm_validator.interactie
        self.interactie_uri = ldm_validator.interactie_uri

        self.proces = ldm_validator.proces
        self.proces_uri = ldm_validator.proces_uri


    def process_model(self):
        # In the rest of this document, we will treat “triples” and “quads” equally:
        # we assume that a quad is simply a triple in a named or default graph.
        """Creates the Named graph with the specified namespaces.
        :return: returns the created Named Graph.
        """
        # Obtaining MDE model information
        self.mde_model_uuid = self.json["model"]["uuid"]
        self.mde_model_code = self.json["model"]["code"]
        self.mde_model_name = self.json["model"]["name"]
        self.mde_model_version = self.json["model"]["version"]
        self.mde_repositoryfilename = self.json["model"]["repositoryfilename"]
        self.mde_modificationdate = self.json["model"]["modificationdate"]
        dt_object = datetime.fromtimestamp(int(self.mde_modificationdate))
        self.mde_versie_datum_model = (
            str(dt_object.year) + "-" + str(dt_object.month) + "-" + str(dt_object.day)
        )
        PROPERTY_PATTERN = r"(\d+(?:\.\d+){2})"
        self.mde_model_version = str(
            re.findall(PROPERTY_PATTERN, self.mde_model_version)
        )
        self.mde_model_version = re.sub(r"[\([{})\]]", "", self.mde_model_version)
        self.mde_model_version = re.sub("'", "", self.mde_model_version)
        self.mde_model_file_name = self.mde_model_uuid + self.mde_model_version
        #todo: I dont know how this got here. should it be removed? -suley
        #self.dom_mde_model_file_name = self.mde_model_uuid + self.mde_model_version

        # Adding custom namespaces
        # naam_kb = self.mde_model_name.replace("LDM", "CIM") #replaced for get_vda_model_name
        # self.naam_kb = "lOC"
        self.g.bind("mb", ldm_cn.NS_MB)
        self.g.bind("lgd", ldm_cn.NS_LGD)
        self.g.bind("kgr", ldm_cn.NS_KGR)
        self.g.bind("skos", SKOS)
        self.g.bind("rdfs", RDFS)
        self.g.bind("dcterms", DCTERMS)
        #todo: I dont know how this got here, should it be removed? -suley
        #hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(self.dom_mde_model_file_name))
        #hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(self.mde_model_file_name))
        #self.model_uri = URIRef(f"urn:uuid:{hash_uuid}")
        #model_version_uri = URIRef(sbm_cn.LM_PREFIX + self.mde_model_version)
        self.model_uri = URIRef(f"urn:uuid:{self.mde_model_uuid}")
        hash_uuid = uuid.uuid5(uuid.NAMESPACE_URL, str(self.mde_model_uuid) + str(self.mde_model_version))
        self.model_version_uri = URIRef(f"urn:uuid:{hash_uuid}")

        # Adding gathered  MDE  model information to the graph
        self.g.add((self.model_uri, RDF.type, ldm_cn.NS_LGD.LogischGegevensdefinitieModel))
        #self.g.add((self.model_uri, RDF.type, sbm_cn.NS_MB.Model))
        #self.g.add((self.model_uri, sbm_cn.NS_KGR.kennisgebied, URIRef("http://modellenbibliotheek.belastingdienst.nl/id/kennisgebied/" + naam_kb)))
        #self.g.add((self.model_uri, RDFS.label, Literal(self.logisch_model)))
        # self.g.add((self.model_uri, RDF.type, sbm_cn.NS_LGD.LogischGegevensdefinitieModel))

        self.g.add(
            (
                self.model_uri,
                RDFS.label,
                Literal(self.get_vda_model_name()),
            )
        )

        self.g.add(
            (
                self.model_uri,
                ldm_cn.NS_MB.naam,
                Literal(self.get_vda_model_name()),
            )
        )
        self.g.add(
            (
                self.model_uri,
                ldm_cn.NS_MB.titel,
                Literal(self.get_vda_model_name()),
            )
        )

        self.g.add((self.model_uri, RDF.type, ldm_cn.NS_MB.Model))

        if self.kb_uri:
            self.g.add(
                (
                    self.model_uri,
                    ldm_cn.NS_KGR.kennisgebied,
                    URIRef(
                        (
                            self.kb_uri
                        )
                    ),
                )
            )

        # Adding gathered  MDE  model version information to the graph
        self.g.add((self.model_version_uri, RDF.type, ldm_cn.NS_MB.Modelversie))
        self.g.add((self.model_version_uri, ldm_cn.NS_MB.versieVan, self.model_uri))
        self.g.add(
            (
                self.model_version_uri,
                ldm_cn.NS_MB.versiedatum,
                Literal(self.mde_versie_datum_model, datatype=XSD.date),
            )
        )
        self.g.add(
            (self.model_version_uri, ldm_cn.NS_MB.versienummer, Literal(self.mde_model_version))
        )

        self.g.add((self.model_version_uri, ldm_cn.NS_MB.status, ldm_cn.NS_MB.Finaal))

        self.g.add(
            (
                self.model_version_uri,
                RDFS.label,
                Literal(self.get_vda_model_name()),
            )
        )

        self.g.add(
            (
                self.model_version_uri,
                ldm_cn.NS_MB.naam,
                Literal(self.get_vda_model_name()),
            )
        )
        self.g.add(
            (
                self.model_version_uri,
                ldm_cn.NS_MB.titel,
                Literal(self.get_vda_model_name()),
            )
        )
        self.g.add(
            (
                self.model_version_uri,
                ldm_cn.NS_MB.registratiemoment,
                Literal(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), datatype=XSD.dateTime),
            )
        )

    def process_entities(self):
        """Processes the entity properties and adds it to the Named graph"""
        for entity in self.json["model"]["entities"]:
            entity_subject = create_uri(entity["uuid"])
            self.g.add((entity_subject, RDFS.isDefinedBy, self.model_uri))
            self.g.add((entity_subject, RDF.type, ldm_cn.NS_LGD.Entiteittype))
            self.g.add((entity_subject, RDFS.label, Literal(entity["name"])))
            self.g.add((entity_subject, ldm_cn.NS_LGD.naam, Literal(entity["name"])))
            try:
                self.g.add(
                    (
                        entity_subject,
                        ldm_cn.NS_LGD.gegevensdefinitie,
                        Literal(rtf_to_text(entity["description"]).strip()),
                    )
                )
            except (TypeError, AttributeError, KeyError):
                pass

            for attribute in entity["attributes"]:
                if attribute["inheritedfrom"] == "-":
                    self.g.add(
                        (
                            entity_subject,
                            ldm_cn.NS_LGD.attribuut,
                            create_uri(attribute["uuid"]),
                        )
                    )

    def process_attributes(self):
        """Processes the attribute properties and adds it to the graph"""
        for entity in self.json["model"]["entities"]:
            for attribute in entity["attributes"]:
                attribute_subject = create_uri(attribute["uuid"])
                if attribute["inheritedfrom"] == "-":
                    self.g.add((attribute_subject, RDF.type, ldm_cn.NS_LGD.Attribuuttype))
                    self.g.add(
                        (attribute_subject, RDFS.label, Literal(attribute["name"]))
                    )
                if attribute["attribute_shortcut_oid"] != "-":
                    self.g.add(
                        (
                            attribute_subject,
                            ldm_cn.NS_LGD.attribuutdomein,
                            create_uri(attribute["attribute_shortcut_uuid"]),
                        )
                    )
                if attribute["attribute_domain_oid"] != "-":
                    self.g.add(
                        (
                            attribute_subject,
                            ldm_cn.NS_LGD.attribuutdomein,
                            create_uri(attribute["attribute_domain_uuid"]),
                        )
                    )

                try:
                    self.g.add(
                        (
                            attribute_subject,
                            ldm_cn.NS_LGD.begripsnaam,
                            Literal(rtf_to_text(attribute["description"]).strip()),
                        )
                    )  # eg [EXM.bsn]
                except (TypeError, AttributeError):
                    pass

    def process_attributes_shortcuts_and_domains(self):
        """Processes the domain properties and adds it to the graph"""
        for domains in self.json["model"]["domains"]:
            domain_subject = create_uri(str(domains["uuid"]))
            self.g.add((domain_subject, RDFS.isDefinedBy, self.model_uri))
            self.g.add((domain_subject, RDF.type, ldm_cn.NS_LGD.Attribuutdomein))
            self.g.add((domain_subject, RDFS.label, Literal(domains["code"])))

    def process_relations(self):
        """Processes the relation properties and adds it to the graph"""
        for relationships in self.json["model"]["relationships"]:
            relationship_subject = create_uri(str(relationships["uuid"]))
            self.g.add((relationship_subject, RDF.type, ldm_cn.NS_LGD.Relatietype))
            self.g.add(
                (relationship_subject, RDFS.label, Literal(relationships["name"]))
            )
            self.g.add((relationship_subject, RDFS.isDefinedBy, self.model_uri))
            self.g.add(
                (
                    relationship_subject,
                    ldm_cn.NS_LGD.naarRolnaam,
                    Literal(relationships["entity2_to_entity1_role"]),
                )
            )
            self.g.add(
                (
                    relationship_subject,
                    ldm_cn.NS_LGD.vanrRolnaam,
                    Literal(relationships["entity1_to_entity2_role"]),
                )
            )
            self.g.add(
                (
                    relationship_subject,
                    ldm_cn.NS_LGD.naarCardinaliteit,
                    Literal(relationships["referenced_entity_cardinality"]),
                )
            )
            self.g.add(
                (
                    relationship_subject,
                    ldm_cn.NS_LGD.vanCardinaliteit,
                    Literal(relationships["referencing_entity_cardinality"]),
                )
            )
            self.g.add(
                (
                    relationship_subject,
                    ldm_cn.NS_LGD.naarEntiteittype,
                    create_uri(Literal(relationships["referencing_entity_uuid"])),
                )
            )
            self.g.add(
                (
                    relationship_subject,
                    ldm_cn.NS_LGD.vanEntiteittype,
                    create_uri(Literal(relationships["referenced_entity_uuid"])),
                )
            )

    def get_model_uri(self):
        """Returns the model uri"""
        return self.model_uri

    def get_model_version_uri(self):
        """Returns the model uri"""
        return self.model_version_uri

    def get_file_name_turtle(self):
        """Returns the name of the turtle file"""
        return self.file_name_turtle

    def get_vda_model_name(self):
        match self.model_type:
            case 'LGA':
                return self.administratie
            case 'LGI':
                return self.interactie
            case 'LGP':
                return self.proces
            case 'CIM':
                if self.naam_kdgb:
                    return f"{self.code_kb} {self.naam_kdgb}"
                else:
                    return f"{self.naam_kb}"

    def transform_ldm_xml_to_rdf(self):
        """Main function that processes Parsing From an RDF document to quads
        the LDM input file and transforms it into the Turtle file"""
        start_mde_runner = timer()
        # 🙏
        self.generate_json()
        self.validate_powerdesigner_model(self.json, self.file_dir, self.file)
        # 👇
        # for all models Deze story zetten we voorlopig even "on hold":
        #  Er is nog geen goede beschrijving van wat een LGA/LGP/LGI precies anders maakt dan een CIM, en deze kunnen daardoor nog niet goed
        self.process_model()

        first_three_letters = str(self.mde_model_name[:3])
        print("hoi " + first_three_letters)
        # Een LGG/LGI/LGA kan ingeladen worden via het indienen van een Modelverzoek
        # Bij het transformeren wordt alleen de modelmetadata getransformeerd, niet het model zelf.
        # CIM only
        if first_three_letters == "CIM" or first_three_letters == "LGD":
            # if first_three_letters == "CIM":
            self.process_entities()
            self.process_attributes()
            self.process_attributes_shortcuts_and_domains()

            if self.json["model"]["relationships"] is not None:
                self.process_relations()

        # 🐍🐢
        self.g.serialize(destination=self.file_dir + self.file_name_turtle)
        f = open(self.file_dir + self.file_name_turtle, "a")
        f.write(f"#Named Graph name: {self.logisch_model}, {self.model_uri}")
        f.close()

        # 🎯
        end_mde_runner = timer()
        elapsed_time = round((end_mde_runner - start_mde_runner), 2)
        print(
            ">>>Measure of the Elapsed Time from mde_runner = "
            + str(elapsed_time)
            + " seconds<<<"
        )
