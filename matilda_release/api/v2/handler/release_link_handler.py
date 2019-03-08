import collections
import uuid
import requests
import json
import os

from matilda_release.db.sqlalchemy.models import ReleaseLink, ReleaseLinkItem
from matilda_release.api.v2.model.model import release_link, release_link_items

from datetime import datetime
from six import iteritems

from matilda_release.db import api as db_api

def get_release_link(release_id=None, link_id=None, filter=None):
    rls_info = db_api.get_release_links(release_id, link_id, filter)
    for item in rls_info:
        for key in release_link:
            if key not in rls_info.keys():
                item[key] = None
    return rls_info


def get_release_link_item(release_link_id=None, link_item_id=None, filter=None):
    rls_info = db_api.get_release_link_items(release_link_id, link_item_id, filter)
    print ("item resp {0}".format(rls_info))
    for item in rls_info:
        for key in release_link_items:
            if key not in item.keys():
                item[key] = None
    return rls_info


def create_release_link(release_id, args):
    rls_link = ReleaseLink()
    rls_link.release_id = release_id
    rls_link.description = args.get('description')
    rls_link.name = args.get('name')
    rls_link.source = args.get('source')
    rls_link.url = args.get('url')
    resp = db_api.create_release_link(rls_link)
    return resp


def create_release_link_item(release_link_id, args):
    rls_link = ReleaseLinkItem()
    rls_link.release_link_id = release_link_id
    rls_link.data = args
    resp = db_api.create_release_link_item(rls_link)
    print(resp)
    return resp

