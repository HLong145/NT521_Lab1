# SECURITY REQUIREMENTS SPECIFICATION - NHOM 06

Dựa trên kết quả phân tích Threat Model cho hàm `json_search()`, hệ thống bắt buộc phải đáp ứng các yêu cầu bảo mật phần mềm sau:

## 1. Functional Security Requirements
- **SR-01 (Role-Based Access Control):** Hàm `json_search` bắt buộc tiếp nhận tham số vai trò: `json_search(key, input_object, role=None)`.
- **SR-02 (Principle of Least Privilege):** Hàm chỉ trả về kết quả nếu vai trò của người gọi (`role`) được phép truy cập trường `key` đó theo chính sách định nghĩa trong `policy.py`:
  - `apiKey`: Chỉ cho phép `role == "admin"`.
  - `managementIpAddress`: Cho phép `role in ["admin", "operator"]`.
  - `issueSummary`: Cho phép `role in ["admin", "operator", "viewer"]`.
- **SR-03 (Fail-Safe Defaults):** Khi không truyền `role` (`role=None`) hoặc `role` không đủ quyền, hàm bắt buộc trả về danh sách rỗng `[]`, không để lộ thông tin hoặc quăng lỗi hệ thống.

## 2. Security Test Traceability Matrix
- Test Case 1: `test_wrong_role_cannot_read_secret` -> Vai trò `viewer` tìm kiếm `apiKey` phải trả về `[]`.
- Test Case 2: `test_operator_cannot_read_apikey` -> Vai trò `operator` tìm kiếm `apiKey` phải trả về `[]`.
- Test Case 3: `test_viewer_cannot_read_management_ip` -> Vai trò `viewer` tìm kiếm `managementIpAddress` phải trả về `[]`.
