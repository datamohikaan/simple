def query_code_kennisgebieden(lookup_code_kb: str):
    return f"""
    prefix kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    select ?kennisgebied 
    where {{ graph <urn:name:kennisgebiedenregister> {{
    ?kennisgebied kgr:code "{lookup_code_kb}".
    ?kennisgebied a kgr:Kennisgebied.
    }}
    }}
    """


def query_naam_kennisdeelgebieden(lookup_naam_kdgb: str, lookup_uri_kb: str):
    return f"""
    PREFIX kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT * WHERE {{
        graph <urn:name:kennisgebiedenregister> {{
            ?kennisgebied a kgr:Kennisdeelgebied.
            ?kennisgebied kgr:onderdeelVan <{lookup_uri_kb}>.
            ?kennisgebied rdfs:label ?label.
    FILTER (LCASE(?label) = LCASE("{lookup_naam_kdgb}"))
        }}
    }}
    """


def query_naam_kennisgebieden(lookup_naam_kgb: str):
    return f"""
    PREFIX kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT * WHERE {{
        graph <urn:name:kennisgebiedenregister> {{
            ?kennisgebied a kgr:Kennisgebied.
            ?kennisgebied rdfs:label ?label.
    FILTER (LCASE(?label) = LCASE("{lookup_naam_kgb}"))
        }}
    }}
    """


def query_naam_administratie(lookup_naam_administratie: str):
    return f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX administratie: <http://modellenbibliotheek.belastingdienst.nl/def/amm#Administratie>
    
    SELECT * WHERE {{
      graph <urn:name:architectuurmodel-actueel> {{
        ?administratie_uri a administratie:.
        ?administratie_uri rdfs:label ?label.
    FILTER (LCASE(?label) = LCASE("{lookup_naam_administratie}"))
      }}
    }}
    """


def query_naam_interactie(lookup_naam_interactie: str):
    return f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX interactie: <http://modellenbibliotheek.belastingdienst.nl/def/amm#Appsrv_koppelvlak>
        
        SELECT * WHERE {{
          graph <urn:name:architectuurmodel-actueel> {{
            ?interactie_uri a interactie:;
  					rdfs:label ?label.
        FILTER (LCASE(?label) = LCASE("{lookup_naam_interactie}"))
          }}
        }}
    """


def query_naam_proces(lookup_naam_proces: str):
    return f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX werkproces: <http://modellenbibliotheek.belastingdienst.nl/def/amm#Werkproces>

    SELECT * WHERE {{
      graph <urn:name:architectuurmodel-actueel> {{
        ?proces_uri a werkproces:;
              		rdfs:label ?label.
        FILTER (LCASE(?label) = LCASE("{lookup_naam_proces}"))
      }}
    }}
    """


def query_code_begrippen(lookup_code_kb: str, lookup_begrip: str):
    return f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    prefix kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    select ?begrip
    where {{
        graph <urn:name:kennisgebiedenregister> {{
            ?kg a kgr:Kennisgebied.
            ?kg kgr:code "{lookup_code_kb}".
        }}
        graph ?bgraph {{
            ?model a skos:ConceptScheme.
            ?model kgr:kennisgebied ?kg.
            ?begrip a skos:Concept.
            ?begrip (skos:prefLabel|skos:hiddenLabel) ?term.
            FILTER (regex(?term,"^{lookup_begrip}$","i"))
        }}
    }}
    """


def query_uri_kennisgebieden(lookup_kb_uri: str):
    return f"""
    PREFIX kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT * WHERE {{
        graph <urn:name:kennisgebiedenregister> {{
            <{lookup_kb_uri}> rdfs:label ?label.
        }}
    }}
    """


def query_uri_architectuurmodel(lookup_bes_uri: str):
    return f"""
    PREFIX kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT * WHERE {{
        graph <urn:name:architectuurmodel-actueel> {{
           <{lookup_bes_uri}> rdfs:label ?label.
        }}
    }}
    """


def query_uri_toetsingslogboek(lookup_modelverzoek_uri: str):
    return f"""
    PREFIX kgr: <http://modellenbibliotheek.belastingdienst.nl/def/kgr#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT * WHERE {{
        graph <urn:name:toetsingslogboek> {{
           <{lookup_modelverzoek_uri}> <http://modellenbibliotheek.belastingdienst.nl/def/tlb#betreft> ?model_uri.
        }}
    }}
    """
