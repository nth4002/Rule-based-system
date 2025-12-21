# Test Suite - Hệ thống Tư vấn Tuyển sinh UIT

## 📋 Tổng quan

Test suite bao gồm **20 test cases** toàn diện để kiểm tra hệ thống Forward Chaining tư vấn tuyển sinh, bao gồm:

- ✅ **Forward Chaining với điểm THPT** (4 tests)
- ✅ **Forward Chaining với điểm ĐGNL + Chứng chỉ** (3 tests)
- ✅ **Forward Chaining với học bổng** (7 tests)
- ✅ **Forward Chaining kết hợp đầy đủ** (6 tests)

Tất cả test cases đều sử dụng hàm `comprehensive_consultation()` để kiểm tra quy trình Forward Chaining 3 bước:
1. **Bước 1**: Lọc theo tổ hợp môn (Rule 1)
2. **Bước 2**: Lọc theo điểm THPT hoặc ĐGNL + chứng chỉ (Rule 2)
3. **Bước 3**: Tìm học bổng phù hợp (Rule 3)

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

✓ PASS | TC001 - Forward Chaining - Điểm THPT cao không có tổ hợp môn
✓ PASS | TC002 - Forward Chaining - Điểm THPT + Tổ hợp môn A00
✓ PASS | TC003 - Forward Chaining - Điểm THPT + Tổ hợp môn A01
...

================================================================================
KẾT QUẢ: 18/20 PASS | 2 FAIL
================================================================================

Báo cáo chi tiết đã được lưu tại: tests/test_report_20241221_143025.json
```

## 📊 Chi tiết Test Cases

### PHẦN 1: Forward Chaining với Điểm THPT

#### TC001: Điểm THPT cao không có tổ hợp môn
- **Input:** `diem_thi: 29.5`, không tổ hợp môn
- **Expected:** 
  - Phương thức: `diem_thi_thpt`
  - Mã ngành: `["7480101", "7480103", "7480201", "75202A1"]`

#### TC002: Điểm THPT + Tổ hợp môn A00
- **Input:** `diem_thi: 28.0`, `to_hop_mon: "A00"`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]` (các ngành chấp nhận A00)

#### TC003: Điểm THPT + Tổ hợp môn A01
- **Input:** `diem_thi: 27.5`, `to_hop_mon: "A01"`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]` (các ngành chấp nhận A01)

#### TC004: Điểm THPT thấp + Tổ hợp môn
- **Input:** `diem_thi: 23.0`, `to_hop_mon: "A00"`
- **Expected:** 
  - Số lượng ngành: `may_be_zero_or_low` (có thể không có ngành nào đạt)

### PHẦN 2: Forward Chaining với Điểm ĐGNL

#### TC005: ĐGNL cao + Chứng chỉ IELTS
- **Input:** `diem_dgnl: 1000`, `IELTS: 7.5`
- **Expected:** 
  - Điểm cộng: `45`
  - Điểm xét tuyển: `1045`
  - Phương thức: `dgnl`
  - Mã ngành: `["7480101", "7480103", "7480201"]`

#### TC006: ĐGNL + Chứng chỉ TOEFL
- **Input:** `diem_dgnl: 950`, `TOEFL iBT: 95`
- **Expected:** 
  - Điểm cộng: `40`
  - Điểm xét tuyển: `990`
  - Số lượng ngành tối thiểu: `3`

#### TC007: ĐGNL không đủ ngưỡng
- **Input:** `diem_dgnl: 550`
- **Expected:** 
  - Số lượng ngành: `0` (chưa đạt ngưỡng ≥600)

### PHẦN 3: Forward Chaining với Học bổng

#### TC008: HSG Quốc gia Tin học Nhất
- **Input:** `diem_thi: 28.0`, `thanh_tich: {ky_thi: "HSG Quốc gia THPT", mon_hoc: "Tin học", giai: "Nhất"}`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]`
  - Học bổng: `["HB001"]`

#### TC009: HSG Quốc gia Toán Nhất
- **Input:** `diem_thi: 27.5`, `thanh_tich: {ky_thi: "HSG Quốc gia THPT", mon_hoc: "Toán", giai: "Nhất"}`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]`
  - Học bổng: `["HB003"]`

#### TC010: Siêu Cup Olympic Tin học (Cúp Vàng)
- **Input:** `diem_thi: 29.0`, `thanh_tich: {ky_thi: "Siêu Cup - Olympic Tin học Việt Nam", mon_hoc: "Tin học", giai: "Vàng"}`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]`
  - Học bổng: `["HB001"]` (Vàng map với Nhất)

#### TC011: Olympic khu vực/quốc tế Ba
- **Input:** `diem_thi: 28.5`, `thanh_tich: {ky_thi: "Olympic khu vực và quốc tế môn Tin học", mon_hoc: "Tin học", giai: "Ba"}`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]`
  - Học bổng: `["HB001"]` (Ba match với "Nhất/Nhì/Ba")

#### TC012-TC014: Các học bổng khác
- **TC012**: HSG Quốc gia Lý Nhất → `["HB003"]`
- **TC013**: HSG Quốc gia Hoá Nhì → `["HB004"]`
- **TC014**: HSG Quốc gia Anh Văn Nhất → `["HB003"]`

### PHẦN 4: Forward Chaining Kết hợp

#### TC015: Điểm cao tự động có học bổng Tân sinh viên
- **Input:** `diem_thi: 28.5` (không có thành tích)
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201"]`
  - Học bổng: `["HB007"]` (tự động với điểm ≥28)

#### TC016: Tổ hợp môn X06 + Điểm cao
- **Input:** `diem_thi: 29.0`, `to_hop_mon: "X06"`
- **Expected:** 
  - Mã ngành: `["7480101", "7480103", "7480201", "7480106"]`

#### TC017: Tổ hợp môn D01 + Điểm trung bình
- **Input:** `diem_thi: 26.0`, `to_hop_mon: "D01"`
- **Expected:** 
  - Mã ngành: `["7480103", "7480104"]`

#### TC018: ĐGNL + IELTS + Tổ hợp môn
- **Input:** `diem_dgnl: 900`, `IELTS: 7.0`, `to_hop_mon: "A00"`
- **Expected:** 
  - Điểm cộng: `40`
  - Điểm xét tuyển: `940`
  - Mã ngành: `["7480106", "7480104"]`

#### TC019: Kịch bản đầy đủ
- **Input:** `diem_thi: 28.5`, `to_hop_mon: "A01"`, `thanh_tich: {...}`
- **Expected:** 
  - Số lượng ngành tối thiểu: `3`
  - Số lượng học bổng tối thiểu: `1`

#### TC020: Kịch bản toàn diện
- **Input:** `diem_dgnl: 1050`, `IELTS: 7.5`, `thanh_tich: {...}`
- **Expected:** 
  - Điểm cộng: `45`
  - Điểm xét tuyển: `1095`
  - Phương thức: `dgnl`
  - Số lượng ngành tối thiểu: `5`
  - Học bổng: `["HB003"]`

## 🛠️ Cấu trúc Test Suite

```
tests/
├── test_cases.json       # Định nghĩa 20 test cases
├── test_runner.py        # Script chạy tests và validation
├── README.md             # Tài liệu này
└── test_report_*.json    # Báo cáo kết quả (auto-generated)
```

## 📝 Cấu trúc Test Case

```json
{
  "id": "TC001",
  "name": "Forward Chaining - Điểm THPT cao không có tổ hợp môn",
  "category": "comprehensive",
  "input": {
    "diem_thi": 29.5,
    "diem_dgnl": null,
    "to_hop_mon": "",
    "chung_chi_ngoai_ngu": null,
    "thanh_tich": null,
    "so_thich": null
  },
  "expected": {
    "status": "success",
    "phuong_thuc": "diem_thi_thpt",
    "should_include_ma_nganh": ["7480101", "7480103", "7480201"],
    "should_include_hoc_bong_ids": ["HB001"],
    "diem_cong_expected": 40,
    "diem_xet_tuyen_expected": 940
  }
}
```

### Các trường Expected phổ biến:

- `status`: `"success"` hoặc `"fail"`
- `phuong_thuc`: `"diem_thi_thpt"` hoặc `"dgnl"`
- `should_include_ma_nganh`: Mảng các mã ngành phải có trong kết quả
- `should_include_hoc_bong_ids`: Mảng các mã học bổng phải có
- `min_majors`: Số lượng ngành tối thiểu
- `min_scholarships`: Số lượng học bổng tối thiểu
- `diem_cong_expected`: Điểm cộng mong đợi (từ chứng chỉ)
- `diem_xet_tuyen_expected`: Điểm xét tuyển sau cộng mong đợi
- `majors_count`: Số lượng ngành cụ thể hoặc `"may_be_zero_or_low"`
- `should_have_hoc_bong_du_kien`: `true` nếu phải có học bổng

## 🔧 Thêm Test Case mới

1. Mở `tests/test_cases.json`
2. Thêm test case mới vào mảng `tests`
3. Định nghĩa `input` và `expected` output theo cấu trúc trên
4. Cập nhật `test_metadata.total_tests`
5. Chạy lại test suite: `python tests/test_runner.py`

## 📈 Báo cáo Test

Báo cáo chi tiết được lưu dưới dạng JSON với thông tin:

- **Timestamp**: Thời gian chạy test
- **Tổng số tests**: Tổng số test cases đã chạy
- **Số lượng pass/fail**: Thống kê kết quả
- **Chi tiết từng test case**: 
  - Input và expected
  - Output thực tế
  - Trạng thái pass/fail
  - Error messages (nếu có)

## 🐛 Debug Test Failures

Nếu test fail, kiểm tra:

1. **Data mismatch**: 
   - Dữ liệu trong `knowledge_base/chuyen_nganh.json` có đúng không?
   - Điểm chuẩn các ngành có thay đổi không?

2. **Logic error**: 
   - Logic trong `rule_based.py` có chính xác không?
   - Forward Chaining 3 bước có hoạt động đúng không?

3. **Expected values**: 
   - Giá trị expected trong test case có hợp lý không?
   - Mã ngành/học bổng có tồn tại trong knowledge base không?

4. **Matching logic**:
   - Logic matching học bổng có đúng không?
   - Normalize môn học/kỳ thi có hoạt động không?


## 🔍 Forward Chaining Process

Hệ thống áp dụng Forward Chaining với 3 bước:

### Bước 1: Lọc theo Tổ hợp môn (Rule 1)
- Nếu có tổ hợp môn, chỉ giữ các ngành chấp nhận tổ hợp đó
- Nếu không có, giữ nguyên tất cả ngành

### Bước 2: Lọc theo Điểm (Rule 2)
- **THPT**: Lọc theo `diem_trung_tuyen` <= điểm thi
- **ĐGNL**: Tính điểm cộng từ chứng chỉ, lọc theo `diem_trung_tuyen_dgnl` <= điểm xét tuyển

### Bước 3: Tìm Học bổng (Rule 3)
- Parse thành tích từ input (kỳ thi, môn học, giải)
- Match với điều kiện học bổng trong knowledge base
- Xử lý đặc biệt cho Siêu Cup (Vàng/Bạc/Đồng)
- Tự động thêm HB007 nếu điểm ≥28
