import asyncio
import json
import aiohttp
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=1, period=15)
def check_limit(url):
    #empty func
    return

async def async_request(url, payload, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            return await response.text()

async def request_all_class_advanced(CRNs):
    tasks = []
    descriptions = []
    for crn in CRNs:
        tasks.append(asyncio.create_task(request_class_advanced(crn)))
    for task in tasks:
        desc = await task
        print(desc)
        descriptions.append(desc)

    return descriptions



async def request_class_advanced(courseReferenceNumber):
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://xe.gonzaga.edu",
        "Referer": "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/classSearch/classSearch"
    }

    # Get all course descs
    url = "http://xe.gonzaga.edu/StudentRegistrationSsb/ssb/searchResults/getCourseDescription"


    payload = "term=202310&courseReferenceNumber=" + str(courseReferenceNumber)
    print("Requesting advanced details for class #" + str(courseReferenceNumber))
    check_limit()
    task = (asyncio.create_task(async_request(url=url, payload=payload, headers=headers)))


f = open("classes.json")
class_list_json = json.load(f)["data"]

# Get all class ids
CRNs = []
for section in class_list_json:
    CRNs.append(section["courseReferenceNumber"])

p = asyncio.run(request_all_class_advanced(CRNs))
print(p)