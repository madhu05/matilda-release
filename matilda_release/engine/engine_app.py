import os

from oslo_config import cfg
from oslo_log import log

from matilda_release.engine.engine import Engine, QueueHandler
from matilda_release.engine import rpc

CONF = cfg.CONF

LOG = log.getLogger(__name__)

def setup_app():
    conf_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../matilda-release/etc/matilda_release.conf'))
    log.register_options(CONF)
    CONF(default_config_files=[conf_file])
    log.setup(CONF, 'matilda-release')
    try:
        rpclient = rpc.RPCManager('matilda-release', CONF)
        engine = Engine()
        endpoints = [QueueHandler(engine)]
        server = rpclient.get_server(topic='matilda-release',
                                     endpoints=endpoints,
                                     executor='blocking')
        LOG.info('MQ Server Starting.......')
        server.start()
        server.wait()
    except Exception as e:
        LOG.error('Failed to start MQ', e)
        raise e

setup_app()
