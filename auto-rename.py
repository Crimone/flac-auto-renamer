import os
import sys
from mutagen.flac import FLAC

def read_titles_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        titles = f.readlines()
    return [title.strip() for title in titles]

def update_flac_titles(folder_path, titles):
    flac_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.flac')])

    if len(flac_files) != len(titles):
        print("Warning: The number of FLAC files and titles do not match.")
    
    for file, title in zip(flac_files, titles):
        file_path = os.path.join(folder_path, file)
        audio = FLAC(file_path)
        audio['title'] = title
        audio.save()

if __name__ == "__main__":

    folder_path = "C:/Users/vivira/OneDrive - mails.jlu.edu.cn/文档/Soulseek Downloads/Soulseek Shared Folder/少女前线交响音乐会/上海公演"
    titles_txt_path = "titles.txt"

    titles = read_titles_from_txt(titles_txt_path)
    update_flac_titles(folder_path, titles)
