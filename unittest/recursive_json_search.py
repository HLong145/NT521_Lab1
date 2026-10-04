from test_data import *
import policy
def json_search(key, input_object, role=None):

    rules = getattr(policy, "POLICY", getattr(policy, "policy", {}))
    
    if key in rules:
        if role is None or role not in rules[key]:
            return []
    ret_val = []
    def _search(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    ret_val.append({k: v})
                if isinstance(v, (dict, list)):
                    _search(v)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    _search(item)
                    
    _search(input_object)
    return ret_val
if __name__ == '__main__':
    print(json_search("issueSummary", data, role="admin"))