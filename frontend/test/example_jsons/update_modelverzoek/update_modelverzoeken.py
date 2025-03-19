import requests

url = "http://127.0.0.1:5000/kennisgebiedenregister/lees/modelverzoeken"

querystring = {"jira_number":"SD001"}

payload = {"jira_number": "SD001"}
headers = {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/10.0.0"
}

response = requests.request("GET", url, json=payload, headers=headers, params=querystring)

print(response.text)