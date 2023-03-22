import os
import sys
from mutagen.flac import FLAC

def add_track_number_to_flac_files(folder_path):
    flac_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.flac')])

    for index, file in enumerate(flac_files, start=1):
        file_path = os.path.join(folder_path, file)
        audio = FLAC(file_path)
        track_number = "{:02}".format(index-1)  # Format the track number with leading zeros
        audio['tracknumber'] = track_number
        audio.save()

if __name__ == "__main__":

    folder_path = "C:/Users/vivira/OneDrive - mails.jlu.edu.cn/文档/Soulseek Downloads/Soulseek Shared Folder/少女前线交响音乐会/上海公演"
    add_track_number_to_flac_files(folder_path)
