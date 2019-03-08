import random
import threading

import six
from oslo_log import log

from matilda_release.client import rpcengine
from matilda_release.service.data_load.thrivent.hpalm_client import HPALMClient
from matilda_release.api.v2.handler import release_handler

LOG = log.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@six.add_metaclass(Singleton)
class WorkerFactory(object):
    _db_client = None
    _rpcengine = None
    _client_initialize = False
    _threadpool = {}
    _init_error = None

    def __init__(self):
        LOG.info('Worker factory initialized? %r ' % WorkerFactory._client_initialize)
        if WorkerFactory._client_initialize is False:
            WorkerFactory._client_init()
        WorkerFactory._client_initialize = True

    @staticmethod
    def _client_init():
        WorkerThread._init_error = None
        try:
            WorkerThread._rpcengine = rpcengine.RpcEngine()
        except Exception as e:
            WorkerThread._init_error = 'ERROR'
        finally:
            WorkerThread._threadpool = {}
            if WorkerThread._init_error is None:
                WorkerThread._client_initialize = True

    @classmethod
    def removeworker(cls, id):
        try:
            del WorkerThread._threadpool[id]
        except KeyError as e:
            LOG.error('Thread failed %s' % id, e)
            raise 'Thread failed %r ' % id

    def getworker(self, worker_payload, component, action):
        thread_id = random.randint(0, 99999999)
        worker = WorkerThread(thread_id=thread_id, request_payload=worker_payload,
                              component=component, action=action)
        WorkerThread._threadpool.update({thread_id: worker})
        return thread_id

    def execute(self, id):
        try:
            worker = WorkerThread._threadpool[id]
        except KeyError:
            raise Exception('Thread %r failed' % id)
        worker.start()


class WorkerThread(threading.Thread):
    _threadpool = {}

    def __init__(self, thread_id, request_payload, component,
                 action, client_error=None):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.client_error = client_error
        self.payload = request_payload
        self.action = action
        self.component = component

    def run(self):
        LOG.info('Thread starting - %s' % self.thread_id)
        LOG.info('payload to be executed %r' % self.payload)
        if self._is_engine_initialized():
            try:
                self._execute(self.component, self.action, self.payload)
            except Exception as e:
                LOG.error('Request failed to execute', e)
                # raise e
            finally:
                WorkerFactory.removeworker(self.thread_id)
        else:
            raise Exception('Engine is not initialized')

    def _is_engine_initialized(self):
        return True

    def _execute(self, component, action, payload):
        release_id = payload['release_id']
        release_name = payload.get('release_name') + '_matilda_poc'
        if component.lower() == 'infra':
            if action.lower() == 'create_test_suites':
                impacted_systems = release_handler.get_infra_release_impacted_application(release_id=release_id)
                hp = HPALMClient(release_name=release_name, impacted_apps=impacted_systems)
                hp.create_target_testset()

