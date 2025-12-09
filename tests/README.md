# Test Suite - Hệ thống Tư vấn Tuyển sinh UIT

## 📋 Tổng quan

Test suite bao gồm 20 test cases toàn diện để kiểm tra các chức năng của hệ thống tư vấn tuyển sinh, bao gồm:

- ✅ Tra cứu theo điểm THPT (3 tests)
- ✅ Tra cứu theo điểm ĐGNL (2 tests)
- ✅ Forward Chaining - Tư vấn theo sở thích (4 tests)
- ✅ Tra cứu FAQ (3 tests)
- ✅ Tra cứu học bổng (3 tests)
- ✅ Tra cứu phương thức tuyển sinh (3 tests)
- ✅ Tìm kiếm tổng hợp (1 test)
- ✅ Tư vấn toàn diện (1 test)

## 🚀 Cách chạy tests

### 1. Chạy tất cả tests

```bash
python tests/test_runner.py
```

### 2. Chạy tests với Python module

```bash
python -m tests.test_runner
```

### 3. Output mẫu

```
================================================================================
BẮT ĐẦU CHẠY 20 TEST CASES
================================================================================

✓ PASS | TC001 - Tìm ngành phù hợp với điểm số cao
✓ PASS | TC002 - Tìm ngành phù hợp với điểm số trung bình
✓ PASS | TC003 - Tìm ngành với điểm số thấp
...

================================================================================
KẾT QUẢ: 18/20 PASS | 2 FAIL
================================================================================

Báo cáo chi tiết đã được lưu tại: tests/test_report_20241209_143025.json
```

## 📊 Chi tiết Test Cases

### PHẦN 1: Tra cứu theo Điểm THPT

#### TC001: Điểm cao (29.5)

- **Input:** `diem_thi: 29.5`
- **Expected:** Tìm thấy ít nhất 10 ngành, bao gồm Trí tuệ Nhân tạo, Kỹ thuật Phần mềm

#### TC002: Điểm trung bình (26.0)

- **Input:** `diem_thi: 26.0`
- **Expected:** Tìm thấy ít nhất 5 ngành phù hợp

#### TC003: Điểm thấp (23.5)

- **Input:** `diem_thi: 23.5`
- **Expected:** Không tìm thấy ngành, có gợi ý phương thức khác

### PHẦN 2: Tra cứu theo ĐGNL

#### TC004: ĐGNL cao với chứng chỉ ngoại ngữ

- **Input:** `diem_dgnl: 1000, IELTS: 7.5`
- **Expected:** Cộng điểm ngoại ngữ, đủ điều kiện tất cả ngành

#### TC005: ĐGNL thấp

- **Input:** `diem_dgnl: 550`
- **Expected:** Không đạt ngưỡng, có gợi ý

### PHẦN 3: Forward Chaining

#### TC006: Sở thích AI/ML

- **Input:** `so_thich: [AI, ML, du_lieu], diem: 28.0`
- **Expected:** Áp dụng luật R004, đề xuất Trí tuệ Nhân tạo, Khoa học Dữ liệu

#### TC007: Sở thích Lập trình

- **Input:** `so_thich: [lap_trinh], diem: 27.5`
- **Expected:** Áp dụng luật R003, đề xuất Kỹ thuật Phần mềm, CNTT

#### TC008: Sở thích An ninh mạng

- **Input:** `so_thich: [bao_mat], diem: 26.5`
- **Expected:** Áp dụng luật R005, đề xuất An toàn Thông tin

#### TC009: Kết hợp nhiều luật

- **Input:** `so_thich: [AI, diem_cao], diem: 29.5`
- **Expected:** Áp dụng R001 + R004, độ tin cậy cao

### PHẦN 4-8: Các test cases khác

- FAQ: Tìm kiếm câu hỏi thường gặp
- Học bổng: Tìm theo thành tích, điểm số
- Phương thức tuyển sinh: Tra cứu thông tin
- Tìm kiếm tổng hợp: Kết hợp nhiều điều kiện
- Tư vấn toàn diện: Phân tích và đề xuất chi tiết

## 🛠️ Cấu trúc Test Suite

```
tests/
├── test_cases.json       # Định nghĩa 20 test cases
├── test_runner.py        # Script chạy tests
└── test_report_*.json    # Báo cáo kết quả (auto-generated)
```

## 📝 Cấu trúc Test Case

```json
{
  "id": "TC001",
  "name": "Tên test case",
  "category": "tra_cuu_theo_diem",
  "input": {
    "diem_thi": 29.5,
    "phuong_thuc": "diem_thi_thpt"
  },
  "expected": {
    "status": "success",
    "min_majors": 10,
    "should_include": ["7480107", "7480104"]
  }
}
```

## 🔧 Thêm Test Case mới

1. Mở `tests/test_cases.json`
2. Thêm test case mới vào mảng `tests`
3. Định nghĩa `input` và `expected` output
4. Chạy lại test suite

## 📈 Báo cáo Test

Báo cáo chi tiết được lưu dưới dạng JSON với thông tin:

- Timestamp
- Tổng số tests
- Số lượng pass/fail
- Chi tiết từng test case
- Error messages (nếu có)

## 🐛 Debug Test Failures

Nếu test fail, kiểm tra:

1. **Data mismatch**: Dữ liệu trong `knowledge_base.json` có đúng không?
2. **Logic error**: Logic trong `rule_based.py` có chính xác không?
3. **Expected values**: Giá trị expected trong test case có hợp lý không?

## 💡 Tips

- Chạy tests sau mỗi lần thay đổi code
- Giữ coverage ít nhất 80%
- Thêm test cases cho edge cases
- Update expected values khi business rules thay đổi

## 📞 Hỗ trợ

Nếu gặp vấn đề với test suite, vui lòng:

1. Kiểm tra log output
2. Xem file test*report*\*.json
3. Debug từng test case riêng lẻ
