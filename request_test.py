import requests 
import datetime

import datetime

def create_daylist(since_date,today_date):
    today_obj = datetime.date(int(today_date[0:4]), int(today_date[5:7]), int(today_date[-2:]))
    since_obj = datetime.date(int(since_date[0:4]), int(since_date[5:7]), int(since_date[-2:]))

    delta = today_obj - since_obj
    thing = [since_obj + datetime.timedelta(days=i) for i in range(delta.days+1)]
    return [x.strftime("%Y-%m-%d") for x in thing]

today_date = datetime.date.today().isoformat()
since_date = str(int(today_date[0:4])-1) + today_date[4:]

days_list = create_daylist(since_date, today_date)
days_hash = {day: 0 for day in days_list}

# example URL: https://api.github.com/repos/BD2KGenomics/toil-rnaseq
# to get issues: https://api.github.com/repos/BD2KGenomics/toil-rnaseq/issues

test_url = "https://api.github.com/repos/BD2KGenomics/toil-rnaseq/issues"
test_suffix = "?state=all&since="+since_date#+"&page=1"
#print(test_url + test_suffix)
test_request = requests.get(test_url + test_suffix)
#print(test_request.json())

#print(test_request.headers)
#print("next" in test_request.headers["Link"])

for test_dict in test_request.json():
    issue_user = test_dict["user"]["login"]
    created_date = test_dict["created_at"][:10]
    print("{} created an issue at {}".format(issue_user, created_date))
    if created_date not in days_hash:
        break
    else:
        days_hash[created_date] += 1
        print("{} created an issue at {}".format(issue_user, created_date))

i=2
if "Link" in test_request.headers:
    while "next" in test_request.headers["Link"]:
        test_request = requests.get(test_url + test_suffix + "&page=" + str(i))
        i += 1
        for test_dict in test_request.json():
            issue_user = test_dict["user"]["login"]
            created_date = test_dict["created_at"][:10]
            if created_date not in days_hash:
                break
            else:
                days_hash[created_date] += 1
                print("{} created an issue at {}".format(issue_user, created_date))

print(days_hash)