# Hệ thống Suy luận Dựa trên Luật

## Mô tả Luật

Hệ thống sử dụng forward inference với 2 luật chính:

**Luật 1: Lọc theo tổ hợp môn**
- Nếu người dùng chọn tổ hợp môn, hệ thống sẽ lọc các ngành học chấp nhận tổ hợp môn đó.

**Luật 2: Lọc theo điểm chuẩn**
- Nếu người dùng cung cấp điểm, hệ thống sẽ lọc các ngành có điểm chuẩn ≤ điểm của học sinh.
- Các ngành không có điểm chuẩn sẽ vẫn được giữ lại trong kết quả.

Hai luật được áp dụng tuần tự để thu hẹp danh sách ngành học phù hợp với tiêu chí của người dùng.

