import collections,requests,json,os,uuid
import random,pytest
from datetime import datetime
from six import iteritems
from werkzeug.exceptions import BadRequest

from handler.environment_handler import get_environments
from matilda_release.api.v2.handler import environment_handler
from matilda_release.api.v2.endpoints import environment
from matilda_release.db import api as db_api
from matilda_release.db.sqlalchemy import models
from matilda_release.api.v2.handler import workflow_handler
from matilda_release.db.sqlalchemy import api as IMPL
#from db.api import add_env_to_release
from matilda_release.api.v2.endpoints.environment import environment


def test_create_environment():
    args = {'release_id': 1, 'name': 'new_env', 'type': 'test'}

    env = models.Environment()
    env.release_id = 1
    env.name = args.get('name')
    env.type = args.get('type')
    environments = get_environments(release_id=1, extended=False)
    print('environments : {}'.format(environments))
    if environment is not None:
        for env_iter in environments:
            if str(env_iter.get('name')).lower() == str(env.name).lower():
                c = ('Environment Name {} already exists for the release'.format(env.name))
                assert c == 'Environment Name new_env already exists for the release'

            if args.get('start_dt') is not None:
                global a, e
                resp = environment_handler.get_environments(1, 'extended=True')
                a = len(resp)
                for i in range(0, a):
                        e = resp[i]['env_id']
                        args = {'start_dt': '2018-12-17T20:47:16', 'create_dt': '2018-12-17T14:48:20', 'status_cd': '1'}
                        sapi = IMPL.add_env_to_release(args)
                        assert sapi['start_dt'] == args['start_dt']
                        assert sapi['create_dt'] == ['create_dt']
                        assert sapi['status_cd'] == ['status_cd']

            if args.get('end_dt') is not None:
                args = {'end_dt': '2018-12-17T20:47:16','start_dt': '2018-12-17T20:47:16', 'create_dt': '2018-12-17T14:48:20'}
                sapi = IMPL.add_env_to_release(args)
                assert sapi['end_dt'] == args['end_dt']
                assert sapi['start_dt'] == ['start_dt']
                assert sapi['create_dt'] == ['create_dt']

