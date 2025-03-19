select entity_attributes_json.model_uuid
     , json_merge_patch(mappings_for_entity_json, identifiers_json,entity_attributes_json) as entities_json
  from entity_attributes_json
  left
  join identifiers_json using (entity_uuid)
  left join mappings_for_entity_json using (entity_uuid)
 
