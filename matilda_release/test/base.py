import os

from oslo_config import cfg



class MatildaReleaseTestBase():

    def __init__(self):
        conf_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../etc/matilda_release.conf'))
        print ('CONF FILE {}'.format(conf_file))
        CONF = cfg.CONF
        CONF(default_config_files=[conf_file])

