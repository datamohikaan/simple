With inheritance_link_group_json
as
(
    select il.inheritance_oid
        , json_group_array(i.code||'__'||ce.code) as inheritance_link_group_json
    from '%MDE_SOURCE_PATH%/inheritance_link.parquet' il
    join '%MDE_SOURCE_PATH%/inheritance.parquet' i on il.inheritance_oid = i.oid
    join '%MDE_SOURCE_PATH%/entity_complete.parquet' ce on il.child_entity_oid = ce.oid  
    group by il.inheritance_oid
)
select i.model_uuid
     , json_group_array( json_object('code',i.code
                                    ,'name',i.name
                                    ,'entity', pe.code
                                    ,'mutually_exclusive',i.mutually_exclusive::boolean
                                    ,'complete',i.complete::boolean
                                    ,'inheritance_relationships',ilgj.inheritance_link_group_json
                                    )
                        ) as inheritances_json
  from '%MDE_SOURCE_PATH%/inheritance.parquet' i
  join '%MDE_SOURCE_PATH%/entity_complete.parquet' pe on i.parent_entity_oid = pe.oid
  join inheritance_link_group_json ilgj on i.oid = ilgj.inheritance_oid
 group by i.model_uuid
 