select model_uuid as model_uuid
     , json_group_array(json_object('alias', name,'uri', mde_namespace_uri)) as namespaces_json  
from '%MDE_SOURCE_PATH%/mde_namespace.parquet'
Group by model_uuid
 