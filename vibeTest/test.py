import yt_dlp

def download_youtube_video(link):
    try:
        # Set download options
        ydl_opts = {
            'format': 'best',  # Download the best quality video
            'outtmpl': '%(title)s.%(ext)s',  # Save file with video title as the name
        }

        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    youtube_link = input("Enter the YouTube video link: ")
    download_youtube_video(youtube_link)