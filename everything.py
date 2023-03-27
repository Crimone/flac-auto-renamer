import time
import os

# 从 txt 文件中逐行读取数据
with open(r'D:\GitHub\flac-auto-renamer\1.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# 打开 Everything 窗口并等待它变为活动窗口
os.system(r'start "C:\Program Files\Everything\Everything.exe"')
time.sleep(1)

# 循环检查每个文件是否存在
for line in lines:
    # 粘贴文件名到 Everything 搜索框
    os.system(f'echo.| set /p="{line}" | everything.exe')

    # 等待搜索结果窗口出现
    time.sleep(0.5)
    while 'Everything' not in os.popen('tasklist /FI "IMAGENAME eq everything.exe" /FI "STATUS eq running" /FO csv').read():
        time.sleep(0.5)

    # 检查搜索结果
    result = os.popen('everything.exe -s -path ' + line).read().strip()
    if result:
        # 如果文件已存在，则在控制台输出提示信息
        print(f'{line} already exists in Everything')
    else:
        # 如果文件不存在，则在控制台输出提示信息
        print(f'{line} does not exist in Everything')

    # 关闭搜索结果窗口
    os.system('taskkill /im everything.exe')

# 在控制台输出完成信息
print('All lines processed.')
