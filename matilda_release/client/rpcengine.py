from oslo_config import cfg
import oslo_messaging as messaging
from oslo_log import log

from matilda_release.engine import rpc

conf = cfg.CONF

LOG = log.getLogger(__name__)

class RpcEngine(object):

    def __init__(self):
        super(RpcEngine, self).__init__()
        try:
            LOG.info('Initializing Request response client')
            rpclient = rpc.RPCManager('matilda-release-resp', conf)
            self._client = rpclient.get_client(topic='matilda-release-resp')
        except Exception as e:
            LOG.error('Server response queue client initialization failed', e)
            raise Exception(e.message)

    def invoke_listener(self, ctxt, payload):
        try:
            LOG.info('Posting request to engine')
            context = self._client.prepare(version='1.0')
            context.cast(ctxt=ctxt,
                         method='invoke_listener',
                         payload=payload)
        except messaging.MessageDeliveryFailure as e:
            LOG.error('Message delivery failed', e)
            raise e
