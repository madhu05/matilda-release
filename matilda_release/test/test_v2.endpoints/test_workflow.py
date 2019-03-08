import requests,json,pytest,random
import mysql.connector
from matilda_release.api.v2.endpoints.workflow import workflow
from matilda_release.db.sqlalchemy import api as IMPL

from matilda_release.api.v2.model.model import workflow, workflow_with_stages, environment_with_workflow, template, \
    templates_drop_down, frequency
from matilda_release.api.v2.handler import workflow_handler

import mysql as db

@pytest.fixture()
def random_generators():
    global name
    c = random.randint(1,9999999)
    name = 'new_wf_{}'.format(c)
    descripion = 'posting_{}'.format(c)
    resp = workflow_handler.get_workflow(1)


@pytest.fixture()
def create_workflow():
    global headers
    headers = {
        'Content-Type': 'application/json'
    }


def test_get():
    base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflows'
    response = requests.get(base_url)
    assert response.status_code == 200


def test_post(create_workflow):
    base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflows'
    data = {"wf_id": 1,"name": "matdemo","template_id": 1,"description": "posting","status_cd": 1,"release_id": 1,
          "release": "dev","frequency_cd": 1,"env_id": 6,"overall_progress": 2,"environment_name": "DemoModify"}
    response = requests.post(base_url, json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_get():
    base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1'
    response = requests.get(base_url)
    print(json.dumps(response.json()))
    assert response.status_code == 200

#
# def test_put():
#     base_url='http://localhost:5000/api/rls/release/1/environment/1/workflow/1'
#     data = {
#           "wf_id": 1,"name": "matdemo","template_id": 1,
#           "description": "updating","status": "active"}
#     response = requests.put(base_url, json.dumps(data), headers=headers)
#     assert response.status_code == 200
#
#
# def test_delete():
#     base_url = 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1'
#     print("status_code=200")


def test_get():
    base_url='http://localhost:5000/api/rls/release/1/environment/1/workflow/1/extended'
    response = requests.get(base_url)
    assert response.status_code == 200


def test_get():
    base_url= 'http://localhost:5000/api/rls/release/1/environment/1/workflow/1/action/Run'
    response = requests.get(base_url)
    assert response.status_code == 200


def test_get():
    base_url='http://localhost:5000/api/rls/templates'
    response = requests.get(base_url)
    assert response.status_code == 200

def test_post():
    base_url='http://localhost:5000/api/rls/templates'
    data = {"template_id": 1,"template_name": "matdev","template_version": 1,"template_json": {"app": "new"}}
    response = requests.put(base_url, json.dumps(data), headers=headers)
    assert response.status_code == 200

def test_get():
    base_url = 'http://localhost:5000/api/rls/templates/1'
    response = requests.get(base_url)
    print(json.dumps(response.json()))
    assert response.status_code == 200

def test_get():
    base_url = 'http://localhost:5000/api/rls/templates/list'
    response = requests.get(base_url)
    print(json.dumps(response.json()))
    assert response.status_code == 200

def test_get():
    base_url = 'http://localhost:5000/api/rls/frequency'
    response = requests.get(base_url)
    print(json.dumps(response.json()))
    assert response.status_code == 200


def test_post():
    base_url = 'http://localhost:5000/api/rls/frequency'
    data = {"frequency_cd": 46,"frequency_description": "daily-6","dag_usage": "@daily","comments": "Run once a day at midnight"}

    response = requests.post(base_url, json.dumps(data), headers=headers)
    #assert response.status_code == 200


@pytest.mark.get_environments
def test_get_WorkflowCollection(random_generators):
    resp = workflow_handler.get_workflow(6)
    wf = IMPL.get_workflow(6, 1)  # Values from database
    a = len(resp)
    for i in range(0,a):
        if resp[i]['name'] == wf[0]['name']:
            e = resp[i]

            assert e['name'] == wf[0]['name']
            assert e['template_id'] == wf[0]['template_id']
            assert e['description'] == wf[0]['description']
            assert e['status_cd'] == wf[0]['status_cd']
            assert e['release_id'] == wf[0]['release_id']
            assert e['release'] == wf[0]['release']


def test_create_WorkflowCollection(random_generators,create_workflow):
    args = {"wf_id": 2,"name": "sample_hack","template_id": 1,"description": "posting_application","create_dt": "2018-12-03T21:40:52.432Z",
        "status_cd": 1,"release_id": 1,"release": "dev","frequency_cd": 1,"env_id": 1,"overall_progress": 2,"environment_name": "new_env"}
    wf = workflow_handler.create_workflow(5, args=args)
    print(wf)

    assert args['name'] == wf[0]['name']
    assert args['template_id'] == wf[0]['template_id']
    assert args['description'] == wf[0]['description']
    assert args['status_cd'] == wf[0]['status_cd']
    assert args['release_id'] == wf[0]['release_id']
    assert args['release'] == wf[0]['release']


@pytest.mark.get_environments
def test_get_WorkflowItemDetailed(random_generators):
    resp = workflow_handler.get_workflow_with_stages(1,1,5)
    wf = IMPL.get_workflow(5, 1)  # Values from database
    a = len(resp)
    for i in range(0,a):
        if resp[i]['name'] == wf[0]['name']:
            e = resp[i]

            assert e['name'] == wf[0]['name']
            assert e['template_id'] == wf[0]['template_id']
            assert e['description'] == wf[0]['description']
            assert e['status_cd'] == wf[0]['status_cd']
            assert e['release_id'] == wf[0]['release_id']
            assert e['release'] == wf[0]['release']


@pytest.mark.get_environments
def test_get_WorkflowItemActions(random_generators):
    resp = workflow_handler.get_workflow_with_stages(1, 1, 5)
    wf = IMPL.get_workflow(5, 1)  # Values from database
    a = len(resp)
    for i in range(0, a):
        if resp[i]['name'] == wf[0]['name']:
            e = resp[i]

            assert e['name'] == wf[0]['name']
            assert e['template_id'] == wf[0]['template_id']
            assert e['description'] == wf[0]['description']
            assert e['status_cd'] == wf[0]['status_cd']
            assert e['release_id'] == wf[0]['release_id']
            assert e['release'] == wf[0]['release']


def test_create_WorkflowItemActions(random_generators,create_workflow):
    args = {"wf_id": 2,"name": "sample_hack","template_id": 1,"description": "posting_application","create_dt": "2018-12-03T21:40:52.432Z",
        "status_cd": 1,"release_id": 1,"release": "dev","frequency_cd": 1,"env_id": 1,"overall_progress": 2,"environment_name": "new_env"}
    wf = workflow_handler.create_workflow(5, args=args)
    print(wf)

    assert args['name'] == wf[0]['name']
    assert args['template_id'] == wf[0]['template_id']
    assert args['description'] == wf[0]['description']
    assert args['status_cd'] == wf[0]['status_cd']
    assert args['release_id'] == wf[0]['release_id']
    assert args['release'] == wf[0]['release']


@pytest.mark.get_environments
def test_get_TemplateCollection(random_generators):
    resp = workflow_handler.get_template(1, 1, 5)
    wf = IMPL.get_workflow(5, 1)  # Values from database
    a = len(resp)
    for i in range(0, a):
        if resp[i]['name'] == wf[0]['name']:
            e = resp[i]

            assert e['name'] == wf[0]['name']
            assert e['template_id'] == wf[0]['template_id']
            assert e['description'] == wf[0]['description']
            assert e['status_cd'] == wf[0]['status_cd']
            assert e['release_id'] == wf[0]['release_id']
            assert e['release'] == wf[0]['release']
            assert e['frequency_cd'] == wf[0]['frequency_cd']


def test_create_TemplateCollection(random_generators,create_workflow):
    args = {"wf_id": 3,"name": "sample","template_id": 1,"description": "posting_application","create_dt": "2018-12-03T21:40:52.432Z",
        "status_cd": 1,"release_id": 1,"release": "dev","frequency_cd": 1,"env_id": 1,"overall_progress": 2,"environment_name": "new_env"}
    wf = workflow_handler.create_template( args)
    print(wf)

    assert args['name'] == wf[0]['name']
    assert args['template_id'] == wf[0]['template_id']
    assert args['description'] == wf[0]['description']
    assert args['status_cd'] == wf[0]['status_cd']
    assert args['release_id'] == wf[0]['release_id']
    assert args['release'] == wf[0]['release']


@pytest.mark.get_environments
def test_get_TemplateItem(random_generators):
    resp = workflow_handler.get_template(1)
    wf = IMPL.get_workflow(5, 1)  # Values from database
    a = len(resp)
    for i in range(0, a):
        if resp[i]['name'] == wf[0]['name']:
            e = resp[i]

            assert e['name'] == wf[0]['name']
            assert e['template_id'] == wf[0]['template_id']
            assert e['description'] == wf[0]['description']
            assert e['status_cd'] == wf[0]['status_cd']
            assert e['release_id'] == wf[0]['release_id']
            assert e['release'] == wf[0]['release']
            assert e['frequency_cd'] == wf[0]['frequency_cd']


@pytest.mark.get_environments
def test_get_TemplateItem(random_generators):
    resp = workflow_handler.get_templates_drop_down_values(template_name='VNFUpgrade')
    wf = IMPL.get_workflow(5, 1)  # Values from database
    a = len(resp)
    for i in range(0, a):
        if resp[i]['name'] == wf[0]['name']:
            e = resp[i]

            assert e['name'] == wf[0]['name']
            assert e['template_id'] == wf[0]['template_id']
            assert e['description'] == wf[0]['description']
            assert e['status_cd'] == wf[0]['status_cd']
            assert e['release_id'] == wf[0]['release_id']
            assert e['release'] == wf[0]['release']
            assert e['frequency_cd'] == wf[0]['frequency_cd']


@pytest.mark.get_environments
def test_get_FrequencyCollection(random_generators):
    resp = workflow_handler.get_frequency()
    wf = IMPL.get_frequency(1)  # Values from database
    a = len(resp)
    for i in range(0, a):
        if resp[i]['frequency_cd'] == wf[0]['frequency_cd']:
            e = resp[i]

            assert e['frequency_cd'] == wf[0]['frequency_cd']
            assert e['frequency_description'] == wf[0]['frequency_description']
            assert e['dag_usage'] == wf[0]['dag_usage']
            assert e['comments'] == wf[0]['comments']
            assert e['cron_expression'] == wf[0]['cron_expression']


def test_FrequencyCollection(random_generators,create_workflow):
    args = {"wf_id": 3,"name": "sample","template_id": 1,"description": "posting_application","create_dt": "2018-12-03T21:40:52.432Z",
        "status_cd": 1,"release_id": 1,"release": "dev","frequency_cd": 1,"env_id": 1,"overall_progress": 2,"environment_name": "new_env"}
    wf  = workflow_handler.create_frequency(args)
    print(wf)

    assert args['frequency_cd'] == wf[0]['frequency_cd']
    assert args['frequency_description'] == wf[0]['frequency_description']
    assert args['dag_usage'] == wf[0]['dag_usage']
    assert args['comments'] == wf[0]['comments']
    assert args['cron_expression'] == wf[0]['cron_expression']