import requests

FILE_NAME = "universitas_swasta_v2.txt"
OUTPUT_FILE = "universities_swasta_v2.csv"

# try to searching universities using the list above
# and save the one that also exist in the search result from PD Dikti website
valid_universities = []
invalid_universities = []


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "api-frontend.kemdikbud.go.id",
    "Origin": "https://pddikti.kemdikbud.go.id",
    "Referer": "https://pddikti.kemdikbud.go.id/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}

with open(FILE_NAME, "r", encoding="utf-8") as file:
    for university in file:
        university = university.strip()

        if university == "" or ":" in university:
            continue
        try:
            response = requests.get(
                f"https://api-frontend.kemdikbud.go.id/hit/{university}",
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                pt_results: list = response.json()["pt"]
                if len(pt_results) > 0:
                    FOUND = False
                    for pt in pt_results:
                        try:
                            pt_name: str = (
                                pt["text"].split("Nama PT: ")[1].split(",")[0]
                            )
                            if pt_name.lower() == university.lower():
                                valid_universities.append(
                                    {
                                        "name": university,
                                        "id": pt["website-link"].split("/data_pt/")[1],
                                    }
                                )
                                FOUND = True
                                break
                        except Exception as e:
                            print(e)
                            print(pt)
                    if not FOUND:
                        invalid_universities.append(university)
        except Exception as e:
            print(e)


with open("valid_" + OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("name,id\n")
    for university in valid_universities:
        file.write(f"{university['name']},{university['id']}\n")

if len(invalid_universities) > 0:
    with open("invalid_" + OUTPUT_FILE, "w", encoding="utf-8") as file:
        for university in invalid_universities:
            file.write(f"{university}\n")
