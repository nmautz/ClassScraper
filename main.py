import requests
import json

# =-----------------------------------=
import requests

session = requests.Session()

response = session.get("https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/searchResults/searchResults")
cookies = session.cookies.get_dict()
session.close()

session_cookie = "JSESSIONID=" + str(cookies['JSESSIONID'])
oracle_cookie = "X-Oracle-BMC-LBS-Route=" + str(cookies['X-Oracle-BMC-LBS-Route'])

url = "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/searchResults/searchResults"

payload = ""
headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Language': "en-US,en;q=0.9",
    'Connection': "keep-alive",
    'Cookie': str(session_cookie) + "; " + str(oracle_cookie),
    'Referer': "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/classSearch/classSearch",
    'Sec-Fetch-Dest': "empty",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Site': "same-origin",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}

i = 0

page_size = 400  # max is 499 ish

responses = []

while i < 2300:
    querystring = {"txt_term": "202310", "startDatepicker": "", "endDatepicker": "",
                   "pageOffset": str(i),
                   "pageMaxSize": str(page_size),
                   "sortColumn": "subjectDescription", "sortDirection": "asc"}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    i += page_size
    responses.append(response.text)

# print(responses)

# Parse responses


print(session_cookie)
print(oracle_cookie)


for response in responses:
    json_response = json.loads(response)

    print(json_response)
