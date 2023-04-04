from colorama import Style, Fore


def print_info(msg: str, color='YELLOW', end='\n',
               print_separator_before=True, print_separator_after=False, separator="*") -> None:
    # печать однострочных сообщений с цветом
    colors = {'yellow': Fore.YELLOW, 'желтый': Fore.YELLOW,
              'green': Fore.GREEN, 'зеленый': Fore.GREEN,
              'red': Fore.RED, 'красный': Fore.RED,
              'blue': Fore.BLUE, 'синий': Fore.BLUE,
              'magenta': Fore.MAGENTA, 'фиолетовый': Fore.MAGENTA,
              '1': Fore.WHITE
              }
    if print_separator_before:
        print(f"{separator * 200}")
    print(colors.get(color, Fore.YELLOW) + str(msg) + Style.RESET_ALL, end=end)
    if print_separator_after:
        print(f"{separator * 200}")