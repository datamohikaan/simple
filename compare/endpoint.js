const DEBUG = false;
//#const endpoint = "https://mbieb2.ont.belastingdienst.nl/modellenbibliotheek/sparql";
//const endpoint = "https://mbieb.tst.belastingdienst.nl/modellenbibliotheek/sparql";
//const endpoint = "http://mbk-fuseki:3030/modellenbibliotheek/sparql";
const endpoint = "https://mbk-fuseki-boscp08-dev.apps.rm3.7wse.p1.openshiftapps.com/modellenbibliotheek/sparql";

if (typeof rdflib !== 'undefined') {
  rdflib.setEndpoint(endpoint);
  rdfvizlib.setEndpoint(endpoint);
}
const welkom =
  '<p>Modellenbibliotheek</p><div class="text-center"><h1 class="display-8 fw-bold">Modellenbibliotheek</h1><div class="col-lg-6 mx-auto"><img class="mb-logo"/><p class="mb-4">U bevindt zich op de <b>DeveloperSandbox</b></p><p class="mb-4">Vanaf deze plek heeft u toegang tot de kennis van de primaire taken die de Belastingdienst uitvoert. Deze kennis over relevante wet-, regelgeving en uitvoeringsbeleid is vastgelegd in modellen. Deze modellen geven weer welke gegevens en regels gebruikt worden en wat de betekenis hiervan is Hoe meer kennis- en gebruiksmodellen beschikbaar zijn, hoe completer onze bibliotheek. Op het <a class="mb-inline-link" rel="menu-link" nav-url="dashboard">dashboard</a> kunt u de voortgang zien.</p></div></div>';

const breadcrumb_title = 'MBieb-ont';
const py_prefix = '/static/';