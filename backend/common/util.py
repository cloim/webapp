import json
import xml.etree.ElementTree as ET
import xmltodict


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


def get_value_by_path(d: dict, path: str):
    if not path:
        return d

    keys = path.split(".")

    for key in keys:
        if key not in d:
            return None
        d = d.get(key)

    return d


async def is_json(obj: any):
    try:
        json.loads(obj)
        return True
    except:
        return False


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
