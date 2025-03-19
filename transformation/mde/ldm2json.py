import os
import duckdb


def read_from_file(file_name: str, source_path: str) -> str:
    with open(file=file_name, mode="r") as f:
        return f.read().replace("%MDE_SOURCE_PATH%", source_path)


# funtie om None waarden uit de dictionary te filteren
def delete_none(_dict):
    """Delete None values recursively from all of the dictionaries, tuples, lists, sets"""
    if isinstance(_dict, dict):
        for key, value in list(_dict.items()):
            if isinstance(value, (list, dict, tuple, set)):
                _dict[key] = delete_none(value)
            elif value is None or key is None:
                del _dict[key]
    elif isinstance(_dict, (list, set, tuple)):
        _dict = type(_dict)(delete_none(item) for item in _dict if item is not None)

    return _dict


def generate_json(source_path: str, target_file: str, debugging=False):
    # query path is relatief aan deze file
    query_path: str = f"{os.path.dirname(__file__)}/queries"

    domains_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/domain_json.sql", source_path=source_path
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from domain_json) to '{source_path}/domain_json.json'"
        )
    # maak het attributes json blok voor een entity
    attributes_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/entity_attributes_json.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from attributes_json) to '{source_path}/attributes_json.json'"
        )

    # maak het entity json , filter de context entities uit
    entity_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/entity_json.sql", source_path=source_path
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from entity_json) to '{source_path}/entity_json.json'"
        )
    # combineer entity en attribute json
    entity_attributes_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/entity_with_attributes_json.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from entity_attributes_json) to '{source_path}/entity_attributes_json.json'"
        )

    # maak namespaces json aan
    namespaces_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/namespaces_json.sql", source_path=source_path
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from namespaces_json) to '{source_path}/namespaces_json.json'"
        )
    # combineer identifier attributes json
    identifiers_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/identifiers_json.sql", source_path=source_path
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from identifiers_json) to '{source_path}/identifiers_json.json'"
        )
    # Maak mappings aan incl attribute mappings
    mappings_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/mappings_with_attribute_mappings_json.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from mappings_json) to '{source_path}/mappings_json.json'"
        )
    # Joins en join conditions
    joins_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/mappings_source_joins_json.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(f"copy(select * from joins_json) to '{source_path}/joins_json.json'")
    # Voeg samen en aggregeer naar entiteitniveau
    mappings_for_entity_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/mappings_for_entity_json.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from mappings_for_entity_json) to '{source_path}/mappings_for_entity_json.json'"
        )
    # combineer entity en identifiers json
    entities_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/entity_with_mappings_and_identifiers.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from entities_json) to '{source_path}/entities_json.json'"
        )
    # maak relationships aan incl joins
    relationships_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/relationship_json.sql", source_path=source_path
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from relationships_json) to '{source_path}/relationship_json.json'"
        )
    # Maak domains aan

    # maak inheritance relationships
    model_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/model_json.sql", source_path=source_path
        )
    )
    # model_json = duckdb.sql(read_from_file(file_name=f"{query_path}/model_json_orig.sql", source_path=source_path))
    if debugging:
        duckdb.sql(f"copy(select * from model_json) to '{source_path}/model_json.json'")
    inheritance_relationships_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/inheritance_relationships_json.sql",
            source_path=source_path,
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from inheritance_relationships_json) to '{source_path}/inheritance_relationships_json.json'"
        )
    # groepeer de inheritance links op inheritance in een json array
    # maak inheritances json aan
    inheritances_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/inheritances_json.sql", source_path=source_path
        )
    )
    if debugging:
        duckdb.sql(
            f"copy(select * from inheritances_json) to '{source_path}/inheritances_json.json'"
        )
    # combineer de top level json objecten tot een model json tbv json export

    export_json = duckdb.sql(
        read_from_file(
            file_name=f"{query_path}/export_json.sql", source_path=source_path
        )
    )
    # export export_json naar bestand
    duckdb.sql(f"copy(select * from export_json) to '{source_path}/ldm.json'")
    # jsonlint /tmp/tmpw0c9czm0/output/ldm.json

    # open model (json)
    # model_dict = {}
    # with open(f'{source_path}/ldm.json', 'r') as json_file:
    #   model_dict = json.load(json_file)

    # schijf weg als model yaml bestand
    # with open(f'{target_file}', 'w') as yaml_file:
    #  yaml.dump(model_dict, yaml_file, sort_keys=False, default_flow_style=False, allow_unicode=True, width=500)

    # verwijder alle None's uit de dictionairy
    # model_dict_no_none =


# delete_none(model_dict)
