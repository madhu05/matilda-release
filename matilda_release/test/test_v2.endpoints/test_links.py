import requests
import pytest,random
import json
import mysql.connector
import mysql as db
import logging
from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import release_link, release_link_items
from matilda_release.api.v2.handler import release_link_handler
from matilda_release.db.sqlalchemy import api as IMPL


@pytest.fixture()
def random_generators():
    global name
    c = random.randint(1,9999999)
    name = 'new_link_{}'.format(c)
    name_one = 'sampleapp_{}'.format(c)
    source = 'matilda_{}'.format(c)
    source_one = 'new_{}'.format(c)
    #resp = release_link_handler.get_release_links(1)


@pytest.fixture()
def create_relaese_link():
    global headers
    headers = {
        'Content-Type': 'application/json'
    }
# def test_get():
#     base_url = 'http://localhost:5000/api/rls/release/1/links'
#     response = requests.get(base_url)
#     #print(json.dumps(response.json()))
#     assert response.status_code == 200


def test_post(random_generators,create_relaese_link):
    base_url = 'http://localhost:5000/api/rls/release/1/links'
    data = {"release_link_id": 1,"name": "sampleapp","url": "http://ghgkli/kyu","source": "sample","description": "posting","release_id": 1}
    response = requests.put(base_url, json.dumps(data), headers=headers)
    assert response.status_code == 204


def test_get():
    base_url = 'http://localhost:5000/api/rls/release/1/link/1/items'
    response = requests.get(base_url)
    print(json.dumps(response.json()))
    assert response.status_code == 200


def test_post(create_relaese_link,random_generators):
    base_url = 'http://localhost:5000/api/rls/release/1/link/1/items'
    data = {
        "release_link_item_id": 1,
        "data": "Posting",
        "release_link_id": 1
}
    response = requests.post(base_url, json.dumps(data), headers=headers)
    assert response.status_code == 201


# def test_put():
#     base_url='http://localhost:5000/api/rls/release//link/2/items'
#     data = {
#         "release_link_item_id": 2,
#         "data": "updating",
#         "release_link_id": 2
#     }
#     response = requests.put(base_url, json.dumps(data), headers=headers)

# def test_delete():
#     base_url = 'http://localhost:5000/api/rls/release/1/link/1/items'



def test_create_release_links(random_generators,create_relaese_link):
    args = {"release_link_id": 2,"name": "demo_link","url": "http://ghtjkyd.com","source": "matilda","description": "posting","release_id": 1}
    api= release_link_handler.create_release_link(1,args)
    print(release_link)

    #assert api['release_link_id'] == args['release_link_id']
    assert api['name'] == args['name']
    assert api['url'] == args['url']
    assert api['source'] == args['source']
    assert api['description'] == args['description']


@pytest.mark.get_release_link_item
def test_get_release_link_item(random_generators,create_relaese_link):
    resp = release_link_handler.get_release_link_item(1, 1)
    db = IMPL.get_release_link_items(1,1) # Values from database
    a = len(resp)
    for i in range(0,a):
        if resp[i]['data'] == db[0]['data']:
            e = resp[i]
            assert e['release_link_item_id'] == db[0]('release_link_item_id')
            assert e['data'] == db('data')
            assert e['release_link_id'] == db[0]('release_link_id')


def test_create_release_link_item(random_generators,create_relaese_link):
    args = {"release_link_item_id": 2, "release_link_id": 2}
    db = IMPL.create_release_link_item(1)
    print(release_link)

    #assert api['release_link_id'] == args['release_link_id']
    assert args['release_link_item_id'] == db('release_link_item_id')
    assert args['data'] == args
    assert args['release_link_id'] ==db('release_link_id')

