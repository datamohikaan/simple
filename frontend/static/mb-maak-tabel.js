function maak_tabel(tabelParameters) {
  DEBUG && console.log('maak_tabel entered');
  DEBUG && console.log('tabelParameters = ' + tabelParameters);

  var entiteit = tabelParameters.entiteit;
  var mb_local = "N"; // Test van René, nog niet verwijderen.

  $("#melding").html("");

  // haal de tabel op
  if (mb_local == "J") {
    $.ajax({
      url: py_prefix + "mb-scherm-queries.json",
      dataType: "json",
      async: false,
      success: function (data) {
        if (data.resultaat == "OK") {
          toon_tabel(data);
        }
      },
    });
  } else {
    $.ajax({
      url: "/" + entiteit + "/all",
      type: "GET",
      async: false,
      success: function (data) {
        if (data.resultaat == "OK") {
          DEBUG && console.log("data inside maak tabel");
          DEBUG && console.log(data);

          data.graph_uri = tabelParameters.graph_uri;
          toon_tabel(data);
        }
      },
    });
  }

  function toon_tabel(data) {
    DEBUG && console.log('toon_tabel entered')
    DEBUG && console.log(data);
    let graph_uri = data.graph_uri;
    $("#main-block-kop").html("Overzicht " + entiteit.replace("_", " ").replace("/"," "));
    tabel = "";

    tabel += '<div id="mbk-gebruiker-acties">';
    $.each(data.gebruiker_acties, function (key, value) {
      tabel +=
        '<button class="btn btn-primary mt-3 mbk-button" id="' +
        value +
        '" rel="mbk-button" actie="' +
        value +
        '">' +
        key +
        "</button> ";
    });
    tabel += "</div>";

    tabel += '<table class="table">';
    tabel += "<thead>";
    tabel += "<tr>";
    aantal_kolommen = 0;
    $.each(data.kolommen, function (key, val) {
      aantal_kolommen++;
      tabel += "<th>" + val + "</th>";
    });
    tabel += "</tr>";
    tabel += "</thead>";

    tabel += "<tfoot>";
    tabel += '<tr colspan="' + aantal_kolommen + '">';
    tabel += "</tr>";
    tabel += "</tfoot>";

    tabel += "<tbody>";
    $.each(data.input_regels, function (regelnummer, regel) {
      tabel += '<tr rij="' + regelnummer + '">';
      $(regel).each(function () {
        var attribuut = this.attribuut;
        var waarde = this.waarde;
        if (typeof waarde === "undefined") {
          waarde = "";
        }
        var link = this.link;
        if (typeof link === "undefined") {
          link = "";
        }
        if (link != "") {
          tabel +=
            '<td><a rel="data-link" entiteit="' +
            entiteit +
            '" primary_key=\'{"' +
            entiteit +
            '_id":"' +
            link +
            "\"}'>" +
            waarde +
            "</a></td>";
        } else {
          tabel += "<td>" + waarde + "</td>";
        }
      });
      tabel += "</tr>";
    });
    tabel += "</tbody>";
    tabel += "</table>";
    tabel += '<div id="form_resultaat"></div>';

    if (!$("div#mbk-tabel").length) {
       $("#main-block-inhoud").append('<div id="mbk-tabel"></div>');
    }
    $("div#mbk-tabel").html(tabel);
    $("div#mbk-tabel").show();

    $("a[rel=data-link]").click(function (e) {
    entiteit = $(this).attr("entiteit");
    // Code to make the rapportage_query table dynamically
    if (entiteit.toLowerCase().startsWith("rapportage_query/")) {
        DEBUG && console.log("Entered maak_tabel for query_rapportage");
        e.preventDefault();

        var primary_key_object = JSON.parse($(this).attr("primary_key"));
        var rapportage_query_id = Object.values(primary_key_object)[0];

        DEBUG && console.log("rapportage_query_id  = " + rapportage_query_id);
        DEBUG && console.log("graphuri = " + graph_uri);

        var queryParameters = Object;
        queryParameters.rapportage_query_id = rapportage_query_id;
        queryParameters.graph_uri = graph_uri;

        nav_toetsing_Querier(queryParameters);


    } else {
        DEBUG && console.log($(this).attr("entiteit"));
        e.preventDefault();
        $("#melding").html("");
        var primary_key = $(this).attr("primary_key");
        var data = "";
        var prefix = "";
        $.each(JSON.parse(primary_key), function (key, val) {
            data = data + prefix + key + "=" + val;
            prefix = "&";
        });
        var entiteit = $(this).attr("entiteit");
        $("#melding").html("");
        $.ajax({
            url: "/" + entiteit + "/read",
            type: "GET",
            data: data,
            async: false,
            success: function (data) {
                if (data.resultaat == "OK") {
                    DEBUG && console.log('query rapportage link succes1 ' + entiteit + ': ' + primary_key);
                    $("#melding").css("color", "green");
                    $("#melding").text(data.opmerking);
                    $("div#mbk-tabel").hide();
                    $("div#mbk-sub").show();
                    toon_formulier(data, tabelParameters);
                    //toon_tabel(data);
                } else {
                    $("#melding").css("color", "red");
                    $("#melding").text(data.opmerking);
                }
                bind_buttons(data.py_acties); //moved bind_buttons inside the success function
            }, //Correct placement of the success function closing bracket.
        });
    }
    });

    bind_buttons(data.py_acties);

  }
  function bind_buttons(py_actie) {
    $("[rel=mbk-button]").click(function (e) {
      e.preventDefault();
      actie = $(this).attr("actie");
      const btn = document.getElementById(this);
      var formData = new FormData();
      formData.append("userid", userid);
      $("#melding").html("");
      $.ajax({
        url: actie,
        type: "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function () {
          document.getElementById(actie).style.background = "orange";
        },
        success: function (data) {
          DEBUG && console.log(data);
          if (data.resultaat == "OK") {
            document.getElementById(actie).style.background = "green";
            $("#melding").css("color", "green");
            $("div#mbk-tabel").hide();
            $("div#mbk-sub").show();
            toon_formulier(data, tabelParameters);
          } else {
            document.getElementById(actie).style.background = "red";
            $("#melding").css("color", "red");
          }
          $("#melding").html(data.opmerking);
        },
      });
      return false;
    });
  }
}
