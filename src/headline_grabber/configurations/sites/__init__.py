from pathlib import Path
from typing import Dict
from typing import Type, TypeVar

import yaml
import os

from headline_grabber.models.news_site import NewsSite

T = TypeVar("T")
path = Path(__file__).parent

file_names = os.listdir(path)

sites: [NewsSite] = [] # type: ignore
site_names: Dict[str, str] = {}


def from_dict(data_class: Type[T], data: dict) -> T:
    if hasattr(data_class, "__annotations__"):
        field_types = data_class.__annotations__
        return data_class(
            **{
                key: (
                    from_dict(field_types[key], value)
                    if isinstance(value, dict)
                    else value
                )
                for key, value in data.items()
            }
        )
    else:
        return data


def load_site_config(file_name: str) -> NewsSite:
    if file_name.endswith(".yaml"):
            with open(f"{path}/{file_name}", "r") as file:
                yml = yaml.safe_load(file)
                site_config = from_dict(NewsSite, yml)
                return site_config
    else:
        return None


def get_sites():
    for file_name in file_names:
        site_config = load_site_config(file_name)
        if site_config:
            sites.append(site_config)
            site_names[site_config.abbreviation] = site_config.name


get_sites()
