import re
import os
import json
import base64
import xml.etree.ElementTree as ET
import xmltodict
from Crypto.Cipher import AES
from datetime import datetime


async def mkdir(path: str):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


async def get_files_recursive(directory: str, extensions=None):
    """
    특정 폴더 및 해당 폴더의 하위 폴더 내에 있는 모든 파일들의 목록을 재귀적으로 가져오는 함수

    :param extensions: 필터링할 확장자 배열
    """
    files_list = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            if extensions is None or filename.endswith(tuple(extensions)):
                filepath = os.path.join(root, filename).replace("\\", "/")
                files_list.append(filepath)

    return files_list


async def files_to_dict(path: str, start_path=None, excludes_dir=[], ext_filter=[]):
    path = path.replace("\\", "/")
    folder_name = os.path.basename(path)
    if folder_name in excludes_dir:
        return None
    if start_path is None:
        start_path = path

    _, ext = os.path.splitext(path)
    id, _ = os.path.splitext(path[len(start_path) + 1 :])
    result = {"id": id, "name": os.path.splitext(folder_name)[0]}

    if os.path.isdir(path):
        children = [
            await files_to_dict(
                os.path.join(path, child), start_path, excludes_dir, ext_filter
            )
            for child in os.listdir(path)
            if not child.startswith(".")
        ]
        children = [child for child in children if child is not None]

        if children:
            children.sort(
                key=lambda x: (not x.get("children", False), x.get("name", "").lower())
            )
            result["children"] = children
        else:
            return None

    if os.path.isfile(path) and not (ext in ext_filter):
        return None

    return result


async def read_file(filepath: str, encoding="utf-8", return_type="text", format_json=False):
    """
    파일의 내용을 반환하는 함수

    :param filepath: 파일 경로
    :param encoding: 인코딩 방식 (기본값: utf-8)
    :param return_type: 반환 타입 (text/json/xml, 기본값: text)
    :return: 파일 내용을 지정한 반환 타입으로 변환한 결과
    """
    with open(filepath, "r", encoding=encoding) as f:
        content = f.read()

    if return_type == "text":
        return content
    elif return_type == "json":
        return json.loads(content)
    elif return_type == "xml":
        return ET.fromstring(content)
    elif return_type == "xmldict":
        result = xmltodict.parse(content)
        if format_json:
            return json.loads(json.dumps(result))
        else:
            return json.loads(json.dumps(result, indent=4))
    else:
        raise ValueError(
            "Invalid return_type. Please specify 'text' or 'json' or 'xml'."
        )


async def save_json(file_path: str, content: dict, encoding="utf-8"):
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


def is_json(obj: any):
    try:
        json.loads(obj)
        return True
    except:
        return False


def is_xml(obj: any):
    try:
        ET.fromstring(obj)
        return True
    except:
        return False


def get_backup_path(file_path):
    extless, ext = os.path.splitext(file_path)
    path, filename = os.path.split(extless)
    paths = path.split("/")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return os.path.join(
        paths[0], "backup", os.sep.join(paths[1:]), f"{filename}{ext}.{timestamp}"
    ).replace("\\", "/")


def get_value_by_path(d: dict, path: str):
    if not path:
        return d

    # 경로를 분할하고 배열 인덱스를 처리하는 함수
    def parse_path(path):
        parts = re.split(r'[\.\[\]]', path)
        return [part for part in parts if part]

    keys = parse_path(path)

    for key in keys:
        if isinstance(d, list):
            try:
                key = int(key)
            except ValueError:
                return None

            if key < 0 or key >= len(d):
                return None
        else:
            if key not in d:
                return None

        d = d[key]

    return d


def find_dict_by_key_value(dict_list: list, target_key: str, target_value: any):
    for d in dict_list:
        if target_key in d and d[target_key] == target_value:
            return d
        elif "children" in d and d["children"] is not None:
            nested_result = find_dict_by_key_value(
                d["children"], target_key, target_value
            )
            if nested_result is not None:
                return nested_result
    return None


def is_dict_equals(dict1: dict, dict2: dict, except_keys: list):
    copy1 = dict1.copy()
    copy2 = dict2.copy()

    for key in except_keys:
        if key in copy1:
            del copy1[key]
        if key in copy2:
            del copy2[key]

    return copy1 == copy2


def extract_form_fields(soup, form_selector):
    data = {}
    form = soup.select_one(form_selector)

    for input in form.findAll("input"):
        if not input.has_attr("name"):
            continue

        if input["type"] in ("submit", "image"):
            continue

        if input["type"] in ("text", "hidden", "password", "submit", "image", "tel", "number", "date"):
            value = ""
            if input.has_attr("value"):
                value = input["value"]
            k = input["name"]
            if k in data:
                if not isinstance(data[k], list):
                    arr = []
                    arr.append(data[k])
                    data[k] = arr
                data[k].append(value)
            else:
                data[k] = value
            continue

        if input["type"] in ("checkbox", "radio"):
            value = ""
            if input.has_attr("checked"):
                if input.has_attr("value"):
                    value = input["value"]
                else:
                    value = "on"
            data[input["name"]] = value
            continue

        assert False, "input type %s not supported" % input["type"]

    for textarea in form.findAll("textarea"):
        if not textarea.has_attr("name"):
            continue
        data[textarea["name"]] = textarea.string or ""

    for select in form.findAll("select"):
        if not select.has_attr("name"):
            continue
        value = ""
        options = select.findAll("option")
        is_multiple = select.has_attr("multiple")
        selected_options = [
            option for option in options
            if option.has_attr("selected")
        ]

        if not selected_options and options:
            selected_options = [options[0]]

        if not is_multiple:
            if len(selected_options) == 1:
                value = selected_options[0]["value"]
        else:
            value = [option["value"] for option in selected_options]

        data[select["name"]] = value
    return data


def encrypt(pepper: str, msg: str):
    cipher = AES.new(pepper.encode(), AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode("utf-8"))
    return base64.b64encode(nonce + tag + ciphertext).decode("utf-8")


def decrypt(pepper: str, encrypted_data: str):
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        nonce = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        cipher = AES.new(pepper.encode(), AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        cipher.verify(tag)
        return plaintext.decode("utf-8")
    except:
        return None