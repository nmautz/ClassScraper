import requests

url = "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/searchResults/searchResults"

payload = ""
headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Language': "en-US,en;q=0.9",
    'Connection': "keep-alive",
    'Cookie': "JSESSIONID=2FB60A4C40C409D471E4841874AA9654; X-Oracle-BMC-LBS-Route=da6c046769f1e065ec273c5b1b3237cab1fca20f27da03a11a2ff120e313e9b656c62fd8a7c42ae88c32e31ea9051fe699b4d9e8aa3439b57323465e; apt.uid=AP-PQQY5YJEHTTA-2-1652683387398-51661655.0.2.4ffdd26d-c3a0-453f-b8d1-328add43f37f",
    'Referer': "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/classSearch/classSearch",
    'Sec-Fetch-Dest': "empty",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Site': "same-origin",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'X-Synchronizer-Token': "f330216e-aff8-44d9-bb67-93e39a9a8ad1"
}

i = 0

page_size = 400  # max is 499 ish

while i < 2300:
    querystring = {"txt_term": "202310", "startDatepicker": "", "endDatepicker": "",
                   "uniqueSessionId": "duhjc1654489778308", "pageOffset": str(i * page_size),
                   "pageMaxSize": str(page_size),
                   "sortColumn": "subjectDescription", "sortDirection": "asc"}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    i += page_size
    print(response.text)

# =-----------------------------------=
import requests


# https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/classSearch/classSearch

def get_cookies(url):
    session = requests.Session()
    print(session.cookies.get_dict())
    response = session.get('url')
    print(session.cookies.get_dict())
