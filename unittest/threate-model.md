# THREAT MODEL FOR JSON_SEARCH() - NHOM 06

## 1. System Overview
Hàm `json_search(key, input_object)` được sử dụng để duyệt đệ quy và trích xuất dữ liệu từ các thông điệp cảnh báo/giám sát mạng do Cisco DNA Center trả về (được mô phỏng trong `test_data.py`).

## 2. Threat Modeling Analysis (STRIDE)

### (a) Actors & Roles
- **admin**: Quản trị viên toàn quyền hệ thống, được phép truy xuất tất cả các trường dữ liệu bao gồm cả chuỗi bí mật và địa chỉ mạng quản trị.
- **operator**: Kỹ sư vận hành mạng, được phép tra cứu thông tin vận hành, cấu trúc mạng, địa chỉ IP quản trị (`managementIpAddress`) và sự cố mạng. Không có quyền đọc chuỗi bí mật xác thực.
- **viewer**: Người theo dõi/giám sát viên, chỉ có quyền đọc thông tin tóm tắt sự cố cảnh báo chung (`issueSummary`). Không được phép xem cấu trúc mạng và thông tin nhạy cảm.

### (b) Sensitive Assets
- **apiKey** (`SNMP-COMMUNITY-STRING-7f3a9c`): Chuỗi bí mật cộng đồng SNMP dùng để xác thực và cấu hình trực tiếp vào thiết bị switch Cisco Catalyst 9300. Mức độ nghiêm trọng: Rất cao (Critical).
- **managementIpAddress** (`10.10.20.21`): Địa chỉ IP cổng quản lý nội bộ của thiết bị mạng lõi. Mức độ nghiêm trọng: Cao (High).
- **issueSummary**: Thông điệp cảnh báo sự cố thiết bị thông thường. Mức độ nghiêm trọng: Thấp (Low).

### (c) Trust Boundary
- Ranh giới giữa người dùng gọi API bên ngoài (các vai trò khác nhau) và hàm nội bộ `json_search()`.
- Lỗ hổng hiện tại: Hàm `json_search(key, input_object)` tin cậy mù quáng mọi lời gọi hàm, không xác thực vai trò (`role`) của người gọi trước khi trả về kết quả.

### (d) STRIDE Mapping
- **Information Disclosure (Lộ lọt thông tin):** Vai trò `viewer` gọi tìm kiếm `apiKey` hoặc `managementIpAddress`, hệ thống vẫn trả về chuỗi bí mật SNMP và IP quản trị do thiếu cơ chế kiểm tra quyền.
- **Elevation of Privilege (Leo thang đặc quyền):** Người dùng có quyền hạn thấp (`viewer`) lợi dụng việc trích xuất được `apiKey` để chiếm quyền điều khiển cấu hình switch mạng lõi.
