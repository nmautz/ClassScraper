import asyncio
import json
import time
from http.client import responses

import aiohttp as aiohttp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.common.by import By

print("Starting Crawler")

TERM_CODE_STR = "202310"

print("Creating Cookies")
# Get Cookies
options = ChromiumOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/registration")
driver.find_element(By.ID, "classSearchLink").click()
driver.find_element(By.ID, "s2id_txt_term").click()
time.sleep(1)  # Waits for terms to load
driver.find_element(By.ID, str(TERM_CODE_STR)).click()  # Selects Fall 2022
driver.find_element(By.ID, "term-go").click()

session_cookie = "JSESSIONID=" + driver.get_cookies()[1]["value"]
oracle_cookie = "X-Oracle-BMC-LBS-Route=" + driver.get_cookies()[0]["value"]

driver.quit()

cookie_string = str(session_cookie) + "; " + str(oracle_cookie)
print("Creating Cookies Done")


# ____________________


async def request_all_classes(responses, tasks):
    i = 0

    page_size = 400
    while i < 6:
        tasks.append(asyncio.create_task(request_classes(i, page_size, responses)))
        i += 1

    for task in tasks:
        await task


async def request_classes(req_num, page_size, responses):
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
    querystring = {"txt_term": str(TERM_CODE_STR), "startDatepicker": "", "endDatepicker": "",
                   "pageOffset": str(req_num * page_size),
                   "pageMaxSize": str(page_size),
                   "sortColumn": "subjectDescription", "sortDirection": "asc"}
    print("Sending Request for " + str(page_size) + " classes. Starting at class #" + str(req_num * page_size))

    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=payload, headers=headers, params=querystring) as response:
            print("Response #" + str(req_num) + " Received")
            responses.append(await response.text())


responses = []
tasks = []

asyncio.run(request_all_classes(responses, tasks))

print("Initial Responses Complete")

# Parse responses
print("Parsing Initial Responses")

print(session_cookie)
print(oracle_cookie)

class_list_dict = {"data": []}

for response in responses:
    json_response = json.loads(response)

    response_length = len(json_response["data"])

    for i in range(0, response_length):

        sectionAttributeCodes = []
        sectionAttributeDescriptions = []
        # Get Section attributes
        attributeCount = len(json_response["data"][i]["sectionAttributes"])
        for c in range(0, attributeCount):
            sectionAttributeCodes.append(json_response["data"][i]["sectionAttributes"][c]["code"])
            sectionAttributeDescriptions.append(json_response["data"][i]["sectionAttributes"][c]["description"])

        # Edge case for faculty section sometimes missing

        profName = ""
        profEmail = ""
        if len(json_response["data"][i]["faculty"]) != 0:
            profName = json_response["data"][i]["faculty"][0]["displayName"]
            profEmail = json_response["data"][i]["faculty"][0]["emailAddress"]

        # Edge case for meetingsFaculty section sometimes missing
        # Set variables to empty str
        beginTime = ""
        buildingDescription = ""
        category = ""
        creditHourSession = ""
        endDate = ""
        endTime = ""
        hoursWeek = ""
        room = ""
        startDate = ""
        sunday = ""
        monday = ""
        tuesday = ""
        wednesday = ""
        thursday = ""
        friday = ""
        saturday = ""
        intrucMethDesc = ""
        campusDesc = ""

        if len(json_response["data"][i]["meetingsFaculty"]) != 0:
            beginTime = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["beginTime"],
            buildingDescription = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"][
                                      "buildingDescription"],
            category = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["category"],
            creditHourSession = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["creditHourSession"],
            endDate = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["endDate"],
            endTime = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["endTime"],
            hoursWeek = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["hoursWeek"],
            room = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["room"],
            startDate = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["startDate"],
            sunday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["sunday"],
            monday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["monday"],
            tuesday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["tuesday"],
            wednesday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["wednesday"],
            thursday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["thursday"],
            friday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["friday"],
            saturday = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["saturday"],
            campusDesc = json_response["data"][i]["meetingsFaculty"][0]["meetingTime"]["campusDescription"]

        class_list_dict["data"].append(

            {
                "id": json_response["data"][i]["id"],
                "subject": json_response["data"][i]["subject"],
                "subjectDescription": json_response["data"][i]["subjectDescription"],
                "courseReferenceNumber": json_response["data"][i]["courseReferenceNumber"],
                "courseNumber": json_response["data"][i]["courseNumber"],
                "scheduleTypeDescription": json_response["data"][i]["scheduleTypeDescription"],
                "courseTitle": json_response["data"][i]["courseTitle"],
                "maximumEnrollment": json_response["data"][i]["maximumEnrollment"],
                "enrollment": json_response["data"][i]["enrollment"],
                "seatsAvailable": json_response["data"][i]["seatsAvailable"],
                "waitCapacity": json_response["data"][i]["waitCapacity"],
                "waitCount": json_response["data"][i]["waitCount"],
                "waitAvailable": json_response["data"][i]["waitAvailable"],
                "professorName": profName,
                "professorEmail": profEmail,
                "beginTime": beginTime,
                "buildingDescription": buildingDescription,
                "campusDescription": campusDesc,
                "category": category,
                "creditHourSession": creditHourSession,
                "endDate": endDate,
                "endTime": endTime,
                "hoursWeek": hoursWeek,
                "room": room,
                "startDate": startDate,
                "sunday": sunday,
                "monday": monday,
                "tuesday": tuesday,
                "wednesday": wednesday,
                "thursday": thursday,
                "friday": friday,
                "saturday": saturday,
                "instructionalMethodDescription": json_response["data"][i]["instructionalMethodDescription"],
                "attributeCodes": sectionAttributeCodes,
                "attributeDesc": sectionAttributeDescriptions

            }
        )

print("Initial Parsing Complete")



jsonSTR = json.dumps(class_list_dict)

jsonSTR = jsonSTR.replace("&#39;", "\'")
jsonSTR = jsonSTR.replace("&amp;", "&")

class_list_dict = json.loads(jsonSTR)

print("Writing result to file classes.json")
f = open("classes.json", "w")
f.write(json.dumps(class_list_dict))
f.close()

print("Finished!")
