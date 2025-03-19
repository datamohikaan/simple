With identifier_json as
(
	select entity_uuid
     , i.uuid as identifier_uuid
     , json_object('code',i.code
                  ,'name',i.name
                  ,'is_primary', i.oid = e.primary_identifier_oid
                  ) 
       as identifier_json
  from '%MDE_SOURCE_PATH%/identifier.parquet' i
  join '%MDE_SOURCE_PATH%/entity.parquet' e
    on i.entity_uuid = e.uuid
 ),
 identifier_attribute_json as
 (
 select ia.identifier_uuid
     , json_object('attributes',json_group_array(json_object('code',a.code))) as identifier_attributes_json
from '%MDE_SOURCE_PATH%/identifier_attribute.parquet' as ia
join '%MDE_SOURCE_PATH%/attribute.parquet' as a on a.oid = ia.attribute_oid 
group by ia.identifier_uuid
 )
 
 select entity_uuid
     , json_object('identifiers',json_group_array(json_merge_patch(identifier_attributes_json,identifier_json))) as identifiers_json
  from identifier_json
  join identifier_attribute_json using (identifier_uuid)
 group by entity_uuid  