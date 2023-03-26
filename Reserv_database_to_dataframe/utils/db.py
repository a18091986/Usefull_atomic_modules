import pathlib
from datetime import datetime
import mysql.connector
from pathlib import Path
import configparser
import pandas as pd
from sqlalchemy import create_engine, text


def mysql_db_connect(user, password, host, database=None):
    if database:
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    else:
        engine = create_engine(f"mysql+pymysql://admin:0gfyfctyr0MYSQL@192.168.2.159")
    return engine


def my_mysql_db_connect(database=None, port=3306):
    """соединение с БД"""
    if database:
        con = mysql.connector.connect(user=user, password=password, host=host,
                                      port=port, database=database)
    else:
        con = mysql.connector.connect(user=user, password=password, host=host)
    cursor = con.cursor()
    return con, cursor


def df_from_db_table(database: str, table: str) -> pd.DataFrame:
    # connection, cursor = my_mysql_db_connect(database=database)
    engine = mysql_db_connect(user, password, host, database)
    connection = engine.connect()
    query = "select * from {}".format(table)
    return pd.read_sql(text(query), connection)


def save_df_from_db_table(database: str, table: str):
    out_path = pathlib.Path('BACKUP', f"{'_'.join(reversed(str(datetime.now().date()).split('-')))}",
                            f"{database}")
    out_path.mkdir(parents=True, exist_ok=True)
    df_from_db_table(database, table).to_csv(pathlib.Path(out_path, f"{table}.csv"), index=False)


def show_all_tables(database: str):
    connection, cursor = my_mysql_db_connect(database=database)
    query = "show tables"
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def show_all_databases():
    connection, cursor = my_mysql_db_connect()
    query = "show databases"
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall() if x[0] not in
            ('information_schema', 'mysql', 'performance_schema', 'sys')]


def show_all_columns(databse: str, table: str):
    connection, cursor = my_mysql_db_connect(databse)
    query = "show columns from {}".format(table)
    cursor.execute(query)
    return [x[0] for x in cursor.fetchall()]


def show_all_db_tables_columns():
    for db in show_all_databases():
        print(f" -database: {db}")
        for table in show_all_tables(db):
            print(f"\t\t -table: {table}")
            for column in show_all_columns(db, table):
                print(f"\t\t\t\t -column: {column}")


def save_all_tables_from_all_db():
    for db in show_all_databases():
        print(f" -database: {db}")
        for table in show_all_tables(db):
            save_df_from_db_table(database=db, table=table)


if __name__ == '__main__':
    # engine = mysql_db_connect()
    # insp = inspect(engine)
    # db_list = insp.get_schema_names()
    # print(db_list)

    config_path = '../config.ini'
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')

    host = config['DB']['HOST']
    user = config['DB']['USER']
    password = config['DB']['PASSWORD']

    engine = mysql_db_connect(user, password, host)
    connection = engine.connect()

else:
    config_path = Path('config.ini')
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')

    host = config['DB']['HOST']
    user = config['DB']['USER']
    password = config['DB']['PASSWORD']
