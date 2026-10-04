import unittest
from test_data import *
from recursive_json_search import json_search

class json_search_test(unittest.TestCase):
    """Lớp kiểm thử đơn vị và bảo mật cho hàm json_search"""
    # 3 Unit Test chức năng ban đầu
    def test_search_found(self):
        """Kiểm tra tìm kiếm key tồn tại thông thường"""
        self.assertTrue([] != json_search('issueSummary', data, role='admin'))

    def test_search_not_found(self):
        """Kiểm tra tìm kiếm key không tồn tại"""
        self.assertTrue([] == json_search('non_existing_key', data, role='admin'))

    def test_is_a_list(self):
        """Kiểm tra kết quả trả về luôn là dạng list"""
        self.assertIsInstance(json_search('issueSummary', data, role='admin'), list)

    # 3 Security Test theo ma trận kiểm thử bảo mật
    def test_wrong_role_cannot_read_secret(self):
        """TC-SEC-01: Không truyền role (role=None) hoặc role viewer không được đọc apiKey"""
        self.assertEqual(json_search('apiKey', data), [])
        self.assertEqual(json_search('apiKey', data, role='viewer'), [])

    def test_operator_cannot_read_apikey(self):
        """TC-SEC-02: Operator không được đọc apiKey, nhưng Admin thì được"""
        self.assertEqual(json_search('apiKey', data, role='operator'), [])
        self.assertTrue(len(json_search('apiKey', data, role='admin')) > 0)

    def test_management_ip_allows_operator_but_not_viewer(self):
        """TC-SEC-03: managementIpAddress cho phép operator truy cập nhưng chặn viewer"""
        self.assertEqual(json_search('managementIpAddress', data, role='viewer'), [])
        res = json_search('managementIpAddress', data, role='operator')
        self.assertTrue(len(res) > 0)
        self.assertIn({'managementIpAddress': '10.10.20.21'}, res)

if __name__ == '__main__':
    unittest.main()