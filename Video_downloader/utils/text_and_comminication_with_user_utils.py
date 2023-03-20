from colorama import Fore, Style


def select_playlist_or_single_video_download():
    # выбор типа скачиваемого - плэйлист или отдельное видео
    download_video_choice = input(f'1 - скачать отдельное видео\n'
                                  f'2 - скачать playlist \n')

    while download_video_choice not in ['1', '2']:
        download_video_choice = input(f'1 - скачать отдельное видео\n'
                                      f'2 - скачать playlist \n')
    return download_video_choice


def select_download_path():
    # выбор пути скачивания видео
    download_video_path = input(f'1 - скачать в папку запуска программы\n'
                                f'2 - скачать в DOWNLOAD на MAIN_WINDOWS\n'
                                f'3 - скачать в TRASH на SYNOLOGY\n'
                                f'4 - скачать в MAIN MAIN_LINUX\n')

    while download_video_path not in ['1', '2', '3']:
        download_video_path = input(f'1 - скачать в папку запуска программы\n'
                                    f'2 - скачать в DOWNLOAD на MAIN_WINDOWS\n'
                                    f'3 - скачать в TRASH на SYNOLOGY\n'
                                    f'4 - скачать в MAIN MAIN_LINUX\n')
    return download_video_path


def get_download_link_from_user():
    return input("Ссылка для скачивания: \n")


def print_info(msg: str, color='YELLOW') -> None:
    # печать однострочных сообщений с цветом
    fore_color = {"YELLOW": Fore.YELLOW, "RED": Fore.RED, "GREEN": Fore.GREEN}
    print(fore_color.get(color, Fore.YELLOW) + msg + Style.RESET_ALL)
