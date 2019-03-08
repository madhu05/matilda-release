import collections
import uuid
import requests
import json
import os
from matilda_release.db.sqlalchemy import api as IMPL
from matilda_release.db.sqlalchemy.models import ReleaseLink, ReleaseLinkItem
from matilda_release.api.v2.model.model import release_link, release_link_items

from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api


def test_create_release_link():
    args = {"release_link_id": 1,"name": "new_link","url": "http://yilykfjmgcf/gh/","source": "matilda","description": "posting","release_id": 1}
    rls_link = ReleaseLink()
    rls_link.release_id = 1
    rls_link.description = args.get('description')
    rls_link.name = args.get('name')
    rls_link.source = args.get('source')
    rls_link.url = args.get('url')
    resp = IMPL.create_release_link(rls_link)
    assert resp['name'] == args.get('name')
    assert resp['source'] == args.get('source')
    assert resp['url'] == args.get('url')
    assert resp['description'] == args.get('description')


def test_get_release_link_item():
    args={ "release_link_item_id": 1,"data": "{'data': 'matilda', 'release_link_id': 1, 'release_link_item_id': 1}","release_link_id": 1}
    rls_info = db_api.get_release_link_items(1, 1)
    resp = IMPL.get_release_link_items(1, 1)
    print("item resp {0}".format(rls_info))
    for item in rls_info:
        for key in release_link_items:
            if key not in item.keys():
                item[key] = None
                assert resp['release_link_item_id'] == args.get('release_link_item_id')
                assert resp['data'] == args.get('data')
                assert resp['release_link_id'] == args.get('release_link_id')


def test_create_release_link_item():
    args = {"release_link_item_id": 2,"release_link_id": 2}
    rls_link = ReleaseLinkItem()
    rls_link.release_link_id = 2
    rls_link.data = args
    resp = IMPL.create_release_link_item(rls_link)
    print(resp)
    assert resp['release_link_item_id'] == args.get('release_link_item_id')
    assert resp['data'] == args
    assert resp['release_link_id'] == args.get('release_link_id')
