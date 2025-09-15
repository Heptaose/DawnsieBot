import yaml, json, os

def json_file(path, data_dict = None) -> int | dict:

    if data_dict is not None:

        with open(path, 'w', encoding = 'utf-8') as _file:

            json.dump(data_dict, _file, ensure_ascii=False, indent=4)

            return 0

    with open(path, 'rb') as _file:

        return json.load(_file)

def yaml_file(path, data_dict = None) -> int | dict:

    if data_dict is not None:

        with open(path, 'w', encoding = 'utf-8') as _file:

            yaml.dump(data_dict, _file, sort_keys=False, default_flow_style = False)

            return 0

    with open(path, 'rb') as _file:

        return yaml.safe_load(_file)

def file_exists(file_path: str) -> bool:
    
    return os.path.isfile(file_path)