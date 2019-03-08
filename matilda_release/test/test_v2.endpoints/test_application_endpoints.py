import json
import pytest
import random
import requests

from matilda_release.api.v2.handler import application_handler
from matilda_release.db.sqlalchemy import api as IMPL


@pytest.mark.random_generators
@pytest.fixture(scope='module')
def random_generators():
    global app_name,t
    c = random.randint(1, 999999999)
    app_name = 'test_application{}'.format(c)

    resp = application_handler.get_applications()
    a = len(resp)
    rand = random.randint(1, a)
    for i in range(0, a):
        if i == rand-1:
            t = resp[i]['project_id']


def test_post(random_generators):

    type = 'application/json'

    global headers
    headers = {
        'Content-Type': type,
        'Accept': type
    }
    global dat
    dat = {
        "app_id": app_name,
        "owner": "nsdew_EKYV",
        "create_dt": "2018-10-01T00:00:00",
        "status": "Active",
        "name": "nesdw_VISDM",
        "project_id": t
    }




    url = 'http://localhost:5000/api/rls/applications'
    response = requests.post(url, data=json.dumps(dat), headers=headers)
    assert response.status_code == 201


def test_get_application():
    url = 'http://localhost:5000/api/rls/applications'
    response = requests.get(url)
    assert response.status_code == 200



@pytest.mark.get_application
def test_get_application():

    global a,t
    db_values = resp = IMPL.get_applications(application_id=None, project_id=None)
    resp = application_handler.get_applications()
    a = len(resp)
    for i in range(0,a):
        if resp[i]['app_id'] == db_values[0]['app_id']:
            t= resp[i]

    assert t['owner'] == db_values[0]['owner']
    assert t['status'] == db_values[0]['status']
    assert t['project_id'] == db_values[0]['project_id']
    assert t['create_dt'] == db_values[0]['create_dt']




