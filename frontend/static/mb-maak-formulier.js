function maak_formulier(formParameters) {
  // haal het formulier op
  $("#melding").html("");

  if (formParameters.verborgenFormulier == "J") {
    // verborgen formulier
    var data = "";
    var prefix = "";
    $.each(JSON.parse(formParameters.primary_key), function (key, val) {
      data = data + prefix + key + "=" + val;
      prefix = "&";
    });

    $.ajax({
      url: "/" + formParameters.entiteit + "/read",
      type: "GET",
      data: data,
      async: false,
      success: function (data) {
        if (data.resultaat == "OK") {
          toon_formulier(data, formParameters);
        }
      },
    });
  } else if (formParameters.verborgenFormulier == "F") {
    // haal het formulier op
    var data = "";
    $.ajax({
      url: "/" + formParameters.entiteit + "/read",
      type: "GET",
      data: data,
      async: false,
      success: function (data) {
        if (data.resultaat == "OK") {
          $("#melding").css("color", "green");
          $("#melding").text(data.opmerking);
          toon_formulier(data, formParameters);
        } else {
          $("#melding").css("color", "red");
          $("#melding").text(data.opmerking);
        }
      },
    });
  } else {
    // wanneer er op een link wordt geklikt, haal het formulier op
    $("a[rel=data-link]").click(function (e) {
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
      DEBUG && console.log('some link has been clicked inside this form ' + entiteit + ': ' + primary_key);
      $.ajax({
        url: "/" + entiteit + "/read",
        type: "GET",
        data: data,
        async: false,
        success: function (data) {
          if (data.resultaat == "OK") {
            $("#melding").css("color", "green");
            $("#melding").text(data.opmerking);
            toon_formulier(data, formParameters);
          } else {
            $("#melding").css("color", "red");
            $("#melding").text(data.opmerking);
          }
        },
      });
    });
  }
}

function toon_formulier(data, formParameters) {
  DEBUG && console.log('toon_formulier entered')
  DEBUG && console.log(data);
  DEBUG && console.log('formParameters.verborgenFormulier = ' + formParameters.verborgenFormulier);
  DEBUG && console.log('formParameters.entiteit = ' + formParameters.entiteit);
  DEBUG && console.log('formParameters.primary_key = ' + formParameters.primary_key);


  formulier = "";
  var upload_attribuut = "";

  if (formParameters.verborgenFormulier == "J") {
    lijn = "<hr/>";
    stijl = 'style="display: none;" class="overlay"';
    formulier += '<div id="mbk-toon-formulier-button">';
    formulier +=
      '<button class="btn btn-primary mt-3" rel="mbk-toon-formulier">Upload ' +
      formParameters.entiteit.replace("_", " ") +
      "</button>";
    formulier += "</div>";
  } else {
    lijn = "";
    stijl = "";
    $("table#table1").hide();
  }
  formulier += lijn;
  formulier += '<div id="mbk-gebruiker-acties">';

  $.each(data.gebruiker_acties, function (key, value) {
    formulier +=
      '<button class="btn btn-primary mt-3 mbk-button" id="' +
      value +
      '" rel="mbk-button" actie="' +
      value +
      '">' +
      key +
      " " +
      formParameters.entiteit.replace("_", " ") +
      "</button> ";
  });

  formulier += "</div>";
  formulier +=
    '<form id="mbk-form"' +
    stijl +
    ' name="formulier" method="POST" enctype="multipart/form-data">';

  // Add hidden form fields for sending the primary_key to backend without showing it as formfield in frontend
  if (formParameters.primary_key){
      var primaryKeyData = JSON.parse(formParameters.primary_key);
      $.each(primaryKeyData, function (key, val) {
        formulier += '<input type="hidden" name="' + key + '" value="' + val + '" />';
      });
  }

  $(data.input_element).each(function () {
    var attribuut = this.attribuut;
    var type = this.type;
    var label = this.label;
    var waarde = this.waarde;
    var regexplanation = this.regexplanation;
    DEBUG && console.log('regexplanation: ' + regexplanation)
    if (typeof regexplanation === "undefined") {
      regexplanation = "";
    }
    var regex = this.regex
    if (typeof regex === "undefined") {
      regex = "";
    }
    if (typeof waarde === "undefined") {
      waarde = "";
    }
    var link = this.link;
    if (typeof link === "undefined") {
      link = "";
    }
    var verplicht = this.verplicht;
    if (typeof verplicht === "undefined") {
      verplicht = "";
    }
    if (verplicht == "required") {
      label = label + " *";
    }

    if (type == "display") {
      formulier +=
        '<div class="form-group"><label for="' +
        attribuut +
        '">' +
        label +
        '</label> <div class="form-control-plaintext">' +
        waarde +
        "</div></div>";
    }
    else if (type == "link") {
      formulier +=
        '<div class="form-group"><label for="' +
        attribuut +
        '">' +
        label +
        '</label> <a href="' +
        link +
        '" class="form-control">' +
        waarde +
        "</a></div>";
    }
    else if (type == "select") {
      formulier +=
        '<div class="form-group"><label for="' +
        attribuut +
        '">' +
        label +
        '</label> <select class="form-select" name="' +
        attribuut +
        '" id="' +
        attribuut +
        '" value="' +
        waarde +
        '">';
      $.each(this.opties, function (key, val) {
        formulier += '<option value="' + key + '"';
        if (val == waarde) {
          formulier += " selected";
        }
        formulier += ">" + val + "</option>";
      });
      formulier += "</select></div>";
    }
    else if (type == "input-text") {
      formulier +=
        '<div class="form-group"><label for="' +
        attribuut +
        '">' +
        label +
        '</label> <input type="text" class="form-control" name="' +
        attribuut +
        '" id="' +
        attribuut +
        '" value="' +
        waarde +
        '" ' +
        verplicht +
        + (regex ? ' pattern="' + regex + '"' : '') +
        + (regexplanation ? ' regexplanation="' + regexplanation + '"' : '') +

        " /></div>";
        // Add validation script after input
        if (regex) {
        formulier += `<script>
            document.getElementById('${attribuut}').addEventListener('input', function() {
              var pattern = new RegExp('${regex}');
              if (!pattern.test(this.value)) {
                this.setCustomValidity('Ongeldige invoer. Dit veld verwacht: ${regexplanation};');
              } else {
                this.setCustomValidity('');
              }
            });
          </script>`;
        }
    }
    else if (type == "input-file") {
      formulier +=
        '<div class="form-group"><label for="' +
        attribuut +
        '">' +
        label +
        '</label> <div><input type="file" class="form-control" name="' +
        attribuut +
        '" id="' +
        attribuut +
        '" value="' +
        waarde +
        '" ' +
        verplicht +
        " />";
      if (waarde != null && waarde != "") {
        formulier +=
          '<div class="mb-input-file-tekst">Vervangt huidige model upload: ' +
          waarde +
          "</div>";
      }
      else {
         formulier +=
          '<div class="mb-input-file-tekst"> Er is nog geen model geupload' +
          waarde +
          "</div>";
      }
      formulier += "</div></div>";
      upload_attribuut = attribuut;
    }
    else if (type == "input-textarea") {

      // below code not working yet
//
//      $("form#query-dienst").submit(function (e) {
//        e.preventDefault();
//        alert('query-dienst');
//
//        var formData = new FormData(this);
//        formData.set("sparqlQuery", yasqe.getValue());
//        formData.append("userid", userid);
//
//        $.ajax({
//          url: "/querydienst",
//          type: "POST",
//          data: formData,
//          cache: false,
//          contentType: false,
//          processData: false,
//          beforeSend: function () {},
//          success: function (data) {
//            $("#query_resultaat").text(data).show();
//          },
//        });
//      });

//       formulier +=
//         '<div class="form-group"><label for="' +
//         attribuut +
//         '">' +
//         label +
//         '</label> <div name="' +
//         attribuut +
//         '" id="' +
//         "yasqe" +
//         '" '+
//         verplicht +
//         '>' +
//         waarde +
//         "</div></div>";

      //untill here not working yet

       formulier +=
         '<div class="form-group"><label for="' +
         attribuut +
         '">' +
         label +
         '</label> <textarea class="form-control" name="' +
         attribuut +
         '" id="' +
         attribuut +
         '" rows="10" cols="80" '+
         verplicht +
         '>' +
         waarde +
         "</textarea></div>";

        DEBUG && console.log("verplicht is: " + verplicht) // waarom is de inhoud van verplicht 'readonly=""'?
      } else if (type == "button") {
        formulier +=
          '<div class="form-group"><label for="' +
          link +
          '">' +
          '</label> <button class="btn btn-primary mt-3 mbk-button" id="' +
          link +
          '" rel="mbk-button" actie="' +
          link +
          '">' +
          label +
          " " +
          "</button> " +
          "</div>";
      } else {
      formulier +=
        '<div class="form-group"><label for="' +
        attribuut +
        '">' +
        label +
        '</label> <span style="font-weight: bold; color: red;">type ' +
        type +
        " heeft geen opmaak !!!!</span></div>";
    }
  });
  formulier += "<div>";

  ButtonTeller = 0;
  $.each(data.py_acties, function (key, value) {
    var buttonText = maak_buttontext(key, value);
    ButtonTeller++;
    if (ButtonTeller == 1) {
      // De eerste button is de submit button
      formulier +=
        '<button id="mbk-button" type="submit" name="formulier" class="btn btn-primary mt-3" actie="' +
        value +
        '">' +
        buttonText +
        "</button> ";
    } else {
      // Alle overige buttons luisteren naar "mbk-button"
      formulier +=
        '<button class="btn btn-primary mt-3" rel="mbk-button" actie="' +
        value +
        '">' +
        buttonText +
        "</button> ";
    }
  });

  if (formParameters.verborgenFormulier == "J") {
    formulier +=
      '<button class="btn btn-secondairy mt-3" rel="mbk-verberg-formulier" actie="annuleren">Terug naar overzicht</button> ';
  } else {
    formulier +=
      '<button class="btn btn-secondairy mt-3" rel="mbk-annuleren" actie="annuleren">Terug naar overzicht</button> ';
  }
  formulier += '</div></form><table class="table" id="table2"></table>';
  $("div#mbk-sub").html(formulier);
  
  // 1. Get the content (waarde) of the textarea
  const textareaElement = document.getElementById("sparql_query");
  if (textareaElement != null){
    const waarde = textareaElement.value; // Get the value
    DEBUG && console.log("textareaelement: " + textareaElement.outerHTML);

    // 2. Replace the textarea with an empty div
    const newDiv = document.createElement("div");
    newDiv.id = "sparql_query"; // Keep the same ID
    textareaElement.replaceWith(newDiv);

    // 3. Initialize Yasqe on the new div
    const yasqe = new Yasqe(document.getElementById("sparql_query"), {
      showQueryButton: false,
    });

    // 4. Put the saved 'waarde' into yasqe,
    yasqe.setValue(waarde);

    // 5. add input element so it can be recognized by the form
    const hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "sparql_query"; // Use the same 'name' as the original textarea
    hiddenInput.id = "sparql_query_hidden"; // Give it a unique ID
    newDiv.parentNode.insertBefore(hiddenInput, newDiv.nextSibling);

    // Update the hidden input whenever Yasqe's content changes
    yasqe.on("change", function () {
        hiddenInput.value = yasqe.getValue();
    });

    // Initialize the hidden input with the current value
    hiddenInput.value = yasqe.getValue();

    // 6. Set readOnly if the original textarea had 'readonly'
    if (textareaElement.outerHTML.includes("readonly")) {
      yasqe.setOption("readOnly", "true");
      yasqe.getWrapperElement().classList.add("yasqe-disabled"); // Add disabled class
    }

  }
  else{
    DEBUG && console.log("do nothing");
  }
  bind_buttons(data.py_acties);

  function bind_buttons(py_actie) {
    $("[rel=mbk-annuleren]").click(function (e) {
      e.preventDefault();
      $("#melding").html("");
      $("div#mbk-sub").html("");
      $("table#table1").show();
      $("div#mbk-tabel").show();
      var tabelParameters = Object;
      DEBUG && console.log('entiteit is: ' + formParameters.entiteit);
      tabelParameters.entiteit = formParameters.entiteit;
      maak_tabel(tabelParameters);
    });

    $("form#mbk-form").submit(function (e) {
      e.preventDefault();
      actie = $("#mbk-button").attr("actie");
      var formData = new FormData(document.getElementById("mbk-form"));
      if (upload_attribuut != "") {
        var fileInput = $("#" + upload_attribuut)[0];
        formData.append(upload_attribuut, fileInput.files[0]);
      }
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
          document.getElementById("mbk-button").style.background = "orange";
        },
        success: function (data) {
          DEBUG && console.log("data: " + data);
          if (data.resultaat == "OK") {
            document.getElementById("mbk-button").style.background = "green";
            $("#melding").css("color", "green");
            DEBUG && console.log('verberg formulier')
          }
          else {
            $("#melding").css("color", "red");
            document.getElementById("mbk-button").style.background = "red";
          }
          $("#melding").text(data.opmerking);

        },
      });
      return false;
    });

    $("[rel=mbk-button]").click(function (e) {
      e.preventDefault();
      actie = $(this).attr("actie");
      const btn = document.getElementById(this);
      var formData2 = new FormData();
      $(data.input_element).each(function () {
        var attribuut = this.attribuut;
        var element = $("#" + attribuut);

        if (attribuut === "sparql_query") { // Check if it's the Yasqe div
            DEBUG && console.log("we are now in yasqe and the val is: " + $("#" + attribuut + "_hidden").val());
            formData2.append(attribuut, $("#" + attribuut + "_hidden").val()); // Retrieve value from hidden input
        } else {
            formData2.append(attribuut, element.val()); // Use standard .val() for other inputs
        }
      });

      if (upload_attribuut != "") {
        var fileInput = $("#" + upload_attribuut)[0];
        formData2.append(upload_attribuut, fileInput.files[0]);
      }
      formData2.append("userid", userid);
      $("#melding").html("");
      $.ajax({
        url: actie,
        type: "POST",
        data: formData2,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function () {
          document.getElementById(actie).style.background = "orange";
        },
        success: function (data) {
          DEBUG && console.log('actie button succes: ' + actie);

          DEBUG && console.log(data);
          if (data.resultaat == "OK") {
            document.getElementById(actie).style.background = "green";
            $("#melding").css("color", "green");
            $("#melding").html(data.opmerking);

            // below code inserted by suley
            // Goal: automatisch de lijst-pagina verversen als je hebt opgeslagen en teruggaat
//            DEBUG && console.log('we zitten in de return-call van een modelverzoek indienen1')
//
//            $("#melding").css("color", "green").html(
//            data.opmerking.replace(/\n/g, "<br>").replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;")
//            );
//            $("#melding").css({
//              "white-space": "pre-wrap",
//              "color": "red",
//            }).text(data.opmerking);

//            // new code experiment inserted by suley:
//            DEBUG && console.log('we zitten in de succes+OK van een actie button')
//            $("table#table1").show();
//            $("div#mbk-tabel").show();
//            var tabelParameters = Object;
//
//            DEBUG && console.log('entiteit is: ' + formParameters.entiteit);
//            tabelParameters.entiteit = formParameters.entiteit;
//            maak_tabel(tabelParameters);

//              DEBUG && console.log('we zitten in de succes+OK van een actie button en voeren annuleren functies uit')

//              e.preventDefault();
//              $("#melding").html("");
//              $("div#mbk-sub").html("");
//              $("table#table1").show();
//              $("div#mbk-tabel").show();
//              var tabelParameters = Object;
//
//              DEBUG && console.log('entiteit is: ' + formParameters.entiteit);
//              DEBUG && console.log('actie is: ' + actie);
//
//              tabelParameters.entiteit = formParameters.entiteit;
//              maak_tabel(tabelParameters);
//              DEBUG && console.log('actie is: ' + actie);
//
//              $("[rel=mbk-annuleren]").click();
//            // tot hier is inserted

            if (actie='') {
              var tabelParameters = Object;
              DEBUG && console.log('entiteit is: ' + formParameters.entiteit);
              tabelParameters.entiteit = formParameters.entiteit;
              maak_tabel(tabelParameters);
            } else {
              toon_formulier(data, formParameters);
            }
          }
          else if (data.resultaat == "SR") {
            document.getElementById(actie).style.background = "green";
            // $("div#form-resultaat").html(data.opmerking); niet meer van toepssing
            rdflib.fetchData(document.getElementById("table2"), data.sparql_query, {
              graph: data.model,
            });


          }
          else {
            document.getElementById(actie).style.background = "red";
            $("#melding").css("color", "red");
            $("#melding").html(data.opmerking);
          }
        },
      });
      return false;
    });

    $("[rel=mbk-toon-formulier]").click(function (e) {
      e.preventDefault();
      $("#mbk-toon-formulier-button").hide();
      $("#mbk-form").show();
    });

    $("[rel=mbk-verberg-formulier]").click(function (e) {
      e.preventDefault();
      $("#mbk-form").hide();
      $("#mbk-toon-formulier-button").show();
    });
  }

  function maak_buttontext(key, data) {
    var buttonText = key;
    if (key == "create") buttonText = "Opslaan " + formParameters.entiteit.replace("_", " ");
    if (key == "update") buttonText = "Wijzigen " + formParameters.entiteit.replace("_", " ");
    if (key == "delete") buttonText = "Verwijderen " + formParameters.entiteit.replace("_", " ");
    if (key == "upload") buttonText = "Indienen " + formParameters.entiteit.replace("_", " ");
    return buttonText;
  }
}
