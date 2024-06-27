from pathlib import Path
from typing import Dict
from typing import Type, TypeVar

import yaml
import os

from src.headline_grabber.models.news_site import NewsSite

T = TypeVar("T")
path = Path(__file__).parent

file_names = os.listdir(path)

sites: [NewsSite] = []
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


for file_name in file_names:
    if file_name.endswith(".yaml"):
        with open(f"{path}/{file_name}", "r") as file:
            yml = yaml.safe_load(file)
            site_config = from_dict(NewsSite, yml)
            sites.append(site_config)
            site_names[site_config.abbreviation] = site_config.name
