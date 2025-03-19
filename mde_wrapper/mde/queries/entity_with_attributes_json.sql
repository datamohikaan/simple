select model_uuid
     , entity_uuid
     , json_merge_patch(attributes_json, entity_json) as entity_attributes_json
  from entity_json
  join attributes_json using(entity_uuid)