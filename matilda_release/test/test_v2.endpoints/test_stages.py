import requests,json,pytest
import mysql.connector
import mysql as db
import logging,random
from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import stage, stage_with_tasks
from matilda_release.api.v2.handler import stage_handler
from matilda_release.db.sqlalchemy import api as IMPL

@pytest.fixture()
def random_generators():
    global stage_name
    c = random.randint(1,9999999)
    stage_ui_id = 'Hack_{}'.format(c)
    stage_ui_id_one = 'Demo_{}'.format(c)
    name = 'DemoHack_{}'.format(c)
    name_one = 'new_{}'.format(c)
    resp = stage_handler.get_stage(1)


@pytest.fixture()
def create_environment():
    global headers
    headers = {
        'Content-Type': 'application/json'
    }



def test_get():
    base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1/stages'
    response = requests.get(base_url)
    print(json.dumps(response.json()))
    assert response.status_code == 200


def test_post():
    base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1/stages'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {"stage_id": 2,"stage_ui_id": "Hack","name": "DemoHack","description": "testing","create_dt": "2018-12-03T20:02:06.842Z",
        "planned_start_dt": "2018-12-03T20:02:06.842Z","planned_end_dt": "2018-12-03T20:02:06.842Z","actual_start_dt": "2018-12-03T20:02:06.842Z",
        "actual_end_dt": "2018-12-03T20:02:06.842Z","status_cd": 1,"owner": "Hack","order": 1,"workflow_id": 2}
    response = requests.post(base_url, json.dumps(data), headers=headers)
    assert response.status_code == 201


def test_get():
    base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1/stage/1'
    response = requests.get(base_url)
    #assert response.status_code == 200


# def test_put():
#     base_url='http://localhost:5000/api/rls/release/1/environment/1/workflow/1/stage/1'
#     data= {"stage_id": 1,"stage_ui_id": "New_app","name": "new_mat"}
#     response = requests.put(base_url, json.dumps(data), headers=headers)
#     assert response.status_code == 204
#
#
# def test_delete():
#     base_url='http://localhost:5000/api/rls/release/1/environment/1/workflow/1/stage/1'
#     print("status_code=204")


def test_get_environment(random_generators):
    resp = stage_handler.get_stage(1)
    stage = IMPL.get_stage(1, 1)  # Values from database
    a = len(resp)
    for i in range(0,a):
        if resp[i]['name'] == stage[0]['name']:
            e = resp[i]

            #assert e['stage_id'] == stage[0]['stage_id']
            assert e['stage_ui_id'] == stage[0]['stage_ui_id']
            assert e['status_cd'] == stage[0]['status_cd']
            assert e['name'] == stage[0]['name']
            assert e['owner'] == stage[0]['owner']


def test_create_stage(random_generators):
    args = {"stage_id": 10,"stage_ui_id": "dev","name": "new","status_cd": 1,
    "status_description": "Defined","owner": "matilda","order": 1,"workflow_id": 1}
    stage =  stage_handler.create_stage(1, args)
    print(stage)
    #assert args['stage_id'] == stage[0]['stage_id']
    assert args['stage_ui_id'] == stage[0]['stage_ui_id']
    assert args['status_cd'] == stage[0]['status_cd']
    assert args['name'] == stage[0]['name']
    assert args['owner'] == stage[0]['owner']
