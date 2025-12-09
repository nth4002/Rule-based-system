"""
Demo Script - Kiểm tra nhanh các chức năng của Inference Engine
"""

from inference.rule_based import RuleBasedInference

# Khởi tạo engine
print("=" * 80)
print("DEMO - HỆ THỐNG TƯ VẤN TUYỂN SINH UIT")
print("=" * 80)
print()

engine = RuleBasedInference()

# Test 1: Tra cứu theo điểm THPT
print("📊 TEST 1: Tra cứu theo điểm THPT (29.5 điểm)")
print("-" * 80)
result = engine.find_majors_by_score(29.5)
print(f"Thông báo: {result['thong_bao']}")
print(f"Số ngành phù hợp: {len(result['danh_sach_nganh'])}")
if result['danh_sach_nganh']:
    print(f"Ngành đầu tiên: {result['danh_sach_nganh'][0]['ten']} - {result['danh_sach_nganh'][0]['diem_chuan']} điểm")
print()

# Test 2: Tra cứu ĐGNL
print("🎯 TEST 2: Tra cứu ĐGNL (1050 điểm + IELTS 7.5)")
print("-" * 80)
result = engine.find_majors_by_dgnl(1050, {'loai': 'IELTS', 'diem': 7.5})
print(f"Thông báo: {result['thong_bao']}")
print(f"Số ngành phù hợp: {len(result['danh_sach_nganh'])}")
if result['danh_sach_nganh'] and 'chi_tiet_diem' in result['danh_sach_nganh'][0]:
    diem_cong = result['danh_sach_nganh'][0]['chi_tiet_diem'].get('diem_cong_ngoai_ngu', 0)
    print(f"Điểm cộng ngoại ngữ: {diem_cong}")
print()

# Test 3: Tư vấn theo sở thích (Forward Chaining)
print("❤️ TEST 3: Tư vấn theo sở thích AI/ML")
print("-" * 80)
result = engine.recommend_by_interests(['thich_AI', 'thich_ML'], 28.0)
print(f"Số luật áp dụng: {len(result['luat_ap_dung'])}")
if result['luat_ap_dung']:
    for rule in result['luat_ap_dung']:
        print(f"- {rule['rule_id']}: {rule['mo_ta']} (Trọng số: {rule['trong_so']})")
print(f"Độ tin cậy: {result.get('do_tin_cay', 0):.0%}")
print(f"Số ngành đề xuất: {len(result['danh_sach_nganh_phu_hop'])}")
if result['danh_sach_nganh_phu_hop']:
    for major in result['danh_sach_nganh_phu_hop'][:3]:
        print(f"  • {major['ten']} - {major.get('trang_thai', 'N/A')}")
print()

# Test 4: Tra cứu FAQ
print("❓ TEST 4: Tra cứu FAQ - 'điểm cao nhất'")
print("-" * 80)
result = engine.search_faq('điểm cao nhất')
if 'faq_id' in result:
    print(f"FAQ ID: {result['faq_id']}")
    print(f"Câu hỏi: {result['cau_hoi']}")
    print(f"Trả lời: {result['tra_loi']}")
else:
    print(f"Thông báo: {result['thong_bao']}")
print()

# Test 5: Học bổng
print("🏆 TEST 5: Tìm học bổng theo điểm cao (29.0)")
print("-" * 80)
result = engine.search_scholarships({'diem_thi': 29.0, 'loai_hoc_bong': 'diem_cao'})
print(f"Thông báo: {result['thong_bao']}")
if result.get('hoc_bong'):
    for hb in result['hoc_bong']:
        print(f"- {hb['ten']}: {hb['gia_tri']}")
print()

# Test 6: Tư vấn toàn diện
print("🎓 TEST 6: Tư vấn toàn diện")
print("-" * 80)
thong_tin = {
    'diem_thi': 28.5,
    'diem_dgnl': 1050,
    'chung_chi_ngoai_ngu': {'loai': 'IELTS', 'diem': 7.0},
    'so_thich': ['thich_AI', 'thich_du_lieu']
}
result = engine.comprehensive_consultation(thong_tin)

print("Điểm mạnh:")
for dm in result['phan_tich_tong_quan']['diem_manh']:
    print(f"  ✓ {dm}")

print(f"\nPhương thức tốt nhất: {result['phan_tich_tong_quan'].get('phuong_thuc_tot_nhat', 'N/A')}")

if result['nganh_de_xuat']:
    print("\nCác ngành đề xuất:")
    for nganh in result['nganh_de_xuat']:
        print(f"  #{nganh['hang']} {nganh['ten']} (Độ phù hợp: {nganh.get('do_phu_hop', 0):.0%})")

if result['hoc_bong_du_kien']:
    print("\nHọc bổng dự kiến:")
    for hb in result['hoc_bong_du_kien']:
        print(f"  🏆 {hb['ten']} - {hb['gia_tri']}")

print()
print("=" * 80)
print("✅ DEMO HOÀN TẤT!")
print("=" * 80)
