import requests
import re
import csv

FILE_INPUT = "input.csv"
FILE_OUTPUT = "output.csv"

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

PT_DETAIL_URL = "https://api-frontend.kemdikbud.go.id/v2/detail_pt/"
PT_DETAIL_PRODI_URL = "https://api-frontend.kemdikbud.go.id/v2/detail_pt_prodi/"

universities_data = []
failed_universities = []

with open(FILE_INPUT, "r", encoding="utf-8") as file:
    # skip header
    next(file)
    for line in file:
        try:
            name, university_id = line.strip().split(",")
            university_detail_response = requests.get(
                PT_DETAIL_URL + university_id, headers=headers, timeout=5
            )
            university_prodies_response = requests.get(
                PT_DETAIL_PRODI_URL + university_id, headers=headers, timeout=5
            )
            university_data = {}
            university_detail_json = university_detail_response.json()
            university_prodi_json = university_prodies_response.json()

            university_data["name"] = university_detail_json["nm_lemb"]
            university_data["id"] = university_detail_json["id_sp"]
            try:
                university_data["alamat"] = re.sub(
                    r"\r\n|\r|\n", " ", university_detail_json["jln"]
                )
            except:
                university_data["alamat"] = ""
            university_data["kota/kab"] = university_detail_json["nama_wil"]
            university_data["no telp"] = university_detail_json["no_tel"]
            university_data["email"] = university_detail_json["email"]
            university_data["website"] = university_detail_json["website"]

            for prodi in university_prodi_json:
                rasio_list_without_20231 = list(
                    filter(lambda x: x["semester"] != "20231", prodi["rasio_list"])
                )

                for rasio in rasio_list_without_20231:
                    try:
                        university_data["Total Dosen - " + rasio["semester"]] += rasio[
                            "dosen"
                        ]
                    except KeyError:
                        university_data["Total Dosen - " + rasio["semester"]] = rasio[
                            "dosen"
                        ]
                    try:
                        university_data["Total Mhs - " + rasio["semester"]] += rasio[
                            "mahasiswa"
                        ]
                    except KeyError:
                        university_data["Total Mhs - " + rasio["semester"]] = rasio[
                            "mahasiswa"
                        ]

            universities_data.append(university_data)
        except Exception as e:
            print(e)
            print(line)
            failed_universities.append(line)

with open(FILE_OUTPUT, "w", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "name",
            "id",
            "alamat",
            "kota/kab",
            "no telp",
            "email",
            "website",
            "Total Dosen - 20191",
            "Total Mhs - 20191",
            "Total Dosen - 20192",
            "Total Mhs - 20192",
            "Total Dosen - 20201",
            "Total Mhs - 20201",
            "Total Dosen - 20202",
            "Total Mhs - 20202",
            "Total Dosen - 20211",
            "Total Mhs - 20211",
            "Total Dosen - 20212",
            "Total Mhs - 20212",
            "Total Dosen - 20221",
            "Total Mhs - 20221",
            "Total Dosen - 20222",
            "Total Mhs - 20222",
        ],
    )
    writer.writeheader()
    for university_data in universities_data:
        writer.writerow(university_data)

with open("failed_" + FILE_OUTPUT, "w", encoding="utf-8") as file:
    for failed_university in failed_universities:
        file.write(failed_university)
