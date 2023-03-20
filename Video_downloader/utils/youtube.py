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
        playlist_info = Playlist(video_link)  # получаем плейлист по ссылке на видео
        video_author = ''.join([x if x not in remove_symbols else '_' for x in video_info.author])
        # video_author = video_info.author
        video_title = ''.join([x if x not in remove_symbols else '_' for x in video_info.title]) + '.mp4'
        # video_title = video_info.title + '.mp4'
        # print(video_title, video_author)
        # print(video_info.title, video_info.author)
        result = [video_title, video_author, len(playlist_info)]
        # print(result)
        log_in_file_and_print_in_terminal(f"Для {video_link} получена информация:\n"
                                          f"Title: {video_info.title}\n"
                                          f"Author: {video_info.author}\n"
                                          f"Playlist количество видео: {len(playlist_info)}")

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

    if one_or_all == 'one' or len_playlist == 0:
        save_dir = pathlib.Path(save_path, video_author)
        prepare_path(save_dir)
        download_single_video(video_link=video_link, save_path=save_dir, filename=video_title)

    elif one_or_all == 'all':
        playlist = Playlist(video_link)
        playlist_title = ''.join([x if x not in remove_symbols else '_' for x in playlist.title])
        video_author = get_info_about_youtube_video(video_link)[1]
        save_dir = pathlib.Path(save_path, playlist_title, video_author)
        prepare_path(save_dir)
        for video_link in playlist:
            try:
                video_info = YouTube(video_link)  # получаем данные о видео по ссылке
                playlist_info = Playlist(video_link)  # получаем плейлист по ссылке на видео
                time.sleep(1)
                video_author = ''.join([x if x not in remove_symbols else '_' for x in video_info.author])
                # video_title = ''.join([x if x not in remove_symbols else '_' for x in video_info.title]) + '.mp4'
                # result = [video_title, video_author, len(playlist_info)]
                log_in_file_and_print_in_terminal(f"Для {video_link} получена информация:\n"
                                                  f"Title: {video_info.title}\n"
                                                  f"Author: {video_info.author}\n"
                                                  f"Playlist количество видео: {len(playlist_info)}")
            except Exception as e:
                print(e)
            # video_title = get_info_about_youtube_video(video_link)[0]
            # download_single_video(video_link=video_link, save_path=save_dir, filename=video_title)

# def download(single_or_playlist: str, download_link: str,
#              base_directory_path=get_value_from_config('DEFAULT_DOWNLOAD_PATH', 'PATH')) -> None:
#     download_type = {"1": download_single_video,
#                      "2": download_playlist}
#
#     download_type[single_or_playlist](download_link, path=Path(base_directory_path))
#
#
# def download_single_video(video_link: str, path=Path.cwd(), file_number=0, is_part_of_playlist=False) -> None:
#     # скачивает видео
#     if random.choice([0, 0, 0, 1]):
#         delay = random.choice([1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9])
#         print_info(f'Перекур: {delay} секунд')
#         time.sleep(delay)
#     remove_symbols = r'«*."/\[]:;-|,»&?!<>'  # символы для исключения в названии файла
#     try:
#         yt = YouTube(video_link)
#         name = str(file_number) + ' ' + ''.join([x for x in yt.title.title().replace(" ", "_")
#                                                  if x not in remove_symbols])[:50] + '.mp4'
#         stream = yt.streams.filter(
#             file_extension='mp4').get_highest_resolution()  # получаем поток с наилучшим качеством
#         try:
#             path_to_save = directory_check_and_creation(Path(path, 'youtube', 'single')) if not is_part_of_playlist \
#                 else directory_check_and_creation(Path(path))
#             stream.download(output_path=path_to_save, filename=name)
#             print_info(f"{name} успешно загружен", color="GREEN")
#         except Exception as e:
#             print_info(f'При загрузке видео произошла ошибка\n{name}\n{yt.watch_url}\n{e}', color="RED")
#     except ConnectionResetError as e:
#         print_info(f'При загрузке видео произошла ошибка\n{video_link}\n{e}', color="RED")
#         delay = random.randint(10, 100)
#         print_info(f'Перекур: {delay} секунд')
#         for i in range(delay):
#             time.sleep(1)
#             if not i % 10:
#                 print(f"{i} / {delay} ", end='')
#         print()
#         download_single_video(video_link, path)
#
#
# def download_playlist(playlist_link: str, path=Path.cwd()):
#     # скачивает playlist
#     p = Playlist(playlist_link)
#     remove_symbols = r'«*."/\[]:;|,»&?!<>'
#     try:
#         title = p.title  # название playlist
#         title = ''.join([x for x in title.replace(" ", "_")
#                          if x not in remove_symbols])
#         final_dir = title
#         path_to_save = directory_check_and_creation(Path(path, "youtube", final_dir))
#         for file_number, video in enumerate(tqdm(p.videos)):
#             download_single_video(video.watch_url, path=Path(path_to_save),
#                                   file_number=file_number, is_part_of_playlist=True)
#     except Exception as e:
#         print_info(f'При получении информации о плейлисте произошла ошибка\n{e}', color="RED")
#         delay = random.choice([1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9])
#         print_info(f'Перекур: {delay} секунд')
#         time.sleep(delay)
#         download_playlist(playlist_link, pat=path)
