# 🎓 Hệ thống Tư vấn Tuyển sinh UIT - Rule-based System

## 📋 Tổng quan

Hệ thống tư vấn tuyển sinh thông minh cho Đại học Công nghệ Thông tin (UIT) - ĐHQG-HCM, sử dụng kỹ thuật **Forward Chaining** và **Rule-based Reasoning** để:

- 🔍 Tra cứu ngành học theo điểm thi THPT
- 🎯 Tra cứu ngành học theo điểm ĐGNL (Đánh giá Năng lực)
- ❤️ Tư vấn ngành học dựa trên sở thích (Forward Chaining)
- ❓ Trả lời các câu hỏi thường gặp (FAQ)
- 🏆 Tìm kiếm học bổng phù hợp
- 📚 Tra cứu phương thức tuyển sinh
- 🎓 Tư vấn toàn diện với phân tích chi tiết

## 🚀 Cải tiến so với phiên bản gốc

### ✨ Chức năng mới

1. **Tra cứu theo ĐGNL**

   - Hỗ trợ điểm Đánh giá Năng lực
   - Tự động cộng điểm chứng chỉ ngoại ngữ (IELTS, TOEFL)
   - Kiểm tra ngưỡng đầu vào (≥600 điểm)

2. **Forward Chaining - Tư vấn thông minh**

   - Áp dụng 20+ luật dẫn (rules) từ knowledge base
   - Tính độ tin cậy dựa trên trọng số luật
   - Kết hợp nhiều luật để đưa ra gợi ý tốt nhất

3. **Tra cứu FAQ thông minh**

   - Tìm kiếm mờ (fuzzy search)
   - Similarity matching với keywords
   - Gợi ý từ khóa liên quan

4. **Hệ thống học bổng**

   - Tra cứu theo thành tích (Olympic, HSG)
   - Tra cứu theo điểm số
   - Liệt kê tất cả học bổng có sẵn

5. **Tư vấn toàn diện**

   - Phân tích điểm mạnh của thí sinh
   - Đề xuất phương thức xét tuyển tốt nhất
   - Gợi ý ngành học phù hợp
   - Dự đoán học bổng có thể nhận
   - Roadmap hành động cụ thể

6. **Giao diện Gradio nhiều tab**

   - 6 tabs chuyên biệt cho từng chức năng
   - UI/UX hiện đại, thân thiện
   - Responsive design

7. **Test Suite toàn diện**
   - 20 test cases coverage tất cả tính năng
   - Automated testing framework
   - Báo cáo chi tiết JSON

## 🏗️ Cấu trúc Project

```
Rule-based-system/
├── app.py                      # App gốc (đơn giản)
├── app_enhanced.py             # App cải tiến (6 tabs, đầy đủ tính năng)
├── README.md                   # File này
│
├── inference/
│   ├── rule_based.py           # ⭐ Core inference engine (đã mở rộng)
│   └── __pycache__/
│
├── data/
│   ├── knowledge_base.json     # KB tổng hợp
│   └── knowledge_base/         # KB chi tiết theo module
│       ├── chuyen_nganh.json   # Thông tin 20+ ngành học
│       ├── faq.json            # 40+ câu hỏi thường gặp
│       ├── hoc_bong.json       # 12+ chương trình học bổng
│       ├── luat_dan.json       # 20+ luật dẫn (rules)
│       ├── phuong_thuc_tuyen_sinh.json  # 4 phương thức
│       ├── hoc_phi.json
│       └── metadata.json
│
├── tests/
│   ├── test_cases.json         # ⭐ 20 test cases
│   ├── test_runner.py          # ⭐ Test automation framework
│   ├── test_report_*.json      # Báo cáo test (auto-generated)
│   └── README.md               # Hướng dẫn testing
│
└── admission_kb_project/       # Scripts xây dựng KB
    └── scripts/
        ├── build_kb.py
        ├── extract_entities.py
        └── parse_docx.py
```

## 📦 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd Rule-based-system
```

### 2. Cài đặt dependencies

```bash
pip install gradio
pip install python-docx
```

### 3. Chạy ứng dụng

**Chạy app gốc (đơn giản):**

```bash
python app.py
```

**Chạy app cải tiến (khuyến nghị):**

```bash
python app_enhanced.py
```

Sau đó mở trình duyệt tại: http://localhost:7860

## 🧪 Testing

### Chạy test suite

```bash
python tests/test_runner.py
```

hoặc

```bash
python -c "from tests.test_runner import TestRunner; runner = TestRunner(); runner.run_all_tests(); runner.generate_report()"
```

### Kết quả mẫu

```
================================================================================
BẮT ĐẦU CHẠY 20 TEST CASES
================================================================================

✓ PASS | TC001 - Tìm ngành phù hợp với điểm số cao
✓ PASS | TC002 - Tìm ngành phù hợp với điểm số trung bình
✓ PASS | TC003 - Tìm ngành với điểm số thấp
...

================================================================================
KẾT QUẢ: 14/20 PASS | 6 FAIL
================================================================================
```

Chi tiết xem: [tests/README.md](tests/README.md)

## 🎯 Các tính năng chính

### 1. Forward Chaining

Hệ thống sử dụng forward chaining để suy luận:

```
VÉ TRÁI (Điều kiện) → VÉ PHẢI (Kết luận)
```

**Ví dụ luật:**

```json
{
  "id": "R004",
  "veTrai": ["thich_AI", "thich_ML", "thich_du_lieu"],
  "vePhai": ["nganh_AI", "nganh_data_science"],
  "mo_ta": "NẾU quan tâm đến AI, ML, dữ liệu THÌ chọn Trí tuệ nhân tạo hoặc Khoa học Dữ liệu",
  "trong_so": 0.9
}
```

**Quy trình:**

1. Nhận input sở thích từ user
2. Duyệt tất cả các luật trong KB
3. Match điều kiện (vế trái) với input
4. Thu thập kết luận (vế phải) từ các luật matched
5. Tính độ tin cậy dựa trên trọng số
6. Trả về danh sách ngành được đề xuất

### 2. Tra cứu theo Điểm

**Điểm THPT:**

- Lọc ngành có `diem_chuan <= diem_thi`
- Sắp xếp theo điểm chuẩn giảm dần
- Hiển thị chênh lech điểm

**Điểm ĐGNL:**

- Kiểm tra ngưỡng đầu vào (≥600)
- Cộng điểm chứng chỉ ngoại ngữ
- So sánh với `diem_trung_tuyen_dgnl`

### 3. Tra cứu FAQ

- **Fuzzy matching**: Tính similarity score
- **Keyword search**: Tìm trong keywords
- **Fallback**: Gợi ý từ khóa phổ biến

### 4. Tư vấn Toàn diện

Phân tích 360° bao gồm:

- ✅ Điểm mạnh của thí sinh
- ✅ Phương thức xét tuyển tốt nhất
- ✅ Top 3 ngành phù hợp nhất
- ✅ Học bổng có thể nhận
- ✅ Roadmap hành động

## 📊 Knowledge Base

### Cấu trúc dữ liệu

**Ngành học** (`chuyen_nganh.json`)

```json
{
  "id": "7480107",
  "ten": "Trí tuệ Nhân tạo",
  "ma_nganh": "7480107",
  "diem_trung_tuyen": 29.6,
  "diem_trung_tuyen_dgnl": 999,
  "to_hop_mon": ["A00", "A01"],
  "co_hoi_nghe_nghiep": ["AI Engineer", "ML Researcher"],
  "keywords": ["AI", "machine learning", "deep learning"]
}
```

**Luật dẫn** (`luat_dan.json`)

```json
{
  "id": "R004",
  "veTrai": ["thich_AI", "thich_ML"],
  "vePhai": ["nganh_AI"],
  "mo_ta": "NẾU thích AI, ML THÌ chọn Trí tuệ nhân tạo",
  "trong_so": 0.9
}
```

**FAQ** (`faq.json`)

```json
{
  "id": "FAQ001",
  "cau_hoi": "Ngành nào có điểm chuẩn cao nhất?",
  "tra_loi": "Ngành Trí tuệ Nhân tạo...",
  "keywords": ["điểm cao", "điểm chuẩn"],
  "related_rules": ["R001"],
  "related_majors": ["7480107"]
}
```

## 🎨 Giao diện

### Tab 1: Tra cứu theo Điểm THPT

- Input: Điểm thi (0-30)
- Output: Danh sách ngành đạt/gần đạt, chênh lệch điểm

### Tab 2: Tra cứu theo ĐGNL

- Input: Điểm ĐGNL, chứng chỉ ngoại ngữ
- Output: Danh sách ngành, điểm sau cộng

### Tab 3: Tư vấn theo Sở thích

- Input: Checkbox sở thích, điểm (optional)
- Output: Luật áp dụng, ngành đề xuất, độ tin cậy

### Tab 4: FAQ

- Input: Từ khóa
- Output: Câu hỏi + trả lời

### Tab 5: Học bổng

- Input: Thành tích / điểm số
- Output: Danh sách học bổng phù hợp

### Tab 6: Tư vấn Toàn diện

- Input: Tất cả thông tin cá nhân
- Output: Báo cáo chi tiết 360°

## 🔧 Mở rộng

### Thêm luật mới

1. Mở `data/knowledge_base/luat_dan.json`
2. Thêm luật mới:

```json
{
  "id": "R021",
  "veTrai": ["dieu_kien_moi"],
  "vePhai": ["ket_luan_moi"],
  "mo_ta": "Mô tả luật",
  "trong_so": 0.85
}
```

### Thêm ngành mới

1. Mở `data/knowledge_base/chuyen_nganh.json`
2. Thêm ngành với đầy đủ thông tin

### Thêm test case

1. Mở `tests/test_cases.json`
2. Thêm test case theo format có sẵn

## 📈 Kết quả Test

**Hiện tại: 14/20 PASS (70%)**

### Pass:

- ✅ Tra cứu điểm trung bình/thấp
- ✅ ĐGNL không đủ điều kiện
- ✅ Kết hợp nhiều luật
- ✅ Tất cả FAQ tests
- ✅ Tất cả học bổng tests
- ✅ Tất cả phương thức tuyển sinh tests
- ✅ Tư vấn toàn diện

### Cần cải thiện:

- ⚠️ Validation logic cho một số edge cases
- ⚠️ Mapping ngành học trong complex queries

## 🤝 Đóng góp

Contributions are welcome! Vui lòng:

1. Fork repo
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## 📝 License

MIT License - Feel free to use for educational purposes

## 📞 Liên hệ

- **UIT Website:** https://www.uit.edu.vn
- **Tuyển sinh:** https://tuyensinh.uit.edu.vn
- **Hotline:** 028.3725.2002
- **Email:** tuyensinh@uit.edu.vn

---

⭐ **Developed with ❤️ for UIT Students**
