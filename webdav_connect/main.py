from dataclasses import dataclass
from dotenv import dotenv_values
import webdav.client as wc


env = dotenv_values(".env")

options = {
    'webdav_hostname': env.get("web_dav_nas_hostname"),
    'webdav_login': env.get("web_dav_nas_login"),
    'webdav_password': env.get("web_dav_nas_password")
}

client = wc.Client(options)

if __name__ == "__main__":
    print(client)