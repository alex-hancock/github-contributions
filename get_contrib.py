import grequests as async
import requests
import datetime

def async_retrieve(repo_url_list, suffix):
    amended_url_list = [url + suffix for url in repo_url_list]
    async_requests = (async.get(url, stream=False) for url in amended_url_list)
    return async.map(async_requests)

def create_daylist(since_date,today_date):
    today_obj = datetime.date(int(today_date[0:4]), int(today_date[5:7]), int(today_date[-2:]))
    since_obj = datetime.date(int(since_date[0:4]), int(since_date[5:7]), int(since_date[-2:]))

    delta = today_obj - since_obj
    thing = [since_obj + datetime.timedelta(days=i) for i in range(delta.days+1)]
    return [x.strftime("%Y-%m-%d") for x in thing]

today_date = datetime.date.today().isoformat()
since_date = str(int(today_date[0:4])-1) + today_date[4:]
days_hash = {day: 0 for day in create_daylist(since_date, today_date)}

# Change how USER is passed at some point...
USER = "jvivian"

#
# Initialize URLs
#
GITHUB_URL = "https://api.github.com"
REPOS_URL  = "/users/" + USER + "/repos?type=all"
ORG_URL = "/users/" + USER + "/orgs"
repo_url_list = []

#
# User owned/member repo request
#
repo_request = requests.get(GITHUB_URL + REPOS_URL)
for repo_dict in repo_request.json():
    # Comment for sublime collapse
    repo_url_list.append(repo_dict["url"])
if "Link" in repo_request.headers:
    page_num = 2
    while "next" in repo_request.headers["Link"]:
        repo_request = requests.get(GITHUB_URL + REPOS_URL + "&page=" + str(page_num))
        page_num += 1
        for repo_dict in repo_request.json():
            repo_url_list.append(repo_dict["url"])

#
# Organizations they belong to, list their repos
#
org_request = requests.get(GITHUB_URL + ORG_URL)
for org_dict in org_request.json():
    org_repos_url = org_dict["repos_url"]
    org_repo_request = requests.get(org_repos_url)
    for repo_dict in org_repo_request.json():
        repo_url_list.append(repo_dict["url"])

    if "Link" in org_repo_request.headers:
        page_num = 2
        while "next" in org_repo_request.headers["Link"]:
            org_repo_request = requests.get(org_repos_url + "?page=" + str(page_num))
            page_num += 1
            for repo_dict in org_repo_request.json():
                repo_url_list.append(repo_dict["url"])


# 
issue_suffix = "/issues?state=all&since=" + since_date
#issue_results = async_retrieve(repo_url_list, issue_suffix)
for repo_url in repo_url_list:
    # for each repo url, get repos issues
    issue_request = requests.get(repo_url + issue_suffix)
    for issue_dict in issue_request.json():
        issue_user = issue_dict["user"]["login"]
        created_date = issue_dict["created_at"][:10]
        print("{} created an issue on {}".format(issue_user, created_date))
        

for issue_request in issue_results:
    print(issue_request.headers)
    break

import sys
sys.exit(0)

# by the API, pull requests SHOULD be integrated as issues, so we don't care about these

# get commits since date with USER as author
# https://developer.github.com/v3/repos/commits/#get-a-single-commit
commit_suffix = ""
#commit_results = async_retrieve(repo_url_list, commit_suffix)
