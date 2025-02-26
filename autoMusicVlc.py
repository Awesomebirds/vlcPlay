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

# 📌 VLC 재생 함수
def play_video(video_path):
    subprocess.Popen([vlc_path, video_path])
    print(f"🎬 재생 시작: {video_path}")

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

        for pause_time, action in pause_times.items():
            if now.hour == pause_time.hour and now.minute == pause_time.minute:
                # 토요일, 일요일에 17:30, 19:00 동작 건너뛰기
                if current_weekday in [5, 6] and pause_time in [datetime.time(17, 29), datetime.time(19, 1)]:
                    print("주말임!")
                    break

                if action == "pause":
                    # VLC 프로세스 종료
                    stop_vlc()
                    print(f"{now} : VLC 종료됨.")
                elif action == "play":
                    # VLC 실행 및 XSPF 파일 재생
                    play_video(playlist_path)
                    print(f"{now} : VLC 재생 시작.")

                break  # 시간 조건 충족 시 다음 시간 확인으로 넘어감

        time.sleep(60)  # 60초마다 시간 확인

if __name__ == "__main__":
    # 스크립트 실행 시 XSPF 파일 최초 실행
    play_video(playlist_path)
    print("스크립트 시작: VLC 및 플레이리스트 실행.")

    check_time_and_control_vlc()