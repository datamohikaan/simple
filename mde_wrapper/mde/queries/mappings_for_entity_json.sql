SELECT  m.entity_uuid,
        json_object('mappings', json_group_array(json_merge_patch(m.mapping_attribute_mapping_json, mapping_source_join_json))) as mappings_for_entity_json
FROM mappings_json m
INNER JOIN joins_json j using (mapping_uuid)    
GROUP BY m.entity_uuid