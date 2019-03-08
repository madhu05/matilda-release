from matilda_release.api.v2.handler import environment_handler

def test_get_env_details():
    resp = environment_handler.get_environment_details(env_id=1)
    print (resp)

test_get_env_details()