# -*- coding: utf-8 -*-
"""
이 스크립트는 지정된 시간에 VLC 미디어 플레이어를 자동으로 제어하기 위해 만들어졌습니다.
특정 시간에 VLC를 실행하여 플레이리스트를 랜덤으로 재생하고, 다른 지정된 시간에는 VLC를 종료합니다.
또한, 주말(토, 일)에는 일부 시간대의 동작을 건너뛰는 기능이 포함되어 있습니다.

[주요 기능]
1. 스크립트 시작 시 지정된 플레이리스트를 랜덤으로 즉시 재생합니다.
2. 매일 정해진 시간에 따라 VLC를 재생하거나 종료합니다.
   - 재생 시간: 13:01, 19:01
   - 종료 시간: 11:29, 17:29
3. 주말(토요일, 일요일)에는 저녁 시간(17:29, 19:01)의 재생/종료 동작을 실행하지 않습니다.
"""

import os
import subprocess
import time
import datetime

# 경로 설정
vlc_path = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"  # VLC 경로
playlist_path = "D:\\playlist.xspf"  # xspf 경로

# 요일 가져오기
current_weekday = datetime.datetime.now().weekday()  # 0월요일 6일요일

# 📌 VLC 종료 함수
def stop_vlc():
    os.system("taskkill /IM vlc.exe /F")
    print("⚔️ VLC 종료")

# 📌 VLC 재생 함수 (수정된 부분)
def play_video(video_path):
    # '--random' 옵션을 추가하여 플레이리스트를 셔플 모드로 재생합니다.
    subprocess.Popen([vlc_path, video_path, '--random'])
    print(f"🎬 랜덤 재생 시작: {video_path}")

def check_time_and_control_vlc():
    """
    특정 시간에 VLC를 제어하고 XSPF 파일을 실행합니다.
    """

    pause_times = {
        datetime.time(11, 29): "pause",
        datetime.time(13, 1): "play",
        datetime.time(17, 29): "pause",
        datetime.time(19, 1): "play",
    }

    while True:
        now = datetime.datetime.now().time()

        # 매 루프마다 요일을 다시 확인하여 날짜가 바뀌어도 정확하게 동작하도록 수정
        current_weekday_inside_loop = datetime.datetime.now().weekday()

        for pause_time, action in pause_times.items():
            if now.hour == pause_time.hour and now.minute == pause_time.minute:
                # 토요일(5), 일요일(6)에 17:29, 19:01 동작 건너뛰기
                if current_weekday_inside_loop in [5, 6] and pause_time in [datetime.time(17, 29), datetime.time(19, 1)]:
                    print(f"주말({pause_time.strftime('%H:%M')})이므로 다음 시간까지 대기합니다.")
                    break

                if action == "pause":
                    # VLC 프로세스 종료
                    stop_vlc()
                    print(f"{now.strftime('%H:%M')} : VLC 종료됨.")
                elif action == "play":
                    # VLC 실행 및 XSPF 파일 재생
                    play_video(playlist_path)
                    print(f"{now.strftime('%H:%M')} : VLC 랜덤 재생 시작.")

                # 해당 시간의 동작을 수행했으면 1분 대기 후 다음 루프로 넘어감
                time.sleep(61) 
                break

        time.sleep(1) # CPU 사용량을 줄이기 위해 1초마다 시간 확인

if __name__ == "__main__":
    # 스크립트 실행 시 XSPF 파일 최초 실행
    play_video(playlist_path)
    print("스크립트 시작: VLC 및 플레이리스트 랜덤 재생.")

    check_time_and_control_vlc()
