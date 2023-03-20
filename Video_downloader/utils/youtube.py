import pathlib
import time
import random
from tqdm import tqdm
from pathlib import Path
from pytube import YouTube, Playlist

from utils.common_funcs import get_value_from_config
from utils.log import log_in_file_and_print_in_terminal


def prepare_path(path: pathlib.Path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def get_info_about_youtube_video(video_link: str) -> list:
    # получение данных о видео по ссылке: название, автор видео, является ли видео частью плейлиста
    remove_symbols = r'«*."/\[]:;-|,»&?! <>'
    try:
        video_info = YouTube(video_link)  # получаем данные о видео по ссылке
        video_author = ''.join([x if x not in remove_symbols else '_' for x in video_info.author])
        video_title = ''.join([x if x not in remove_symbols else '_' for x in video_info.title]) + '.mp4'
        try:
            playlist_info = Playlist(video_link)  # получаем плейлист по ссылке на видео
            result = [video_title, video_author, len(playlist_info)]
        except:
            result = [video_title, video_author, 0]
        log_in_file_and_print_in_terminal(f"Для {video_link} получена информация:\n"
                                          f"Title: {video_info.title}\n"
                                          f"Author: {video_info.author}\n"
                                          f"Playlist количество видео: {result[2]}")
    except Exception as e:
        result = [None, None, None]
        log_in_file_and_print_in_terminal(f"Для {video_link} не удалось получить информацию\n{e}", loglevel=2,
                                          print_in_terminal=True)
    return result


def download_single_video(video_link: str, filename: str, save_path=pathlib.Path.cwd()):
    """
    скачивание отдельного видео по ссылке на youtube
    save_path - путь для сохранения
    """
    try:
        yt = YouTube(video_link)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first() \
            .download(output_path=save_path, filename=filename)
        log_in_file_and_print_in_terminal(f"загружено в {save_path} {video_link}", print_in_terminal=True)
    except Exception as e:
        log_in_file_and_print_in_terminal(f"сбой загрузки {video_link}\n{e}", print_in_terminal=True)
        for i in range(5):
            delay = random.choice([1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9])
            log_in_file_and_print_in_terminal(f"Таймаут {delay} секунд. Попытка {i + 1}", print_in_terminal=True)
            time.sleep(delay)
            try:
                yt = YouTube(video_link)
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first() \
                    .download(output_path=save_path, filename=filename)
                log_in_file_and_print_in_terminal(f"загружено в {save_path} {video_link}", print_in_terminal=True)
                break
            except Exception as e:
                pass


def download_youtube_video(video_link: str, save_path=pathlib.Path.cwd(), one_or_all='one'):
    """
    скачивание видео по ссылке на youtube
    save_path - путь для сохранения + добавляются подпапки исходя из названия кананала и плейлиста
    one_or_all - скачивать весь плейлист или только отдельное видео
    """
    remove_symbols = r'«*."/\[]:;-|,»&?! <>'
    video_title, video_author, len_playlist = get_info_about_youtube_video(video_link)
    print(video_title)
    if one_or_all == 'one' or len_playlist == 0:
        save_dir = pathlib.Path(save_path, video_author)
        prepare_path(save_dir)
        download_single_video(video_link=video_link, save_path=save_dir, filename=video_title)

    elif one_or_all == 'all' and len_playlist:
        playlist = Playlist(video_link)
        playlist_title = ''.join([x if x not in remove_symbols else '_' for x in playlist.title])
        video_author = get_info_about_youtube_video(video_link)[1]
        save_dir = pathlib.Path(save_path, playlist_title, video_author)
        prepare_path(save_dir)
        for video_link in tqdm(playlist):
            try:
                video_title = get_info_about_youtube_video(video_link)[0]
                download_single_video(video_link=video_link, save_path=save_dir, filename=video_title)
            except Exception as e:
                print(e)

