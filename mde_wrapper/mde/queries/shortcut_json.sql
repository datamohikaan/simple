select uuid, json_group_array
(json_object('uuid', uuid, 'oid', oid, 'code', code, 'name', name)) as shortcuts_json
from '%MDE_SOURCE_PATH%/shortcut.parquet'
group by model_uuid
