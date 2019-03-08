import random,pytest
from matilda_release.db.api import create_application, IMPL
from matilda_release.api.v2.handler import application_handler



@pytest.mark.random_generators
@pytest.fixture(scope='module')
def random_generators():
    global app_name,t
    c = random.randint(1, 999999999)
    app_name = 'demo_test {}'.format(c)

    resp = application_handler.get_applications()
    a = len(resp)
    rand = random.randint(1, a)
    for i in range(0, a):
        if i == rand:
            t = resp[i]['project_id']




def test_create_applications(random_generators):

    args = {'app_id': app_name, 'owner': 'Matilda', 'create_dt': '2018-10-01T00:00:00',
            'status': 'Active', 'project_id': t}

    dapi = IMPL.create_application(args)
    print(dapi)

    assert dapi['app_id'] == args['app_id']
    assert dapi['owner'] == args['owner']
    assert dapi['create_dt'] == args['create_dt']
    assert dapi['status'] == args['status']
    assert dapi['project_id'] == args['project_id']













    # ap = models.Application(app_id='Not Service Contracts', owner='Matilda', create_dt='2018-10-01T00:00:00',
    #                         status='Active', project_id='NSTP')
    # assert ap['app_id'] == 'Not Service Contracts'
    # assert ap['owner'] == 'Matilda'
    # assert ap['create_dt'] == '2018-10-01T00:00:00'
    # assert ap['status'] == 'Active'
    # assert ap['project_id'] == 'NSTP'
    # assert isinstance(ap['app_id'],str)
    # assert isinstance(ap['owner'],str)
    # assert isinstance(ap['owner'],str)
    # assert isinstance(ap['create_dt'],str)
    # assert isinstance(ap['status'],str)
    # #assert_non_nullable(ap,'owner')
    # #assert_max_length(ap,'owner',45)
    # #resp = db_api.create_application(ap)
