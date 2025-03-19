SELECT 
        e.model_uuid,
        e.uuid as entity_uuid,
        m.uuid as mapping_uuid, 
        json_object(
            'code', m.code,
            'name', m.name,
            'attribute_mappings', 
            json_group_array(
                json_object(
                    'target_attribute_code', a.code,
                    'source_join_alias', COALESCE(so.join_alias, so.code),
                    'source_attribute_code', sa.code 
        ))) as mapping_attribute_mapping_json
FROM '%MDE_SOURCE_PATH%/mapping.parquet' m
inner join '%MDE_SOURCE_PATH%/entity.parquet' e
    on m.entity_oid = e.oid
INNER JOIN '%MDE_SOURCE_PATH%/attribute_mapping.parquet' am
    on am.mapping_uuid = m.uuid
INNER JOIN '%MDE_SOURCE_PATH%/attribute.parquet' a
    on am.attribute_oid = a.oid
INNER JOIN  '%MDE_SOURCE_PATH%/mdde_source_object.parquet' so
    on am.source_object_oid = so.oid	  
INNER JOIN  '%MDE_SOURCE_PATH%/attribute_mapping_source.parquet' ams
    on ams.attribute_mapping_uuid = am.uuid
INNER JOIN '%MDE_SOURCE_PATH%/attribute.parquet' sa
    on ams.attribute_oid = sa.oid	 
GROUP BY 
        e.model_uuid,
        e.uuid,
        m.uuid,
        m.code,
        m.name
