import shutil
import time
from datetime import datetime
from pathlib import Path
import configparser
from utils.log import log_in_file_and_print_in_terminal
import subprocess

config = configparser.ConfigParser()
config_path = Path('config.ini')
config.read(config_path, encoding='utf-8')


def path_create(fin_dir: str):
    try:
        path = Path(f"/home/behappyman/mnt_nas_handmaderezerv/_GIT_STUDY_PET/DB/{fin_dir}")
        path.mkdir(parents=True, exist_ok=True)

    except Exception as e:
        path = Path(f"\\\\192.168.2.222\\handmaderezerv\\_GIT_STUDY_PET\\DB\\{fin_dir}")
        path.mkdir(parents=True, exist_ok=True)
    return path


def dump_dbs(host, user, password, db_list, save_path, port='3306'):
    for db in db_list:
        try:
            subprocess.Popen(f'mysqldump -h {host} -P {port} -u {user} -p{password} {db} > {save_path}/{db}.sql',
                             shell=True)
        except Exception as e:
            log_in_file_and_print_in_terminal(f"При сохранении БД {db}: {e}")


for db_config in ['DB_ISKANDAR', "DB_SAPRONOVO_FROM_OUT"]:
    cur_time = str(datetime.now()).split('.')[0].replace(':', '_').replace("-", "_").replace(" ", '_')
    save_dir = path_create(f"{db_config}_{cur_time}")

    host = config[db_config]['HOST']
    user = config[db_config]['USER']
    password = config[db_config]['PASSWORD']
    dbs = eval(config[db_config]['dbs'])

    dump_dbs(host, user, password, dbs, save_dir)
    time.sleep(3)
    shutil.make_archive(f"{save_dir}", 'zip', save_dir)
    time.sleep(3)
    shutil.rmtree(save_dir)
