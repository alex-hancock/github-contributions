import requests
import datetime

'''
Fetch contributions of a GitHub user in the 
last year (365 days).

Contributions contain:
-issues opened by a user
-commits made on a master repository
-pull requests opened on a master repository
'''

list_of_repo_urls = []

USER = "alex-hancock"

GITHUB_URL = "https://api.github.com"
REPOS_URL  = "/users/" + USER + "/repos%3Ftype=all"
ORGS_URL = "/users/" + USER + "/orgs"

today = datetime.date.today().isoformat()
since_date = str(int(today[0:4])-1) + today[4:]

repo_request = requests.get(GITHUB_URL + REPOS_URL)
for repo_dict in repo_request.json():
    # repo is a dictionary
    list_of_repo_urls.append(repo_dict["url"])
    # print(repo["url"])

orgs_request = requests.get(GITHUB_URL + ORGS_URL)
for org_dict in orgs_request.json():
    org_repos_url = org_dict["repos_url"]
    org_repo_request = requests.get(org_repos_url)
    for repo_dict in org_repo_request.json():
        list_of_repo_urls.append(repo_dict["url"])

for repo_url in list_of_repo_urls:
    print(repo_url)

    # get issues since last year with USER as creator with state=all
    # https://developer.github.com/v3/issues/?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc#list-issues

    # by the API, pull requests SHOULD be integrated as issues, so we don't care about these

    # get commits since date with USER as author
    # https://developer.github.com/v3/repos/commits/#get-a-single-commit

    '''
    Ideas:

    Probably have to single out issues/pull requests individually, I'm okay with that. 

    With commits, I think it's best to extract "for commit in blank" and create a 
    hash table with dates. 

    (is there an easy way to create a hash table of all days with initialize value 
    to zero, and then just increment? who knows...)
 
    But yeah, collect commits, go through each and grab date to fill out

    Good luck, kid.
    '''