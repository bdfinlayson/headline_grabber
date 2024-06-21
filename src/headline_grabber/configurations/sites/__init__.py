from pathlib import Path
import yaml
import os

from ...models.news_site import NewsSite

path = Path(__file__).parent

file_names = os.listdir(path)

sites = []

for file_name in file_names:
    if file_name.endswith(".yaml"):
        with open(f'{path}/{file_name}', 'r') as file:
            yml = yaml.safe_load(file)
            site_config = NewsSite(**yml)
            sites.append(site_config)
