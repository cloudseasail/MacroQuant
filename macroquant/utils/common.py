import pandas as pd
import json
import sys
from datetime import datetime, time
from pathlib import Path

def AppendSeries(df, series, ignore_index=True):
    return pd.concat([df,pd.DataFrame(series).T],ignore_index=ignore_index)

SETTING_FILE_NAME = "settings.json"
TEMP_FOLDER = ".cache"


def _get_temp_dir(temp_name: str=TEMP_FOLDER):
    cwd: Path = Path.cwd()
    temp_path: Path = cwd.joinpath(temp_name)

    if temp_path.exists():
        return temp_path

    if not temp_path.exists():
        temp_path.mkdir()

    return temp_path


def get_file_path(filename: str) -> Path:
    """
    Get path for temp file with filename.
    """
    return _get_temp_dir().joinpath(filename)


def load_json(filename: str) -> dict:
    """
    Load data from json file in temp path.
    """
    filepath: Path = get_file_path(filename)

    if filepath.exists():
        with open(filepath, mode="r", encoding="UTF-8") as f:
            data: dict = json.load(f)
        return data
    else:
        save_json(filename, {})
        return {}
    
def save_json(filename: str, data: dict) -> None:
    """
    Save data into json file in temp path.
    """
    filepath: Path = get_file_path(filename)
    with open(filepath, mode="w+", encoding="UTF-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

def load_setting():
    return load_json(SETTING_FILE_NAME)
def save_setting(d):
    data = load_setting()
    for name in d:
        data[name] = d[name]
    save_json(SETTING_FILE_NAME, data)