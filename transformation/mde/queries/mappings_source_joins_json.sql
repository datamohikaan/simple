WITH Join_conditions as
(
  select jc.source_object_uuid as Source_Object_Uuid, 
  			json_group_array(
  			json_object( 'parent_join', so.code,
                'parent_join_alias', COALESCE(so.join_alias, so.code),
                'parent_join_entity', se.code,
  						  'parent_join_attribute', pa.code,
  						  'child_join_attribute', ca.code,
  						  'join_operator', COALESCE(jc.join_operator, '=')
  						  )) as join_conditions_json
  from '%MDE_SOURCE_PATH%/mdde_join_condition.parquet' jc
  inner join '%MDE_SOURCE_PATH%/mdde_source_object.parquet' so
     on jc.parent_source_object_oid = so.oid
  inner join '%MDE_SOURCE_PATH%/attribute_complete.parquet' pa
    on jc.parent_attribute_oid = pa.oid
  inner join '%MDE_SOURCE_PATH%/attribute_complete.parquet' ca
     on jc.child_attribute_oid = ca.oid
  INNER JOIN '%MDE_SOURCE_PATH%/entity_complete.parquet' se
    ON so.joined_entity = se.oid
  GROUP BY jc.source_object_uuid
)
SELECT 
        e.model_uuid,
        e.uuid as entity_uuid,
        m.uuid as mapping_uuid, 
        json_object(
            'code', m.code,
            'name', m.name,
            'source_joins', 
            json_group_array(
                json_object(
                    'code', so.code,
                    'source_model', COALESCE(tm.code, md.code),
                    'source_entity', se.code,
                    'join_type', so.join_type,
                    'alias', COALESCE(so.join_alias, so.code),
                    'join_conditions', jc.join_conditions_json
        ))) as mapping_source_join_json
FROM '%MDE_SOURCE_PATH%/mapping.parquet' m
inner join '%MDE_SOURCE_PATH%/entity.parquet' e
    on m.entity_oid = e.oid
INNER JOIN  '%MDE_SOURCE_PATH%/mdde_source_object.parquet' so
    on so.mapping_uuid = m.uuid	 
INNER JOIN '%MDE_SOURCE_PATH%/entity_complete.parquet' se
    ON so.joined_entity = se.oid
LEFT JOIN '%MDE_SOURCE_PATH%/session_shortcut.parquet' ss
  ON se.oid = ss.shortcut_oid
LEFT JOIN '%MDE_SOURCE_PATH%/target_model.parquet' tm
  ON ss.target_model_uuid = tm.uuid
LEFT JOIN '%MDE_SOURCE_PATH%/model.parquet' md
    on se.model_uuid = md.uuid
LEFT JOIN Join_conditions jc
  on so.uuid = jc.Source_Object_Uuid
GROUP BY 
        e.model_uuid,
        e.uuid,
        m.uuid,
        m.code,
        m.name
