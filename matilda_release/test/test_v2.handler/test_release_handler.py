import json,pytest,random
from matilda_release.db.sqlalchemy.models import Release, AppReleaseInfo, InfraRelease, VnfRelease
from matilda_release.api.v2.handler import application_handler
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd
from matilda_release.db.sqlalchemy import api as IMPL
from datetime import datetime
from matilda_release.api.v2.handler.release_handler import get_release_name_list


from matilda_release.db import api as db_api


""" Testing Create_release for the application """
#""" Creating random release_name """
@pytest.fixture()
def random_generators():
    global release_name
    c = random.randint(1, 9999999999)
    release_name = 'test_release{}'.format(c)


def test_create_release_application(random_generators):

    #Getting application_id and project_id from the application handler
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

    #getting platform_id

    # platforms = db_api.get_platforms(platform_id=None, name=None)
    # rand = random.randint(1,len(platforms) )
    # for i in range(1,len(platforms)):
    #     if i == rand:
    #         pltfrm_id = platforms[i]['platform_id']
    #
    # pltfrm_id =pltfrm_id

    platforms = db_api.get_platforms(platform_id=1, name='Windows')
    pltfrm_id = platforms[0]['platform_id']
    print(pltfrm_id)

    # getting os_id
    # operating_systems = db_api.get_operating_systems(os_id=None, platform_id=None, name=None)
    # rand = random.randint(1, len(operating_systems))
    # for i in range(1, len(operating_systems)):
    #     if i == rand:
    #         operating_id = operating_systems[i]['os_id']
    #
    # operating_id = operating_id


    operating_systems = db_api.get_operating_systems(os_id=1, platform_id=1, name='Windows Server 2008')
    operating_id = operating_systems[0]['os_id']



    args = {'description': 'This is demo release', 'name': release_name, 'version': '1.0', 'release_type_cd': 1,
            'status_cd': 1,
            'release_dt': datetime.now(), 'create_dt': datetime.now(),'app_id':t,'project_id':s,'platform_id' : pltfrm_id,
             'os_id':operating_id}

    master_release = IMPL.create_release(args)

    assert master_release['description'] == args['description']
    assert master_release['name'] == args['name']
    assert master_release['version'] == args['version']
    assert master_release['release_type_cd'] == args['release_type_cd']
    assert master_release['create_dt'] == args['create_dt']

    #resp_args = args

    #resp_args['release_id'] = master_release.get('release_id')

    """  Taking release_type_....1 for application and 2 for infra """
    release_type_cd = master_release['release_type_cd']

    if release_type_cd == rls_type_cd.application.release_type_cd:
        app_vo = AppReleaseInfo()
        app_vo.application_id = args.get('app_id')
        app_vo.project_id = args.get('project_id')
        app_vo.release_id = master_release.get('release_id')

        resp = db_api.create_app_release(app_vo)

        assert resp['application_id'] == args['app_id']
        assert resp['project_id'] == args['project_id']
        assert resp['release_id'] == master_release.get('release_id')

    elif release_type_cd == rls_type_cd.application.release_type_cd:
        infra_vo = InfraRelease()
        infra_vo.platform_id = args.get('platform_id')
        infra_vo.release_id = master_release.get('release_id')
        infra_vo.os_id = args.get('os_id')

        resp = db_api.create_infra_release(infra_vo)

        assert resp['os_id'] == args['os_id']
        assert resp['platform_id'] == args['platform_id']
        assert resp['release_id'] == args['release_id']


    elif release_type_cd == rls_type_cd.vnf.release_type_cd:
        pass


def test_get_release_name_list():
    releases = db_api.get_release_details()
    res = get_release_name_list()
    # for i in len(res):
    #     assert res['release_names'][i] ==  releases[i]['name']

    """ Checking for first value in the list"""
    assert res['release_names'][0] ==  releases[0]['name']

def test_get_release_type():
    args ={'release_type_cd':1,'release_type_description':'Application'}
    resp= IMPL.get_release_type_cd()
    assert resp[0]['release_type_cd'] == args['release_type_cd']
    assert resp[0]['release_type_description'] == args['release_type_description']








