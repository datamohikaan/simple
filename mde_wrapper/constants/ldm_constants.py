from utils.constants import *

######################################################################################################################
# LDM Model #
######################################################################################################################
VERSION = "Version"
OBJECT_ID = "ObjectID"
NAME = "Name"
ANNOTATION = "Annotation"
DESCRIPTION = "Description"
MODIFICATION_DATE = "ModificationDate"
REF_ENT_ID = "RefEntID"
ID = "Id"

ENTITY2TOENTITY1ROLE = "Entity2ToEntity1Role"
ENTITY1TOENTITY2ROLE = "Entity1ToEntity2Role"
ENTITY1TOENTITY2ROLECARDINALITY = "Entity1ToEntity2RoleCardinality"
ENTITY2TOENTITY1ROLECARDINALITY = "Entity2ToEntity1RoleCardinality"
MODEL_PROPERTY_SET = [
    OBJECT_ID,
    VERSION,
    NAME,
    "Code",
    ANNOTATION,
    "RepositoryFilename",
    "CreationDate",
    "Creator",
    MODIFICATION_DATE,
    "Modifier",
    DESCRIPTION,
    "Comments",
]
ENTITY_PROPERTY_SET = [
    OBJECT_ID,
    NAME,
    "Code",
    "CreationDate",
    "Creator",
    MODIFICATION_DATE,
    "Modifier",
    DESCRIPTION,
]
ATTRIBUTE_PROPERTY_SET = [
    OBJECT_ID,
    NAME,
    "Code",
    "CreationDate",
    "Creator",
    MODIFICATION_DATE,
    "Modifier",
    "DataType",
    "Length",
    DESCRIPTION,
]
INDEX_PROPERTY_SET = [
    OBJECT_ID,
    NAME,
    "Code",
    "CreationDate",
    "Creator",
    MODIFICATION_DATE,
    "Modifier",
]
IDXATTRIBUTE_PROPERTY_SET = [
    OBJECT_ID,
    "CreationDate",
    "Creator",
    MODIFICATION_DATE,
    "Modifier",
]
RELATIONSHIP_PROPERTY_SET = [
    OBJECT_ID,
    NAME,
    "Code",
    "CreationDate",
    "Creator",
    MODIFICATION_DATE,
    "Modifier",
    "Entity2ToEntity1Role",
    "Entity1ToEntity2Role",
    "Entity1ToEntity2RoleCardinality",
    "Entity2ToEntity1RoleCardinality",
]
RELENTITY_PROPERTY_SET = [OBJECT_ID, NAME, "Code", MODIFICATION_DATE]
DOMAIN_PROPERTY_SET = [OBJECT_ID, NAME, "Code", MODIFICATION_DATE]
SHORTCUT_PROPERTY_SET = [OBJECT_ID, NAME, "Code", "TargetID", MODIFICATION_DATE]

PROPERTY_PATTERN = r"(\d+(?:\.\d+){2})"

