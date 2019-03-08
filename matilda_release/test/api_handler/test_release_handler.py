from matilda_release.api.v2.handler import release_handler
from matilda_release.api.v2.endpoints.release import ReleaseItem

def test_get_release():
    rls_id = 152
    resp = release_handler.get_release(release_id=rls_id)
    print ("length {}".format(len(resp)))
    print (resp)

def test_get_release_api():
    rls_id = 1
    rs = ReleaseItem()
    resp = rs.get(rls_id)
    print(resp)

test_get_release()