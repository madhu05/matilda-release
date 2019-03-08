from oslo_config import cfg
import messaging
from oslo_log import log

from matilda_release.engine import rpc

conf = cfg.CONF

LOG = log.getLogger(__name__)

class RpcAPI(object):

    def __init__(self):
        super(RpcAPI, self).__init__()
        try:
            LOG.info('Initializing Request Queue client')
            rpclient = rpc.RPCManager('matilda-release', conf)
            self._client = rpclient.get_client(topic='matilda-release')
        except Exception as e:
            LOG.error('Server request queue client initialization failed', e)
            raise e

    def invoke_notifier(self, ctxt, payload, component, action):
        try:
            LOG.info('Posting request to engine')
            context = self._client.prepare(version='1.0')
            context.cast(ctxt=ctxt,
                         method='invoke_notifier',
                         payload=payload,
                         component=component,
                         action=action)
        except messaging.MessageDeliveryFailure as e:
            LOG.error('Message delivery failed', e)
            raise e
