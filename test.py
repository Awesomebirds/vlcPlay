import os
import random
import subprocess
import time

# 📌 영상 폴더 경로 설정
video_folder = r"C:\Videos"

# 📌 영상 파일 목록 가져오기
videos = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mkv"))]

# 📌 랜덤으로 하나 선택 후 VLC 실행 (전체화면 + 반복 재생 + 90분 후 종료)
if videos:
    selected_video = random.choice(videos)
    process = subprocess.Popen([
        "C:\\VLC\\vlc.exe",
        "--fullscreen", "--loop", selected_video
    ])
    # 90분(5400초) 대기
    time.sleep(5400)
    
    # VLC 강제 종료
    process.terminate()
else:
    print("영상이 없습니다. 폴더를 확인하세요.")
