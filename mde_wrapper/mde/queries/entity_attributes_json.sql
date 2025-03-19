With attributes_extended as
(
select *
     , case when DataType = 'I' then 'integer'
            when DataType = 'SI' then 'smallinteger'
            when DataType = 'LI' then 'largeinteger'
            when DataType = 'DT' then 'dateandtime'
            when DataType = 'TS' then 'timestamp'
            when DataType = 'D' then 'date'
            when DataType = 'T' then 'time'
            when substring(datatype,1,2) = 'VA' then 'variablecharacters'
            when substring(datatype,1,2) = 'DC' then 'numeric'
            when substring(datatype,1,1) = 'A' then 'characters'
            when substring(datatype,1,1) = 'N' then 'numeric'
            else 'text'
       end as dt
     , tijdscontext_oid is not null as historized
from '%MDE_SOURCE_PATH%/attribute.parquet'
)
select a.entity_uuid
     , json_object('attributes',json_group_array(json_object('code',a.code
                                                            ,'name',a.name
                                                            ,'uuid',a.uuid
                                                            ,'beweringscontext_uuid', bewerings_ctx.entity_uuid
                                                            ,'registratie_context_uuid', registratie_ctx.entity_uuid
                                                            ,'tijdscontext_uuid', tijds_ctx.entity_uuid
                                                            ,'type',a.dt
                                                            ,'length',a.length::integer
                                                            ,'precision',a.precision
                                                            ,'mandatory',a.mandatory::boolean
                                                            ,'historized',a.historized
                                                            ,'stereotype',a.stereotype
                                                            ,'inheritedfrom', coalesce(a.inheritedfrom, '-')
                                                            ,'attribute_shortcut_oid', ifnull(a.attribute_shortcut_oid, '-')
                                                            ,'attribute_shortcut_uuid',s.uuid
                                                            ,'attribute_shortcut_code',s.code
                                                            ,'description',a.description
                                                            ,'comment',a.comment
                                                            ,'attribute_domain_oid' ,coalesce( a.attribute_domain_oid, '-')
                                                            ,'attribute_domain_uuid',d.uuid
                                                            ,'attribute_domain_code',d.code
                                                            ,'path', coalesce(mde_AttributePath, '')
                                                            )
                                                )
                  )
       as attributes_json
  from attributes_extended a
  left join '%MDE_SOURCE_PATH%/domain_complete.parquet'  s
  on attribute_shortcut_oid = s.oid
  left join '%MDE_SOURCE_PATH%/domain_complete.parquet'  d
  on attribute_domain_oid = d.oid
  left join '%MDE_SOURCE_PATH%/entity_complete.parquet' bewerings_ctx
  on a.beweringscontext_oid = bewerings_ctx.oid
  left join '%MDE_SOURCE_PATH%/entity_complete.parquet' registratie_ctx
  on a.registratie_context_oid = registratie_ctx.oid
  left join '%MDE_SOURCE_PATH%/entity_complete.parquet' tijds_ctx
  on a.tijdscontext_oid = tijds_ctx.oid
 group by a.entity_uuid
 
 