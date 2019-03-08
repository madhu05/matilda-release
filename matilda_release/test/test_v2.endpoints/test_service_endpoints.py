import logging
import pytest,random,requests,json
from flask import request
from flask_restplus import Resource
from matilda_release.db.sqlalchemy import api as IMPL
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import service, action, service_fields, services_with_actions_fields, services_by_category
from matilda_release.api.v2.handler import service_handler


pytest.mark.random_generators
@pytest.fixture(scope='module')
def random_generators():
    global service_name,unique_service_id
    c = random.randint(1, 99999999)
    service_name = 'test_service{}'.format(c)
    unique_service_id = random.randint(1, 999999999)


def test_post_service(random_generators):

    type = 'application/json'

    global headers
    headers = {
        'Content-Type': type,
        'Accept': type
                }
    global dat
    dat= {
        "service_id": unique_service_id,
        "name": service_name,
        "category": "max_stringv",
        "comments": "This is demo Test",
        "actions": [
            {
                "action_id": 1,
                "name": "mex_stringv",
                "description": "This is demo action",
                "service_id": unique_service_id
            }
        ]
            }
    print(dat['name'])
    print(dat['service_id'])


    url = 'http://localhost:5000/api/plugin/services'
    response = requests.post(url, data=json.dumps(dat), headers=headers)
    assert response.status_code == 201

def test_create_service(random_generators):

    dat= {
        "service_id": unique_service_id,
        "name": service_name,
        "category": "max_stringv",
        "comments": "This is demo Test",
        "actions": [
            {
                "action_id": 1,
                "name": "mex_stringv",
                "description": "This is demo action",
                "service_id": 1
            }
        ]
            }
    print(dat['name'])

    resp = IMPL.create_service(dat)


    assert resp['service_id'] == dat.get('service_id')
    assert resp['category'] == dat.get('category')
    assert resp['comments'] == dat.get('comments')
    assert resp['name'] == dat.get('name')


def test_get_service():

    url= 'http://localhost:5000/api/plugin/services'
    response = requests.get(url)
    assert response.status_code == 200


def test_post_serviceid_action():

    global unique_action_id
    unique_action_id = random.randint(1, 999999999)
    type = 'application/json'

    global headers
    headers = {
        'Content-Type': type,
        'Accept': type
    }
    global dat
    dat = {
        "action_id": unique_action_id,
        "name": "nedw_dqmo",
        "description": "xnew_string",
        "service_id": 1
    }

    url = 'http://localhost:5000/api/plugin/service/1/actions'
    response = requests.post(url, data=json.dumps(dat), headers=headers)
    assert response.status_code == 201


def test_get_service_id():

    url= 'http://localhost:5000/api/plugin/service/1'
    response = requests.get(url)
    assert response.status_code == 200

def create_service_id_action():

    global unique_action_id
    unique_action_id = random.randint(1, 999999999)

    args ={
        "action_id": unique_action_id ,
        "name": "nedw_dqmo",
        "description": "xnew_string",
        "service_id": 1
    }
    resp = IMPL.create_action(args)

    assert resp['action_id'] == args.get('action_id')
    assert resp['name'] == args.get('name')
    assert resp['description'] == args.get('description')
    assert resp['service_id'] == args.get('service_id')

