import asyncio
import json
import aiohttp


async def async_request(url, payload, headers, limit_message):

    if limit_message != "":
        print(limit_message)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                return await response.text()
    except:
        print("rate limit sleeping...")
        await asyncio.sleep(15)
        return await async_request(url, payload, headers, limit_message + " trying again")


async def safe_request_in_mass(CRNs, request_function):
    tasks = []
    taskCRNPair = []
    results = {}

    for i in range(0, len(CRNs)):
        tasks.append(asyncio.create_task(request_function(CRNs[i])))
        taskCRNPair.append(CRNs[i])

        if i % 1500 == 0 or i == len(CRNs) - 1:
            for c in range(0, len(tasks)):
                task = await tasks[c]
                result = await task
                results[str(taskCRNPair[c])] = result
                if result == None:
                    print("Rate limit!!")
            tasks.clear()
            taskCRNPair.clear()
            print(str(i / len(CRNs) * 100)[0:5] + "% complete")
    return results



async def request_class_desc(courseReferenceNumber):
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://xe.gonzaga.edu",
        "Referer": "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/classSearch/classSearch"
    }

    # Get all course descs
    url = "https://xe.gonzaga.edu/StudentRegistrationSsb/ssb/searchResults/getCourseDescription"

    payload = "term=202310&courseReferenceNumber=" + str(courseReferenceNumber)
    task = (asyncio.create_task(async_request(url=url, payload=payload, headers=headers, limit_message="")))
    return task


async def main():
    f = open("classes.json")
    class_list_json = json.load(f)["data"]

    # Get all class ids
    CRNs = []
    for section in class_list_json:
        CRNs.append(section["courseReferenceNumber"])

    print("Starting search")

    results = await safe_request_in_mass(CRNs, request_class_desc)

    print("Searching complete")



    file = open("classes.json", 'r')

    class_list_raw_json = json.load(file)

    class_list_json = class_list_raw_json["data"]

    file.close()


    for section in class_list_json:
        section["description"] = results[section["courseReferenceNumber"]]

    file = open("classes.json", 'w')

    class_list_str = json.dumps(class_list_raw_json)

    file.write(class_list_str)

    print("results saved to classes.json")



asyncio.run(main())
