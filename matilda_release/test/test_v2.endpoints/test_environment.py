import json
import pytest
import random

import requests

from matilda_release.api.v2.handler import environment_handler
from matilda_release.db.sqlalchemy import api as IMPL


@pytest.fixture()
def random_generators():
    global env_name
    c = random.randint(1,9999999)
    name = 'new_env_{}'.format(c)
    name_one = 'Demo_{}'.format(c)
    env_type = 'test_{}'.format(c)
    env_type_one = 'new_{}'.format(c)
    resp = environment_handler.get_environment()


@pytest.fixture()
def create_environment():
    global headers
    headers = {
        'Content-Type': 'application/json'
    }


def test_get_EnvironmentCollection():
    base_url = 'http://localhost:5000/api/rls/release/2/envs'
    response = requests.get(base_url)
    assert response.status_code == 200


def test_post_EnvironmentCollection(create_environment,random_generators):
    data={"env_id": 11,"name": "Demonew", "env_type_cd": 2,"start_dt": "2018-12-26T22:00:37",
  "create_dt": "2018-12-26T16:35:33","status_cd": 1,"status_description": "Defined","env_type_description": "Testing",
        "release_id": 1}
    base_url = 'http://localhost:5000/api/rls/release/1/envs'
    response= requests.post(base_url, json.dumps(data),headers=headers)
    #assert response.status_code == 200


def test_get_EnvironmentItem():
    base_url = 'http://localhost:5000/api/rls/release/1/env/1'
    response = requests.get(base_url)
    assert response.status_code == 200


# def test_put_EnvironmentItem():
#     base_url = 'http://localhost:5000/api/rls/release/1/env/1'
#     data = {"env_id": 1,"name": "DemoModify","type": "New_App"}
#     response = requests.put(base_url, json.dumps(data), headers=headers)
#     assert response.status_code == 204


# def test_post_CloneEnvironment(create_environment):
#     base_url = 'http://localhost:5000/api/rls/release/2/env/2/clone'
#     data={"env_id": 2,"env_name": "MatildaDemoo","env_type": "Development","wf_id": 2}
#     response = requests.post(base_url,json.dumps(data),headers=headers)
#     assert response.status_code == 200


def test_get_EnvironmentItemActions():
    base_url = 'http://localhost:5000/api/rls/release/1/env/1/action/pass'
    response = requests.get(base_url)
    pass


# def test_post_EnvironmentItemActions(random_generators,create_environment):
#     base_url = 'http://localhost:5000/api/rls/release/1/env/1/action/start'
#     resp = environment_handler.start_environment(1, 1)
#     a = len(resp)
#     for i in range(0,a):
#         if i['action'] == 'start':
#             print('action {}'.format('action'))
#             return True


@pytest.mark.get_environments
def test_get_environment(random_generators):
    resp = environment_handler.get_environments(1)
    env = IMPL.get_environment(1, 1)  # Values from database
    a = len(resp)
    for i in range(0,a):
        if resp[i]['name'] == env[0]['name']:
            e = resp[i]

            assert e['name'] == env[0]['name']
            assert e['version'] == env[0]['version']
            assert e['create_dt'] == env[0]['create_dt']
            assert e['status_type_cd'] == env[0]['status_type_cd']
            assert e['status_description'] == env[0]['status_description']
            assert e['release_id'] == env[0]['release_id']


def test_create_environment(random_generators):
    global get_var, args
    args = {"env_id": 2,"name": "demo_test44087","type": "env_type","create_dt": "2018-12-03T03:10:53.166Z",
            "start_dt": "2018-12-03T03:10:53.166Z","end_dt": "2018-12-03T03:10:53.166Z",
        "status_cd": 1,"release_id": 3}
    env = environment_handler.create_environment(release_id=3, args=args)
    print(env)

    #assert env['env_id'] == args['env_id']
    assert env['name'] == args['name']
    assert env['status_cd'] == args['status_cd']
    #assert env['release_id'] == args['release_id']


def test_get_environment():
    resp = environment_handler.get_environment_details(1,2)
    env = IMPL.get_environment(1, 2)  # Values from database
    a = len(resp)
    for i in range(0,a):
        if resp[0]['name'] == env[0]['name']:
            e = resp[i]

            assert e['name'] == env[1]['name']
            assert e['version'] == env[1]['version']
            assert e['create_dt'] == env[1]['create_dt']
            assert e['status_type_cd'] == env[1]['status_type_cd']
            assert e['status_description'] == env[1]['status_description']
            assert e['release_id'] == env[1]['release_id']


# def test_create_environment(random_generators):
#     global get_var, args
#     args = {"env_id": 2,"name": "env_name_one","type": "env_type_one","create_dt": "2018-12-03T03:10:53.166Z","start_dt": "2018-12-03T03:10:53.166Z","end_dt": "2018-12-03T03:10:53.166Z",
#         "status_cd": 1,"release_id": 1}
#     get_var = args['env_id']
#     env = environment_handler.clone_environment(release_id=None,env_id=None)
#
#     assert env['env_id'] == args['env_id']
#     assert env['name'] == args['name']
#     assert env['type'] == args['type']
#     assert env['status_cd'] == args['status_cd']
#     assert env['release_id'] == args['release_id']




