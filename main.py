import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.common.by import By
import requests
import time

# Get Cookies
options = ChromiumOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/registration")
driver.find_element(By.ID, "classSearchLink").click()
driver.find_element(By.ID, "s2id_txt_term").click()
time.sleep(1)
driver.find_element(By.ID, "202310").click()
driver.find_element(By.ID, "term-go").click()

session_cookie = "JSESSIONID=" + driver.get_cookies()[1]["value"]
oracle_cookie = "X-Oracle-BMC-LBS-Route=" + driver.get_cookies()[0]["value"]

driver.quit()

cookie_string = str(session_cookie) + "; " + str(oracle_cookie)

# ____________________


# prepare request
url = "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/searchResults/searchResults"

payload = ""
headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Language': "en-US,en;q=0.9",
    'Connection': "keep-alive",
    'Cookie': cookie_string,
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
