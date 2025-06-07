import yt_dlp
import os

def download_highest_quality_video(link, sub_folder):
    try:
        # 設定下載目錄
        base_directory = "/Users/hank/Library/Mobile Documents/com~apple~CloudDocs/99_roach/60_呈/01_高中/28.maslu數學/數乙歷屆"
        output_directory = os.path.join(base_directory, sub_folder)  # 加入子資料夾
        # 確保目錄存在
        os.makedirs(output_directory, exist_ok=True)

        # 設定下載選項
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # 限制最高畫質為 1080p
            'merge_output_format': 'mp4',                                    # 合併輸出為 MP4 格式
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),  # 儲存到指定目錄
            'ignoreerrors': True,                                            # 忽略下載錯誤
        }

        # 使用 yt-dlp 下載影片或播放清單
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)  # 提取資訊
            if 'entries' in info:  # 如果是播放清單
                print(f"檢測到播放清單，共 {len(info['entries'])} 部影片")
                for entry in info['entries']:
                    if entry is None:  # 如果條目為 None，跳過
                        print("跳過無效的播放清單條目")
                        continue
                    try:
                        video_title = entry.get('title', 'unknown_title')
                        output_file = os.path.join(output_directory, f"{video_title}.mp4")
                        if os.path.exists(output_file):
                            print(f"檔案已存在，跳過下載: {output_file}")
                            continue
                        ydl.download([entry['webpage_url']])
                    except Exception as e:
                        # 記錄錯誤並跳過
                        print(f"跳過無法下載的影片: {entry.get('title', 'unknown_title')}，錯誤原因: {e}")
                        with open(os.path.join(output_directory, "error_log.txt"), "a") as log_file:
                            log_file.write(f"無法下載的影片: {entry.get('title', 'unknown_title')}，錯誤原因: {e}\n")
            else:  # 如果是單一影片
                try:
                    video_title = info.get('title', 'unknown_title')
                    output_file = os.path.join(output_directory, f"{video_title}.mp4")
                    if os.path.exists(output_file):
                        print(f"檔案已存在，跳過下載: {output_file}")
                        return
                    ydl.download([link])
                except Exception as e:
                    print(f"無法下載影片: {info.get('title', 'unknown_title')}，錯誤原因: {e}")
                    with open(os.path.join(output_directory, "error_log.txt"), "a") as log_file:
                        log_file.write(f"無法下載影片: {info.get('title', 'unknown_title')}，錯誤原因: {e}\n")
        print("下載完成！")
    except Exception as e:
        print(f"下載過程中發生錯誤: {e}")
        with open(os.path.join(output_directory, "error_log.txt"), "a") as log_file:
            log_file.write(f"下載過程中發生錯誤: {e}\n")

if __name__ == "__main__":
    sub_folder = input("請輸入子資料夾名稱: ")
    youtube_link = input("請輸入 YouTube 影片或播放清單連結: ")
    download_highest_quality_video(youtube_link, sub_folder)