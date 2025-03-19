import pandas as pd
import numpy as np
import psycopg2
import requests
from icecream import ic

import frontend.ep.config as config
from utils.constants import (
    POSTGRES_MAPPING,
    PATH,
    MAPPING,
    ADDITIONAL_COLUMNS,
    INSERT_QUERY, UPDATE_QUERY,
)
from datetime import datetime
import os
from rdflib import Graph
from utils import constants as cn


class KennisgebiedenregisterCreator:
    def __init__(self):
        self.TURTLE_ROOT_DIR = (
                os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
                + os.sep
                + "utils"
                + os.sep
                + "fuseki_turtles"
        )
        self.g = Graph()
        # self.g.parse(
        #     self.TURTLE_ROOT_DIR + os.sep + "kennisgebiedenregister.ttl",
        #     format="turtle",
        # )
        kennisgebiedenregister_turtle = requests.get(
            config.DATASTORE_ENDPOINT + "?graph=urn:name:kennisgebiedenregister", verify=False).text
        self.g.parse(data=kennisgebiedenregister_turtle, format="turtle")
        triples = []
        for subj, pred, obj in self.g:
            triples.append(
                {
                    # "subject": subj.encode("utf-8"),
                    # "predicate": pred.encode("utf-8"),
                    # "object": obj.encode("utf-8"),
                    "subject": subj,
                    "predicate": pred,
                    "object": obj,
                }
            )
        self.df = pd.DataFrame(triples)

    def create_databaseschema(self):
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        for kennisgebiedenregister_table in cn.POSTGRES_MAPPING:
            db_cursor.execute(
                cn.POSTGRES_MAPPING[kennisgebiedenregister_table][cn.CREATE_QUERY]
            )
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

    def add_table_kennisgebiedenregister(self, table_name: str):
        """This function fills a specific table from the Kennisgebiedenregister
        :param:
            table_name: the table name that needs to be added to the PostgreSQL database. The table name serves as a key for database fill.
        """
        table_params = POSTGRES_MAPPING[table_name]

        if table_name == "kennisgebieden" or table_name == "kennisdeelgebieden":
            kennisgebieden_or_kennisdeelgebieden = self.df[
                self.df["subject"]
                # .apply(lambda x: x.decode("utf-8"))
                .str.contains(table_params[PATH])
                & self.df["object"]
                # .apply(lambda x: x.decode("utf-8"))
                .str.contains(table_params[PATH].capitalize())
                ]["subject"]
            table_df = (
                (
                    self.df[
                        self.df["subject"]
                        # .apply(lambda x: x.decode("utf-8"))
                        .str.contains(table_params[PATH])
                    ]
                        .groupby(["subject", "predicate"])["object"]
                        .apply(lambda x: ",".join(x))
                        .reset_index()
                        .pivot(index="subject", columns="predicate", values="object")
                        .replace(np.nan, "")
                )
                .loc[kennisgebieden_or_kennisdeelgebieden]
                .reset_index()
            )
        else:
            table_df = (
                self.df[
                    self.df["subject"]
                    # .apply(lambda x: x.decode("utf-8"))
                    .str.contains(table_params[PATH])]
                .groupby(["subject", "predicate"])["object"]
                    # .apply(lambda x: ",".join(x.str.decode("utf-8")))
                    .apply(lambda x: ",".join(x))
                    .reset_index()
                    .pivot(index="subject", columns="predicate", values="object")
                    .reset_index()
                    .replace(np.nan, "")
                # .applymap(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)
            )
        table_df.columns = [col.strip() for col in table_df.columns]

        # Writing to database
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        for i in range(len(table_df)):
            table_items = [
                table_df[table_params[MAPPING][key.strip()]][i]
                for key in table_params[MAPPING].keys()
            ]
            if table_params[ADDITIONAL_COLUMNS] is not None:
                table_items += table_params[ADDITIONAL_COLUMNS]
            db_cursor.execute(
                table_params[INSERT_QUERY],
                (
                    table_df["subject"][i],
                    *table_items,
                    datetime.now(),
                ),
            )
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

    def fill_database(self):
        try:
            self.create_databaseschema()
            for table_name in POSTGRES_MAPPING.keys():
                ic(table_name)
                self.add_table_kennisgebiedenregister(table_name=table_name)
            print("Kennisgebiedenregister tabellen zijn gevuld!", flush=True)
        except ():
            print("Vullen van het Kennisgebiedenregister is mislukt.", flush=True)

    def edit_table(self, table_name, uri, *args):
        """
        params:
        uri: is usually uri, but in the case of kennisdeelgebieden its called file_id
        """
        table_params = POSTGRES_MAPPING[table_name]

        # Writing to database
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute(
                table_params[UPDATE_QUERY],
                (
                    *args,
                    datetime.now(),
                    uri
                )
            )
        except IndexError as e:
            print('IndexError means you have inputted one too few arguments', flush=True)
            db_connection.commit()
            db_cursor.close()
            db_connection.close()
            raise e

        except TypeError as e:
            print('TypeError means you probably have inputted one too many arguments', flush=True)
            db_connection.commit()
            db_cursor.close()
            db_connection.close()
            raise e

        db_connection.commit()
        db_cursor.close()
        db_connection.close()


class ModeltoetsingsverzoekenCreator:
    def __init__(self):
        self.TURTLE_ROOT_DIR = (
                os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
                + os.sep
                + "utils"
                + os.sep
                + "fuseki_turtles"
        )
        self.g = Graph()
        # self.g.parse(
        #     self.TURTLE_ROOT_DIR + os.sep + "toetsingslogboek.ttl",
        #     format="turtle",
        # )
        toetsingslogboek_turtle = requests.get(
            config.DATASTORE_ENDPOINT + "?graph=urn:name:toetsingslogboek", verify=False).text

        self.g.parse(data=toetsingslogboek_turtle, format="turtle")
        triples = []
        for subj, pred, obj in self.g:
            triples.append(
                {
                    # "subject": subj.encode("utf-8"),
                    # "predicate": pred.encode("utf-8"),
                    # "object": obj.encode("utf-8"),
                    "subject": subj,
                    "predicate": pred,
                    "object": obj,
                }
            )
        self.df = pd.DataFrame(triples)

    def create_databaseschema(self):
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            cn.POSTGRES_MAPPING['modelverzoeken'][cn.CREATE_QUERY]
        )
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

    def add_table_kennisgebiedenregister(self, table_name: str):
        """This function fills a specific table from the Kennisgebiedenregister
        :param:
            table_name: the table name that needs to be added to the PostgreSQL database. The table name serves as a key for database fill.
        """
        table_params = POSTGRES_MAPPING[table_name]

        if table_name == "kennisgebieden" or table_name == "kennisdeelgebieden":
            kennisgebieden_or_kennisdeelgebieden = \
                self.df[
                    self.df["subject"]
                    # .apply(lambda x: x.decode("utf-8"))
                    .str.contains(table_params[PATH]) & self.df["object"]
                # .apply(lambda x: x.decode("utf-8"))
                    .str.contains(table_params[PATH].capitalize())
                ]["subject"]
            table_df = (
                (
                    self.df[
                        self.df["subject"]
                        # .apply(lambda x: x.decode("utf-8"))
                        .str.contains(table_params[PATH])]
                    .groupby(["subject", "predicate"])["object"]
                        .apply(lambda x: ",".join(x))
                        .reset_index()
                        .pivot(index="subject", columns="predicate", values="object")
                        .replace(np.nan, "")
                )
                .loc[kennisgebieden_or_kennisdeelgebieden]
                .reset_index()
            )
        else:
            table_df = (
                self.df[
                    self.df["subject"]
                    # .apply(lambda x: x.decode("utf-8"))
                    .str.contains(table_params[PATH])]
                .groupby(["subject", "predicate"])["object"]
                    # .apply(lambda x: ",".join(x.str.decode("utf-8")))
                    .apply(lambda x: ",".join(x))
                    .reset_index()
                    .pivot(index="subject", columns="predicate", values="object")
                    .reset_index()
                    .replace(np.nan, "")
                # .applymap(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)
            )
        table_df.columns = [col.strip() for col in table_df.columns]

        # Writing to database
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        for i in range(len(table_df)):
            table_items = []
            for key in table_params[MAPPING].keys():
                value = table_df[table_params[MAPPING][key.strip()]][i]
                if key == "bd_user":
                    value = value.split('/')[-1]
                table_items.append(value)

            if table_params[ADDITIONAL_COLUMNS] is not None:
                table_items += table_params[ADDITIONAL_COLUMNS]
            db_cursor.execute(
                table_params[INSERT_QUERY],
                (
                    table_df["subject"][i],
                    *table_items[1:],
                    datetime.now(),
                ),
            )
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

    def fill_database(self):
        try:
            self.create_databaseschema()

            self.add_table_kennisgebiedenregister(table_name='modelverzoeken')
            print("Modelverzoek tabellen zijn gevuld!", flush=True)
        except ():
            print("Vullen van Modelverzoeken is mislukt.", flush=True)

    def edit_table(self, table_name, uri, *args):
        """
        params:
        uri: is usually uri, but in the case of kennisdeelgebieden its called file_id
        """
        table_params = POSTGRES_MAPPING[table_name]

        # Writing to database
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        try:
            db_cursor.execute(
                table_params[UPDATE_QUERY],
                (
                    *args,
                    datetime.now(),
                    uri
                )
            )
        except IndexError as e:
            print('IndexError means you have inputted one too few arguments', flush=True)
            db_connection.commit()
            db_cursor.close()
            db_connection.close()
            raise e

        except TypeError as e:
            print('TypeError means you probably have inputted one too many arguments', flush=True)
            db_connection.commit()
            db_cursor.close()
            db_connection.close()
            raise e

        db_connection.commit()
        db_cursor.close()
        db_connection.close()


# TODO: ONDERSTAANDE CODE RUNNEN VOOR LOKAAL VULLEN VAN POSTGRESQL
if __name__ == "__main__":
    #k = KennisgebiedenregisterCreator()
    #k.fill_database()

    m = ModeltoetsingsverzoekenCreator()
    m.fill_database()

    #k.edit_table('domeinen', 'http://modellenbibliotheek.belastingdienst.nl/id/domein/Auto', 'naam2222', 'ketaketen', 'banan')
    #k.edit_table('kennisgebieden', 'http://modellenbibliotheek.belastingdienst.nl/id/kennisgebied/ITVoorIV', 'naam', 'code', 'domein', 'type_kennisgebied', 'status', 'afbakeningstype', 'verantwoordelijk_organisatieonderdeel', 'primaire_datasteward', 'aanvullende_informatie')
