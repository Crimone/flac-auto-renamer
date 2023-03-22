import os
import csv
from mutagen.flac import FLAC

def edit_flac_metadata(folder_path, track_data_file):
    # 读取CSV文件
    with open(track_data_file, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # 获取文件夹中的FLAC文件
        flac_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.flac')])

        for row, flac_file in zip(reader, flac_files):
            file_path = os.path.join(folder_path, flac_file)
            audio = FLAC(file_path)

            # 设置标题、碟片号和音轨号
            audio['title'] = row["title"]
            audio['discnumber'] = str(row["disc_number"])
            audio['tracknumber'] = str(row["track_number"])

            audio.save()

if __name__ == "__main__":
    folder_path = 'C:/Users/vivira/OneDrive - mails.jlu.edu.cn/文档/Soulseek Downloads/Soulseek Shared Folder/少女前线交响音乐会/日本公演'
    track_data_file = 'tracklist.csv'
    edit_flac_metadata(folder_path, track_data_file)
