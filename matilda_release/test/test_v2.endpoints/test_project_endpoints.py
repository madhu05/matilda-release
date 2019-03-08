import pytest,requests,json,random
import datetime
import logging
from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import project, project_with_apps
from matilda_release.api.v2.handler import project_handler
from matilda_release.db.sqlalchemy import api as IMPL
#from matilda_release.api.v2.app import main


#@pytest.mark.random_generators
@pytest.fixture()
def random_generators():
    c = random.randint(1, 999999999)
    global project_id, project_name,project_id_one,project_name_one
    project_id = 'test_NSTP{}'.format(c)
    project_id_one = 'demo_NSTP{}'.format(c)
    project_name ='DEMO_test{}'.format(c)
    project_name_one ='test_demo{}'.format(c)


    resp = project_handler.get_projects()


@pytest.fixture()
def create_project(random_generators):
    global project_id, project_name
    type = 'application/json'
    global headers
    headers = {
        'Content-Type': type,
        'Accept': type
    }
    global data
    data = {
        "project_id": project_id,
        "name": project_name,
        "owner": 'Matilda',
        "create_dt": "2018-10-01T00:00:00",
        "status": "Non-Active"
    }



def test_post_project(create_project):
    url = 'http://localhost:5000/api/rls/projects'
    response = requests.post(url,data=json.dumps(data),headers=headers)
    assert response.status_code == 201




def test_get_project():
    url = 'http://localhost:5000/api/rls/projects'
    resp = project_handler.get_projects()
    response = requests.get(url)
    assert response.status_code == 200



def test_create_project(random_generators):
    global get_var,args
    args = {'project_id': project_id_one, 'name': project_name_one, 'create_dt': '2018-10-01T00:00:00',
            'status': 'Active', 'owner': 'Matilda'}
    get_var = args['project_id']
    project = project_handler.create_project(args)
    print(project)

    assert project['project_id'] == args['project_id']
    assert project['name'] == args['name']
    #assert project['create_dt'] == args['create_dt']
    assert project['status'] == args['status']
    assert project['owner'] == args['owner']


def test_get_project():

    global a,res
    db_values =IMPL.get_projects(project_id=None)
    resp = project_handler.get_projects()
    a=len(resp)
    for i in range(0,a-1):
        if resp[i]['project_id'] == db_values[0]['project_id']:
            res = resp[i]

    assert res['project_id'] == db_values[0]['project_id']
    assert res['name'] == db_values[0]['name']
    assert res['owner'] == db_values[0]['owner']
    assert res['create_dt'] == db_values[0]['create_dt']
    assert res['status'] == db_values[0]['status']




