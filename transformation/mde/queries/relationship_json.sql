With relationship_join_json as
(
	select rj.relationship_uuid
	     , json_group_array(a1.code) as referencing_attributes
	     , json_group_array(a2.code) as referenced_attribute
	  from '%MDE_SOURCE_PATH%/relationship_join.parquet' rj 
	  join '%MDE_SOURCE_PATH%/attribute.parquet' a1 on rj.attribute1_oid = a1.oid
	  join '%MDE_SOURCE_PATH%/attribute.parquet' a2 on rj.attribute2_oid = a2.oid
	group by rj.relationship_uuid
)
select r.model_uuid
     , json_group_array( json_object('code',r.code
                                    ,'name',r.name
                                    ,'uuid', r.uuid
                                    ,'referencing_entity',e1.code
                                    ,'referencing_entity_uuid',e1.uuid
                                    ,'referencing_entity_cardinality',entity1_to_entity2_role_cardinality
                                    ,'referencing_attributes',referencing_attributes
                                    ,'entity1_to_entity2_role',entity1_to_entity2_role
                                    ,'referenced_entity',e2.code
                                    ,'referenced_entity_uuid',e2.uuid
                                    ,'referenced_entity_cardinality',entity2_to_entity1_role_cardinality
                                    ,'referenced_attribute',referenced_attribute
                                    ,'entity2_to_entity1_role',entity2_to_entity1_role
                                    ,'historized',r.tijdscontext_oid is not null
                                    )
                        )
       as relationships_json
  from '%MDE_SOURCE_PATH%/relationship.parquet' r
  join '%MDE_SOURCE_PATH%/entity.parquet' e1 on r.entity1_oid = e1.oid
  join '%MDE_SOURCE_PATH%/entity.parquet' e2 on r.entity2_oid = e2.oid
  left join relationship_join_json rjj on rjj.relationship_uuid = r.uuid
 group by r.model_uuid
 