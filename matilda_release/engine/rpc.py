import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as logging
from oslo_messaging.rpc import dispatcher
from oslo_serialization import jsonutils
from oslo_service import periodic_task

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class JsonPayloadSerializer(messaging.NoOpSerializer):
    @staticmethod
    def serialize_entity(context, entity):
        return jsonutils.to_primitive(entity, convert_instances=True)


class RequestContextSerializer(messaging.Serializer):
    def __init__(self, base):
        self._base = base

    def serialize_entity(self, context, entity):
        if not self._base:
            return entity
        return self._base.serialize_entity(context, entity)

    def deserialize_entity(self, context, entity):
        if not self._base:
            return entity
        return self._base.deserialize_entity(context, entity)

    def serialize_context(self, context):
        return context

    def deserialize_context(self, context):
        return context


class RPCManager(object):
    def __init__(self, topic, conf):
        self.topic = topic
        self.conf = conf
        global TRANSPORT
        TRANSPORT = self.create_transport(self.get_transport_url())
        serializer = RequestContextSerializer(JsonPayloadSerializer())

    def create_transport(self, url):
        return messaging.get_transport(CONF,
                                       url=url)

    def get_transport_url(self, url_str=None):
        return messaging.TransportURL.parse(CONF, url_str)

    def get_server(self, topic, endpoints, executor, server='0.0.0.0', serializer=None):
        assert TRANSPORT is not None
        target = messaging.Target(topic=topic, server=server)
        if serializer is None:
            serializer = RequestContextSerializer(serializer)
        access_policy = dispatcher.DefaultRPCAccessPolicy
        executor = executor if executor else 'eventlet'
        return messaging.get_rpc_server(TRANSPORT,
                                        target,
                                        endpoints,
                                        executor=executor,
                                        serializer=serializer,
                                        access_policy=access_policy)

    def get_client(self, topic, serializer=None):
        assert TRANSPORT is not None
        target = messaging.Target(topic=topic)
        serializer = RequestContextSerializer(serializer)

        return messaging.RPCClient(TRANSPORT,
                                   target,
                                   serializer=serializer)


class ClientRouter(periodic_task.PeriodicTasks):
    """Creates RPC clients that honor the context's RPC transport
    or provides a default.
    """

    def __init__(self, default_client):
        super(ClientRouter, self).__init__(CONF)
        self.default_client = default_client
        self.target = default_client.target
        self.version_cap = default_client.version_cap
        self.serializer = getattr(default_client, 'serializer', None)
        # self.run_periodic_tasks(context.RequestContext(overwrite=False))

    def _client(self, context, transport=None):
        if transport:
            return messaging.RPCClient(transport, self.target,
                                       serializer=self.serializer)
        else:
            return self.default_client

    def by_instance(self, context, instance):
        if context.mq_connection:
            return self._client(context, transport=context.mq_connection)
        else:
            return self.default_client

    def by_host(self, context, host):
        if context.mq_connection:
            return self._client(context, transport=context.mq_connection)
        else:
            return self.default_client
