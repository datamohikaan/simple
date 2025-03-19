import os
import sys
import traceback

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import warnings
import requests
import psycopg2
import frontend.ep.config as config
import constants as cn

# TODO: old code from Peter commented below, delete if you see this in (pre-)develop or after 31-3-2025
# ###################### CONTAINER PLATFORM ENDPOINTS #####################
# DATASTORE_ENDPOINT = "http://mbk-fuseki:3030/modellenbibliotheek"
# DB_CONFIG = {
#         "dbname": "database1",
#         "user": "user1",
#         "password": "password1",
#         "host": "mbk-postgres",
#         "port": "5432",
# }
# DATASTORE_LOOKUP_ENDPOINT = DATASTORE_ENDPOINT + "/sparql"


class FusekiRestorer:
    def __init__(self):
        self.TURTLE_ROOT_DIR = (
            os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
            + os.sep
            + "utils"
            + os.sep
            + "fuseki_turtles"
        )
        self.fuseki_uris = self.obtain_current_graphs_from_fuseki()
        self.postgres_uris = self.obtain_current_graphs_from_postgres()
        self.missing_uris = list(self.postgres_uris - self.fuseki_uris)

    @staticmethod
    def obtain_current_graphs_from_fuseki():
        graph_uris = []
        all_graphs_query = "SELECT DISTINCT ?g WHERE {GRAPH ?g{}}"
        all_graphs = requests.post(
            config.DATASTORE_LOOKUP_ENDPOINT,
            data={"query": all_graphs_query},
            verify=False,
        ).json()["results"]["bindings"]

        for g in all_graphs:
            graph_uris.append(g["g"]["value"])
        return set(graph_uris)

    @staticmethod
    def obtain_current_graphs_from_postgres():
        graph_uris = []
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()

        query = "SELECT named_graph FROM modelverzoeken WHERE substr(file_extension,1,4) = '.xls';"
        db_cursor.execute(query)
        for named_graph in db_cursor.fetchall():
            graph_uris.append(named_graph)
        return set(graph_uris)

    def write_standard_fuseki_turtles(self):
        for turtle_file in os.listdir(self.TURTLE_ROOT_DIR):
            with open(self.TURTLE_ROOT_DIR + os.sep + turtle_file) as f:
                rdfdata = f.read()

            endpoint = (
                config.DATASTORE_ENDPOINT
                + "?graph=urn:name:"
                + turtle_file.replace(".ttl", "")
            )
            requests.put(
                endpoint,
                data=rdfdata.encode("utf-8"),
                headers=cn.turtle_headers,
                verify=False
            )

    def restore_fuseki(self):
        # obtain turtle from postgres
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()

        # writing to fuseki
        self.write_standard_fuseki_turtles()
        query = f"SELECT binary_data FROM ppModellen WHERE named_graph = %s AND substr(file_extension,1,4) = '.xls';"

        for uri in self.missing_uris:
            values = [uri]
            try:
                db_cursor.execute(query, values)
                db_connection.commit()

                rdfdata = db_cursor.fetchone()[0].tobytes()
                requests.put(
                    config.DATASTORE_ENDPOINT + "?graph=" + uri,
                    data=rdfdata,
                    headers=cn.turtle_headers,
                    verify=False,
                )
                db_cursor.close()
                db_connection.close()
            except Exception as e:
                warnings.warn(f"Failed restoring model: '{uri}' from postgres into fuseki"
                      f"\nERRORMESSAGE: {e}: {''.join(traceback.format_stack())}", category=UserWarning)


def main():
    fuseki_restorer = FusekiRestorer()
    # obtain_current_graphs_from_postgres
    # fuseki_restorer.write_standard_fuseki_turtles()

    print(f" hello hybrid Fuseki:PostgresQL on {CURRENT_DIR} nice to see you again! ")

    # Print Fuseki Report
    print(f"There are {len(fuseki_restorer.fuseki_uris)} named graphs in Fuseki:")
    [print(uri) for uri in fuseki_restorer.fuseki_uris]
    print(
        "----------------------------------------------------------------------------------"
    )

    # Print Postgres Report
    print(f"There are {len(fuseki_restorer.postgres_uris)} named graphs in Postgres:")
    [print(uri) for uri in fuseki_restorer.postgres_uris]
    print(
        "----------------------------------------------------------------------------------"
    )

    # Difference between two databases and restore
    if len(fuseki_restorer.missing_uris) > 0:
        print(f"There are {len(fuseki_restorer.missing_uris)} in postgres not in fuseki: ")
        [print(uri) for uri in fuseki_restorer.missing_uris]

        print(f"Restoring {len(fuseki_restorer.missing_uris)} models from postgres into fuseki.  ")
        fuseki_restorer.restore_fuseki()
    else:
        print("There are no named graphs to restore. Fuseki and Postgres are in sync.")


if __name__ == "__main__":
    warnings.filterwarnings("once")
    main()
