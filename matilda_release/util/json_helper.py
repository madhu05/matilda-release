import json
import ast

# creating a utility to convert stings with mix of single quote and double quote and escape characters to proper dict and json.
# This is created to fix the encryption issue
def create_dict_from_json_string(value):
    print('dict value:{}'.format(value))
    if type(value) is str:
        value = ast.literal_eval(value)
    final_dict = dict()
    for k,v in value.items():
        #print(k,v)
        try:
            final_dict[k]=json.loads(v)
        except:
            final_dict[k]=v
    return final_dict

def create_json_from_string(value):
    return json.dumps(create_dict_from_json_string(value))



# print(create_json_from_string({'file_path': '{"test":"test2_enc"}'}))
# print(create_json_from_string({'file_path': '{\"test\":\"test2_enc\"}'}))
# print(create_json_from_string({'file_path': "{\"test\":\"test2_enc\"}"}))
# print(create_json_from_string({"file_path": "{\"test\":\"test2_enc\"}"}))
# print(create_dict_from_json_string({}))