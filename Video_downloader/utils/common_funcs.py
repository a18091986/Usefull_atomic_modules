import configparser


def get_value_from_config(config_chapter: str, value_name: str) -> str:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    value = config[config_chapter][value_name]
    return value
