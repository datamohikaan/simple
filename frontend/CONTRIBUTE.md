# API-endpoint development standards

## API Design Principles
- **Use Standard HTTP Status Codes**: Utilize HTTP status codes correctly to convey the outcome of API requests (e.g., `200 OK`, `404 Not Found`, `500 Internal Server Error`).
- **RESTful Design**: Use appropriate HTTP methods (GET for when data is requested, POST when the request creates something, PUT when the request updates something in-place, DELETE when a request deletes something) for operations.
- **Logging**: Log errors and relevant variables using either `app.logger.info()` or `ic()`, *not* `print()`.

## Routing
```python
@app.route("/kennisgebiedenregister/read/<table>", methods=["GET"])
def lees_kennisgebiedenregister(table: str):
```
- **Routing** Above is an example of endpoint-routing, the first line defines which path is made open for API calls. 
The second line defines which function is called at this endpoint. These both have to be unique across the app.
- **Methods** In the first line you also see the method GET, an endpoint should only receive one method type.
- **Naming convention** The naming convention is topic>action>resource, where topics can be nested such as ``Toetsingslogboek/Logs/...``, actions are CRUD operations such as `read`, `update` etc.
- **Topics** The topics are defined in `frontend/ep/mb-json-routes.json`
- **Route storage** All routes should be present in `frontend/ep/config.py` under `##################### FLASK ENDPOINTS #####################`. To have an overview of all available endpoints.
- **Dynamic Links** Above you can see that after read there is a variable <table>, 
- this can be seen as the input variable for the function. 
For example `/kennisgebiedenregister/read/domeinen>` will cause the same effect as a call to `lees_kennisgebiedenregister(domeinen)`
- **py_acties** Upon completing an action, the user should receive the next possible actions to be performed on this resource along with their paths. 
These are CRUD operations and are defined in `frontend/ep/mb-json-routes.json`


## Postgres mapping
In the `utils/constants.py` you will find `POSTGRES_MAPPING` this is a collection of all attributes and metadata about the 
tables stored in Postgres. For API development the relevant ones are;
- **MAPPING** this must contain every attribute. It links the attribute to its corresponding RDF-uri. Which contains standardised data-agreements and conventions that this attribute follows. This is needed for the Knowledge Graph, if you have to add a new attribute and dont know its RDF-URI, just put `attribute_name:attribute_name?` 
- **PRIMARY_KEY** this maps an attribute to be the primary key
- **ATTRIBUTES** this contains a list of each attribute along with its metadata. `type` stands for html element type, where 'hide' means it won't get shown to the frontend, `label` stands for the text on the webpage, `waarde` is the value inside. In case of a 'select'-type, `options` are the list of possible options.

## Input and Return values
### Input in GET-requests
- When using GET, the input values can be retrieved using `request.args.get(your_value, str)`. The GET values are always added to the HTTP URL, for example:
`127.0.0.1:5000/kennisgebiedenregister/read/medewerkers?uri=http://modellenbibliotheek.belastingdienst.nl/id/medewerker/dam0j01`. 
Here the `?uri=` with value `http://modellenbibliotheek.belastingdienst.nl/id/medewerker/dam0j01` is added to the base path of `127.0.0.1:5000/kennisgebiedenregister/read/medewerker`

### Input in POST, PUT-requests
- When using POST or PUT the input values are a FormData and can be retrieved using `upload_data = dict(request.form)`. 
This will create a dict from which you can retrieve the value of any key such as `upload_data['db_user']`

### Return values
- In our API the return value of an endpoint is always a jsonified dictionary along with a code. 
```python 
return jsonify({"error": "Geen velden om te wijzigen"}), 400 
```
```python 
return jsonify({"success": f"Update succesvol. {rows_updated} row(s) updated at {datetime.now()}"}), 200
```
- Try to always give *some* feedback back to the frontend, also when your code crashes. 
- Make sure to use the correct response codes, 200 for success, 500 for unexpected server-side errors, 
- and other codes can be found in https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

### Backend-Frontend Data contracts
To ensure quick development and proper coordination between Back- and Frontend we must decide on one convention for data-exchange.
This is in the directory `frontend/test/example_jsons`.
- This directory contains a map for each path in the API. 
- Inside the map you can find an example .curl file for the desired http-request input, aswell as an example .json file for the corresponding output.
- Your return values must be in line with the example in the Data Contract.
- This Data Contract can be used manually in Insomnia, where you can upload the .curl file and perform the HTTP-request.
- This Data Contract can also be used for automated testing in the future.


## Authorisation
There are three relevant mappings for authorisation,
1. `frontend/ep/mb-json-users.json` this maps each user to each usergroep
2. `frontend/ep/mb-json-groep.json` this contains data about each usergroep and contains the usermenu for each usergroep
3. `frontend/ep/config.py` this contains the protected pages and protected endpoints that each user has access to

before every request, the following code will run;
````python
# Global before request hook for checking role access
@app.before_request
def before(func_request=None):
    """
    Function requires 'usergroep' to have been defined in the app before being called it

    """
````
This function checks if the to-be accessed page and endpoint fall under UNACCESSIBLE_PAGES for this current user