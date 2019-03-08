import pytest
from matilda_release.api.v2.handler import release_handler
from matilda_release.test.it import test_data

class TestRelease():

    def test_create_release(self):
        rls = test_data.get_mock_release()
        resp = release_handler.create_release(rls)
        print (resp)

tr = TestRelease()
tr.test_create_release()