from matilda_release.db import api
from matilda_release.util.status_helper import ReleaseTypeCdDefinition as rls_type_cd

def get_release():
    release_id = None
    resp = api.get_release_details(release_id=release_id, release_type_cd=rls_type_cd.application.release_type_cd)
    print ("length {}".format(len(resp)))
    #resp = [r._asdict() for r in resp]
    print (resp)

get_release()