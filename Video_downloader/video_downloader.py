from utils.common_funcs import get_value_from_config
from utils.youtube import download_youtube_video
#import download, get_info_about_youtube_video,
from utils.text_and_comminication_with_user_utils import \
    select_playlist_or_single_video_download, select_download_path, get_download_link_from_user



# 1. скачивание плэйлиста или отдельных видео

# playlist_or_single_video = select_playlist_or_single_video_download()
# download_link = get_download_link_from_user()

# download(playlist_or_single_video, download_link)
download_youtube_video('https://youtu.be/cXCuXNwzdfY?list=PLIJLLSrXDPojDGKW0WZ7sU0eO3nyn0oDc', one_or_all='all')
# 2.
