import os
import sys
import argparse
import asyncio

from common.util import read_file, get_value_by_path

APP_CONF: dict = None


def conf(key_path: str):
    v = get_value_by_path(APP_CONF, key_path)
    if v is None:
        raise Exception(f"'{key_path}' 설정을 찾을 수 없습니다")
    return v


if APP_CONF is None:
    parser = argparse.ArgumentParser()
    parser.add_argument("env", type=str, action="store", help="환경 이름을 지정합니다")
    args = parser.parse_args()

    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = f"{root_path}/config_{args.env}.json"

    if not os.path.exists(config_path):
        print(f"No such file '{config_path}'")
        sys.exit()
    config = asyncio.run(read_file(config_path, return_type="json"))

    APP_CONF = config["app"]
    APP_CONF["env"] = args.env
