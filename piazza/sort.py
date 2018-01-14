import os
import json
from glob import glob
from slugify import slugify


def iter_post_paths(dir_=''):
    for path in glob(os.path.join(dir_, '*.json')):
        yield path


def iter_posts(dir_=''):
    for path in iter_post_paths(dir_):
        with open(path) as file_:
            post = json.load(file_)
        yield post


def get_folders(post):
    return [slugify(f) for f in post.get('folders', [])]
