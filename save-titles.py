import json
import requests
from bs4 import BeautifulSoup

def fetch_titles_from_vgmdb(album_url):
    response = requests.get(album_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tracklist_div = soup.find('div', id='tracklist')

    tracks = []
    disc = 0
    for table in tracklist_div.find_all('table', class_='role'):
        disc = disc + 1
        for row in table.find_all('tr', class_='rolebit'):
            number_cell = row.find('td', class_='smallfont')
            title_cell = row.find_all('td')[1]
            track_number = number_cell.text.strip()
            title = title_cell.text.strip()
            tracks.append({"disc_number": disc, "track_number": track_number, "title": title})

    # 将提取到的音轨信息保存到JSON文件
    with open('tracklist.json', 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=2)

    print("音轨信息已保存到tracklist.json文件")

if __name__ == "__main__":

    album_url = "https://vgmdb.net/album/89880"

    titles = fetch_titles_from_vgmdb(album_url)

