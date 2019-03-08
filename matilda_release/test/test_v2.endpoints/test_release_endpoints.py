import logging
import pytest,random,datetime,requests,json
from flask import request
from flask_restplus import Resource
from matilda_release.api.v2.handler import application_handler
from matilda_release.api.v2.restplus import api
from matilda_release.api.v2.model.model import release, release_params, release_with_artifacts, release_type, \
    platforms_with_os, vnf_node_type_with_sites, rls_clone, \
    operating_system, infra_release_impacted_systems, release_names
from matilda_release.api.v2.handler import release_handler
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd
from matilda_release.db import api as db_api
from matilda_release.db.api import get_application_release_details
from matilda_release.db.sqlalchemy import api as IMPL




""" Testing Create_release for the application """
#""" Creating random release_name """
@pytest.fixture()
def random_generators():
    global release_name
    c = random.randint(1, 9999999999)
    release_name = 'demo_test_{}'.format(c)


def test_post_release(random_generators):

    global t, s , pltfrm_id, operating_id
    resp = application_handler.get_applications()
    a = len(resp)
    rand = random.randint(1, a)
    for i in range(0, a):
        if i == rand-1:
            t = resp[i]['app_id']
            s = resp[i]['project_id']
    t=t
    s=s

    operating_systems = db_api.get_operating_systems(os_id=1, platform_id=1, name='Windows Server 2008')
    operating_id = operating_systems[0]['os_id']

    platforms = db_api.get_platforms(platform_id=1, name='Windows')
    pltfrm_id = platforms[0]['platform_id']
    print(pltfrm_id)

    type = 'application/json'

    global headers
    headers = {
        'Content-Type': type,
        'Accept': type
    }
    global dat
    dat =  {
        "release_id": random.randint(1,9999),
        "name": release_name,
        "version": "1.0",
        "release_dt": "2018-11-30T20:02:02.709Z",
        "project_id": s,
        "project_name": "string",
        "application_id": t,
        "application_name": "string",
        "os_id": operating_id,
        "os_name": "string",
        "platform_id": pltfrm_id,
        "platform_name": "NTSP",
        "vnf_site": "string",
        "vnf_node": "string",
        "release_type_cd": 1,
        "release_type_description": "string",
        "status_cd": 1,
        "status_description": "this is demo_status",
        "duration": "string",
        "description": "This is demo description"

    }

    url = 'http://localhost:5000/api/rls/releases'
    response = requests.post(url, data=json.dumps(dat), headers=headers)
    assert response.status_code == 200



def test_get_release_types():

    url= 'http://localhost:5000/api/rls/release_types'
    response = requests.get(url)
    assert response.status_code == 200



def test_get_platforms():

    url= 'http://localhost:5000/api/rls/Platforms'
    response = requests.get(url)
    assert response.status_code == 200


def test_get_operatingsystems():

    url= 'http://localhost:5000/api/rls/OperatingSystems'
    response = requests.get(url)
    assert response.status_code == 200


def test_get_releases_names():

    url= 'http://localhost:5000/api/rls/releases/names'
    response = requests.get(url)
    assert response.status_code == 200



@pytest.mark.get_release
def test_get_release_application():
    resp = release_handler.get_release(release_id=None, release_type_cd=1)
    a=resp[0]['release_id']
    """ Checking get_release for the application Type"""
    db_values = get_application_release_details(release_id=a, release_name=None)
    assert resp[0]['name'] == db_values[0]['name']
    assert resp[0]['version'] == db_values[0]['version']
    assert resp[0]['create_dt'] == db_values[0]['create_dt']
    assert resp[0]['status_type_cd'] == db_values[0]['status_type_cd']



@pytest.mark.get_operatingsystems
def test_get_operatingsystems():    #testing for os_id = 1
    resp = release_handler.get_operating_system(1)
    db_values = IMPL.get_operating_system(os_id=1,name=None, platform_id=None)
    assert resp[0]['name'] == db_values[0]['name']
    assert resp[0]['platform_id'] ==  db_values[0]['platform_id']
    assert resp[0] ['version'] ==  db_values[0]['version']


@pytest.mark.get_release_names
def test_get_release_names():                     #checking for TestEncoder in release_names
    global release_list
    rm = release_handler.get_release_name_list()
    """ Checking for the Db values"""
    db_values = IMPL.get_application_release_Details(release_id=None, name=None)
    """ Checking the first value of db values is in release_handler or not"""
    a = len(rm['release_names'])
    for i in range(0, a):
        if rm['release_names'][i] == db_values[0][0]['name']:
            release_list = rm['release_names'][i]


    assert release_list == db_values[0][0]['name']


@pytest.mark.get_platforms
def test_get_platforms():   #testing for platform_id = 1
    resp = release_handler.get_platform(platform_id=1)
    """ Checking with platform_id with 1 """
    db_values =  IMPL.get_platform(platform_id=1,name=None)

    assert resp[0]['name'] == db_values[0]['name']
    assert resp[0]['platform_id'] == db_values[0]['platform_id']



