import unittest
from test_data import data, key1, key2
from recursive_json_search import json_search


class json_search_test(unittest.TestCase):
    """Lớp kiểm thử đơn vị và bảo mật cho hàm json_search."""

    # 3 Baseline Functional Tests
    def test_search_found(self):
        """Kiểm tra tìm kiếm key tồn tại với role hợp lệ trả về kết quả không rỗng."""
        self.assertTrue([] != json_search(key1, data, role="admin"))

    def test_search_not_found(self):
        """Kiểm tra tìm kiếm key không tồn tại trả về danh sách rỗng []."""
        self.assertTrue([] == json_search(key2, data, role="admin"))

    def test_is_a_list(self):
        """Kiểm tra kết quả trả về của hàm json_search luôn là một đối tượng list."""
        self.assertIsInstance(json_search(key1, data, role="admin"), list)

    # Security Tests validating role permissions defined in policy.py
    def test_wrong_role_cannot_read_secret(self):
        """TC-SEC-01: Không truyền role (role=None) hoặc role viewer không được đọc apiKey."""
        self.assertEqual(json_search("apiKey", data), [])
        self.assertEqual(json_search("apiKey", data, role=None), [])
        self.assertEqual(json_search("apiKey", data, role="viewer"), [])

    def test_operator_cannot_read_apikey(self):
        """TC-SEC-02: Role operator không được đọc apiKey, chỉ admin mới có quyền truy cập."""
        self.assertEqual(json_search("apiKey", data, role="operator"), [])
        admin_res = json_search("apiKey", data, role="admin")
        self.assertTrue(len(admin_res) > 0)
        self.assertIn({"apiKey": "SNMP-COMMUNITY-STRING-7f3a9c"}, admin_res)

    def test_viewer_cannot_read_management_ip(self):
        """TC-SEC-03: Role viewer không được đọc managementIpAddress, trong khi operator và admin thì được."""
        self.assertEqual(json_search("managementIpAddress", data, role="viewer"), [])
        self.assertEqual(json_search("managementIpAddress", data, role=None), [])
        
        operator_res = json_search("managementIpAddress", data, role="operator")
        self.assertTrue(len(operator_res) > 0)
        self.assertIn({"managementIpAddress": "10.10.20.21"}, operator_res)

        admin_res = json_search("managementIpAddress", data, role="admin")
        self.assertTrue(len(admin_res) > 0)
        self.assertIn({"managementIpAddress": "10.10.20.21"}, admin_res)

    def test_management_ip_allows_operator_but_not_viewer(self):
        """TC-SEC-04: Xác nhận quyền truy cập managementIpAddress cho phép operator và chặn viewer."""
        self.assertEqual(json_search("managementIpAddress", data, role="viewer"), [])
        res = json_search("managementIpAddress", data, role="operator")
        self.assertTrue(len(res) > 0)
        self.assertIn({"managementIpAddress": "10.10.20.21"}, res)

    def test_issuesummary_role_permissions(self):
        """TC-SEC-05: issueSummary cho phép admin, operator, viewer truy cập nhưng chặn khi role=None."""
        self.assertEqual(json_search("issueSummary", data, role=None), [])
        for role in ["admin", "operator", "viewer"]:
            res = json_search("issueSummary", data, role=role)
            self.assertTrue(len(res) > 0)


if __name__ == '__main__':
    unittest.main()
