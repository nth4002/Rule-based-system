import json
import os

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
    
    def forward_inference(self, to_hop_mon=None, diem=None):
        """
        Forward inference với 2 rules:
        Rule 1: Nếu chọn tổ hợp môn, lọc các ngành chấp nhận tổ hợp đó
        Rule 2: Nếu có điểm, lọc các ngành có điểm chuẩn <= điểm của học sinh
        """
        results = self.majors.copy()
        
        # Rule 1: Lọc theo tổ hợp môn
        if to_hop_mon:
            results = [m for m in results if to_hop_mon in m.get('to_hop_mon', [])]
        
        # Rule 2: Lọc theo điểm chuẩn
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

