import os

from lxml import etree
import pyarrow as pa
import pyarrow.parquet as pq
import yaml
import logging
import datetime
import uuid

from striprtf.striprtf import rtf_to_text


def extract(
    sourcefile,
    modelfile,
    targetpath,
    job_id: str = str(uuid.uuid4().hex),
    current_timestamp: datetime = datetime.datetime.now(),
):
    """
    Extract entities defined in <modelfile> from an XML <sourcefile> and output to parquet file(s) in <targetpath>.
    <job_id> and <current_timestamp> are used to fill the fields sed_run_id en sed_created. If not provided a default is used.
    """

    # declare
    files = []

    logging.info(f"Extracting {sourcefile} using model {modelfile} to {targetpath}")
    # read xml
    xml_fobj = open(sourcefile, "r")
    doc = etree.parse(xml_fobj)
    root = doc.getroot()

    # read yml
    print(type(modelfile))
    modelfile2 = modelfile.replace('\n', '').replace("\\\\", "__").rstrip()
    print(f"modelfile = {modelfile}", flush=True)
    print(f"modelfile2 = {modelfile2}", flush=True)
    print(os.path.exists(modelfile))

    yml_fobj = open(modelfile, "r")
    yml_dict = yaml.safe_load(yml_fobj)
    nsmap = {}
    # build namespace mapping
    for ns in yml_dict["model"]["namespaces"]:
        logging.debug("Adding namespace alias %s with uri %s", ns["alias"], ns["uri"])
        nsmap[ns["alias"]] = ns["uri"]

    # loop through all entities as specified in the yaml
    for entity in yml_dict["model"]["entities"]:
        logging.debug(
            "Entity '%s' with %s attributes (%s)"
            % (
                entity["code"],
                len(entity["attributes"]),
                ", ".join(i["code"] for i in entity["attributes"]),
            )
        )

        # loop through all attributes of the entity as specified in the yaml
        # and use the specified path to get the corresponding value
        # set the schema of all attributes to string!
        attributes = {}
        schema = []
        for attribute in entity["attributes"]:
            attributes[attribute["code"]] = []
            schema.append((attribute["code"], pa.string()))
        for entity_element in root.xpath(entity["path"], namespaces=nsmap):
            for attribute in entity["attributes"]:
                node = entity_element.xpath(attribute["path"], namespaces=nsmap)
                if node is not None and len(node) > 0:
                    if isinstance(node[0], etree._Element):
                        if len(node) == 1:
                            # List with one Element: text of the element and strip rtf
                            #attributes[attribute["code"]].append(node[0].text)
                            attributes[attribute["code"]].append(rtf_to_text(node[0].text).strip())
                        else:
                            # List with more Elements: comma separated string
                            text_list = [el.text for el in node]
                            attributes[attribute["code"]].append(",".join(text_list))
                            # TODO: Type as array in Parquet
                    elif isinstance(node, etree._ElementUnicodeResult):
                        # String (bijv. resultaat van XPath)
                        attributes[attribute["code"]].append(node)
                    else:
                        # Attribute
                        attributes[attribute["code"]].append(node[0])
                else:
                    attributes[attribute["code"]].append(None)

        # write to parquet
        filename = targetpath + "/" + entity["code"] + ".parquet"
        logging.info(
            "Writing '%s' with %s rows and %s columns"
            % (filename, len(attributes[attribute["code"]]), len(entity["attributes"]))
        )
        pa_schema = pa.schema(schema)
        pa_table = pa.Table.from_pydict(attributes, schema=pa_schema)

        # Add job id as run id to the table
        pa_table = pa_table.append_column(
            "sed_run_id", pa.array([job_id] * len(pa_table), pa.string())
        )
        # Add current timestamp to the table
        pa_table = pa_table.append_column(
            "sed_created",
            pa.array([current_timestamp] * len(pa_table), pa.timestamp("us")),
        )
        pq.write_table(pa_table, filename)
        files.append(filename)

    return files
