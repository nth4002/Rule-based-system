# 🎓 HƯỚNG DẪN SỬ DỤNG - Hệ thống Tư vấn Tuyển sinh UIT

## 📚 Mục lục

1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt](#cài-đặt)
3. [Chạy ứng dụng](#chạy-ứng-dụng)
4. [Hướng dẫn sử dụng các chức năng](#hướng-dẫn-sử-dụng)
5. [Test và Demo](#test-và-demo)
6. [FAQ](#faq)

---

## 🎯 Giới thiệu

Hệ thống Tư vấn Tuyển sinh UIT là một ứng dụng AI sử dụng **Forward Chaining** và **Rule-based Reasoning** để:

- ✅ Tìm ngành học phù hợp theo điểm thi
- ✅ Tư vấn thông minh dựa trên sở thích
- ✅ Tra cứu học bổng và FAQ
- ✅ Đưa ra báo cáo tư vấn toàn diện

---

## 💻 Cài đặt

### Bước 1: Cài đặt Python

Đảm bảo bạn đã cài Python 3.8+ trên máy:

```bash
python --version
```

### Bước 2: Clone repository

```bash
git clone <repository-url>
cd Rule-based-system
```

### Bước 3: Cài đặt thư viện

```bash
pip install gradio
```

---

## 🚀 Chạy ứng dụng

### Cách 1: Chạy app đơn giản

```bash
python app.py
```

### Cách 2: Chạy app cải tiến (Khuyến nghị) ⭐

```bash
python app_enhanced.py
```

### Cách 3: Chạy demo nhanh

```bash
python demo.py
```

Sau khi chạy, mở trình duyệt tại: **http://localhost:7860**

---

## 📖 Hướng dẫn sử dụng

### 🔍 Tab 1: Tra cứu theo Điểm THPT

**Mục đích:** Tìm các ngành bạn có thể xét tuyển dựa trên điểm thi THPT.

**Cách sử dụng:**

1. Nhập điểm thi của bạn (VD: 27.5)
2. Nhấn **"Tìm kiếm"**

**Kết quả:**

- Danh sách các ngành **đạt điểm chuẩn**
- Danh sách các ngành **gần đạt** (chênh lệch < 1 điểm)
- Chênh lệch điểm so với điểm chuẩn

**Ví dụ:**

```
Input: 27.5 điểm
Output:
✅ Bạn có thể xét tuyển vào 10 ngành với điểm số này

Các ngành phù hợp:
1. Khoa học Máy tính - Điểm chuẩn: 27.2 (Cao hơn 0.3 điểm)
2. Kỹ thuật Phần mềm - Điểm chuẩn: 26.0 (Cao hơn 1.5 điểm)
...
```

---

### 🎯 Tab 2: Tra cứu theo ĐGNL

**Mục đích:** Tìm ngành theo điểm Đánh giá Năng lực ĐHQG-HCM.

**Cách sử dụng:**

1. Nhập điểm ĐGNL (VD: 1050)
2. (Tùy chọn) Chọn loại chứng chỉ ngoại ngữ: IELTS / TOEFL / TOEIC
3. (Tùy chọn) Nhập điểm chứng chỉ (VD: 7.5)
4. Nhấn **"Tìm kiếm"**

**Cộng điểm ngoại ngữ:**

- **IELTS:**
  - ≥ 7.5: +45 điểm
  - ≥ 7.0: +40 điểm
  - ≥ 6.5: +30 điểm
  - ≥ 6.0: +20 điểm
- **TOEFL iBT:**
  - ≥ 100: +45 điểm
  - ≥ 90: +40 điểm
  - ≥ 80: +30 điểm

**Ví dụ:**

```
Input:
- Điểm ĐGNL: 1000
- Chứng chỉ: IELTS 7.5

Output:
🎯 Điểm cộng từ chứng chỉ: +45 điểm
💯 Điểm xét tuyển: 1045 điểm
✅ Chúc mừng! Bạn đủ điều kiện xét tuyển vào tất cả các ngành của UIT
```

---

### ❤️ Tab 3: Tư vấn theo Sở thích

**Mục đích:** Áp dụng **Forward Chaining** để đề xuất ngành học dựa trên sở thích.

**Cách sử dụng:**

1. Chọn 1 hoặc nhiều sở thích (checkbox):

   - 🤖 AI & Machine Learning
   - 📊 Phân tích dữ liệu
   - 💻 Lập trình
   - 🔒 Bảo mật & An ninh mạng
   - 🎮 Game & Đồ họa
   - 🌐 Mạng máy tính
   - 📱 Phát triển ứng dụng

2. (Tùy chọn) Nhập điểm thi để kiểm tra khả năng đỗ
3. Nhấn **"Nhận tư vấn"**

**Kết quả:**

- Các **luật được áp dụng** (Rules applied)
- **Trọng số** của mỗi luật
- Danh sách ngành **được đề xuất**
- **Độ tin cậy** tổng thể

**Ví dụ:**

```
Input:
- Sở thích: AI, Machine Learning, Dữ liệu
- Điểm thi: 28.0

Output:
📋 Các luật được áp dụng:
R004 (90%): NẾU quan tâm đến AI, ML, dữ liệu
            THÌ chọn Trí tuệ nhân tạo hoặc Khoa học Dữ liệu

✅ Các ngành được đề xuất:
1. Trí tuệ Nhân tạo
   - Điểm chuẩn: 29.6
   - Trạng thái: Gần đạt
   - Lý do: Phù hợp với sở thích AI, ML

2. Khoa học Dữ liệu
   - Điểm chuẩn: 27.7
   - Trạng thái: Đạt
   - Lý do: Phù hợp với phân tích dữ liệu

📊 Độ tin cậy: 90%
```

---

### ❓ Tab 4: Câu hỏi thường gặp

**Mục đích:** Tìm kiếm câu trả lời cho các câu hỏi về tuyển sinh.

**Cách sử dụng:**

1. Nhập từ khóa (VD: "học phí", "điểm cao", "học bổng")
2. Nhấn **"Tìm kiếm"**

**Hệ thống sử dụng:**

- **Fuzzy matching** - tìm kiếm mờ
- **Keyword matching** - khớp từ khóa
- **Similarity score** - tính độ tương đồng

**Ví dụ câu hỏi phổ biến:**

- "Ngành nào có điểm chuẩn cao nhất?"
- "Học phí UIT là bao nhiêu?"
- "Tôi thích lập trình nên học ngành gì?"
- "Học bổng UIT có những loại nào?"

---

### 🏆 Tab 5: Học bổng

**Mục đích:** Tìm các chương trình học bổng phù hợp.

**Cách sử dụng:**

**Cách 1: Tìm theo thành tích**

1. Nhập thành tích (VD: "Giải Nhất Olympic Tin học")
2. Nhấn **"Tìm kiếm"**

**Cách 2: Tìm theo điểm số**

1. Nhập điểm thi (VD: 29.0)
2. Nhấn **"Tìm kiếm"**

**Cách 3: Xem tất cả**

1. Tick vào **"Xem tất cả học bổng"**
2. Nhấn **"Tìm kiếm"**

**Các loại học bổng:**

- 🥇 Học bổng Olympic Tin học (250 triệu đồng)
- 🥈 Học bổng HSG Quốc gia (160 triệu đồng)
- 🎓 Học bổng Tân sinh viên Xuất sắc (60 triệu đồng)
- 💼 Học bổng Khuyến khích
- ... và nhiều hơn nữa

---

### 🎓 Tab 6: Tư vấn Toàn diện

**Mục đích:** Nhận báo cáo tư vấn chi tiết 360°.

**Cách sử dụng:**

1. Điền **đầy đủ** thông tin cá nhân:

   - Điểm thi THPT
   - Điểm ĐGNL (nếu có)
   - Tổ hợp môn
   - Chứng chỉ ngoại ngữ (nếu có)
   - Thành tích đặc biệt (nếu có)
   - Sở thích

2. Nhấn **"Tạo Báo cáo Tư vấn"**

**Báo cáo bao gồm:**

1. **💪 Phân tích điểm mạnh**

   - Điểm thi cao
   - Điểm ĐGNL xuất sắc
   - Chứng chỉ ngoại ngữ
   - Thành tích đặc biệt

2. **🎯 Phương thức xét tuyển tốt nhất**

   - ĐGNL / THPT / Tuyển thẳng
   - Điểm xét tuyển sau cộng

3. **📚 Top 3 ngành được đề xuất**

   - Tên ngành
   - Điểm chuẩn
   - Trạng thái (Đạt/Gần đạt)
   - Lý do phù hợp
   - Độ phù hợp (%)

4. **🏆 Học bổng dự kiến**

   - Tên học bổng
   - Giá trị
   - Xác suất nhận

5. **📝 Roadmap hành động**
   - Các bước cần làm cụ thể
   - Thứ tự ưu tiên

**Ví dụ output:**

```
🎓 BÁO CÁO TƯ VẤN TOÀN DIỆN

💪 Điểm mạnh của bạn:
✓ Điểm thi THPT cao (28.5)
✓ Điểm ĐGNL xuất sắc (1050)
✓ Có chứng chỉ IELTS 7.0

Phương thức xét tuyển tốt nhất: ĐGNL
Điểm xét tuyển sau cộng: 1090

🎯 Các ngành được đề xuất:

#1 Trí tuệ Nhân tạo
- Mã ngành: 7480107
- Điểm chuẩn: 29.6 (THPT) / 999 (ĐGNL)
- Trạng thái: Đạt (theo ĐGNL)
- Lý do: Phù hợp hoàn hảo với sở thích AI
- Độ phù hợp: 95%

#2 Khoa học Dữ liệu
- Độ phù hợp: 93%

🏆 Học bổng dự kiến:
- Học bổng Tân sinh viên Xuất sắc: 60.000.000 đồng
  Xác suất: Cao

📝 Các bước cần làm:
1. Đăng ký xét tuyển ngành Trí tuệ nhân tạo theo ĐGNL
2. Chuẩn bị hồ sơ minh chứng cho học bổng
3. Dự phòng đăng ký ngành Khoa học Dữ liệu
```

---

## 🧪 Test và Demo

### Chạy demo nhanh

```bash
python demo.py
```

Demo sẽ test 6 chức năng chính:

1. Tra cứu điểm THPT
2. Tra cứu ĐGNL
3. Tư vấn theo sở thích
4. FAQ
5. Học bổng
6. Tư vấn toàn diện

### Chạy test suite

```bash
python tests/test_runner.py
```

Hoặc:

```bash
python -c "from tests.test_runner import TestRunner; runner = TestRunner(); runner.run_all_tests(); runner.generate_report()"
```

Chi tiết: [tests/README.md](tests/README.md)

---

## ❓ FAQ

### 1. App không chạy được?

**Giải pháp:**

- Kiểm tra Python version: `python --version` (cần >= 3.8)
- Cài đặt lại Gradio: `pip install --upgrade gradio`
- Kiểm tra port 7860 có bị chiếm không

### 2. Không tìm thấy ngành phù hợp?

**Nguyên nhân:**

- Điểm thi quá thấp (< 24 điểm)
- Tổ hợp môn không được ngành nào chấp nhận

**Giải pháp:**

- Thử phương thức xét tuyển khác (ĐGNL, tuyển thẳng)
- Xem gợi ý từ hệ thống

### 3. Làm sao để cộng điểm ngoại ngữ?

Vào tab **"Tra cứu theo ĐGNL"**, điền:

- Điểm ĐGNL
- Loại chứng chỉ (IELTS/TOEFL)
- Điểm chứng chỉ

Hệ thống sẽ tự động cộng điểm theo quy định.

### 4. Tôi có nhiều sở thích, nên chọn ngành nào?

Sử dụng tab **"Tư vấn Toàn diện"**:

- Điền đầy đủ thông tin
- Chọn tất cả sở thích
- Hệ thống sẽ phân tích và đề xuất ngành phù hợp nhất

### 5. Độ tin cậy là gì?

**Độ tin cậy** = Mức độ chắc chắn của hệ thống về đề xuất

- **90-100%**: Rất phù hợp, khuyến nghị cao
- **80-90%**: Phù hợp tốt
- **70-80%**: Khá phù hợp
- **< 70%**: Cân nhắc thêm

---

## 📞 Liên hệ & Hỗ trợ

- **Website:** https://tuyensinh.uit.edu.vn
- **Hotline:** 028.3725.2002
- **Email:** tuyensinh@uit.edu.vn
- **Địa chỉ:** Khu phố 6, P. Linh Trung, TP. Thủ Đức, TP.HCM

---

## 📄 License

MIT License - Free for educational purposes

---

**Developed with ❤️ for UIT Students**

_Version: 2.0 Enhanced_
