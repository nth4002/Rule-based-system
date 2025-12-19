import json
import os
from pickle import NONE
import re
from difflib import SequenceMatcher

class RuleBasedInference:
    """Hệ thống suy luận dựa trên luật đơn giản để giới thiệu ngành học"""
    
    def __init__(self, kb_path=None):
        """Khởi tạo với đường dẫn đến knowledge base"""
        if kb_path is None:
            # Tìm đường dẫn knowledge_base.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            kb_path = os.path.join(current_dir, '..', 'data', 'knowledge_base.json')
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.kb = json.load(f)
        
        self.majors = self.kb.get('chuyen_nganh', [])
        
        # Load additional knowledge bases
        kb_dir = os.path.join(os.path.dirname(kb_path), 'knowledge_base')
        self.faqs = self._load_json(os.path.join(kb_dir, 'faq.json'))
        self.scholarships = self._load_json(os.path.join(kb_dir, 'hoc_bong.json'))
        self.rules = self._load_json(os.path.join(kb_dir, 'luat_dan.json'))
        self.admission_methods = self._load_json(os.path.join(kb_dir, 'phuong_thuc_tuyen_sinh.json'))
    
    def _load_json(self, path):
        """Load JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def forward_inference(self, to_hop_mon=None, diem=None):
        """
        Forward inference với 2 rules:
        Rule 1: Nếu chọn tổ hợp môn, lọc các ngành chấp nhận tổ hợp đó
        Rule 2: Nếu có điểm, lọc các ngành có điểm chuẩn <= điểm của học sinh
        """
        results = self.majors.copy()
        
        # Level 1: Lọc theo tổ hợp môn
        if to_hop_mon:
            results = [m for m in results if to_hop_mon in m.get('to_hop_mon', [])]
        
        # Level 2: Lọc theo điểm chuẩn
        if diem is not None:
            filtered_results = []
            for m in results:
                diem_chuan = m.get('diem_trung_tuyen')
                # Chỉ lọc nếu có điểm chuẩn và điểm >= điểm chuẩn
                if diem_chuan is not None and diem >= diem_chuan:
                    filtered_results.append(m)
                # Nếu không có điểm chuẩn, vẫn giữ lại
                elif diem_chuan is None:
                    filtered_results.append(m)
            results = filtered_results
        
        return results
    
    def format_output(self, majors):
        """Định dạng kết quả để hiển thị"""
        if not majors:
            return "Không tìm thấy ngành học phù hợp với tiêu chí của bạn."
        
        output = f"Tìm thấy {len(majors)} ngành học phù hợp:\n\n"
        
        for i, major in enumerate(majors, 1):
            output += f"{i}. {major.get('ten', 'N/A')}\n"
            output += f"   Mã ngành: {major.get('ma_nganh', 'N/A')}\n"
            output += f"   Mô tả: {major.get('mo_ta', 'N/A')}\n"
            
            diem_chuan = major.get('diem_trung_tuyen')
            if diem_chuan:
                output += f"   Điểm chuẩn: {diem_chuan}\n"
            
            co_hoi = major.get('co_hoi_nghe_nghiep', [])
            if co_hoi:
                output += f"   Cơ hội nghề nghiệp: {', '.join(co_hoi)}\n"
            
            chi_tieu = major.get('chi_tieu')
            if chi_tieu:
                output += f"   Chỉ tiêu: {chi_tieu}\n"
            
            output += "\n"
        
        return output
    
    # ============= PHẦN 1: TRA CỨU THEO ĐIỂM SỐ =============
    
    def find_majors_by_score(self, diem_thi, phuong_thuc='diem_thi_thpt'):
        """Tìm ngành phù hợp theo điểm số"""
        result = {
            'danh_sach_nganh': [],
            'thong_bao': '',
            'goi_y': []
        }
        
        matching_majors = []
        near_majors = []
        
        for major in self.majors:
            diem_chuan = major.get('diem_trung_tuyen')
            if diem_chuan is None:
                continue  # Bỏ qua các ngành không có điểm chuẩn
            
            chenh_lech = diem_thi - diem_chuan
            
            major_info = {
                'ma_nganh': major.get('ma_nganh'),
                'ten': major.get('ten'),
                'diem_chuan': diem_chuan,
                'chenh_lech': round(chenh_lech, 2)
            }
            
            if chenh_lech >= 0:
                major_info['trang_thai'] = 'Đạt điểm chuẩn'
                matching_majors.append(major_info)
            elif chenh_lech >= -1:
                major_info['trang_thai'] = 'Gần đạt điểm chuẩn'
                near_majors.append(major_info)
        
        # Sắp xếp theo điểm chuẩn giảm dần
        matching_majors.sort(key=lambda x: x['diem_chuan'], reverse=True)
        near_majors.sort(key=lambda x: x['diem_chuan'], reverse=True)
        
        if matching_majors:
            result['danh_sach_nganh'] = matching_majors[:10] + near_majors[:3]
            result['thong_bao'] = f"Bạn có thể xét tuyển vào {len(matching_majors)} ngành với điểm số này"
        else:
            result['thong_bao'] = f"Rất tiếc, điểm số của bạn chưa đủ để xét tuyển vào bất kỳ ngành nào của UIT"
            if near_majors:
                nearest = near_majors[0]
                result['thong_bao'] += f" (Điểm chuẩn thấp nhất: {nearest['diem_chuan']} điểm - Ngành {nearest['ten']})"
            
            result['goi_y'] = [
                "Xem xét phương thức xét tuyển ĐGNL (Đánh giá năng lực)",
                "Tham gia kỳ thi SAT/ACT để xét tuyển theo chứng chỉ quốc tế",
                "Cải thiện điểm số và xét tuyển bổ sung"
            ]
        
        return result
    
    # ============= PHẦN 2: TRA CỨU THEO ĐGNL =============
    
    def find_majors_by_dgnl(self, diem_dgnl, chung_chi_ngoai_ngu=None):
        """Tìm ngành theo điểm ĐGNL"""
        result = {
            'danh_sach_nganh': [],
            'thong_bao': '',
            'goi_y': []
        }
        
        # Tính điểm cộng từ chứng chỉ ngoại ngữ
        diem_cong = 0
        if chung_chi_ngoai_ngu:
            loai = chung_chi_ngoai_ngu.get('loai', '').upper()
            diem_cn = chung_chi_ngoai_ngu.get('diem', 0)
            
            if loai == 'IELTS':
                if diem_cn >= 7.5:
                    diem_cong = 45
                elif diem_cn >= 7.0:
                    diem_cong = 40
                elif diem_cn >= 6.5:
                    diem_cong = 30
                elif diem_cn >= 6.0:
                    diem_cong = 20
            elif loai == 'TOEFL IBT':
                if diem_cn >= 100:
                    diem_cong = 45
                elif diem_cn >= 90:
                    diem_cong = 40
                elif diem_cn >= 80:
                    diem_cong = 30
        
        diem_xet_tuyen = diem_dgnl + diem_cong
        
        # Kiểm tra ngưỡng đầu vào
        if diem_dgnl < 600:
            result['thong_bao'] = "Điểm ĐGNL của bạn chưa đạt ngưỡng đầu vào (≥600 điểm)"
            result['goi_y'] = [
                "Đăng ký thi lại kỳ thi ĐGNL",
                "Xem xét phương thức xét tuyển điểm thi THPT",
                "Nâng cao điểm ĐGNL bằng chứng chỉ ngoại ngữ (cộng tối đa 120 điểm)"
            ]
            return result
        
        matching_majors = []
        for major in self.majors:
            diem_chuan_dgnl = major.get('diem_trung_tuyen_dgnl')
            if diem_chuan_dgnl is None:
                continue  # Bỏ qua các ngành không có điểm chuẩn ĐGNL
            
            if diem_xet_tuyen >= diem_chuan_dgnl:
                major_info = {
                    'ma_nganh': major.get('ma_nganh'),
                    'ten': major.get('ten'),
                    'diem_chuan_dgnl': diem_chuan_dgnl,
                    'diem_xet_tuyen': diem_xet_tuyen,
                    'trang_thai': 'Đạt điểm chuẩn'
                }
                
                if diem_cong > 0:
                    major_info['chi_tiet_diem'] = {
                        'diem_dgnl': diem_dgnl,
                        'diem_cong_ngoai_ngu': diem_cong
                    }
                
                matching_majors.append(major_info)
        
        matching_majors.sort(key=lambda x: x['diem_chuan_dgnl'], reverse=True)
        
        if matching_majors:
            result['danh_sach_nganh'] = matching_majors
            if len(matching_majors) == len(self.majors):
                result['thong_bao'] = "Chúc mừng! Bạn đủ điều kiện xét tuyển vào tất cả các ngành của UIT"
            else:
                result['thong_bao'] = f"Bạn đủ điều kiện xét tuyển vào {len(matching_majors)} ngành"
        else:
            result['thong_bao'] = "Điểm ĐGNL của bạn chưa đủ để xét tuyển"
        
        return result
    
    # ============= PHẦN 3: FORWARD CHAINING - ÁP DỤNG LUẬT DẪN =============
    
    def recommend_by_interests(self, so_thich_list, diem_thi=None):
        """Tư vấn ngành học dựa trên sở thích bằng forward chaining"""
        result = {
            'luat_ap_dung': [],
            'danh_sach_nganh_phu_hop': [],
            'do_tin_cay': 0
        }
        
        if not so_thich_list:
            return result
        
        # Tìm các luật phù hợp
        applied_rules = []
        recommended_major_ids = set()
        
        for rule in self.rules:
            ve_trai = rule.get('veTrai', [])
            # Kiểm tra xem có sở thích nào khớp với điều kiện của luật
            if any(st in ve_trai for st in so_thich_list):
                ve_phai = rule.get('vePhai', [])
                applied_rules.append({
                    'rule_id': rule.get('id'),
                    'mo_ta': rule.get('mo_ta'),
                    'trong_so': rule.get('trong_so', 0.5),
                    'nganh_goi_y': ve_phai
                })
                recommended_major_ids.update(ve_phai)
        
        result['luat_ap_dung'] = applied_rules
        
        # Map các ID ngành sang thông tin chi tiết
        major_map = self._build_major_mapping()
        
        recommended_majors = []
        for major_id in recommended_major_ids:
            major = major_map.get(major_id)
            if major:
                major_info = {
                    'ma_nganh': major.get('ma_nganh'),
                    'ten': major.get('ten'),
                    'diem_chuan': major.get('diem_trung_tuyen'),
                    'co_hoi_nghe_nghiep': major.get('co_hoi_nghe_nghiep', [])
                }
                
                # Kiểm tra điểm nếu có
                if diem_thi is not None:
                    diem_chuan = major.get('diem_trung_tuyen', 30)
                    if diem_thi >= diem_chuan:
                        major_info['trang_thai'] = 'Đạt'
                    elif diem_thi >= diem_chuan - 1:
                        major_info['trang_thai'] = 'Gần đạt'
                    else:
                        major_info['trang_thai'] = 'Chưa đạt'
                    
                    # Lý do phù hợp
                    major_info['ly_do'] = self._generate_reason(so_thich_list, major)
                
                recommended_majors.append(major_info)
        
        # Sắp xếp theo điểm chuẩn
        if diem_thi is not None:
            recommended_majors.sort(key=lambda x: abs(x.get('diem_chuan', 30) - diem_thi))
        
        result['danh_sach_nganh_phu_hop'] = recommended_majors
        
        # Tính độ tin cậy trung bình
        if applied_rules:
            result['do_tin_cay'] = sum(r['trong_so'] for r in applied_rules) / len(applied_rules)
        
        return result
    
    def _build_major_mapping(self):
        """Tạo mapping từ mã ngành sang thông tin ngành"""
        mapping = {}
        
        # Mapping từ ID luật sang mã ngành thực tế
        id_to_code = {
            'nganh_AI': '7480107',                # Trí tuệ Nhân tạo
            'nganh_data_science': '7460108',      # Khoa học Dữ liệu (đã sửa từ 7340408)
            'nganh_phan_mem': '7480103',          # Kỹ thuật Phần mềm (đã sửa từ 7480104)
            'nganh_MMT': '7480102',               # Mạng máy tính
            'nganh_mang': '7480102',              # Alias cho MMT
            'nganh_TMDT': '7340122',              # Thương mại Điện tử
            'nganh_HTTT': '7480104',              # Hệ thống Thông tin (đã sửa từ 7340405)
            'nganh_CNTT': '7480201',              # Công nghệ Thông tin
            'nganh_KHMT': '7480101',              # Khoa học Máy tính (đã sửa từ 7480103)
            'nganh_an_toan_TT': '7480202',        # An toàn Thông tin
            'nganh_ATTT': '7480202'               # Alias
        }
        
        for major in self.majors:
            ma_nganh = major.get('ma_nganh')
            mapping[ma_nganh] = major
            
            # Thêm mapping cho các ID trong luật
            for logic_id, code in id_to_code.items():
                if code == ma_nganh:
                    mapping[logic_id] = major
        
        return mapping
    
    def _generate_reason(self, so_thich_list, major):
        """Tạo lý do phù hợp dựa trên sở thích"""
        reasons = []
        
        if 'thich_AI' in so_thich_list or 'thich_ML' in so_thich_list:
            if 'AI' in major.get('ten', '') or 'Trí tuệ' in major.get('ten', ''):
                reasons.append('Phù hợp với sở thích AI, ML')
        
        if 'thich_du_lieu' in so_thich_list:
            if 'Dữ liệu' in major.get('ten', ''):
                reasons.append('Phù hợp với phân tích dữ liệu')
        
        if 'thich_lap_trinh' in so_thich_list:
            if any(k in major.get('keywords', []) for k in ['lập trình', 'phần mềm']):
                reasons.append('Phù hợp với lập trình')
        
        if 'thich_bao_mat' in so_thich_list or 'thich_an_ninh_mang' in so_thich_list:
            if 'An toàn' in major.get('ten', '') or 'Bảo mật' in major.get('ten', ''):
                reasons.append('Phù hợp với bảo mật, an ninh mạng')
        
        return ', '.join(reasons) if reasons else 'Phù hợp với ngành CNTT'
    
    # ============= PHẦN 4: TRA CỨU FAQ =============
    
    def search_faq(self, tu_khoa):
        """Tìm kiếm FAQ theo từ khóa"""
        if not tu_khoa:
            return {'thong_bao': 'Vui lòng nhập từ khóa tìm kiếm'}
        
        tu_khoa_lower = tu_khoa.lower()
        best_match = None
        best_score = 0
        
        for faq in self.faqs:
            # Tìm trong câu hỏi
            score = self._similarity(tu_khoa_lower, faq.get('cau_hoi', '').lower())
            
            # Tìm trong keywords
            for keyword in faq.get('keywords', []):
                kw_score = self._similarity(tu_khoa_lower, keyword.lower())
                score = max(score, kw_score)
            
            if score > best_score:
                best_score = score
                best_match = faq
        
        if best_match and best_score > 0.3:
            result = {
                'faq_id': best_match.get('id'),
                'cau_hoi': best_match.get('cau_hoi'),
                'tra_loi': best_match.get('tra_loi'),
                'luat_lien_quan': best_match.get('related_rules', []),
                'nganh_lien_quan': best_match.get('related_majors', [])
            }
            
            if 'chi_tiet' in best_match:
                result['chi_tiet'] = best_match['chi_tiet']
            
            return result
        else:
            return {
                'thong_bao': 'Không tìm thấy câu hỏi phù hợp trong cơ sở dữ liệu',
                'goi_y_tu_khoa': [
                    'học phí UIT',
                    'học bổng',
                    'phương thức tuyển sinh',
                    'điểm chuẩn'
                ]
            }
    
    def _similarity(self, str1, str2):
        """Tính độ tương đồng giữa 2 chuỗi"""
        if str1 in str2 or str2 in str1:
            return 0.9
        return SequenceMatcher(None, str1, str2).ratio()
    
    # ============= PHẦN 5: TRA CỨU HỌC BỔNG =============
    
    def search_scholarships(self, input_data):
        """Tìm kiếm học bổng"""
        # thanh_tich = input_data.get('thanh_tich', '')
        # diem_thi = input_data.get('diem_thi')
        # loai_hoc_bong = input_data.get('loai_hoc_bong')
        # loai_truy_van = input_data.get('loai_truy_van')
        
        
        ky_thi = input_data.get('ky_thi', None)
        mon_hoc = input_data.get('mon_hoc', None)
        giai = input_data.get('giai', None)
        
        # if loai_truy_van == 'tat_ca':
        #     return {
        #         'tong_so_hoc_bong': len(self.scholarships),
        #         'danh_sach_hoc_bong': [
        #             {
        #                 'id': hb.get('id'),
        #                 'ten': hb.get('ten'),
        #                 'gia_tri': hb.get('gia_tri')
        #             }
        #             for hb in self.scholarships
        #         ]
        #     }
        
        matching_scholarships = []
        
        for scholarship in self.scholarships:
            matched = False
            
            # # Tìm theo thành tích
            # if thanh_tich:
            #     keywords = scholarship.get('keywords', [])
            #     for keyword in keywords:
            #         if keyword.lower() in thanh_tich.lower():
            #             matched = True
            #             break
            
            # # Tìm theo điểm cao
            # if loai_hoc_bong == 'diem_cao' and diem_thi:
            #     if 'xuất sắc' in scholarship.get('ten', '').lower() or 'tân sinh viên' in scholarship.get('ten', '').lower():
            #         # Kiểm tra điều kiện
            #         for dk in scholarship.get('dieu_kien', []):
            #             if '28' in dk and diem_thi >= 28:
            #                 matched = True
            #             elif '1100' in dk:  # ĐGNL
            #                 matched = True
            
            matching_conditions = scholarship['dieu_kien']
            patterns = [ky_thi, mon_hoc, giai]
            for condition in matching_conditions:
                if all( p.lower() in condition.lower() for p in patterns):
                    matched=True
                    print(scholarship.get('ten'))
                    break
            
            if matched:
                hb_info = {
                    'id': scholarship.get('id'),
                    'ten': scholarship.get('ten'),
                    'gia_tri': scholarship.get('gia_tri'),
                    'dieu_kien': scholarship.get('dieu_kien', [])
                }
                
                if scholarship.get('ghi_chu'):
                    hb_info['ghi_chu'] = scholarship.get('ghi_chu')
                
                matching_scholarships.append(hb_info)
        
        if matching_scholarships:
            result = {
                'hoc_bong': matching_scholarships,
                'thong_bao': f"Bạn đủ điều kiện nhận {len(matching_scholarships)} học bổng"
            }
            
            if matching_scholarships[0].get('id') == 'HB001':
                result['thong_bao'] = "Chúc mừng! Bạn đủ điều kiện nhận học bổng giá trị cao nhất"
            
            return result
        else:
            return {
                'hoc_bong': [],
                'thong_bao': 'Không tìm thấy học bổng phù hợp với tiêu chí'
            }
    
    # ============= PHẦN 6: PHƯƠNG THỨC TUYỂN SINH =============
    
    def get_admission_methods(self, phuong_thuc=None, loai_truy_van=None):
        """Lấy thông tin phương thức tuyển sinh"""
        if loai_truy_van == 'tat_ca_phuong_thuc':
            return {
                'tong_so_phuong_thuc': len(self.admission_methods),
                'danh_sach': [
                    {
                        'id': pt.get('id'),
                        'ten': pt.get('ten')
                    }
                    for pt in self.admission_methods
                ]
            }
        
        if phuong_thuc:
            # Map tên phương thức sang ID
            method_map = {
                'tuyen_thang': 'PT01',
                'dgnl': 'PT02',
                'thpt': 'PT03',
                'quoc_te': 'PT04'
            }
            
            method_id = method_map.get(phuong_thuc)
            
            for method in self.admission_methods:
                if method.get('id') == method_id:
                    return {
                        'id': method.get('id'),
                        'ten': method.get('ten'),
                        'doi_tuong': method.get('doi_tuong', []),
                        'nguyen_tac_xet_tuyen': method.get('nguyen_tac_xet_tuyen', []),
                        'huong_dan_thu_tuc': method.get('huong_dan_thu_tuc', [])
                    }
        
        return {'thong_bao': 'Không tìm thấy phương thức tuyển sinh'}
    
    # ============= PHẦN 7: TÌM KIẾM TỔNG HỢP =============
    
    def complex_search(self, input_data):
        """Tìm kiếm tổng hợp với nhiều điều kiện"""
        diem_thi = input_data.get('diem_thi')
        so_thich = input_data.get('so_thich', [])
        to_hop_mon = input_data.get('to_hop_mon')
        
        # Bước 1: Lọc theo tổ hợp môn
        candidates = self.forward_inference(to_hop_mon=to_hop_mon, diem=None)
        
        # Bước 2: Lọc theo điểm
        if diem_thi:
            candidates = [m for m in candidates if m.get('diem_trung_tuyen', 30) <= diem_thi]
        
        # Bước 3: Áp dụng luật dẫn cho sở thích
        rules_applied = []
        if so_thich:
            recommendation = self.recommend_by_interests(so_thich, diem_thi)
            rules_applied = [r['rule_id'] for r in recommendation.get('luat_ap_dung', [])]
            
            # Ưu tiên các ngành được gợi ý từ luật
            recommended_ids = set()
            for major in recommendation.get('danh_sach_nganh_phu_hop', []):
                recommended_ids.add(major.get('ma_nganh'))
        
        # Xếp hạng các ngành
        ranked_majors = []
        for major in candidates:
            ma_nganh = major.get('ma_nganh')
            diem_chuan = major.get('diem_trung_tuyen', 30)
            
            major_info = {
                'ma_nganh': ma_nganh,
                'ten': major.get('ten'),
                'diem_chuan': diem_chuan,
                'ly_do_phu_hop': []
            }
            
            # Tính độ phù hợp
            do_phu_hop = 0
            
            if diem_thi:
                chenh_lech = diem_thi - diem_chuan
                major_info['trang_thai'] = 'Đạt' if chenh_lech >= 0 else 'Chưa đạt'
                major_info['ly_do_phu_hop'].append(
                    f"Điểm của bạn {'cao hơn' if chenh_lech >= 0 else 'thấp hơn'} điểm chuẩn {abs(chenh_lech):.1f} điểm"
                )
                
                # Điểm càng vượt chuẩn thì độ phù hợp càng cao (nhưng không quá xa)
                if chenh_lech >= 0:
                    do_phu_hop += min(0.5, chenh_lech / 10)
            
            if so_thich and ma_nganh in recommended_ids:
                major_info['ly_do_phu_hop'].append('Phù hợp với sở thích')
                do_phu_hop += 0.4
            
            if to_hop_mon:
                major_info['ly_do_phu_hop'].append(f'Chấp nhận tổ hợp môn {to_hop_mon}')
                do_phu_hop += 0.1
            
            major_info['do_phu_hop'] = round(do_phu_hop, 2)
            ranked_majors.append(major_info)
        
        # Sắp xếp theo độ phù hợp
        ranked_majors.sort(key=lambda x: x['do_phu_hop'], reverse=True)
        
        # Tìm học bổng tiềm năng
        hoc_bong_co_the_nhan = []
        if diem_thi and diem_thi >= 28:
            hoc_bong_co_the_nhan.append('HB007')
        
        return {
            'ket_qua_tim_kiem': {
                'nganh_phu_hop_nhat': ranked_majors[:5],
                'luat_ap_dung': rules_applied,
                'hoc_bong_co_the_nhan': hoc_bong_co_the_nhan
            }
        }
    
    # ============= PHẦN 8: TƯ VẤN TOÀN DIỆN =============
    
    def comprehensive_consultation(self, thong_tin):
        """
        Tư vấn toàn diện với Forward Chaining:
        Bước 1: Lọc theo tổ hợp môn (Rule 1)
        Bước 2: Lọc theo điểm THPT hoặc ĐGNL + chứng chỉ (Rule 2)
        Bước 3: Tìm học bổng phù hợp (Rule 3 - nếu có thành tích)
        """
        diem_thi = thong_tin.get('diem_thi')
        diem_dgnl = thong_tin.get('diem_dgnl')
        to_hop_mon = thong_tin.get('to_hop_mon')
        chung_chi = thong_tin.get('chung_chi_ngoai_ngu')
        thanh_tich = thong_tin.get('thanh_tich', '')
        so_thich = thong_tin.get('so_thich', [])
        
        result = {
            'phan_tich_tong_quan': {
                'diem_manh': []
            },
            'nganh_de_xuat': [],
            'hoc_bong_du_kien': [],
            'luat_ap_dung': [],
            'goi_y_hanh_dong': [],
            'trace': []  # Thêm traceability để theo dõi các bước suy luận
        }
        
        # Phân tích điểm mạnh
        if diem_thi and diem_thi >= 28:
            result['phan_tich_tong_quan']['diem_manh'].append(f'Điểm thi THPT cao ({diem_thi})')
        
        if diem_dgnl and diem_dgnl >= 1000:
            result['phan_tich_tong_quan']['diem_manh'].append(f'Điểm ĐGNL xuất sắc ({diem_dgnl})')
        
        if chung_chi:
            loai = chung_chi.get('loai')
            diem = chung_chi.get('diem')
            result['phan_tich_tong_quan']['diem_manh'].append(f'Có chứng chỉ {loai} {diem}')
        
        if thanh_tich:
            result['phan_tich_tong_quan']['diem_manh'].append(f'Có thành tích {thanh_tich}')
        
        # ============= FORWARD CHAINING - BƯỚC 1: LỌC THEO TỔ HỢP MÔN =============
        candidates = self.majors.copy()
        step1_trace = {
            'buoc': 1,
            'ten_buoc': 'Lọc theo tổ hợp môn',
            'rule': 'Rule 1: Nếu có tổ hợp môn, chỉ giữ các ngành chấp nhận tổ hợp đó',
            'input': {
                'so_nganh_ban_dau': len(candidates),
                'to_hop_mon': to_hop_mon if to_hop_mon else 'Không có'
            },
            'output': {}
        }
        
        if to_hop_mon:
            candidates = [m for m in candidates if to_hop_mon in m.get('to_hop_mon', [])]
            step1_trace['output'] = {
                'so_nganh_sau_loc': len(candidates),
                'nganh_duoc_giu_lai': [m.get('ten') for m in candidates[:5]]  # Hiển thị 5 ngành đầu
            }
            step1_trace['ket_qua'] = f'Đã lọc từ {len(self.majors)} ngành xuống {len(candidates)} ngành chấp nhận tổ hợp {to_hop_mon}'
        else:
            step1_trace['output'] = {
                'so_nganh_sau_loc': len(candidates),
                'nganh_duoc_giu_lai': 'Tất cả ngành (không lọc)'
            }
            step1_trace['ket_qua'] = 'Không có tổ hợp môn, giữ nguyên tất cả ngành'
        
        result['trace'].append(step1_trace)
        
        # ============= FORWARD CHAINING - BƯỚC 2: LỌC THEO ĐIỂM =============
        step2_trace = {
            'buoc': 2,
            'ten_buoc': 'Lọc theo điểm',
            'input': {
                'so_nganh_truoc_buoc': len(candidates),
                'diem_thi': diem_thi if diem_thi else None,
                'diem_dgnl': diem_dgnl if diem_dgnl else None,
                'chung_chi': chung_chi if chung_chi else None
            },
            'output': {}
        }
        
        final_candidates = []
        phuong_thuc_su_dung = None
        diem_xet_tuyen_cuoi = None
        
        # Trường hợp 1: Có điểm THPT (ưu tiên nếu có tổ hợp môn)
        if diem_thi and (to_hop_mon or not diem_dgnl):
            phuong_thuc_su_dung = 'diem_thi_thpt'
            diem_xet_tuyen_cuoi = diem_thi
            
            for major in candidates:
                diem_chuan = major.get('diem_trung_tuyen')
                if diem_chuan is None:
                    # Nếu không có điểm chuẩn, vẫn giữ lại
                    final_candidates.append(major)
                elif diem_thi >= diem_chuan:
                    final_candidates.append(major)
            
            step2_trace['rule'] = f'Rule 2a: Lọc theo điểm THPT ({diem_thi} điểm)'
            step2_trace['output'] = {
                'so_nganh_sau_loc': len(final_candidates),
                'diem_su_dung': diem_thi,
                'phuong_thuc': 'Điểm thi THPT'
            }
            step2_trace['ket_qua'] = f'Đã lọc từ {len(candidates)} ngành xuống {len(final_candidates)} ngành đạt điểm chuẩn THPT'
        
        # Trường hợp 2: Có điểm ĐGNL (nếu không có điểm THPT hoặc điểm ĐGNL tốt hơn)
        elif diem_dgnl:
            phuong_thuc_su_dung = 'dgnl'
            
            # Tính điểm cộng từ chứng chỉ
            diem_cong = 0
            if chung_chi:
                loai = chung_chi.get('loai', '').upper()
                diem_cn = chung_chi.get('diem', 0)
                
                if loai == 'IELTS':
                    if diem_cn >= 7.5:
                        diem_cong = 45
                    elif diem_cn >= 7.0:
                        diem_cong = 40
                    elif diem_cn >= 6.5:
                        diem_cong = 30
                    elif diem_cn >= 6.0:
                        diem_cong = 20
                elif loai == 'TOEFL IBT':
                    if diem_cn >= 100:
                        diem_cong = 45
                    elif diem_cn >= 90:
                        diem_cong = 40
                    elif diem_cn >= 80:
                        diem_cong = 30
            
            diem_xet_tuyen_cuoi = diem_dgnl + diem_cong
            
            # Kiểm tra ngưỡng đầu vào
            if diem_dgnl >= 600:
                for major in candidates:
                    diem_chuan_dgnl = major.get('diem_trung_tuyen_dgnl')
                    if diem_chuan_dgnl is None:
                        continue
                    
                    if diem_xet_tuyen_cuoi >= diem_chuan_dgnl:
                        final_candidates.append(major)
                
                step2_trace['rule'] = f'Rule 2b: Lọc theo điểm ĐGNL ({diem_dgnl} điểm) + chứng chỉ (cộng {diem_cong} điểm) = {diem_xet_tuyen_cuoi} điểm'
                step2_trace['output'] = {
                    'so_nganh_sau_loc': len(final_candidates),
                    'diem_dgnl': diem_dgnl,
                    'diem_cong': diem_cong,
                    'diem_xet_tuyen': diem_xet_tuyen_cuoi,
                    'phuong_thuc': 'ĐGNL + Chứng chỉ'
                }
                step2_trace['ket_qua'] = f'Đã lọc từ {len(candidates)} ngành xuống {len(final_candidates)} ngành đạt điểm chuẩn ĐGNL'
            else:
                step2_trace['rule'] = f'Rule 2b: Điểm ĐGNL ({diem_dgnl}) chưa đạt ngưỡng đầu vào (≥600 điểm)'
                step2_trace['output'] = {
                    'so_nganh_sau_loc': 0,
                    'diem_dgnl': diem_dgnl,
                    'phuong_thuc': 'ĐGNL (chưa đạt ngưỡng)'
                }
                step2_trace['ket_qua'] = 'Điểm ĐGNL chưa đạt ngưỡng đầu vào, không có ngành nào phù hợp'
        
        else:
            # Không có điểm nào
            final_candidates = candidates
            step2_trace['rule'] = 'Rule 2: Không có điểm để lọc'
            step2_trace['output'] = {
                'so_nganh_sau_loc': len(final_candidates),
                'phuong_thuc': 'Không có'
            }
            step2_trace['ket_qua'] = 'Không có điểm để lọc, giữ nguyên tất cả ngành'
        
        result['trace'].append(step2_trace)
        
        # Lưu phương thức tốt nhất
        if phuong_thuc_su_dung:
            result['phan_tich_tong_quan']['phuong_thuc_tot_nhat'] = phuong_thuc_su_dung
            if diem_xet_tuyen_cuoi:
                result['phan_tich_tong_quan']['diem_xet_tuyen_sau_cong'] = diem_xet_tuyen_cuoi
        
        # ============= FORWARD CHAINING - BƯỚC 3: TÌM HỌC BỔNG =============
        step3_trace = {
            'buoc': 3,
            'ten_buoc': 'Tìm học bổng phù hợp',
            'input': {
                'thanh_tich': thanh_tich if thanh_tich else 'Không có'
            },
            'output': {}
        }
        
        if thanh_tich:
            # Parse thành tích từ chuỗi hoặc dictionary
            if isinstance(thanh_tich, dict):
                ky_thi = thanh_tich.get('ky_thi', '')
                mon_hoc = thanh_tich.get('mon_hoc', '')
                giai = thanh_tich.get('giai', '')
            else:
                # Parse từ chuỗi "Giải {giai} {mon_hoc} {ky_thi}"
                parts = thanh_tich.split()
                giai = parts[1] if len(parts) > 1 else ''
                mon_hoc = parts[2] if len(parts) > 2 else ''
                ky_thi = ' '.join(parts[3:]) if len(parts) > 3 else ''
            
            # Tìm học bổng phù hợp
            input_data = {
                'ky_thi': ky_thi,
                'mon_hoc': mon_hoc,
                'giai': giai
            }
            hb_result = self.search_scholarships(input_data)
            
            if hb_result.get('hoc_bong'):
                for hb in hb_result['hoc_bong']:
                    result['hoc_bong_du_kien'].append({
                        'id': hb.get('id'),
                        'ten': hb.get('ten'),
                        'gia_tri': hb.get('gia_tri'),
                        'xac_suat_nhan': 'Cao' if hb.get('id') in ['HB001', 'HB002', 'HB003', 'HB004'] else 'Trung bình'
                    })
                
                step3_trace['rule'] = f'Rule 3: Tìm học bổng theo thành tích ({thanh_tich})'
                step3_trace['output'] = {
                    'so_hoc_bong_tim_duoc': len(result['hoc_bong_du_kien']),
                    'danh_sach_hoc_bong': [hb['ten'] for hb in result['hoc_bong_du_kien']]
                }
                step3_trace['ket_qua'] = f'Tìm thấy {len(result["hoc_bong_du_kien"])} học bổng phù hợp với thành tích'
            else:
                step3_trace['rule'] = f'Rule 3: Không tìm thấy học bổng phù hợp với thành tích ({thanh_tich})'
                step3_trace['output'] = {
                    'so_hoc_bong_tim_duoc': 0
                }
                step3_trace['ket_qua'] = 'Không tìm thấy học bổng phù hợp'
        else:
            step3_trace['rule'] = 'Rule 3: Không có thành tích để tìm học bổng'
            step3_trace['output'] = {
                'so_hoc_bong_tim_duoc': 0
            }
            step3_trace['ket_qua'] = 'Không có thành tích, bỏ qua bước tìm học bổng'
        
        result['trace'].append(step3_trace)
        
        # Thêm học bổng dựa trên điểm cao (nếu có)
        if diem_thi and diem_thi >= 28:
            result['hoc_bong_du_kien'].append({
                'id': 'HB007',
                'ten': 'Học bổng Tân sinh viên Xuất sắc',
                'gia_tri': '60.000.000 đồng',
                'xac_suat_nhan': 'Cao'
            })
        
        # ============= XỬ LÝ KẾT QUẢ NGÀNH HỌC =============
        # Sắp xếp và format kết quả từ final_candidates
        if final_candidates:
            # Sắp xếp theo điểm chuẩn (cao xuống thấp)
            final_candidates.sort(key=lambda x: x.get('diem_trung_tuyen', 0) or x.get('diem_trung_tuyen_dgnl', 0), reverse=True)
            
            for rank, major in enumerate(final_candidates, 1):
                ma_nganh = major.get('ma_nganh')
                ten = major.get('ten')
                
                # Xác định điểm chuẩn và trạng thái
                if phuong_thuc_su_dung == 'diem_thi_thpt':
                    diem_chuan = major.get('diem_trung_tuyen')
                    if diem_chuan is None:
                        trang_thai = 'Không có điểm chuẩn'
                        ly_do = 'Ngành này không có điểm chuẩn THPT'
                    elif diem_thi >= diem_chuan:
                        chenh_lech = diem_thi - diem_chuan
                        trang_thai = 'Đạt'
                        ly_do = f'Điểm của bạn cao hơn điểm chuẩn {chenh_lech:.1f} điểm'
                    else:
                        trang_thai = 'Chưa đạt'
                        ly_do = f'Điểm của bạn thấp hơn điểm chuẩn {diem_chuan - diem_thi:.1f} điểm'
                else:  # ĐGNL
                    diem_chuan = major.get('diem_trung_tuyen_dgnl')
                    if diem_chuan is None:
                        trang_thai = 'Không có điểm chuẩn'
                        ly_do = 'Ngành này không có điểm chuẩn ĐGNL'
                    elif diem_xet_tuyen_cuoi >= diem_chuan:
                        chenh_lech = diem_xet_tuyen_cuoi - diem_chuan
                        trang_thai = 'Đạt'
                        ly_do = f'Điểm xét tuyển của bạn cao hơn điểm chuẩn {chenh_lech:.1f} điểm'
                    else:
                        trang_thai = 'Chưa đạt'
                        ly_do = f'Điểm xét tuyển của bạn thấp hơn điểm chuẩn {diem_chuan - diem_xet_tuyen_cuoi:.1f} điểm'
                
                result['nganh_de_xuat'].append({
                    'hang': rank,
                    'ma_nganh': ma_nganh,
                    'ten': ten,
                    'diem_chuan': diem_chuan,
                    'trang_thai': trang_thai,
                    'ly_do': ly_do,
                    'do_phu_hop': 0.8 if trang_thai == 'Đạt' else 0.5
                })
        
        # Gợi ý hành động
        if result['nganh_de_xuat']:
            nganh_top = result['nganh_de_xuat'][0]
            phuong_thuc = result['phan_tich_tong_quan'].get('phuong_thuc_tot_nhat', 'diem_thi_thpt')
            
            result['goi_y_hanh_dong'].append(
                f"1. Đăng ký xét tuyển ngành {nganh_top['ten']} theo phương thức {phuong_thuc.upper()}"
            )
            
            if len(result['nganh_de_xuat']) > 1:
                result['goi_y_hanh_dong'].append(
                    f"2. Dự phòng đăng ký ngành {result['nganh_de_xuat'][1]['ten']}"
                )
        
        if result['hoc_bong_du_kien']:
            result['goi_y_hanh_dong'].append(
                f"{len(result['goi_y_hanh_dong']) + 1}. Dự phòng đăng ký {len(result['hoc_bong_du_kien'])} học bổng (tổng giá trị dự kiến: {sum(int(hb['gia_tri'].replace('.000.000 đồng', '')) for hb in result['hoc_bong_du_kien'])}.000.000 đồng)"
            )
        
        # Nếu không có ngành nào đạt yêu cầu
        if not result['nganh_de_xuat']:
            if diem_thi:
                result['goi_y_hanh_dong'].append(
                    "⚠️ Điểm hiện tại chưa đủ để đạt các ngành phù hợp với sở thích. Hãy cố gắng nâng cao điểm số hoặc cân nhắc các ngành khác."
                )
            else:
                result['goi_y_hanh_dong'].append(
                    "ℹ️ Vui lòng cung cấp điểm thi để nhận tư vấn chi tiết hơn."
                )
        
        return result

