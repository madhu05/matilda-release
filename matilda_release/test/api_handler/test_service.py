from matilda_release.api.v2.endpoints import service

def test_output_fields():
    sop = service.ServiceOutputFields()
    resp = sop.get(10, 39)
    print ("Resp {}".format(resp))

test_output_fields()