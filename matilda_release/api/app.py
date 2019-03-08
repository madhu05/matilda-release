from oslo_config import cfg
import oslo_messaging as messaging
from oslo_log import log

#from aims_core.rpc import rpc
import rpc
from matilda_release.api.v2.app import app

import json
import sys


CONF = cfg.CONF

opts = [
        cfg.StrOpt('api_host', default='0.0.0.0'),
        cfg.StrOpt('api_port', default=8888),
]
CONF.register_opts(opts)

LOG = log.getLogger(__name__)


def setup_app():
    try:
        LOG.info('Setting up API server at %s:%s' % (CONF.api_host, CONF.api_port))
        LOG.info('Starting Listener Queue')
        rpclient = rpc.RPCManager('matilda-release-resp', CONF)
        server = rpclient.get_server(topic='matilda-release-resp',
                                     endpoints=[],
                                     executor='eventlet')
        server.start()
    except Exception as e:
        LOG.error("Error while starting Listener MQ", e)
        raise e


def build_server():
    log.register_options(CONF)
    CONF(sys.argv[1:], default_config_files=['/root/matilda/matilda-release/etc/matilda_release.conf'])
    log.setup(CONF, 'aims')
    host, port = CONF.api_host, CONF.api_port
    #debug = CONF.debug
    setup_app()
    LOG.info('App server running on %r:%r' % (host, port))
    app.run(host, int(port), debug=True)

build_server()
