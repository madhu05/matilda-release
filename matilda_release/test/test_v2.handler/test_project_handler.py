import logging
import random,pytest
from matilda_release.db.api import IMPL, create_project



@pytest.mark.random_generators
@pytest.fixture(scope='module')
def random_generators():
    c = random.randint(1, 999999999)
    global project_id, project_name
    project_id = 'test_NSTP{}'.format(c)
    project_name ='DEMO_test{}'.format(c)


def test_create_projects(random_generators):

    args = {'project_id': project_id, 'owner': 'Matilda', 'create_dt': '2018-10-01T00:00:00',
            'status': 'Active', 'name': project_name}

    dapi = IMPL.create_project(args)
    print(dapi)

    assert dapi['owner'] == args['owner']
    assert dapi['create_dt'] == args['create_dt']
    assert dapi['status'] == args['status']
    assert dapi['project_id'] == args['project_id']
    assert dapi['name'] == args['name']

