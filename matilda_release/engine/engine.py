from multiprocessing import Process

from oslo_log import log

from matilda_release.client import rpcengine
from matilda_release.engine import worker

LOG = log.getLogger(__name__)


class QueueHandler(object):

    def __init__(self, engine):
        super(QueueHandler, self).__init__()
        self._engine = engine
        self._rpcengine = rpcengine.RpcEngine()
        self.factory = worker.WorkerFactory()

    def invoke_notifier(self, ctxt, payload, component, action):
        LOG.info('Message from API %r' % payload)
        LOG.info('Component %r and action %r' % (component, action))
        worker = self.factory.getworker(worker_payload=payload, component=component,
                                        action=action)
        self.factory.execute(worker)


class Engine(object):

    def __init__(self):
        super(Engine, self).__init__()

    def _execute(self):
        pass

    def start(self):
        process = Process(target=self._execute)
        try:
            process.start()
            process.join()
        except KeyboardInterrupt:
            process.terminate()


class VirtEngine(object):

    def __init__(self):
        super(VirtEngine, self).__init__()

    def call_worker(self, args):
        worker_factory = worker.WorkerFactory()
        virt_worker = worker_factory.getworker(args)
        worker_factory.execute(virt_worker)
