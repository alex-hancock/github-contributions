import datetime

def create_daylist(since_date,today_date):
    today_obj = datetime.date(int(today_date[0:4]), int(today_date[5:7]), int(today_date[-2:]))
    since_obj = datetime.date(int(since_date[0:4]), int(since_date[5:7]), int(since_date[-2:]))

    delta = today_obj - since_obj
    thing = [since_obj + datetime.timedelta(days=i) for i in range(delta.days+1)]
    return [x.strftime("%Y-%m-%d") for x in thing]

# Change how USER is passed at some point...
USER = "alex-hancock"
GITHUB_URL = "https://api.github.com"
REPOS_URL  = "/users/" + USER + "/repos%3Ftype=all"
ORGS_URL = "/users/" + USER + "/orgs"

today_date = datetime.date.today().isoformat()
since_date = str(int(today_date[0:4])-1) + today_date[4:]

days_list = create_daylist(since_date, today_date)
days_hash = {day: 0 for day in days_list}

print(days_hash)