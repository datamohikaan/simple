select model_uuid, json_group_array
(json_object('uuid', uuid, 'oid', oid,   'code', code, 'name', name, 'datatype', datatype, 'length', length , 'description', description)) as domains_json
from '%MDE_SOURCE_PATH%/domain_complete.parquet'
group by model_uuid