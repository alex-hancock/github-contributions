import grequests as async
import requests
import datetime
import sys
import getpass

from requests.auth import HTTPBasicAuth
username = input("GitHub username:")
password = getpass.getpass("GitHub password: ")
GITHUB_AUTH = HTTPBasicAuth('alex-hancock', password)

USER = input("Please enter the username you'd like to search for: ")

today_date = datetime.date.today().isoformat()
since_date = str(int(today_date[0:4])-1) + today_date[4:]
days_hash = {day: 0 for day in create_daylist(since_date, today_date)}

#
# Initialize URLs
#
GITHUB_URL = "https://api.github.com"
REPOS_URL  = "/users/" + USER + "/repos?type=all"
ORG_URL = "/users/" + USER + "/orgs"
repo_url_list = []

def add_repo(repo_dict):
    # dictionary checking done in retry section
    repo_url_list.append(repo_dict["url"])

def issue_increment_days_hash(issue_dict):
    issue_user = issue_dict["user"]["login"]
    created_date = issue_dict["created_at"][:10]
    if created_date in days_hash and issue_user == USER:
        days_hash[created_date] += 1

def commit_increment_days_hash(commit_dict):
    commit_user = commit_dict["author"]["login"]
    created_date = commit_dict["commit"]["author"]["date"][:10]
    if created_date in days_hash and commit_user == USER:
        days_hash[created_date] += 1

def requests_with_retry(desired_url, dictionary_function):
    request_obj = requests.get(desired_url, auth=GITHUB_AUTH)

    if request_obj.status_code != 200:
        if request_obj.status_code == 409:
            # Encounter when repository is empty
            return
        else:
            print("Failure during request to {}".format(desired_url))
            print("Returned: {}".format(request_obj.json()))
            sys.exit(1)

    for request_dict in request_obj.json():
        dictionary_function(request_dict)

    if "Link" in request_obj.headers.keys():
        page_num = 2
        while "next" in request_obj.headers["Link"]:
            page_suffix = "&page=" if "?" in desired_url else "?page="
            request_obj = requests.get(desired_url + page_suffix + str(page_num), auth=GITHUB_AUTH)
            page_num += 1
            for request_dict in request_obj.json():
                dictionary_function(request_dict)

def create_daylist(since_date,today_date):
    today_obj = datetime.date(int(today_date[0:4]), int(today_date[5:7]), int(today_date[-2:]))
    since_obj = datetime.date(int(since_date[0:4]), int(since_date[5:7]), int(since_date[-2:]))

    delta = today_obj - since_obj
    thing = [since_obj + datetime.timedelta(days=i) for i in range(delta.days+1)]
    return [x.strftime("%Y-%m-%d") for x in thing]

#
# User owned/member repo request
#
print("Checking repositories of which", USER, "is either an owner or member...")
requests_with_retry(GITHUB_URL + REPOS_URL, add_repo)
print("Done!")

#
# Organizations they belong to, list their repos
#
print("Checking repositories of", USER, "organizations...")
org_request = requests.get(GITHUB_URL + ORG_URL, auth=GITHUB_AUTH)
for org_dict in org_request.json():
    requests_with_retry(org_dict["repos_url"], add_repo)
print("Done!")

#
# Collect issues
# 
print("Accounting for issues/pull requests...")
issue_suffix = "/issues?state=all&since=" + since_date
#issue_results = async_retrieve(repo_url_list, issue_suffix)
for repo_url in repo_url_list:
    requests_with_retry(repo_url + issue_suffix, issue_increment_days_hash)
print("Done!")

#
# Collect commits
#
print("Accounting for commits...")
commit_suffix = "/commits?author=" + USER + "&since=" + since_date
#commit_results = async_retrieve(repo_url_list, commit_suffix)
for repo_url in repo_url_list:
    requests_with_retry(repo_url + commit_suffix, commit_increment_days_hash)
print("Done!")

contribution_list = days_hash.values()
print(contribution_list)