select uuid as model_uuid
     , json_object( 'uuid',uuid
                  , 'code',code
                  ,'name',name
                  ,'comment',comment
                  ,'author',author
                  ,'repositoryfilename', repositoryfilename
                  ,'modificationdate', modificationdate
                  ,'version', version
                  ,'namespaces', ANY_VALUE(namespaces_json)
                  , 'cdc_properties',
                  json_object(
	                  'cdc_timestamp_field', ANY_VALUE(cdc_timestamp_field),
	                  'cdc_recordtype_field', ANY_VALUE(cdc_recordtype_field),
	                  'cdc_changetype_field', ANY_VALUE(cdc_changetype_field),
	                  'cdc_occurrence_field', ANY_VALUE(cdc_occurrence_field),
	                  'cdc_recordtype_mapping',
	                  json_object(
	                  	'snapshot_type', ANY_VALUE(cdc_recordtype_snapshot),
	                  	'addition_type', ANY_VALUE(cdc_recordtype_addition),
	                  	'modification_type', ANY_VALUE(cdc_recordtype_modification),
	                  	'deletion_type', ANY_VALUE(cdc_recordtype_deletion)
	                  ),
	                  'cdc_changetype_mapping',
	                  json_object(
	                  	'before_state', ANY_VALUE(cdc_changetype_before),
	                  	'after_state', ANY_VALUE(cdc_changetype_after)
	                  )
                  ),
				  'validity_properties',
				  json_object(
						'functional_valid_from_field', ANY_VALUE(m.mde_FunctionalValidFromField),
						'functional_valid_until_field', ANY_VALUE(m.mde_FunctionalValidUntilField),
						'functional_valid_until_is_inclusive', IFNULL(ANY_VALUE(m.mde_FunctionalUntilFieldIsInclusive), 'false'),
						'technical_valid_from_field', ANY_VALUE(m.mde_TechnicalValidFromField),
						'technical_valid_until_field', ANY_VALUE(m.mde_TechnicalValidUntilField),
						'technical_valid_until_is_inclusive', IFNULL(ANY_VALUE(m.mde_TechnicalUntilFieldIsInclusive), 'false')
				  )
                  ,'entities', json_group_array(e.entities_json),
				  'relationships', ANY_VALUE(r.relationships_json),
                  'domains', ANY_VALUE(ds.domains_json)
                  )
       as model_json
  from '%MDE_SOURCE_PATH%/model.parquet' m
  left join entities_json e
    on e.model_uuid = m.uuid
  left join relationships_json r
    on r.model_uuid = m.uuid
  left join domains_json ds
    on ds.model_uuid = m.uuid
  left join namespaces_json ns
    on ns.model_uuid = m.uuid
  group by m.uuid, m.code, m.name, m.comment, m.author, m.version, m.repositoryfilename, m.modificationdate