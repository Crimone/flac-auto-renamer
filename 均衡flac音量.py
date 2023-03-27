import librosa
import soundfile as sf

# 加载音频文件
audio_path = r"C:\Users\vivira\OneDrive - mails.jlu.edu.cn\文档\Soulseek Downloads\Soulseek Shared Folder\少女前线交响音乐会\东京公演\Chapter 02.flac"
y, sr = sf.read(audio_path)


# 根据平均响度调整音频的增益
y = librosa.effects.normalize(y, rms=-20)

# 保存调整后的音频文件为 FLAC 格式
output_path = r'your_output_audio_file_path.flac'
sf.write(output_path, y, sr)
