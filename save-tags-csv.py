import csv
import requests
from bs4 import BeautifulSoup

def fetch_titles_from_vgmdb(album_url):
    response = requests.get(album_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tracklist = []

    for disc in soup.find_all("span", style="font-size:8pt"):
        if disc.b and disc.get_text(strip=True).startswith("Disc"):
            disc_number = int(disc.b.get_text(strip=True).split(" ")[1])

            table = disc.find_next("table", class_="role")
            for track in table.find_all("tr", class_="rolebit"):
                track_number = int(track.find("span", class_="label").get_text(strip=True))
                title = track.find("td", colspan="2").get_text(strip=True)

                tracklist.append({"disc_number": disc_number, "track_number": track_number, "title": title})

    # 将数据保存到CSV文件
    with open("tracklist.csv", "w", encoding="utf-8", newline="") as csvfile:
        fieldnames = ["disc_number", "track_number", "title"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for track in tracklist:
            writer.writerow(track)

    print("已将抓取到的数据保存到tracklist.csv文件中。")

if __name__ == "__main__":

    album_url = "https://vgmdb.net/album/89880"

    titles = fetch_titles_from_vgmdb(album_url)


