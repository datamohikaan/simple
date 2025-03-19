select ent.model_uuid
     , ent.uuid as entity_uuid
     , json_object('code',ent.code
                  ,'name',ent.name
                  ,'comment',ent.comment
                  ,'uuid', ent.uuid
                  ,'beweringscontext_uuid', bewerings_ctx.entity_uuid
                  ,'registratie_context_uuid', registratie_ctx.entity_uuid
                  ,'tijdscontext_uuid', tijds_ctx.entity_uuid
                  ,'stereotype', ent.stereotype
                  ,'description', ent.description
                  ,'sql_expression', ent.mdde_sql_expression
                  ,'path', ent.mde_EntityPath                  
                  ,'validity', 
                  json_object(
                    'functional_validity_type', ent.mde_TypeOfFunctionalValidity,
                    'functional_valid_from_field', func_val_from.code,
                    'functional_valid_until_field', func_val_until.code,
                    'functional_valid_until_is_inclusive', ent.mde_FunctionalUntilFieldIsInclusive,
                    'technical_valid_from_field', tech_val_from.code,
                    'technical_valid_until_field', tech_val_until.code,
                    'technical_valid_until_is_inclusive', ent.mde_TechnicalUntilFieldIsInclusive
                  )
                  ) 
       as entity_json
  from '%MDE_SOURCE_PATH%/entity.parquet' ent
  left join '%MDE_SOURCE_PATH%/attribute.parquet' func_val_from
   on ent.mde_FunctionalValidFromField = func_val_from.oid
  left join '%MDE_SOURCE_PATH%/attribute.parquet' func_val_until
   on ent.mde_FunctionalValidUntilField = func_val_until.oid
  left join '%MDE_SOURCE_PATH%/attribute.parquet' tech_val_from
   on ent.mde_TechnicalValidFromField = tech_val_from.oid
  left join '%MDE_SOURCE_PATH%/attribute.parquet' tech_val_until
   on ent.mde_TechnicalValidUntilField = tech_val_until.oid
  left join '%MDE_SOURCE_PATH%/entity_complete.parquet' bewerings_ctx
   on ent.beweringscontext_oid = bewerings_ctx.oid
  left join '%MDE_SOURCE_PATH%/entity_complete.parquet' registratie_ctx
   on ent.registratie_context_oid = registratie_ctx.oid
  left join '%MDE_SOURCE_PATH%/entity_complete.parquet' tijds_ctx
   on ent.tijdscontext_oid = tijds_ctx.oid
 where coalesce(ent.stereotype,'') not in ('tijdscontext','beweringscontext','registratiecontext','contextgroep')