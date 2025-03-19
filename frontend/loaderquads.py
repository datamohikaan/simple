import sys
from datetime import datetime
from timeit import default_timer as timer
import requests
from frontend.ep.config import DATASTORE_ENDPOINT


class LoaderQuads:
    def __init__(self, file_dir: str, file_name: str, uri: str, file_name_turtle: str):
        self.uri = uri
        self.file_dir = file_dir
        self.file_name = file_name
        self.file_name_turtle = file_name_turtle
        #self.file_name_turtle = file_name + ".ttl"
        print("file_name_turtle="+self.file_name_turtle)

    def load_sparql(self):
        start_quadloader = timer()
        endpoint = DATASTORE_ENDPOINT + "?graph=" + self.uri
        print("uri =" + self.uri)
        print("endpoint =" + endpoint)
        # copy the contents of the demo.py file to  a new file called demo1.py
        #API_ROOT_DIR = os.path.join(os.getcwd(),"frontend" ,"static")
        #api_file_name = "turtle.ttl"
        #source_file = self.file_dir + os.sep + self.file_name_turtle
        #target_file = API_ROOT_DIR + os.sep + api_file_name
        #shutil.copyfile(  source_file, target_file  )

        # copy the contents of the the turtle file MDE_OUT_PUT_DIR to static 4quick acces only.
        #FileNotFoundError: [Errno 2] No such file or directory: '/deployment/static/turtle.ttl'
        #API_ROOT_DIR = os.path.join(os.getcwd(), "static")
        #api_file_name = "turtle.ttl"
        #source_file = self.file_dir + os.sep + self.file_name_turtle
        #target_file = API_ROOT_DIR + os.sep + api_file_name
        #shutil.copyfile(source_file, target_file)
        print("file_dir =" + self.file_dir)
        print("file_name_turtle =" + self.file_name_turtle)
        rdfdata = open(self.file_dir + self.file_name_turtle, encoding="utf8").read()
        print(rdfdata[:10])
        headers = {"Content-Type": "text/turtle;charset=utf-8"}
        r = requests.put(
            endpoint, data=rdfdata.encode("utf-8"), headers=headers, verify=False
        )
        print(r)

        end_quadloader = timer()
        elapsed_time = round((end_quadloader - start_quadloader), 2)
        print(
            ">>>Measure of the Elapsed Time from LoaderQuads = "
            + str(elapsed_time)
            + " seconds<<<"
        )

        if r.status_code == 200 or r.status_code == 201:
            self._write_sparql_request_200(
                self.file_dir, self.file_name, self.uri, endpoint
            )
            print("")
            print("---------------------------------------")
            print("")
            print(self.file_dir)
            print(self.file_name_turtle)
            print(r.elapsed)
            print(r.content)
            print(r.url)
            print(r"          /^\         ")
            print(r"         |' '|        ")
            print(r"   /\     |_|     /\  ")
            print(r"   | \___/' `\___/ |  ")
            print(r"    \_/  \___/  \_/   ")
            print(r"     |\__/   \__/|    ")
            print(r"     |/  \___/  \|    ")
            print(r"    ./\__/   \__/\,   ")
            print(r"    | /  \___/  \ |   ")
            print(r"    \/     V     \/   ")
            print("r = requests.put(" + endpoint + ")")
            print(
                ">>>Measure of the Elapsed Time from LoaderQuads = "
                + str(elapsed_time)
                + " seconds<<<"
            )
            print("Your pages are served under:\n")
            _uri = self.uri.replace(":", "%3A")
            # very first draft of everything
            print("# SELECT DISTINCT ?g WHERE {GRAPH ?g{}}")
            print("SELECT *")
            print("WHERE")
            print(" {")
            print("    GRAPH <" + self.uri + "> {")
            print("    # GRAPH ?graph { ")
            print("    ?subject ?predicate ?object")
            print("   }")
            print("}")
            print("")

        if r.status_code > 399:
            print(r"  ___ _ __ _ __ ___  _ __ ")
            print(r" / _ \ '__| '__/ _ \| '__|")
            print(r"|  __/ |  | | | (_) | |   ")
            print(r" \___|_|  |_|  \___/|_|   ")
            print(r.status_code)
            print("                         ")
            print("Woops.something went wrong  r.status_code > 399 ", file=sys.stderr)
        return {

        }

    @staticmethod
    def _write_sparql_request_200(file_dir, file_name, uri, endpoint):
        file_name_request = file_dir + file_name + ".rq"
        now0 = datetime.now()
        dt_string = now0.strftime("%d/%m/%Y %H:%M:%S")
        print("File Name sparql query : ", file_name_request)
        jsonlinter = (
            "jsonlint " + file_dir + "output/ldm.json" + " > ~/Downloads/ldm.json "
        )
        print(jsonlinter)
        f = open(file_name_request, "w+")

        _uri = uri.replace(":", "%3A")
        f.write("# " + file_name_request + " \n")
        f.write("# date and time =" + dt_string + "\n)")
        f.write("#" + file_name_request + "\n")
        f.write("# uri = " + uri + "\n")
        f.write("# SparqlEndpoint= " + endpoint + "\n")
        f.write("###############\n")

        f.write("SELECT * \n")
        f.write("WHERE \n")
        f.write(" {\n")
        f.write("     GRAPH <" + uri + "> {\n")
        f.write("    ?subject ?predicate ?object\n")
        f.write("   }\n")
        f.write("}\n")
        f.write("############ first draft of everything \n")
        f.write("SELECT * \n")
        f.write("WHERE \n")
        f.write(" {\n")
        f.write("    GRAPH ?graph {")
        f.write("\n")
        f.write("    ?subject ?predicate ?object\n")
        f.write("   }\n")
        f.write("}\n")
        f.write("############ very first draft of everything \n")
        f.write("#SELECT DISTINCT ?g WHERE {GRAPH ?g{}}\n")
        f.write("SELECT ?s ?p ?o \n")
        f.write("WHERE \n")
        f.write("{ ?s ?p ?o . } \n")
        f.write("####### Happy sparqling!  ##### \n")
        f.write(r"          /^\         \n")
        f.write(r"         |200|        \n")
        f.write(r"   /\     |_|     /\  \n")
        f.write(r"   | \___/' `\___/ |  \n")
        f.write(r"    \_/  \___/  \_/   \n")
        f.write(r"     |\__/   \__/|    \n")
        f.write(r"     |/  \___/  \|    \n")
        f.write(r"    ./\__/   \__/\,   \n")
        f.write(r"    | /  \___/  \ |   \n")
        f.write(r"    \/ 200 V 201 \/   \n")
        f.write("r = requests.put(" + endpoint + "\n")
        f.write("Your pages are served under:\n")
        _uri = uri.replace(":", "%3A")
        f.write("Happy spARQl-ing . ")
        f.close()
