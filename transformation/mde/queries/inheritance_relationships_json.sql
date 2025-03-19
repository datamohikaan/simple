select il.model_uuid
     , json_group_array( json_object('code',i.code||'__'||ce.code
                                    ,'name',ce.name||' is subtype of '||pe.name
                                    ,'referencing_entity',ce.code
                                    ,'referencing_entity_cardinality','1,1'
                                    --,'referencing_attributes',referencing_attributes
                                    ,'referenced_entity',pe.code
                                    ,'referencied_entity_cardinality','1,1'
                                    --,'referenced_attribute',referenced_attribute
                                    )
                        )
       as inheritance_relationships_json
  from '%MDE_SOURCE_PATH%/inheritance_link.parquet' il
  join  '%MDE_SOURCE_PATH%/inheritance.parquet' i on il.inheritance_oid = i.oid
  join  '%MDE_SOURCE_PATH%/entity_complete.parquet'  pe on i.parent_entity_oid = pe.oid
  join  '%MDE_SOURCE_PATH%/entity_complete.parquet'  ce on il.child_entity_oid = ce.oid
 group by il.model_uuid