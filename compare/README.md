export sourcesuleymo="/Users/boscp08/src/Projects/bitbucket-bd/mbk-frontend"
export targetsuleymo='/Users/boscp08/src/Projects/github-cloud/mbk-frontend-mde'
export mdeconfig='/Users/boscp08/src/Projects/gitlab-pi8/mbk-frontend-20240723-bb'

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   frontend/app.py
	modified:   frontend/turtle_creator.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	transformation/tr_transformer.py
	validation/tr_validator.py

   # 1. Transform file into .ttl AND insert this ttl into Fuseki
    def transform_turtle_and_create_model_fuseki(file_content_bytes, model_type):
        # (The combination of DELETE+INSERT is equal to an update of the whole graph in Fuseki)

        ## Pre-work for the transformation
        dir_path = tempfile.mkdtemp()

        input_file_path = os.path.join(dir_path, file_name)
        print(input_file_path)
        with open(input_file_path, "wb") as f:
            f.write(file_content_bytes)

            # Transformation
            ## ALSO INSERTS THE NEW .ttl QUAD IN FUSEKI
            # Transformation in code
            try:
                turtle_creator = TurtleCreator([fr"{input_file_path}"], model_type=model_type)
                turtle_creator.create_turtle()

            #     Transformation in subprocess
            #     result = subprocess.run(
            #         [
            #             "python",
            #             "-c",
            #             # f'from frontend.turtle_creator import TurtleCreator; turtle_creator = TurtleCreator([r"{input_file_path}"]); turtle_creator.create_turtle(); print("VDA naam = ", turtle_creator.get_vda_model_name()); print("yml = ", turtle_creator.get_yml_data())'
            #             f'from frontend.turtle_creator import TurtleCreator; turtle_creator = TurtleCreator([r"{input_file_path}"]); turtle_creator.create_turtle(); print("VDA naam = ", turtle_creator.get_vda_model_name())',
            #         ],
            #         capture_output=True,
            #         text=True,
            #     )
            #
            #     assert result.returncode == 0
            #     app.logger.info(f"TTL-TRANSFORMATION SUCCES: {result.returncode}")
            # except AssertionError as e:
            #     app.logger.info(result.returncode)
            #     app.logger.info(result.stdout)
            #     app.logger.info(e)
            #     return jsonify(
            #         {
            #             "error": f"Er is iets misgegaan bij de ttl-transformatie van het bestand. Weet je zeker dat je een BMS of Powerdesigner LDM bestand hebt gekozen?"}), 400
            # TODO: delete comments above if you see this after december 2024

            except Exception as e:
                app.logger.exception(f"ERROR: An exception occurred:\n{traceback.format_stack()}")

                melding = f"Er is iets misgegaan bij de ttl-transformatie van het bestand. Weet je zeker dat je een BMS of Powerdesigner LDM bestand hebt gekozen?"
                melding_manager.meld(ms.ERROR, melding)

        return str(turtle_creator.uri), turtle_creator.get_vda_model_name()

    transform_turtle_and_create_model_fuseki(file_content_bytes, 'TRT')
    







def one_time_add_table_toetsingsrapport_to_database():
    query = cn.POSTGRES_MAPPING['toetsingsrapport'][cn.CREATE_QUERY] #TODO: REMOVE DROP TABLE WHEN MOVING TO DEVELOP
    try:
        db_connection = psycopg2.connect(**config.DB_CONFIG)
        db_cursor = db_connection.cursor()
        db_cursor.execute(query)
        db_connection.commit()
    except Exception as e:
        app.logger.exception(f"ERROR: An exception occurred:\n{traceback.format_stack()}")


one_time_add_table_toetsingsrapport_to_database() #TODO: REMOVE DROP TABLE WHEN MOVING TO DEVELOP



```

@app.route("/toetsingsrapport/upload", methods=["POST"])
@add_melding_manager
def upload_toetsingsrapport(melding_manager, table='toetsingsrapport'):
    py_acties = {key: value for key, value in routes['py_acties'][table].items()}
    primary_key_attribute = cn.POSTGRES_MAPPING[table][cn.PRIMARY_KEYS][0]
    upload_data = dict(request.form)
    try:
        primary_key = upload_data[primary_key_attribute]
        #primary_key = [request.args.get(key) for key in request.args][0]
    except Exception as e:
        error_msg = f"No primary_key found in query_params, make sure to add it to the formData"
        melding_manager.meld(ms.ERROR, error_msg)
        return jsonify({
            "opmerking": f"No primary_key found in query_params, make sure to add it to the formData"}), 200

    # upload_data = dict(request.form)
    # load binary_data to file_content_bytes
    # todo: should be an assertion instead of an if
    if 'binary_data' in request.files \
            and request.files['binary_data'].filename != '' and request.files['binary_data'] != 'undefined':
        app.logger.info('binary_data in request.files and request.files[\'binary_data\'].filename != empty')
        # Retrieve the file from the request
        file = request.files['binary_data']

        file_name = file.filename.replace(" ", "_")
        file_extension = "." + file_name.split(".")[-1:][0]
        file_title = file_name.replace(file_extension, "")
        file_content_bytes = file.read()
        required_file_extension_start = ".xl"

        if not file_extension.startswith(required_file_extension_start):
            error_msg = f"Het formaat van het aangeleverd bestand ({file_extension}) voldoet niet. Alleen een Excel conform het SBM formaat ({required_file_extension_start}*) is toegestaan."
            melding_manager.meld(ms.ERROR, error_msg)
            return jsonify(
                {"opmerking": error_msg}), 200

    else:
        error_msg = f"Geen bestand ontvangen"
        melding_manager.meld(ms.ERROR, error_msg)
        return jsonify(
            {"error": error_msg}), 200

    db_connection = psycopg2.connect(**config.DB_CONFIG)
    db_cursor = db_connection.cursor()
    with db_cursor:
        # TODO: db_cursor.execute(create_table_query) optional, todo, if going to new environment/production
        query = f"""
            {cn.POSTGRES_MAPPING[table][cn.INSERT_QUERY]}
          """
        values = [primary_key, file_content_bytes, file_name]

        #        AND bd_user = '{username}'
        app.logger.info(f"query = {query}")
        #app.logger.info(f"values = {values}") toomuch

        try:
            db_connection = psycopg2.connect(**config.DB_CONFIG)
            db_cursor = db_connection.cursor()
            db_cursor.execute(query, values)
            # Check the number of updated rows
            rows_updated = db_cursor.rowcount
            db_connection.commit()
            db_cursor.close()
            db_connection.close()

        except Exception as e:
            app.logger.exception(f"{e}: {traceback.format_exc()}")
            error_msg = f"\nOploaden toetsingsrapport mislukt.\nDe inhoud van het toetsingsrapport '{file_name}' kon niet worden opgehaald. Controleer of de inhoud van het bestand klopt. Mocht de fout zich blijven herhalen, dan kunt u hiervan een melding maken zodat het beheerteam u verder kan helpen."
            melding_manager.meld(ms.ERROR, error_msg)
            return jsonify({
                "resultaat": "ERROR",
                "opmerking": error_msg,
                "py_acties": py_acties,
                "titel": f"Upload toetsingsrapport",
            }), 200

    # 1. Transform file into .ttl AND insert this ttl into Fuseki
    def transform_turtle_and_create_model_fuseki(file_content_bytes, model_type):
        # (The combination of DELETE+INSERT is equal to an update of the whole graph in Fuseki)

        ## Pre-work for the transformation
        dir_path = tempfile.mkdtemp()

        input_file_path = os.path.join(dir_path, file_name)
        print(input_file_path)
        with open(input_file_path, "wb") as f:
            f.write(file_content_bytes)

            # Transformation
            ## ALSO INSERTS THE NEW .ttl QUAD IN FUSEKI
            # Transformation in code
            try:
                turtle_creator = TurtleCreator([fr"{input_file_path}"], model_type=model_type)
                turtle_creator.create_turtle()

            #     Transformation in subprocess
            #     result = subprocess.run(
            #         [
            #             "python",
            #             "-c",
            #             # f'from frontend.turtle_creator import TurtleCreator; turtle_creator = TurtleCreator([r"{input_file_path}"]); turtle_creator.create_turtle(); print("VDA naam = ", turtle_creator.get_vda_model_name()); print("yml = ", turtle_creator.get_yml_data())'
            #             f'from frontend.turtle_creator import TurtleCreator; turtle_creator = TurtleCreator([r"{input_file_path}"]); turtle_creator.create_turtle(); print("VDA naam = ", turtle_creator.get_vda_model_name())',
            #         ],
            #         capture_output=True,
            #         text=True,
            #     )
            #
            #     assert result.returncode == 0
            #     app.logger.info(f"TTL-TRANSFORMATION SUCCES: {result.returncode}")
            # except AssertionError as e:
            #     app.logger.info(result.returncode)
            #     app.logger.info(result.stdout)
            #     app.logger.info(e)
            #     return jsonify(
            #         {
            #             "error": f"Er is iets misgegaan bij de ttl-transformatie van het bestand. Weet je zeker dat je een BMS of Powerdesigner LDM bestand hebt gekozen?"}), 400
            # TODO: delete comments above if you see this after december 2024

            except Exception as e:
                app.logger.exception(f"ERROR: An exception occurred:\n{traceback.format_stack()}")

                melding = f"Er is iets misgegaan bij de ttl-transformatie van het bestand. Weet je zeker dat je een BMS of Powerdesigner LDM bestand hebt gekozen?"
                melding_manager.meld(ms.ERROR, melding)

        return str(turtle_creator.uri), turtle_creator.get_vda_model_name()

    transform_turtle_and_create_model_fuseki(file_content_bytes, 'TRT')

    melding_manager.meld()
    return jsonify({
        "resultaat": "OK",
        "opmerking": "Gegevens succesvol opgeslagen.",
        "py_acties": py_acties,
        "titel": f"Upload toetsingsrapport",
    }), 200

```