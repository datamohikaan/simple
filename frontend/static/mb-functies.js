var toetsing_param;
var title;
const queryParameters = Object;
queryParameters.page = "";
var query_json_object;

$(document).ready(function () {
  $(function () {
    let url = new URL(window.location.href);
    window.history.replaceState(null, "", url.origin);

    let usermenu_object = JSON.parse(usermenu.replaceAll("&#34;", '"'));
    let parameters_string = parameters.replaceAll("&amp;", "&");
    let regel =
      '<a class="nav-link dropdown-toggle" id="dropdown01" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">' +
      usernaam +
      " (" +
      usergroepnaam +
      ")" +
      "</a>";
    $(regel).appendTo("#mb-usermenu");
    let items = [];
    $.each(usermenu_object, function (key, val) {
      $(regel).appendTo("mb-usermenuitem");
      items.push(
        '<a class="dropdown-item" rel="menu-link" nav-url="' +
          key +
          '">' +
          val +
          "</a>"
      );
    });
    $("<div/>", {
      class: "dropdown-menu",
      html: items.join(""),
    }).appendTo("#mb-usermenu");
    $("#mb-usermenu").addClass("mb-xxuserid");

    $.ajax({
      url: py_prefix + "mb-json-query.json",
      dataType: "json",
      async: false,
      success: function (data) {
        query_json_object = data;
      },
    });

    $("[rel=mb-bld-logo]").click(function (e) {
      e.preventDefault();
      if ($("#mb-bld-logo").css("display") == "none") {
        $("#mb-bld-logo").show();
      } else {
        $("#mb-bld-logo").hide();
      }
      return false;
    });

    $("a[rel=menu-link]").click(function (e) {
      e.preventDefault();
      $("#melding").html("");
      $(".dropdown-menu").removeClass("show");
      let pageValue = $(this).attr("nav-url");
      queryParameters.page = pageValue;
      page_open(queryParameters);
      return false;
    });

    rdflib.enableLinkCallback(true);
    $("#main-block-inhoud").html(welkom);

    //RJ console.log("Url parameters = " + parameters_string);
    let queryString = new URLSearchParams(parameters_string);
    //RJ console.log("Url queryString = " + queryString);
    queryParameters.page = queryString.get("page");
    if (queryParameters.page != null) {
      queryParameters.graph = queryString.get("graph");
      queryParameters.uri = queryString.get("uri");
      queryParameters.term = queryString.get("term");
      queryParameters.kg = queryString.get("kg");
      queryParameters.vnr = queryString.get("vnr");
      queryParameters.vdate = queryString.get("vdate");
      queryParameters.rdate = queryString.get("rdate");

      /*********************************************
       * Onderstaand is voor test
       ******************************************* */
      let inhoud = "";
      for (const key in queryParameters) {
        const value = queryParameters[key];
        if (value != null) {
          inhoud += " " + key + "=" + value + "\n";
        }
      }
      //RJ console.log(inhoud);
      page_open(queryParameters);
    }

    $("[rel=home-link]").click(function () {
      let url = new URL(window.location.href);
      window.location.href = url.origin;
      return false;
    });

    $("[rel=zoeken]").click(function () {
      $("#melding").html("");
      queryParameters.term = $("[name=term]").val().trim();
      search(queryParameters);
      return false;
    });

    $("#search-input").keypress(function (e) {
      var key = e.which;
      if (key == 13) {
        // the enter key code
        $("[rel=zoeken]").click();
        return false;
      }
    });

    $("#melding").click(function (e) {
      e.preventDefault();
      alert(title);
      return false;
    });
  });

  (function () {
    "use strict";
    window.addEventListener(
      "load",
      function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName("needs-validation");
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
          form.addEventListener(
            "submit",
            function (event) {
              if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
              }
              form.classList.add("was-validated");
            },
            false
          );
        });
      },
      false
    );
  })();
});

/*********************************************
 * Onderstaand is voor https://jira.belastingdienst.nl/secure/attachment/921108/aanpassingen.txt
 * GVG-6054-Overzicht-kennisbronnen_detailpagina
 * https://jira.belastingdienst.nl/browse/GVG-6054
 ******************************************* */

function kennisbronnen(queryParameters) {
  let query_table1 = lees_query("kennisbronnen_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Kennisbronnen");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
  return false;
}

function domeinen(queryParameters) {
  let query_table1 = lees_query("domeinen_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Domeinen");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
  return false;
}

function nav_domein(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_domein_table1");
  let query_table2 = lees_query("nav_domein_table2");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="domeinen.html">Domeinen</a> / Domein'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table><h3>Kennisgebieden</h3>\
    <table class="table kennisgebied" id="table2"></table>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    uri: subjecturi,
  });
  bind_link(queryParameters);

  return false;
}
// end  GVG-6054-Overzicht-kennisbronnen_detailpagina

function lees_query(query_lees_key) {
  //RJ console.log(query_lees_key);
  if (query_json_object.hasOwnProperty(query_lees_key)) {
    return query_json_object[query_lees_key].join(" ");
  } else {
    let melding = query_lees_key + " komt niet voor in de query_json_object.";
    $("#melding").html(melding);
  }
}

function lees_querier(query_lees_key) {
  DEBUG && console.log(query_lees_key);
  var rapportage_query_object = Object;
  $("#melding").html("");
  var data = "query_lees_key = " + query_lees_key
  $.ajax({
      url: "/" + "rapportage_query" + "/read", // maybe change in future
      type: "GET",
      data: data,
      async: false,
      success: function (data) {
          if (data.resultaat == "OK") {
              DEBUG && console.log('query rapportage dynamisch link succes: ' + query_lees_key);
                for (let element of data.input_element) {
                  if (element.attribuut === "sparql_query") {
                      rapportage_query_object.sparql_query = element.waarde;
                  }
                  else if (element.attribuut === "naam") {
                      rapportage_query_object.naam = element.waarde;
                  }
                  else if (element.attribuut === "beschrijving") {
                      rapportage_query_object.beschrijving = element.waarde;
                  }
                }
          } else {
              let melding = query_lees_key + " komt niet voor in de database.";
              $("#melding").html(melding);
          }
      },
  });

  return rapportage_query_object;

//  var data2 = "model = " + query_lees_key
//
//  // second call is to combine the graph_uri inside the sparql_query. Nog niet af!
//  $.ajax({
//      url: "/" + "rapportage_query" + "/uitvoeren_query", // maybe change in future
//      type: "GET",
//      data: data2,
//      async: false,
//      success: function (data2) {
//          if (data.resultaat == "OK") {
//              DEBUG && console.log('query rapportage dynamisch link succes ' + ': ' + query_lees_key);
//                for (let element of data.input_element) {
//                  if (element.label === "Query") {
//                      query_table2 = element.waarde;
//                      break; // Stop de loop zodra we de waarde hebben gevonden
//                  }
//                }
//          } else {
//              let melding = query_lees_key + " komt niet voor in de database.";
//              $("#melding").html(melding);
//          }
//      },
//  });
}

function maak_options(optionName) {
  let uitvoer = "";
  $.ajax({
    url: py_prefix + "mb-json-options.json",
    dataType: "json",
    async: false,
    success: function (data) {
      $.each(data, function (groep, options) {
        if (groep == optionName) {
          $.each(options.options, function (key, val) {
            uitvoer += '<option value="' + key + '">' + val + "</option>";
          });
        }
      });
    },
  });
  return uitvoer;
}

function link_callback() {
  let pageValue = event.currentTarget.dataset.link;
  let graphuri = event.currentTarget.dataset.graphuri;
  let subjecturi = event.currentTarget.dataset.subjecturi;

  queryParameters.page = pageValue;
  queryParameters.graph = graphuri;
  queryParameters.uri = subjecturi;

  page_open(queryParameters);
  return false;
}

function page_open(queryParameters) {
  let pageValue = queryParameters.page;

  $("#melding").html("");
  if (typeof window[pageValue] === "function") {
    window[pageValue](queryParameters);
  } else {
    let melding =
      pageValue +
      " is in deze versie van de modellenbibliotheek nog niet geïmplementeerd.";
    $("#main-block-inhoud").html("");
    $("#main-block-kop").html("");
    title =
      "page: " +
      queryParameters.pageValue +
      "\r\ngraphuri: " +
      queryParameters.graph +
      "\r\nsubjecturi: " +
      queryParameters.uri;
    //RJ console.log("Melding: " + melding);
    $("#melding").html(melding);
    $("#melding").prop("title", title);
  }
  return false;
}

function maak_history(queryParameters) {
  //RJ console.log(queryParameters);
  let pageValue = queryParameters.page;
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;

  let inhoud = "";
  let voorloop = "?";
  for (let key in queryParameters) {
    let value = queryParameters[key];
    if (value != null) {
      if (key == "uri") {
        value = encodeURIComponent(value);
      }
      inhoud += voorloop + key + "=" + value;
      voorloop = "&";
    }
  }
  if (inhoud != "") {
    let url = new URL(window.location.href);
    window.history.pushState(null, "", url.origin + inhoud);
    $("#mb-bld-logo").append(inhoud + " <br/>");
  }
}

function bind_link(queryParameters) {
  // Voeg een download icon toe aan de links naar modellen:
  // nav_inModelversie

  for (const key in queryParameters) delete queryParameters[key];

  $("[rel=breadcrumb-link]").click(function (e) {
    e.preventDefault();
    $("#melding").html("");
    let url = $(this).attr("menu-url");
    queryParameters.page = url.split(".")[0];
    page_open(queryParameters);
    return false;
  });
}

function zet_download_links(queryParameters) {
  //RJ console.log(queryParameters);
  let pageValue = queryParameters.page;
  $("[data-link=nav_SBM]").each(function () {
    //RJ console.log("test");
    //RJ alert("test");
  });
}

function toetsing_return() {
  page_open(toetsing_param);
  return false;
}

function setBreadcrumb(breadcrumbs) {
  $("#breadcrumb").html(
    '<a rel="home-link" href="">' + breadcrumb_title + "</a>" + breadcrumbs
  );
}

/*********************************************
 * Onderstaand is voor https://jira.belastingdienst.nl/secure/attachment/921108/aanpassingen.txt
 * GVG-6054-Overzicht-kennisbronnen_detailpagina
 * https://jira.belastingdienst.nl/browse/GVG-6054
 ******************************************* */

function registerwijzigingen(queryParameters) {
  let query_table1 = lees_query("registerwijzigingen_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Registerwijzigingen");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1, {});

  // maak_history(queryParameters);
  bind_link(queryParameters);
  return false;
}

function dashboard(queryParameters) {
  let query_table1 = lees_query("dashboard_table1");
  let query_table2 = lees_query("dashboard_table2");
  maak_history(queryParameters);

  setBreadcrumb(" / Dashboard");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    '<p>Onderstaand dashboard geeft inzicht in stand van de modelleeropgave.</p>\
  <ul><li>Ingericht betekent dat zowel de datasteward, kennishouder als beherende afdeling geregistreerd is in het kennisgebiedenregister</li>\
  <li>Aangeboden betekent dat de modellen zijn aangeboden ter toetsing en publicatie bij de Modelautoriteit</li>\
  <li>Beschikbaar betekent dat de modellen zijn gepubliceerd in de Modellenbibliotheek</li>\
  <li>Herbruikbaar betekent dat de modellen zijn gepubliceerd in de Modellenbibliotheek met kwaliteitslabel A of B</li></ul>\
  <p>Er is ook een <a rel="breadcrumb-link" menu-url="dashboard2.html">dashboard per kennisgebied</a> beschikbaar.</p>'
  );
  rdflib.fetchData(document.getElementById("table1"), query_table1, {});
  rdflib.fetchData(document.getElementById("table2"), query_table2, {});

  bind_link(queryParameters);
  return false;
}

function nav_dashboard_kg_info(queryParameters) {
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("dashboard_kg_info_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="dashboard.html">Dashboard</a> / Dashboard modellen per kennisgebied'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });

  bind_link(queryParameters);
  return false;
}

function nav_dashboard_dom_info(queryParameters) {
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("dashboard_dom_info_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="dashboard.html">Dashboard</a> / Dashboard modellen per kennisgebied'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });

  bind_link(queryParameters);
  return false;
}

function dashboard2(queryParameters) {
  let query_table1 = lees_query("dashboard2_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="dashboard.html">Dashboard</a> / Dashboard kennisgebieden'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1, {});

  bind_link(queryParameters);
  return false;
}

function find(queryParameters) {
  let uriParam = queryParameters.uri;
  let termParam = queryParameters.term;
  let kgParam = queryParameters.kg;
  let vnrParam = queryParameters.vnr;

  maak_history(queryParameters);

  setBreadcrumb(" / find");
  $("#main-block-inhoud").html(
    '<div class="px-4 py-5 my-5 text-center">\
     <h1 class="display-5 fw-bold">Oeps!</h1><div class="col-lg-6 mx-auto">\
     <p class="lead mb-4">Het begrip "<span id="term">..</span>" komt niet voor in de kennisbank. </p></div></div>'
  );
  $("#main-block-kop").html("");

  let graphquery = lees_query("find_graphquery");
  if (kgParam) {
    graphquery =
      graphquery + "?m kgr:kennisgebied ?kg." + lees_query("find_kgquery");
  }
  graphquery = graphquery + "}}";

  rdflib.fetchValue(
    uriParam,
    graphquery,
    { term: termParam, code: kgParam },
    (uri) => {
      queryParameters.uri = uri;
      queryParameters.page = "nav_begrip";
      page_open(queryParameters);
    }
  );

  document.getElementById("term").innerHTML = termParam;

  bind_link(queryParameters);
  return false;
}

function kennisbanken(queryParameters) {
  let query_table1 = lees_query("kennisbanken_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Kennisbanken");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
  return false;
}

function kennisgebiedenregister(queryParameters) {
  const queryData = {
    query_id: "kennisgebiedenregister_table1",
    query_parameters: [],
    //query_id: "nav_toetsingskader_table1",
    //query_parameters: {"URI":"1234", "GRAPH":"4567"}
  };
  fetch("/querier", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(queryData),
  }).then((response) => response.json());
  //RJ .then((data) => console.log(data));

  let query_table1 = lees_query("kennisgebiedenregister_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / kennisgebiedenregister");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  rdflib.fetchData(document.getElementById("table1"), query_table1), {};

  bind_link(queryParameters);
  return false;
}

function magazijn(queryParameters) {
  let query_table1 = lees_query("magazijn_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / magazijn");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
  return false;
}

function toetsingslogboek(queryParameters) {
  let query_table1 = lees_query("toetsingslogboek_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Toetsingslogboek");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html(
    '<p>Onderstaande tabel geeft alle openstaande verzoeken aan de Modelautoriteit weer. Door op de link te klikken, is meer informatie te vinden via het ticket van de servicedesk.</p>\
  <p>Verzoeken met de status "Ingediend" zijn nog niet opgepakt door de Modelautoriteit. Verzoeken met de status "Onderhanden" zijn daadwerkelijk in behandeling bij de Modelautoriteit. Voor de overige verzoeken geldt dat de Modelautoriteit wacht op een reactie van de indiener.</p>'
  );
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);

  // Verander de Jira links naar een functie
  // Settimeout is nodig om een kleine vertraging te creëren zodat de DOM gereed is voor aanpassing.
  setTimeout(function () {
    $("#table1-uitgeschakeld tr").each(function (index) {
      if (index != 0) {
        var jira_number = $(this).find("td:nth-child(2)").text();
        var graphuri = $(this).find("td:nth-child(4) a").attr("data-graphuri");
        $(this)
          .find("td:nth-child(2)")
          .html(
            '<a rel="data-link" entiteit="modelverzoeken" primary_key=\'{"jira_number":"' +
              jira_number +
              '", "named_graph":"' +
              graphuri +
              "\"}'>" +
              jira_number +
              "</a>"
          );
      }
    });
    var formParameters = Object;
    formParameters.verborgenFormulier = "N";
    formParameters.entiteit = "toetsingslogboek";
    maak_formulier(formParameters);
  }, 500);

  return false;
}

function toetsingslogboek_(queryParameters) {
  let query_table1 = lees_query("toetsingslogboek__table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Toetsingslogboek");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html(
    '<p>Alle afgeronde verzoeken kunnen hier gevonden worden: <a rel="breadcrumb-link" menu-url="verzoeken.html">afgeronde verzoeken</a>.</p>\
  <p>Alle modellen in de modellenbibliotheek kunnen hier gevonden worden: <a rel="breadcrumb-link" menu-url="toetsingsmodellen.html">alle modellen</a>.</p>'
  );
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
    // Verander de Jira links naar een functie
  // Settimeout is nodig om een kleine vertraging te creëren zodat de DOM gereed is voor aanpassing.
  setTimeout(function () {
    $("#table1 tr").each(function (index) {
      console.log('inside function')
      if (index != 0) {
        var modelverzoek_uri = $(this).find("td:nth-child(1) a").attr("href");
        var jira_number = $(this).find("td:nth-child(1)").text();
        var graphuri = $(this).find("td:nth-child(4) a").attr("data-graphuri");
        $(this)
          .find("td:nth-child(1)")
          .html(
            '<a rel="data-link" entiteit="modelverzoeken" primary_key=\'{"modelverzoek_uri":"' +
              modelverzoek_uri +
              '", "named_graph":"' +
              graphuri +
              "\"}'>" +
              jira_number +
              "</a>"
          );
      }
    });
    var formParameters = Object;
    formParameters.verborgenFormulier = "N";
    formParameters.entiteit = "modelverzoek";
    maak_formulier(formParameters);
  }, 500);

  return false;
}

// GVG-6220
function over(queryParameters) {
  let query_table1 = lees_query("toetsingslogboek__table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Over");

  $("#main-block-kop").html("");
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><table class="table" id="table2"></table><table class="table" id="table3"></table>'
  );
  $.ajax({
    url: py_prefix + "mb-json-over.json",
    dataType: "json",
    async: false,
    success: function (data) {
      $("#table1").html(data["tekst"].join(" "));
      $("#table2").append("<tr>");
      for (title of data.titelChangelog) {
        $("#table2").append("<th>" + title + "</th>");
      }
      $("#table2").append("</tr>");
      $("#table3").html(data["disclaimer"].join(" "));
    },
  });
  $.ajax({
    url: py_prefix + "mb-json-changelog.json",
    dataType: "json",
    async: false,
    success: function (data) {
      ToonAantalReleaseNotes = 10; // Het maximaal aantal te tonen release notes.
      $(data.release_note).each(function () {
        if (this.zichtbaar == "J") {
          if (ToonAantalReleaseNotes < 1) {
            return false;
          }
          $("#table2").append(
            "<tr><td>" +
              this.versienummer +
              "</td><td>" +
              this.versiedatum +
              "</td><td>" +
              this.omschrijving +
              "</td></tr>"
          );
          ToonAantalReleaseNotes--;
        }
      });
    },
  });
  return false;
}

function search(queryParameters) {
  let query_table1 = lees_query("search_table1");

  setBreadcrumb(" / Zoeken");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html(
    "<p>Zoekresultaten voor: <b>" + queryParameters.term + "</b></p>"
  );

  // const term = urlParams.get("term").replace(/[^a-zA-Z0-9\s]/g, "");
  rdflib.fetchData(document.getElementById("table1"), query_table1, {
    term: queryParameters.term,
  });

  bind_link(queryParameters);
  return false;
}

function upload() {
  setBreadcrumb(" / Upload model");
  $("#main-block-kop").html(
    "<p>Hier kun je je model uploaden om aan te bieden voor de Modellenbibliotheek. De met een * aangegeven velden zijn verplicht.</p>"
  );
  $("#main-block-inhoud").html(
    '\
  <form id="upload-model" name="upload-model" method="POST" enctype="multipart/form-data">\
  \
  <div class="form-group">\
    <label for="bd_user">Eigen user Id *</label>\
    <input type="text" name="bd_user" id="bd_user" class="form-control" value="' +
      userid +
      '" required/>\
  </div>\
  <div class="form-group">\
    <label for="domein">Domein actief</label>\
    <div><input type="text" name="domein" id="domein" class="form-control"/></div>\
  </div>\
  <div class="form-group">\
    <label for="titelVerzoek">Titel van het verzoek *</label>\
    <div><input type="text" name="titelVerzoek" id="titelVerzoek" class="form-control" value="Dit is de titel" required/></div>\
  </div>\
    <div class="form-group">\
    <label for="soortVerzoek">Soort verzoek *</label>\
    <select class="form-control" id="soortVerzoek" name="soortVerzoek"required>' +
      maak_options("soortVerzoek") +
      '</select>\
  </div>\
    <div class="form-group">\
    <label for="soortModel">Soort model *</label>\
    <select class="form-control" id="soortModel" name="soortModel" required>' +
      maak_options("soortModel") +
      '</select>\
  </div>\
  </div>\
    <div class="form-group">\
    <label for="modelStatus">Model status *</label>\
    <select class="form-control" id="modelStatus" name="modelStatus" required>' +
      maak_options("modelStatus") +
      '</select>\
  </div>\
    <div class="form-group">\
    <label for="sdJiraItemnummer">Service desk Jira itemnummer *</label>\
    <input type="text" name="sdJiraItemnummer" id="sdJiraItemnummer" class="form-control" value="SD1212123" required/>\
  </div>\
  <div class="form-group">\
    <label for="extraModelleurs">Extra modelleurs</label>\
    <input type="text" name="extraModelleurs" id="extraModelleurs" class="form-control" placeholder="Geef het user_id van de extra modelleur(s) gescheiden door een komma"/>\
  </div>\
  <div class="form-group">\
    <label for="opmerkingen">Opmerkingen</label>\
    <div><input type="text" name="opmerkingen" id="opmerkingen" class="form-control"/></div>\
  </div>\
  <div class="form-group">\
    <label for="fileToUpload">Kies het model voor upload</label>\
    <input type="file" name="fileToUpload" id="fileToUpload" class="form-control" required/>\
  </div>\
  <button id="btn" type="submit" name="upload_data" class="btn btn-primary mt-3">Modelverzoek indienen</button>\
  </form>\
  <div id="upload_resultaat"></div>\
  '
  );

  $("form#upload-model").submit(function (e) {
    e.preventDefault();
    //alert('upload-model');
    const btn = document.getElementById("btn");
    btn.style.backgroundColor = "orange";
    btn.innerHTML = "uploading and transforming...";

    var formData = new FormData(this);
    var fileInput = $("#fileToUpload")[0];

    formData.append("userid", userid);
    formData.append("fileToUpload", fileInput.files[0]);

    $.ajax({
      url: "/upload",
      type: "POST",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      beforeSend: function () {
        $("#btn").css({ "background-color": "orange" });
        $("#btn").prop("value", "Verwerken");
        $("#btn").text("Verwerken");
      },
      success: function (data) {
        console.log(JSON.stringify(data));
        if (data.resultaat == "OK") {
          $("#btn").css({ "background-color": "green" });
          $("#btn").prop("value", "Gereed");
          $("#btn").text("Gereed");
        } else {
          $("#btn").css({ "background-color": "red" });
          $("#btn").prop("value", "Gereed");
          $("#btn").text("Fout opgetreden");
        }
        //$("#upload_resultaat").html(data.opmerking).show();
        // below code inserted by suley
        DEBUG && console.log('we zitten in de return-call van een modelverzoek indienen2')

        $("#upload_resultaat").html(
        data.opmerking.replace(/\n/g, "<br>").replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;")
        );
      },
    });
    return false;
  });
  return false;
}

function upload_nieuw() {
  setBreadcrumb(" / Upload model");
  $("#main-block-kop").html(
    "<p>Hier kun je je model uploaden om aan te bieden voor de Modellenbibliotheek. De met een * aangegeven velden zijn verplicht.</p>"
  );

  $("#main-block-inhoud").html('<div id="mbk-sub"></div>');

  var formParameters = Object;
  formParameters.verborgenFormulier = "F";
  formParameters.entiteit = "modelverzoekIndienen";
  maak_formulier(formParameters);
  return false;
}

function toevoegen_gebruikers() {
  setBreadcrumb(" / Toevoegen gebruikers");
  $("#main-block-kop").html(
    "<p>Hier kun je een excel toevoegen om gebruikers toe te voegen aan de Modellenbibliotheek.</p>"
  );

  $("#main-block-inhoud").html(
    '\
  <form id="toevoegen-gebruikers" name="toevoegen-gebruikers" method="POST" enctype="multipart/form-data">\
  \
  <label for="fileToUpload">Upload de template met de gebruikers die je wilt toevoegen</label>\
  <input type="file" name="fileToUpload" id="fileToUpload" class="form-control" required/>\
  <button type="submit" name="upload_data" class="btn btn-primary mt-3">Upload</button>\
  </form>\
  <div id="upload_resultaat"></div>\
  '
  );

  $("form#toevoegen-gebruikers").submit(function (e) {
    e.preventDefault();

    var formData = new FormData(this);
    var fileInput = $("#fileToUpload")[0];

    $.ajax({
      url: "/toevoegen_gebruikers",
      type: "POST",
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      beforeSend: function () {},
      success: function (response) {
        alert(response);
      },
    });
    return false;
  });
  return false;
}

function download_model() {
  setBreadcrumb(" / Download model");
  $("#main-block-kop").html(
    "<p>Hier kun je geuploade modellen downloaden.</p>"
  );

  $(document).ready(function () {
    $.ajax({
      url: "/download",
      type: "GET",
      success: function (models) {
        displayModels(models);
      },
    });
  });
}

function download_turtle() {
  setBreadcrumb(" / Download model");
  $("#main-block-kop").html(
    "<p>Hier kun je geuploade modellen downloaden.</p>"
  );

  $(document).ready(function () {
    $.ajax({
      url: "/turtle_",
      type: "GET",
      success: function (models) {
        displayModels(models);
      },
    });
  });
}

function displayModels(models) {
  var tableHTML =
    "<table><thead><tr><th>Model naam</th><th>Graph URI</th><th>Upload moment</th><th>Model status</th></tr></thead><tbody>";
  models.forEach(function (model) {
    let fileName = model[0] + model[1];
    tableHTML += `<tr><td><a href='/download/${model[5]}/${model[0]}' download>${fileName}</a></td><td>${model[2]}</td><td>${model[3]}</td><td>${model[4]}</td></tr>`;
  });
  tableHTML += "</tbody</table>";
  $("#main-block-inhoud").html(tableHTML);
}

function query_dienst() {
  setBreadcrumb(" / Querydienst");
  $("#main-block-kop").html(
    "<p>Hier kun je je query ingeven om uit te laten voeren door de Modellenbibliotheek.</p>"
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-tabel"></div><div id="mbk-sub"></div>'
  );
  var tabelParameters = Object;
  tabelParameters.entiteit = "rapportage_query";
  tabelParameters.verborgenFormulier = "N";
  maak_tabel(tabelParameters);
}

function fuseki_herstel() {
  setBreadcrumb(" / Fuseki Herstel");
  $("#main-block-kop").html(
    "<p>Hier kun je de Fuseki database herstellen, mits dit nodig is.</p>"
  );
  $("#main-block-inhoud").html('<div id="herstel_resultaat"></div>');
  var wachtwoord = window.prompt("Wachtwoord: ");
  if (wachtwoord === "MbiebFusekiHerstel!") {
    var button = $("<button/>", {
      text: "Fuseki Herstellen",
      click: function () {
        var bevestig = window.confirm(
          "De Fuseki database wordt hersteld, weet u zeker dat u door wilt gaan?"
        );
        if (bevestig) {
          $.ajax({
            url: "/fuseki_restore",
            method: "GET",
            success: function (data) {
              $("#herstel_resultaat")
                .html(data.replace(/\n/g, "<br>").replace(/ /g, "&nbsp;"))
                .show();
            },
          });
        }
      },
    });
    $("#main-block-inhoud").append(button);
  } else {
    $("#herstel_resultaat").html("Geen toegang.").show();
  }
}

function nav_CIM(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_CIM_table1");
  let query_table2 = lees_query("nav_CIM_table2");
  let query_graph1 = lees_query("nav_CIM_graph1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="kennisbanken.html">Kennisbanken</a> / CIM Model'
  );
  $("#main-block-inhoud").html(
    '<div class="row"><div class="col-3 scrollable"><ul class="tree" id="tree1"></table></div><div class="col"><table class="table" id="table1"></table><div id="download"><a href="/original/' +
      subjecturi +
      '" class="btn btn-primary">Download originele model</a> \
            <a href="/turtle/' +
      subjecturi +
      '" class="btn btn-primary">Download gepubliceerde model</a></div><div id="graph1" style="width:100%; height:500px"></div></div></div>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: graphuri,
  });
  const types = [
    "http://modellenbibliotheek.belastingdienst.nl/def/lgd#Entiteittype",
    "http://modellenbibliotheek.belastingdienst.nl/def/lgd#Relatietype",
    "http://modellenbibliotheek.belastingdienst.nl/def/lgd#Attribuutdomein",
  ];
  const propuri =
    "http://modellenbibliotheek.belastingdienst.nl/def/lgd#attribuut";

  rdflib.fetchTreeCB(
    document.getElementById("tree1"),
    { notation: "erd", graph: graphuri, types: types, lower: propuri },
    (params) => {
      const table1 = document.getElementById("table1");
      const graph1 = document.getElementById("graph1");
      download.innerHTML = "";
      table1.innerHTML = "";
      graph1.innerHTML = "";
      rdflib.fetchTriples(table1, query_table2, params);
      rdfvizlib.displayTriples(graph1, query_graph1, params);
    }
  );
  zet_download_links(queryParameters);

  bind_link(queryParameters);
  return false;
}

function nav_SBM(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_SBM_table1");
  let query_table2 = lees_query("nav_SBM_table2");
  let query_graph1 = lees_query("query_begrip_graph1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="kennisbanken.html">Kennisbanken</a> / Semantisch Model'
  );
  $("#main-block-inhoud").html(
    '<div class="row"><div class="col-3 scrollable"><ul class="tree" id="tree1"></table></div><div class="col"><table class="table" id="table1"></table><div id="download"><a href="/original/' +
      subjecturi +
      '" class="btn btn-primary">Download originele model</a> \
            <a href="/turtle/' +
      subjecturi +
      '" class="btn btn-primary">Download gepubliceerde model</a></div><div id="graph1" style="width:100%; height:500px"></div></div></div>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: graphuri,
  });
  const classuri = "http://www.w3.org/2004/02/skos/core#Concept";
  const propuri = "http://www.w3.org/2004/02/skos/core#broader";
  rdflib.fetchTreeCB(
    document.getElementById("tree1"),
    {
      notation: "concepts",
      layout: "fdp",
      graph: graphuri,
      class: classuri,
      upper: propuri,
    },
    (params) => {
      const table1 = document.getElementById("table1");
      const graph1 = document.getElementById("graph1");
      download.innerHTML = "";
      table1.innerHTML = "";
      graph1.innerHTML = "";
      rdflib.fetchTriples(table1, query_table2, params);
      rdfvizlib.displayTriples(graph1, query_graph1, params);
    }
  );

  zet_download_links(queryParameters);

  bind_link(queryParameters);
  return false;
}

function nav_begrip(queryParameters) {
  query_begrip(queryParameters);
  return false;
}

function nav_broader(queryParameters) {
  query_begrip(queryParameters);
  return false;
}

function nav_related(queryParameters) {
  query_begrip(queryParameters);
  return false;
}

function query_begrip(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let graphquery = lees_query("query_begrip_graphquery");
  let query_table1 = lees_query("query_begrip_table1");
  let query_graph1 = lees_query("query_begrip_graph1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="kennisbanken.html">Kennisbanken</a> / Semantisch Model / Begrippen'
  );
  $("#main-block-inhoud").html(
    '<div class="row"><div class="col-3 scrollable"><ul class="tree" id="tree1"></table></div><div class="col"><table class="table" id="table1"></table><div id="graph1" style="width:100%; height:500px"/></div></div>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchValue(graphuri, graphquery, { uri: subjecturi }, (graphuri) => {
    const classuri = "http://www.w3.org/2004/02/skos/core#Concept";
    const propuri = "http://www.w3.org/2004/02/skos/core#broader";
    rdflib.fetchTreeCB(
      document.getElementById("tree1"),
      {
        notation: "concepts",
        layout: "fdp",
        graph: graphuri,
        class: classuri,
        upper: propuri,
      },
      (params) => {
        const table1 = document.getElementById("table1");
        const graph1 = document.getElementById("graph1");
        table1.innerHTML = "";
        graph1.innerHTML = "";
        rdflib.fetchTriples(table1, query_table1, params);
        rdfvizlib.displayTriples(graph1, query_graph1, params);
      }
    );
    rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
      uri: subjecturi,
      graph: graphuri,
    });
    rdfvizlib.displayTriples(document.getElementById("graph1"), query_graph1, {
      notation: "concepts",
      layout: "fdp",
      uri: subjecturi,
      graph: graphuri,
    });
  });

  bind_link(queryParameters);
  return false;
}

function nav_kennisgebied(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_kennisgebied_table1");
  let query_table2 = lees_query("nav_kennisgebied_table2");
  let query_table3 = lees_query("nav_kennisgebied_table3");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="kennisgebiedenregister.html">Kennisgebiedenregister</a> / Kennisgebied'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table><h3>Kennisdeelgebieden</h3>\
    <table class="table kennisdeelgebied" id="table2"></table><h3>Kennisbronnen (wet- en regelgeving)</h3>\
    <table class="table kennisbron" id="table3"></table>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table3"), query_table3, {
    uri: subjecturi,
  });
  bind_link(queryParameters);
  return false;
}

function nav_toetsing(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_toetsing_table1");
  let query_table2 = lees_query("nav_toetsing_table2");
  maak_history(queryParameters);

  // Bewaar de huidige parameters voor breadcrumb
  toetsing_param = queryParameters;
  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / Toetsing'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande tabel geeft een overzicht van de toetsingen die uitgevoerd kunnen worden voor dit model</p>"
  );

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: graphuri,
  });

  let model_type;
  // Add MutationObserver to detect when table content is loaded
  const observer = new MutationObserver(() => {
    const rows = document.querySelectorAll("#table1 tr");
    if (rows.length > 0) {
      let model_type;

      // Find the row with 'type' in first column
      rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        if (cells.length >= 2 &&
            cells[0].textContent.toLowerCase().includes("type")) {
          model_type = cells[1].textContent.trim();
        }
      });

      // Use the found model_type
      if (model_type) {
        DEBUG && console.log("Model Type:", model_type);
        var tabelParameters = Object;
        tabelParameters.entiteit = "rapportage_query/" + model_type;
        DEBUG && console.log(tabelParameters.entiteit);
        tabelParameters.graph_uri = graphuri;
        maak_tabel(tabelParameters);
      }

      observer.disconnect(); // Stop observing after finding
    }
  });

  // Start observing table for DOM changes
  observer.observe(document.getElementById("table1"), {
    childList: true,  // Watch for added/removed children
    subtree: true     // Observe nested elements
  });

 //oude code
  DEBUG && rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: graphuri,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  maak_formulier(formParameters);
  return false;
}

function nav_toetsing_Querier(queryParameters) {
  DEBUG && console.log("nav_toetsing_querier");

  let graphuri = queryParameters.graph_uri;
  let rapportage_query_id = queryParameters.rapportage_query_id;


  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_toetsing_table1");

  let rapportage_query_object = lees_querier(rapportage_query_id.replace("urn:uuid:", ""));

  var query_table2 = rapportage_query_object.sparql_query
  // Remove commas, line breaks, and double quotes
  query_table2 = query_table2
    .replace(/@GRAPH@/g, graphuri) // replace @GRAPH@ with the graphuri
    .replace(/,\s*\n/g, ' ') // remove comma-whitespace-newline combo's
    .replace(/\n/g, ' ') // remove newline characters
    .replace(/"/g, '') // Remove double quotes
    .replace(/\s+/g, ' ') // distill multiple spaces into one space
    .trim(); // remove leading and trailing whitespace

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Begrippen met cirkelverwijzing'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<h1>" + rapportage_query_object.naam + "</h1>" +
    "<p>" + rapportage_query_object.beschrijving + "</p>"
  );
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: graphuri,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    uri: graphuri,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_BegrippenMetCirkelverwijzing(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_BegrippenMetCirkelverwijzing_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_BegrippenMetCirkelverwijzing_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Begrippen met cirkelverwijzing'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande begrippen hebben een directe of indirecte cirkelverwijzing. Dit ontstaat als in een definitie van een begrip naar dit begrip zelf wordt verwezen, of als er via verwijzingen in definities een lus te maken is (A->B->..->Z->A</p>"
  );
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_KennisbronnenZonderVindbareLocatie(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_KennisbronnenZonderVindbareLocatie_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_KennisbronnenZonderVindbareLocatie_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Kennisbronnen zonder vindbare locatie'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaan overzicht geeft alle kennisbronnen weer die geen vindbare bronlocatie hebben. Dit zijn kennisbronnen zonder enige bronlocatie en kennisbronnen met een bronlocatie die geen URL betreft, maar slechts een tekstuele verwijzing.</p>"
  );
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_BegrippenMetOnbekendeKennisbron(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_BegrippenMetOnbekendeKennisbron_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_BegrippenMetOnbekendeKennisbron_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Begrippen met onbekende kennisbron'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande begrippen hebben wel een verwijzing naar een kennisbron, maar die verwijzing kan niet verbonden worden met in het model gespecificeerde kennisbron</p>"
  );
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_BegrippenMetVerwijsfouten(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_BegrippenMetVerwijsfouten_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_BegrippenMetVerwijsfouten_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Begrippen met verwijsfouten'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_BegrippenZonderKennisbron(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_BegrippenZonderKennisbron_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_BegrippenZonderKennisbron_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Begrippen zonder kennisbron'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_BegrippenZonderLineage(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_toetsing_BegrippenZonderLineage_table1");
  let query_table2 = lees_query("nav_toetsing_BegrippenZonderLineage_table2");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Begrippen zonder horizontale lineage'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande begrippen hebben geen relaties naar andere begrippen. Vaak komt dat omdat in de definitie niet met blokhaaken [..] naar een begrip wordt verwezen. Ook kan het voorkomen dat er wel blokhaken zijn gebruikt, maar het betreffende begrip kan niet gevonden worden, waardoor er geen relatie is gelegd.</p>"
  );

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_Kennisbrongebruik(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_toetsing_Kennisbrongebruik_table1");
  let query_table2 = lees_query("nav_toetsing_Kennisbrongebruik_table2");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Kennisbrongebruik'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    '<p>Onderstaande lijst geeft het overzicht van aantal verwijzingen naar een in dit model gespecificeerde kennisbron. Bij nul begrippen is sprake van een kennisbron die onnodig opgenomen is in dit model, of de verwijzingen naar deze kennisbron kloppen niet. Verwijzingen werken alleen als deze verwijzingen eindigen op de waarde in de kolom "link". Deze kolom mag niet leeg zijn.</p>'
  );
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_CIMElementenIncorrecteLineage(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_CIMElementenIncorrecteLineage_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_CIMElementenIncorrecteLineage_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / LGD Elementen met incorrecte lineage'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande LGD modelelementen hebben verwijzen niet naar een begrip in hetzelfde kennis(deel)gebied. Hierboven is aangegeven welke versie van het semantisch model daarbij wordt gebruikt. Als dit niet wordt getoond, of alleen een URI (en geen naam), dan kan het betreffende semantische model niet gevonden worden (en zullen alle modelelementen geen correcte lineage hebben).</p>"
  );

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_CIMElementenZonderLineage(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_CIMElementenZonderLineage_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_CIMElementenZonderLineage_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / LGD Elementen zonder lineage'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande LGD modelelementen verwijzen niet naar een begrip in hetzelfde kennis(deel)gebied.</p>"
  );

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_LosseEntiteittypen(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_toetsing_LosseEntiteittypen_table1");
  let query_table2 = lees_query("nav_toetsing_LosseEntiteittypen_table2");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Losse entiteittypen'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande entiteittypen hebben geen enkele relatie met een ander element in het LGD. Hoewel dit niet in alle gevallen foutief is, kan het wel een indicatie zijn op een overbodig uitgewerkt stukje model of een entiteittype dat per ongeluk nog is achtergebleven in het opgeleverde model.</p>"
  );

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_OntbrekendeAttribuutdomeinen(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_OntbrekendeAttribuutdomeinen_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_OntbrekendeAttribuutdomeinen_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Ontbrekende attribuutdomeinen'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Bij onderstaande attribuuttypen is geen attribuutdomein gespecificeerd, of wordt verwezen naar een onbekend attribuutdomein.</p>"
  );
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_toetsing_OverbodigeAttribuutdomeinen(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query(
    "nav_toetsing_OverbodigeAttribuutdomeinen_table1"
  );
  let query_table2 = lees_query(
    "nav_toetsing_OverbodigeAttribuutdomeinen_table2"
  );
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / <a onclick="toetsing_return()">Toetsing</a> / Overbodige attribuutdomeinen'
  );
  $("#main-block-inhoud").html(
    '<table class="table" id="table1"></table><div id="mbk-sub"></div><table class="table" id="table2"></table>'
  );
  $("#main-block-kop").html(
    "<p>Onderstaande attribuutdomeinen worden niet gebruikt in het model, maar zijn wel onderdeel van het model (NB: shortcuts zijn al uit dit overzicht gefiltered)</p>"
  );

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    graph: subjecturi,
  });

  bind_link(queryParameters);
  var formParameters = Object;
  formParameters.primary_key = '{"named_graph":"' + graphuri + '"}';
  formParameters.entiteit = "toetsingsrapport";
  formParameters.verborgenFormulier = "J";
  //maak_formulier(formParameters);
  return false;
}

function nav_triples(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb("");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  const graphparam = graphuri;
  const querypre = "?query=construct%7B%3Fs%3Fp%3Fo%7Dwhere%7Bgraph%3C";
  const querypost = "%3E%7B%3Fs%3Fp%3Fo%7D%7D";
  window.location.replace(endpoint + querypre + graphparam + querypost);

  bind_link(queryParameters);
  return false;
}

/*********************************************
 * Onderstaand is voor https://jira.belastingdienst.nl/secure/attachment/921108/aanpassingen.txt
 * GVG-6054-Overzicht-kennisbronnen_detailpagina
 * https://jira.belastingdienst.nl/browse/GVG-6054
 ******************************************* */

function nav_wijziging(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_wijziging_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="registerwijzigingen.html">Registerwijzigingen</a> / Wijziging'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });

  bind_link(queryParameters);
  return false;
}

function nieuw_type(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_type");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_afbakeningstype(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_afbakeningstype");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_domein(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_domein");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_grondslag(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_grondslag");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_status(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_status");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_isDefinedBy(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_isDefinedBy");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_related(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_related");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_inModelversie(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_inModelversie");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nieuw_kennisbron(queryParameters) {
  let graphuri = queryParameters.graph;
  let subjecturi = queryParameters.uri;
  maak_history(queryParameters);

  setBreadcrumb(" / nieuw_kennisbron");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  bind_link(queryParameters);
  return false;
}

function nav_toetsingskader(queryParameters) {
  /* let graphuri = queryParameters.graph; */
  const graphuri = "urn:name:toetsingskader";
  let subjecturi = queryParameters.uri;
  let query_table1 = lees_query("nav_toetsingskader_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / Toetsingskader'
  );
  $("#main-block-inhoud").html(
    '<div class="row"><div class="col-3 scrollable"><ul class="tree" id="tree1"></table></div><div class="col"><table class="table" id="table1"></table></div></div>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
    graph: graphuri,
  });
  const classuri = "http://www.w3.org/ns/dqv#Metric";
  const propuri = "http://www.w3.org/ns/dqv#inDimension";
  const types = ["http://www.w3.org/ns/dqv#Dimension"];
  rdflib.fetchTree(
    document.getElementById("tree1"),
    document.getElementById("table1"),
    query_table1,
    { graph: graphuri, upper: propuri, types: types }
  );

  bind_link(queryParameters);
  return false;
}

function nav_toetsingsrapport(queryParameters) {
  let subjecturi = queryParameters.uri;
  let query_kwlabel = lees_query("nav_toetsingsrapport_kwlabel");
  let query_table1 = lees_query("nav_toetsingsrapport_table1");
  let query_table2 = lees_query("nav_toetsingsrapport_table2");
  let query_table3 = lees_query("nav_toetsingsrapport_table3");
  let query_table4 = lees_query("nav_toetsingsrapport_table4");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / Toetsingsrapport'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>\
    <ul class="nav nav-tabs" id="myTab" role="tablist">\
      <li class="nav-item" role="presentation">\
        <button class="nav-link active" id="kwaliteitslabel-tab" data-bs-toggle="tab" data-bs-target="#kwaliteitslabel" type="button" role="tab" aria-controls="kwaliteitslabel" aria-selected="true">Kwaliteitslabel</button>\
      </li>\
      <li class="nav-item" role="presentation">\
        <button class="nav-link" id="dimensies-tab" data-bs-toggle="tab" data-bs-target="#dimensies" type="button" role="tab" aria-controls="dimensies" aria-selected="false">Dimensies</button>\
      </li>\
      <li class="nav-item" role="presentation">\
        <button class="nav-link" id="metingen-tab" data-bs-toggle="tab" data-bs-target="#metingen" type="button" role="tab" aria-controls="metingen" aria-selected="false">Metingen</button>\
      </li>\
      <li class="nav-item" role="presentation">\
        <button class="nav-link" id="advies-tab" data-bs-toggle="tab" data-bs-target="#advies" type="button" role="tab" aria-controls="advies" aria-selected="false">Advies</button>\
      </li>\
    </ul>\
    <div class="tab-content" id="myTabContent">\
      <div class="tab-pane fade show active" id="kwaliteitslabel" role="tabpanel" aria-labelledby="kwaliteitslabel-tab">\
        <p>De Modelautoriteit heeft het volgende kwaliteitslabel toegekend:</p>\
        <div style="display:flex;"><div><p style="font-size:40px; margin-left:30px; margin-right:30px;" id="kwlabel">?</p></div><div><p id="toelichting"/></div></div>\
     </div>\
      <div class="tab-pane fade" id="dimensies" role="tabpanel" aria-labelledby="dimensies-tab">\
        <p>Onderstaande tabel geeft het oordeel van de Modelautoriteit per toetsdimensie:</p>\
        <table class="table" id="table4"></table>\
      </div>\
      <div class="tab-pane fade" id="metingen" role="tabpanel" aria-labelledby="metingen-tab">\
        <p>Onderstaande tabel geeft inzicht in de kwaliteit van het model</p>\
        <table class="table" id="table2"></table>\
      </div>\
      <div class="tab-pane fade" id="advies" role="tabpanel" aria-labelledby="advies-tab">\
        <p>Onderstaande tabel geeft een overzicht van de adviezen van de Modelautoriteit</p>\
        <table class="table" id="table3"></table>\
      </div>\
    </div>\
  '
  );
  $("#main-block-kop").html("");
  rdflib.fetchValue(null, query_kwlabel, { uri: subjecturi }, (kwaliteit) => {
    const kwlabel = document.getElementById("kwlabel");
    const toelichting = document.getElementById("toelichting");
    kwlabel.innerHTML = kwaliteit.split('|')[0];
    toelichting.innerHTML = kwaliteit.split('|')[1];
  });

  rdflib.fetchTriples(document.getElementById("table1"), query_table1, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table2"), query_table2, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table3"), query_table3, {
    uri: subjecturi,
  });
  rdflib.fetchData(document.getElementById("table4"), query_table4, {
    uri: subjecturi,
  });

  bind_link(queryParameters);
  return false;
}

//function nav_inModelversie(queryParameters) {
//    let uri = queryParameters.graph;
//    const turtle_url = `/turtle_${uri}`;
//    fetch(turtle_url)
//        .then(response => {
//            const blob = response.blob();
//            const link = document.createElement('a');
//            link.download = 'turtle.ttl';
//            link.href = window.URL.createObjectURL(blob);
//            document.body.appendChild(link);
//            link.click();
//            document.body.removeChild(link);
//        })
//        .catch(error => console.error('Kan Turtle niet ophalen:', error));
//        zet_download_links(queryParameters);
//}

function verzoeken(queryParameters) {
  let graphuri = queryParameters.graph;
  let query_table1 = lees_query("verzoeken_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / Afgeronde verzoeken'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");

  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
  return false;
}

function toetsingsmodellen(queryParameters) {
  let graphuri = queryParameters.graph;
  let query_table1 = lees_query("toetsingsmodellen_table1");
  maak_history(queryParameters);

  setBreadcrumb(
    ' / <a rel="breadcrumb-link" menu-url="toetsingslogboek_.html">Toetsingslogboek</a> / Alle modellen'
  );
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1);

  bind_link(queryParameters);
  return false;
}

function modelverzoeken(queryParameters) {
  let query_table1 = lees_query("modelverzoeken_table1");
  maak_history(queryParameters);

  setBreadcrumb(" / Mijn modelverzoeken");
  $("#main-block-inhoud").html(
    '<div id="mbk-sub"></div><table class="table" id="table1"></table>'
  );
  $("#main-block-kop").html("");
  rdflib.fetchData(document.getElementById("table1"), query_table1, {
    user: userid,
  });

  bind_link(queryParameters);
  // Verander de Jira links naar een functie
  // Settimeout is nodig om een kleine vertraging te creëren zodat de DOM gereed is voor aanpassing.
  setTimeout(function () {
    $("#table1 tr").each(function (index) {
      if (index != 0) {
        var modelverzoek_uri = $(this).find("td:nth-child(1) a").attr("href");
        var jira_number = $(this).find("td:nth-child(1)").text();
        var graphuri = $(this).find("td:nth-child(4) a").attr("data-graphuri");
        $(this)
          .find("td:nth-child(1)")
          .html(
            '<a rel="data-link" entiteit="modelverzoeken" primary_key=\'{"modelverzoek_uri":"' +
              modelverzoek_uri +
              '", "named_graph":"' +
              graphuri +
              "\"}'>" +
              jira_number +
              "</a>"
          );
      }
    });
    var formParameters = Object;
    formParameters.verborgenFormulier = "N";
    formParameters.entiteit = "modelverzoek";
    maak_formulier(formParameters);
  }, 500);
  return false;
}
