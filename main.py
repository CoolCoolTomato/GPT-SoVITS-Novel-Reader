import os
import re
import requests
import json
import io
from pydub import AudioSegment

novel = "诡秘之主.txt"
url = "http://127.0.0.1:9880/tts"
payload = {
    "text_lang": "zh",
    "ref_audio_path": "W:/code/Python/tts/hutao.wav",
    "prompt_lang": "zh",
    "prompt_text": "北斗姐可是璃月名人，她不认识我没关系，我认识她就行。",
    "text_split_method": "cut2",
    "batch_size": 20,
    "media_type": "wav",
    "streaming_mode": False,
    "top_k": 5,
    "top_p": 1,
    "temperature": 1,
    "batch_threshold": 0.75,
    "split_bucket": True,
    "speed_factor": 1,
    "fragment_interval": 0.3,
    "seed": -1,
    "parallel_infer": True,
    "repetition_penalty": 1.35
}

def process_novel(file_path):
    current_volume = ""
    current_chapter = ""
    chapter_content = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            volume_match = re.match(r'^第(\w+)部', line)
            if volume_match:
                if current_volume:
                    if save_chapter(current_volume, current_chapter, chapter_content):
                        pass
                    else:
                        print("保存失败：", current_volume, current_chapter)
                        return 
                current_volume = volume_match.group(1)
                current_chapter = ""
                chapter_content = []
                os.makedirs(current_volume, exist_ok=True)
                continue
            
            chapter_match = re.match(r'^第(\w+)章', line)
            if chapter_match:
                if current_chapter:
                    if save_chapter(current_volume, current_chapter, chapter_content):
                        pass
                    else:
                        print("保存失败：", current_volume, current_chapter)
                        return 
                current_chapter = chapter_match.group(1)
                chapter_content = []
                continue
            
            if current_chapter:
                chapter_content.append(line)
    
    # 保存最后一章
    if current_volume and current_chapter:
        save_chapter(current_volume, current_chapter, chapter_content)
def save_chapter(volume, chapter, content):
    if not content:
        return True
    
    combined_audio = AudioSegment.empty()
    
    for i in range(0, len(content), 15):
        chunk = content[i:i+15]
        text = "".join(chunk)
        text.strip()
        if text != "":
            data = payload
            data["text"] = text
            
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, data=json.dumps(data), headers=headers)
            
            if response.status_code == 200:
                audio_segment = AudioSegment.from_wav(io.BytesIO(response.content))
                combined_audio += audio_segment
            else:
                print(f"请求失败,状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
    
    file_path = f"{volume}/{chapter}.wav"
    combined_audio.export(file_path, format="wav")
    
    print(f"WAV文件已成功生成并保存为 {file_path}")
    return True

# 使用脚本
if __name__ == "__main__":
    process_novel(novel)
