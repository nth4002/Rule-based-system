import gradio as gr
import json
from inference.rule_based import RuleBasedInference

# Khởi tạo inference engine
inference_engine = RuleBasedInference()

# ============= HELPER FUNCTIONS =============

def format_major_simple(major_info):
    """Định dạng thông tin ngành học đơn giản"""
    output = f"### {major_info.get('ten', 'N/A')}\n"
    output += f"**Mã ngành:** {major_info.get('ma_nganh', 'N/A')}\n"
    
    if 'diem_chuan' in major_info:
        output += f"**Điểm chuẩn:** {major_info['diem_chuan']}\n"
    
    if 'trang_thai' in major_info:
        output += f"**Trạng thái:** {major_info['trang_thai']}\n"
    
    if 'chenh_lech' in major_info:
        chenh_lech = major_info['chenh_lech']
        if chenh_lech > 0:
            output += f"**Điểm của bạn cao hơn:** {chenh_lech} điểm\n"
        elif chenh_lech < 0:
            output += f"**Điểm cần thêm:** {abs(chenh_lech)} điểm\n"
    
    if 'ly_do' in major_info:
        output += f"**Lý do phù hợp:** {major_info['ly_do']}\n"
    
    if 'do_phu_hop' in major_info:
        output += f"**Độ phù hợp:** {major_info['do_phu_hop']:.0%}\n"
    
    output += "\n"
    return output

# ============= TAB 1: TRA CỨU THEO ĐIỂM =============

def search_by_score(diem_thi):
    """Tìm ngành theo điểm thi THPT"""
    if not diem_thi:
        return "⚠️ Vui lòng nhập điểm thi!"
    
    result = inference_engine.find_majors_by_score(float(diem_thi))
    
    output = f"## 📊 {result['thong_bao']}\n\n"
    
    if result['danh_sach_nganh']:
        output += "### ✅ Các ngành phù hợp:\n\n"
        for major in result['danh_sach_nganh'][:10]:
            output += format_major_simple(major)
    
    if result.get('goi_y'):
        output += "\n### 💡 Gợi ý:\n"
        for goi_y in result['goi_y']:
            output += f"- {goi_y}\n"
    
    return output

def search_by_score_with_combo(diem_thi, to_hop_mon):
    """Tìm ngành theo điểm thi THPT và tổ hợp môn"""
    if not diem_thi:
        return "⚠️ Vui lòng nhập điểm thi!"
    
    # Lọc theo tổ hợp môn nếu có
    if to_hop_mon:
        majors = inference_engine.forward_inference(to_hop_mon=to_hop_mon, diem=float(diem_thi))
        
        if not majors:
            return f"❌ Không tìm thấy ngành học phù hợp với tổ hợp môn **{to_hop_mon}** và điểm số **{diem_thi}**"
        
        output = f"## 📊 Tìm thấy {len(majors)} ngành phù hợp\n\n"
        output += f"**Tổ hợp môn:** {to_hop_mon} | **Điểm thi:** {diem_thi}\n\n"
        output += "### ✅ Các ngành phù hợp:\n\n"
        
        for major in majors[:15]:
            diem_chuan = major.get('diem_trung_tuyen')
            if diem_chuan:
                chenh_lech = float(diem_thi) - diem_chuan
                major_info = {
                    'ma_nganh': major.get('ma_nganh'),
                    'ten': major.get('ten'),
                    'diem_chuan': diem_chuan,
                    'chenh_lech': chenh_lech,
                    'trang_thai': 'Đạt điểm chuẩn' if chenh_lech >= 0 else 'Chưa đạt'
                }
                output += format_major_simple(major_info)
        
        return output
    else:
        # Không có tổ hợp môn, tra cứu bình thường
        return search_by_score(diem_thi)

# ============= TAB 2: TRA CỨU THEO ĐGNL =============

def search_by_dgnl(diem_dgnl, loai_cc, diem_cc):
    """Tìm ngành theo điểm ĐGNL"""
    if not diem_dgnl:
        return "⚠️ Vui lòng nhập điểm ĐGNL!"
    
    chung_chi = None
    if loai_cc and diem_cc:
        chung_chi = {'loai': loai_cc, 'diem': float(diem_cc)}
    
    result = inference_engine.find_majors_by_dgnl(float(diem_dgnl), chung_chi)
    
    output = f"## 📊 {result['thong_bao']}\n\n"
    
    if result['danh_sach_nganh']:
        if chung_chi:
            diem_cong = result['danh_sach_nganh'][0].get('chi_tiet_diem', {}).get('diem_cong_ngoai_ngu', 0)
            if diem_cong > 0:
                output += f"**🎯 Điểm cộng từ chứng chỉ ngoại ngữ:** {diem_cong} điểm\n\n"
        
        output += "### ✅ Các ngành phù hợp:\n\n"
        for major in result['danh_sach_nganh'][:10]:
            output += format_major_simple(major)
    
    if result.get('goi_y'):
        output += "\n### 💡 Gợi ý:\n"
        for goi_y in result['goi_y']:
            output += f"- {goi_y}\n"
    
    return output

# ============= TAB 3: TƯ VẤN THEO SỞ THÍCH =============

def recommend_by_interests_no_score(interests_selected):
    """Tư vấn ngành theo sở thích (không cần điểm thi)"""
    if not interests_selected:
        return "⚠️ Vui lòng chọn ít nhất một sở thích!"
    
    result = inference_engine.recommend_by_interests(interests_selected, None)
    
    output = "## 🎯 Kết quả tư vấn ngành học\n\n"
    
    if result.get('luat_ap_dung'):
        output += "### 📋 Các luật được áp dụng:\n\n"
        for rule in result['luat_ap_dung']:
            output += f"**{rule['rule_id']}** ({rule['trong_so']:.0%}): {rule['mo_ta']}\n\n"
    
    if result.get('danh_sach_nganh_phu_hop'):
        output += "### ✅ Các ngành được đề xuất:\n\n"
        for major in result['danh_sach_nganh_phu_hop']:
            output += format_major_simple(major)
    
    if result.get('do_tin_cay'):
        output += f"\n**📊 Độ tin cậy:** {result['do_tin_cay']:.0%}\n"
    
    return output

# ============= TAB 4: TÌM KIẾM FAQ =============

def search_faq(keyword):
    """Tìm kiếm câu hỏi thường gặp"""
    if not keyword:
        return "⚠️ Vui lòng nhập từ khóa tìm kiếm!"
    
    result = inference_engine.search_faq(keyword)
    
    if 'faq_id' in result:
        output = f"## ❓ {result['cau_hoi']}\n\n"
        output += f"### 💬 Trả lời:\n\n{result['tra_loi']}\n\n"
        
        if result.get('chi_tiet'):
            output += "### 📋 Chi tiết:\n\n"
            for key, value in result['chi_tiet'].items():
                output += f"**{key}:** {value}\n\n"
        
        return output
    else:
        output = f"## {result['thong_bao']}\n\n"
        if result.get('goi_y_tu_khoa'):
            output += "### 💡 Các từ khóa gợi ý:\n"
            for kw in result['goi_y_tu_khoa']:
                output += f"- {kw}\n"
        return output

def search_faq_enhanced(faq_id, keyword):
    """Tìm kiếm FAQ với dropdown hoặc keyword"""
    # Ưu tiên dropdown nếu có
    if faq_id:
        # Tìm FAQ theo ID
        for faq in inference_engine.faqs:
            if faq.get('id') == faq_id:
                output = f"## ❓ {faq['cau_hoi']}\n\n"
                output += f"### 💬 Trả lời:\n\n{faq['tra_loi']}\n\n"
                
                if faq.get('chi_tiet'):
                    output += "### 📋 Chi tiết:\n\n"
                    for key, value in faq['chi_tiet'].items():
                        output += f"**{key}:** {value}\n\n"
                
                return output
        
        return "❌ Không tìm thấy câu hỏi này!"
    
    # Nếu không có dropdown, dùng keyword
    elif keyword:
        return search_faq(keyword)
    else:
        return "⚠️ Vui lòng chọn câu hỏi hoặc nhập từ khóa tìm kiếm!"

# ============= TAB 5: HỌC BỔNG =============

def search_scholarships(thanh_tich, diem_thi, show_all):
    """Tìm kiếm học bổng"""
    input_data = {}
    
    if show_all:
        input_data['loai_truy_van'] = 'tat_ca'
    elif thanh_tich:
        input_data['thanh_tich'] = thanh_tich
    elif diem_thi:
        input_data['diem_thi'] = float(diem_thi)
        input_data['loai_hoc_bong'] = 'diem_cao'
    else:
        return "⚠️ Vui lòng nhập thông tin hoặc chọn 'Xem tất cả học bổng'!"
    
    result = inference_engine.search_scholarships(input_data)
    
    if 'tong_so_hoc_bong' in result:
        output = f"## 🏆 Tổng số học bổng: {result['tong_so_hoc_bong']}\n\n"
        for hb in result['danh_sach_hoc_bong']:
            output += f"### {hb['ten']}\n"
            output += f"**Mã:** {hb['id']} | **Giá trị:** {hb['gia_tri']}\n\n"
    elif result.get('hoc_bong'):
        output = f"## {result['thong_bao']}\n\n"
        for hb in result['hoc_bong']:
            output += f"### 🏆 {hb['ten']}\n"
            output += f"**Giá trị:** {hb['gia_tri']}\n\n"
            if hb.get('dieu_kien'):
                output += "**Điều kiện:**\n"
                for dk in hb['dieu_kien']:
                    output += f"- {dk}\n"
                output += "\n"
            if hb.get('ghi_chu'):
                output += f"*{hb['ghi_chu']}*\n\n"
    else:
        output = f"## {result['thong_bao']}\n"
    
    return output

def search_scholarships_enhanced_no_score(hb_id, thanh_tich):
    """Tìm kiếm học bổng với dropdown (không cần điểm thi)"""
    # Ưu tiên dropdown nếu có
    if hb_id:
        if hb_id == "tat_ca":
            # Xem tất cả
            result = inference_engine.search_scholarships({'loai_truy_van': 'tat_ca'})
            output = f"## 🏆 Tổng số học bổng: {result['tong_so_hoc_bong']}\n\n"
            for hb in result['danh_sach_hoc_bong']:
                output += f"### {hb['ten']}\n"
                output += f"**Mã:** {hb['id']} | **Giá trị:** {hb['gia_tri']}\n\n"
            return output
        
        elif hb_id == "khuyenkhich":
            # Tìm các học bổng khuyến khích
            output = "## 🏆 Các học bổng Khuyến khích\n\n"
            for hb in inference_engine.scholarships:
                if 'khuyến khích' in hb.get('ten', '').lower() or 'khuyến khích' in str(hb.get('keywords', [])).lower():
                    output += f"### {hb['ten']}\n"
                    output += f"**Giá trị:** {hb['gia_tri']}\n\n"
                    if hb.get('dieu_kien'):
                        output += "**Điều kiện:**\n"
                        for dk in hb['dieu_kien']:
                            output += f"- {dk}\n"
                        output += "\n"
            return output
        
        else:
            # Tìm học bổng cụ thể theo ID
            for hb in inference_engine.scholarships:
                if hb.get('id') == hb_id:
                    output = f"## 🏆 {hb['ten']}\n\n"
                    output += f"**Mã:** {hb['id']}\n\n"
                    output += f"**Giá trị:** {hb['gia_tri']}\n\n"
                    
                    if hb.get('dieu_kien'):
                        output += "### Điều kiện:\n"
                        for dk in hb['dieu_kien']:
                            output += f"- {dk}\n"
                        output += "\n"
                    
                    if hb.get('so_luong'):
                        output += f"**Số lượng:** {hb['so_luong']}\n\n"
                    
                    if hb.get('ghi_chu'):
                        output += f"**Ghi chú:** {hb['ghi_chu']}\n\n"
                    
                    return output
            
            return "❌ Không tìm thấy học bổng này!"
    
    # Nếu không có dropdown, dùng thành tích
    elif thanh_tich:
        return search_scholarships(thanh_tich, None, False)
    else:
        return "⚠️ Vui lòng chọn loại học bổng hoặc nhập thành tích tìm kiếm!"

# ============= TAB 6: TƯ VẤN TOÀN DIỆN =============

def comprehensive_consultation(diem_thi, diem_dgnl, to_hop, loai_cc, diem_cc, thanh_tich, interests):
    """Tư vấn toàn diện"""
    if not any([diem_thi, diem_dgnl]):
        return "⚠️ Vui lòng nhập ít nhất điểm thi THPT hoặc điểm ĐGNL!"
    
    thong_tin = {}
    
    if diem_thi:
        thong_tin['diem_thi'] = float(diem_thi)
    if diem_dgnl:
        thong_tin['diem_dgnl'] = float(diem_dgnl)
    if to_hop:
        thong_tin['to_hop_mon'] = to_hop
    if loai_cc and diem_cc and diem_cc > 0:  # CHỈ thêm chứng chỉ khi điểm > 0
        thong_tin['chung_chi_ngoai_ngu'] = {'loai': loai_cc, 'diem': float(diem_cc)}
    if thanh_tich:
        thong_tin['thanh_tich'] = thanh_tich
    if interests:
        thong_tin['so_thich'] = interests
    
    result = inference_engine.comprehensive_consultation(thong_tin)
    
    output = "## 🎓 BÁO CÁO TƯ VẤN TOÀN DIỆN\n\n"
    
    # Phân tích tổng quan
    if result.get('phan_tich_tong_quan'):
        pt = result['phan_tich_tong_quan']
        output += "### 💪 Điểm mạnh của bạn:\n"
        for dm in pt.get('diem_manh', []):
            output += f"- {dm}\n"
        output += "\n"
        
        if pt.get('phuong_thuc_tot_nhat'):
            output += f"**Phương thức xét tuyển tốt nhất:** {pt['phuong_thuc_tot_nhat'].upper()}\n\n"
        
        if pt.get('diem_xet_tuyen_sau_cong'):
            output += f"**Điểm xét tuyển sau cộng:** {pt['diem_xet_tuyen_sau_cong']}\n\n"
    
    # Ngành đề xuất
    output += "### 🎯 Các ngành được đề xuất:\n\n"
    if result.get('nganh_de_xuat') and len(result['nganh_de_xuat']) > 0:
        for nganh in result['nganh_de_xuat']:
            output += f"**#{nganh['hang']} {nganh['ten']}**\n"
            output += f"- Mã ngành: {nganh['ma_nganh']}\n"
            output += f"- Điểm chuẩn: {nganh.get('diem_chuan', 'N/A')}\n"
            output += f"- Trạng thái: {nganh.get('trang_thai', 'N/A')}\n"
            if nganh.get('ly_do'):
                output += f"- Lý do: {nganh['ly_do']}\n"
            output += f"- Độ phù hợp: {nganh.get('do_phu_hop', 0):.0%}\n\n"
    else:
        output += "⚠️ **Điểm hiện tại chưa đủ để đạt các ngành phù hợp với sở thích. Hãy cố gắng nâng cao điểm số hoặc cân nhắc các ngành khác.**\n\n"
    
    # Học bổng
    if result.get('hoc_bong_du_kien'):
        output += "### 🏆 Học bổng dự kiến:\n\n"
        for hb in result['hoc_bong_du_kien']:
            output += f"**{hb['ten']}**\n"
            output += f"- Giá trị: {hb['gia_tri']}\n"
            output += f"- Xác suất nhận: {hb['xac_suat_nhan']}\n\n"
    
    # Gợi ý hành động
    if result.get('goi_y_hanh_dong'):
        output += "### 📝 Các bước cần làm:\n"
        for i, hanh_dong in enumerate(result['goi_y_hanh_dong'], 1):
            output += f"{i}. {hanh_dong}\n"
    
    return output

# ============= GRADIO INTERFACE =============

with gr.Blocks(title="Hệ thống Tư vấn Tuyển sinh UIT") as app:
    
    gr.Markdown("""
    <div class="header">
        <h1>🎓 HỆ THỐNG TƯ VẤN TUYỂN SINH</h1>
        <h2>Đại học Công nghệ Thông tin - ĐHQG-HCM</h2>
        <p>Hệ thống hỗ trợ Forward Chaining, Tra cứu thông minh</p>
    </div>
    """)
    
    with gr.Tabs():
        # TAB 1: Tra cứu theo điểm THPT
        with gr.Tab("📊 Tra cứu theo Điểm THPT"):
            gr.Markdown("### Tìm ngành phù hợp dựa trên điểm thi THPT")
            with gr.Row():
                with gr.Column(scale=1):
                    diem_thpt = gr.Number(label="Điểm thi THPT (0-30)", minimum=0, maximum=30, step=0.1)
                    to_hop_thpt = gr.Dropdown(
                        choices=[
                            ("Tất cả tổ hợp", ""),
                            ("A00 - Toán, Vật lý, Hóa học", "A00"),
                            ("A01 - Toán, Vật lý, Tiếng Anh", "A01"),
                            ("D01 - Toán, Văn, Tiếng Anh", "D01"),
                            ("D07 - Toán, Hóa học, Tiếng Anh", "D07"),
                            ("D08 - Toán, Sinh học, Tiếng Anh", "D08"),
                            ("X06 - Toán, Vật lý, Tin học", "X06"),
                            ("X26 - Toán, Tiếng Anh, Tin học", "X26"),
                        ],
                        label="Tổ hợp môn (tùy chọn)",
                        value=""
                    )
                    btn_thpt = gr.Button("🔍 Tìm kiếm", variant="primary")
                with gr.Column(scale=2):
                    output_thpt = gr.Markdown()
            
            btn_thpt.click(search_by_score_with_combo, inputs=[diem_thpt, to_hop_thpt], outputs=[output_thpt])
        
        # TAB 2: Tra cứu theo ĐGNL
        with gr.Tab("🎯 Tra cứu theo ĐGNL"):
            gr.Markdown("### Tìm ngành phù hợp dựa trên điểm Đánh giá Năng lực")
            with gr.Row():
                with gr.Column(scale=1):
                    diem_dgnl_input = gr.Number(label="Điểm ĐGNL (600-1200)", minimum=0, maximum=1200)
                    loai_cc_dgnl = gr.Dropdown(
                        choices=["IELTS", "TOEFL iBT", "TOEIC"],
                        label="Loại chứng chỉ ngoại ngữ (tùy chọn)"
                    )
                    diem_cc_dgnl = gr.Number(label="Điểm chứng chỉ", minimum=0, maximum=10, step=0.5)
                    btn_dgnl = gr.Button("🔍 Tìm kiếm", variant="primary")
                with gr.Column(scale=2):
                    output_dgnl = gr.Markdown()
            
            btn_dgnl.click(
                search_by_dgnl,
                inputs=[diem_dgnl_input, loai_cc_dgnl, diem_cc_dgnl],
                outputs=[output_dgnl]
            )
        
        # TAB 3: Tư vấn theo sở thích
        with gr.Tab("❤️ Tư vấn theo Sở thích"):
            gr.Markdown("### Hệ thống áp dụng Forward Chaining để đề xuất ngành")
            with gr.Row():
                with gr.Column(scale=1):
                    interests = gr.CheckboxGroup(
                        choices=[
                            ("🤖 AI & Machine Learning", "thich_AI"),
                            ("📊 Phân tích dữ liệu", "thich_du_lieu"),
                            ("💻 Lập trình", "thich_lap_trinh"),
                            ("🔒 Bảo mật & An ninh mạng", "thich_bao_mat"),
                            ("🎮 Game & Đồ họa", "thich_game"),
                            ("🌐 Mạng máy tính", "thich_mang"),
                            ("📱 Phát triển ứng dụng", "thich_phat_trien_ung_dung")
                        ],
                        label="Chọn sở thích của bạn"
                    )
                    btn_interests = gr.Button("🎯 Nhận tư vấn", variant="primary")
                with gr.Column(scale=2):
                    output_interests = gr.Markdown()
            
            btn_interests.click(
                recommend_by_interests_no_score,
                inputs=[interests],
                outputs=[output_interests]
            )
        
        # TAB 4: FAQ
        with gr.Tab("❓ Câu hỏi thường gặp"):
            gr.Markdown("### Tìm kiếm câu hỏi và câu trả lời")
            with gr.Row():
                with gr.Column(scale=1):
                    faq_dropdown = gr.Dropdown(
                        choices=[
                            ("Chọn câu hỏi có sẵn...", ""),
                            ("Ngành nào có điểm chuẩn cao nhất?", "FAQ001"),
                            ("Ngành nào có điểm chuẩn thấp nhất?", "FAQ002"),
                            ("Tôi thích lập trình nên học ngành gì?", "FAQ003"),
                            ("Tôi quan tâm đến AI thì nên học ngành gì?", "FAQ004"),
                            ("Điểm ĐGNL bao nhiêu thì được xét tuyển?", "FAQ005"),
                            ("Làm sao để được tuyển thẳng?", "FAQ006"),
                            ("Có chương trình nào liên kết với nước ngoài không?", "FAQ007"),
                            ("Tôi biết tiếng Nhật, có chương trình nào phù hợp không?", "FAQ008"),
                            ("Ngành An toàn Thông tin học gì?", "FAQ009"),
                            ("Thương mại điện tử học những gì?", "FAQ010"),
                            ("Học phí UIT là bao nhiêu?", "FAQ011"),
                        ],
                        label="Chọn câu hỏi có sẵn"
                    )
                    faq_keyword = gr.Textbox(label="Hoặc nhập từ khóa tìm kiếm", placeholder="VD: học phí, điểm cao nhất...")
                    btn_faq = gr.Button("🔍 Tìm kiếm", variant="primary")
                with gr.Column(scale=2):
                    output_faq = gr.Markdown()
            
            btn_faq.click(search_faq_enhanced, inputs=[faq_dropdown, faq_keyword], outputs=[output_faq])
        
        # TAB 5: Học bổng
        with gr.Tab("🏆 Học bổng"):
            gr.Markdown("### Tra cứu các chương trình học bổng")
            with gr.Row():
                with gr.Column(scale=1):
                    hb_dropdown = gr.Dropdown(
                        choices=[
                            ("Chọn loại học bổng...", ""),
                            ("🥇 Học bổng Olympic Tin học Hạng Nhất (250 triệu)", "HB001"),
                            ("🥈 Học bổng Olympic Tin học Hạng Nhì (200 triệu)", "HB002"),
                            ("🥉 Học bổng HSG Quốc gia Giải Nhất (160 triệu)", "HB003"),
                            ("🏆 Học bổng Olympic các môn Hạng Nhất (160 triệu)", "HB004"),
                            ("🎖️ Học bổng Tân sinh viên Xuất sắc (60 triệu)", "HB007"),
                            ("💡 Học bổng Khuyến khích (10-50 triệu)", "khuyenkhich"),
                            ("📚 Xem tất cả học bổng", "tat_ca"),
                        ],
                        label="Chọn loại học bổng"
                    )
                    thanh_tich_hb = gr.Textbox(
                        label="Hoặc nhập thành tích",
                        placeholder="VD: Giải Nhất Olympic Tin học..."
                    )
                    btn_hb = gr.Button("🔍 Tìm kiếm", variant="primary")
                with gr.Column(scale=2):
                    output_hb = gr.Markdown()
            
            btn_hb.click(
                search_scholarships_enhanced_no_score,
                inputs=[hb_dropdown, thanh_tich_hb],
                outputs=[output_hb]
            )
    
    gr.Markdown("""
    ---
    ### 📞 Liên hệ
    - **Website:** https://tuyensinh.uit.edu.vn
    - **Hotline:** 028.3725.2002
    - **Email:** tuyensinh@uit.edu.vn
    """)

if __name__ == "__main__":
    print("🚀 Khởi động hệ thống tư vấn tuyển sinh UIT với Gradio...")
    print("📍 Truy cập: http://localhost:7860")
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)
