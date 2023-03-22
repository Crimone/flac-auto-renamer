import os
import csv
from mutagen.flac import FLAC

def read_csv_data(csv_file_path):
    data = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def get_flac_files(folder_path):
    return [file for file in os.listdir(folder_path) if file.lower().endswith('.flac')]

def edit_flac_metadata(folder_path, csv_file_path):
    csv_data = read_csv_data(csv_file_path)
    flac_files = get_flac_files(folder_path)

    for flac_file in flac_files:
        file_path = os.path.join(folder_path, flac_file)
        audio = FLAC(file_path)

        discnumber = audio.get('discnumber', [None])[0]
        tracknumber = audio.get('tracknumber', [None])[0]

        # 在CSV数据中查找匹配的碟片号和音轨号
        matching_row = None
        for row in csv_data:
            if row['disc_number'] == discnumber and row['track_number'] == tracknumber:
                matching_row = row
                break

        if matching_row:
            audio['title'] = matching_row['title']
            audio.save()
        else:
            print(f"未找到与 {flac_file} 匹配的数据")

folder_path = 'path/to/your/flac/files'
csv_file_path = 'path/to/your/csv/file.csv'
edit_flac_metadata(folder_path, csv_file_path)
