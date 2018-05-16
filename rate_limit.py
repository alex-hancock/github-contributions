import requests
import getpass

from requests.auth import HTTPBasicAuth
print("Please enter your GitHub credentials for additional API calls.")
username = input("GitHub username: ")
password = getpass.getpass("GitHub password: ")
GITHUB_AUTH = HTTPBasicAuth('alex-hancock', password)

GITHUB_URL = "https://api.github.com"
request_obj = requests.get(GITHUB_URL + "/rate_limit", auth=GITHUB_AUTH)
print(request_obj.json())