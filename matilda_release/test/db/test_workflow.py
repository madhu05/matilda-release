from matilda_release.db import api

def test_get_workflow():
    resp = api.get_workflow(env_id=1)
    print (resp)

test_get_workflow()

sample_workflow = {

}