# coding: utf-8

from piazza_api import Piazza
import json


def save(post):
    cid = post.get('nr')
    if cid is not None:
        with open('{}.json'.format(cid), 'w') as f:
            json.dump(post, f, indent=2)


p = Piazza()
p.user_login()
ga = p.network('j6f5zm92gj34gi')

for post in ga.iter_all_posts():
    save(post)
