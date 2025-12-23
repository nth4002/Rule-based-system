import gradio as gr
from inference.rule_based import RuleBasedInference

# Khởi tạo inference engine
inference_engine = RuleBasedInference()

# ============= HỌC BỔNG =============

def search_scholarships(thanh_tich):
    """Tìm kiếm học bổng"""
    if not thanh_tich:
        return "⚠️ Vui lòng nhập thông tin!"
    
    result = inference_engine.search_scholarships(thanh_tich)
    
    output = ""
    if 'tong_so_hoc_bong' in result:
        output = f"## 🏆 Tổng số học bổng: {result['tong_so_hoc_bong']}\n\n"
        for hb in result['danh_sach_hoc_bong']:
            output += f"### {hb['ten']}\n"
            output += f"**Mã:** {hb['id']} | **Giá trị:** {hb['gia_tri']}\n\n"
    
    if result.get('hoc_bong'):
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

def search_scholarships_enhanced_no_score(ky_thi, mon_hoc, giai):
    """Tìm kiếm học bổng với 3 dropdown (kỳ thi, môn học, giải)"""
    if not ky_thi or not giai:
        return "⚠️ Vui lòng chọn đầy đủ kỳ thi và giải!"
    
    thanh_tich = {
        'ky_thi': ky_thi,
        'mon_hoc': mon_hoc,
        'giai': giai
    }
    
    return search_scholarships(thanh_tich)

# ============= TAB 6: TƯ VẤN TOÀN DIỆN =============

def comprehensive_consultation(diem_thi, diem_dgnl, to_hop, loai_cc, diem_cc, thanh_tich, interests, top_k=10):
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
    if loai_cc and diem_cc and diem_cc > 0:
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
    
    # Ngành đề xuất - giới hạn theo top_k
    output += f"### 🎯 Top {top_k if top_k else 'tất cả'} ngành được đề xuất:\n\n"
    if result.get('nganh_de_xuat') and len(result['nganh_de_xuat']) > 0:
        nganh_list = result['nganh_de_xuat']
        if top_k and top_k > 0:
            nganh_list = nganh_list[:top_k]
        
        for nganh in nganh_list:
            output += f"**#{nganh['hang']} {nganh['ten']}**\n"
            output += f"- Mã ngành: {nganh['ma_nganh']}\n"
            output += f"- Điểm chuẩn: {nganh.get('diem_chuan', 'N/A')}\n"
            output += f"- Trạng thái: {nganh.get('trang_thai', 'N/A')}\n"
            if nganh.get('ly_do'):
                output += f"- Lý do: {nganh['ly_do']}\n"
            output += f"- Độ phù hợp: {nganh.get('do_phu_hop', 0):.0%}\n\n"
        
        if top_k and len(result['nganh_de_xuat']) > top_k:
            output += f"*Hiển thị {top_k}/{len(result['nganh_de_xuat'])} ngành. Tổng số ngành đủ điều kiện: {len(result['nganh_de_xuat'])}*\n\n"
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
    
    # Traceability - Hiển thị các bước suy luận
    if result.get('trace'):
        output += "\n---\n\n"
        output += "### 🔍 TRACEABILITY - CÁC BƯỚC SUY LUẬN (FORWARD CHAINING)\n\n"
        for step in result['trace']:
            output += f"#### Bước {step['buoc']}: {step['ten_buoc']}\n\n"
            output += f"**Rule:** {step['rule']}\n\n"
            output += f"**Input:**\n"
            for key, value in step.get('input', {}).items():
                output += f"- {key}: {value}\n"
            output += f"\n**Output:**\n"
            for key, value in step.get('output', {}).items():
                if isinstance(value, list):
                    output += f"- {key}: {', '.join(str(v) for v in value[:5])}{'...' if len(value) > 5 else ''}\n"
                else:
                    output += f"- {key}: {value}\n"
            output += f"\n**Kết quả:** {step.get('ket_qua', 'N/A')}\n\n"
            output += "---\n\n"
    
    return output

# ============= HÀM RESET =============

def reset_form():
    """Reset tất cả các input về giá trị mặc định"""
    return (
        gr.update(value=None),      # diem_thpt
        gr.update(value=""),         # to_hop_thpt
        gr.update(value=None),      # diem_dgnl_input
        gr.update(value=""),        # loai_cc_dgnl
        gr.update(value=None),      # diem_cc_dgnl
        gr.update(value=""),        # ky_thi_hb
        gr.update(value="Tin học"), # mon_hoc_hb
        gr.update(value=""),        # giai_hb
        gr.update(value=3),        # top_k
        gr.update(value="")         # output_all
    )

# ============= HÀM XỬ LÝ TỔNG HỢP =============

def process_all_inputs(diem_thpt, to_hop_thpt, diem_dgnl, loai_cc, diem_cc, ky_thi_hb, mon_hoc_hb, giai_hb, top_k):
    """Xử lý tất cả input và trả về kết quả tổng hợp"""
    output = ""
    
    # Xử lý thành tích học bổng
    thanh_tich = None
    if ky_thi_hb and giai_hb:
        thanh_tich = f"Giải {giai_hb} {mon_hoc_hb} {ky_thi_hb}"
    
    # Kiểm tra xem có ít nhất điểm THPT hoặc ĐGNL không
    has_score = (diem_thpt and diem_thpt > 0) or (diem_dgnl and diem_dgnl > 0)
    
    if has_score:
        # Xử lý top_k: nếu không có hoặc <= 0 thì hiển thị tất cả
        top_k_value = int(top_k) if top_k and top_k > 0 else None
        result = comprehensive_consultation(
            diem_thpt, diem_dgnl, to_hop_thpt, loai_cc, diem_cc, thanh_tich, None, top_k_value
        )
        output += result + "\n\n"
    else:
        output += "## ⚠️ Thông báo\n\n"
        output += "Vui lòng nhập ít nhất **điểm thi THPT** hoặc **điểm ĐGNL** để nhận tư vấn về ngành học.\n\n"
    
    # Nếu có thông tin học bổng, thêm kết quả tra cứu học bổng
    if ky_thi_hb and giai_hb:
        if has_score:
            output += "---\n\n"
        output += "## 🏆 KẾT QUẢ TRA CỨU HỌC BỔNG\n\n"
        hb_result = search_scholarships_enhanced_no_score(ky_thi_hb, mon_hoc_hb, giai_hb)
        output += hb_result
    
    if not has_score and not (ky_thi_hb and giai_hb):
        output = "⚠️ Vui lòng nhập ít nhất một trong các thông tin sau:\n"
        output += "- Điểm thi THPT hoặc Điểm ĐGNL (để nhận tư vấn ngành học)\n"
        output += "- Thông tin học bổng (kỳ thi, môn học, giải) để tra cứu học bổng"
    
    return output

# ============= GRADIO INTERFACE =============

custom_css = """
    .gradio-container {
        background-color: white !important;
        color: black !important;
    }
    body {
        background-color: white !important;
        color: black !important;
    }
    .markdown {
        background-color: white !important;
        color: black !important;
    }
    .markdown p, .markdown h1, .markdown h2, .markdown h3, .markdown h4, .markdown h5, .markdown h6 {
        color: black !important;
    }
    .output-markdown {
        background-color: white !important;
        color: black !important;
    }
"""

with gr.Blocks(title="Hệ thống Tư vấn Tuyển sinh UIT") as app:
    
    gr.Markdown("""
    <div class="header">
        <h1>🎓 HỆ THỐNG TƯ VẤN TUYỂN SINH</h1>
        <h2>Đại học Công nghệ Thông tin - ĐHQG-HCM</h2>
        <p>Hệ thống hỗ trợ Forward Chaining, Tra cứu thông minh</p>
    </div>
    """)
    
    gr.Markdown("### 📝 Điền thông tin của bạn vào form bên dưới để nhận tư vấn")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("#### 📊 Điểm thi THPT")
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
            
            gr.Markdown("#### 🎯 Điểm ĐGNL & Chứng chỉ")
            diem_dgnl_input = gr.Number(label="Điểm ĐGNL (600-1200)", minimum=0, maximum=1200)
            loai_cc_dgnl = gr.Dropdown(
                choices=["", "IELTS", "TOEFL iBT", "TOEIC"],
                label="Loại chứng chỉ ngoại ngữ (tùy chọn)",
                value=""
            )
            diem_cc_dgnl = gr.Number(label="Điểm chứng chỉ", minimum=0, maximum=10, step=0.5)
            
            gr.Markdown("#### 🏆 Thành tích")
            ky_thi_hb = gr.Dropdown(
                choices=[
                    ("Chọn kỳ thi...", ""),
                    ("Kỳ thi HSG Quốc gia THPT", "kỳ thi HSG Quốc gia THPT"),
                    ("Kỳ thi Siêu Cup - Olympic Tin học Việt Nam", "kỳ thi Siêu Cup - Olympic Tin học Việt Nam"),
                    ("Kỳ thi Olympic khu vực và quốc tế môn Tin học", "kỳ thi Olympic khu vực và quốc tế môn Tin học"),
                    ("Kỳ thi Olympic Tin học Việt Nam", "kỳ thi Olympic Tin học Việt Nam"),
                ],
                label="Kỳ thi",
                value=""
            )
            mon_hoc_hb = gr.Dropdown(
                choices=[
                    ("Tin học", "Tin học"),
                    ("Toán", "Toán"),
                    ("Lý", "Lý"),
                    ("Hoá", "Hoá"),
                    ("Anh Văn", "Anh Văn"),
                ],
                label="Môn học",
                value="Tin học"
            )
            giai_hb = gr.Dropdown(
                choices=[
                    ("Chọn giải...", ""),
                    ("Nhất", "Nhất"),
                    ("Nhì", "Nhì"),
                    ("Ba", "Ba"),
                    ("Khuyến khích", "Khuyến khích"),
                ],
                label="Giải",
                value=""
            )
            
            # Hàm cập nhật dropdown giải dựa trên kỳ thi
            def update_giai_choices(ky_thi):
                if ky_thi == "kỳ thi Siêu Cup - Olympic Tin học Việt Nam":
                    return gr.update(choices=[
                        ("Chọn giải...", ""),
                        ("Vàng", "Vàng"),
                        ("Bạc", "Bạc"),
                        ("Đồng", "Đồng"),
                    ], value="")
                else:
                    return gr.update(choices=[
                        ("Chọn giải...", ""),
                        ("Nhất", "Nhất"),
                        ("Nhì", "Nhì"),
                        ("Ba", "Ba"),
                        ("Khuyến khích", "Khuyến khích"),
                    ], value="")
            
            # Khi kỳ thi thay đổi, cập nhật dropdown giải
            ky_thi_hb.change(
                fn=update_giai_choices,
                inputs=[ky_thi_hb],
                outputs=[giai_hb]
            )
            
            gr.Markdown("#### ⚙️ Tùy chọn")
            top_k = gr.Number(
                label="Số lượng ngành hiển thị (Top K)",
                minimum=1,
                maximum=100,
                value=3,
                step=1,
                info="Nhập số lượng ngành muốn xem (để trống hoặc 0 để xem tất cả)"
            )
            
            with gr.Row():
                btn_submit = gr.Button("🚀 Nhận tư vấn", variant="primary", size="lg")
                btn_reset = gr.Button("🔄 Reset", variant="secondary", size="lg")
        
        with gr.Column(scale=2):
            output_all = gr.Markdown()
    
    btn_submit.click(
        process_all_inputs,
        inputs=[
            diem_thpt, to_hop_thpt, diem_dgnl_input, loai_cc_dgnl, diem_cc_dgnl,
            ky_thi_hb, mon_hoc_hb, giai_hb, top_k
        ],
        outputs=[output_all]
    )
    
    btn_reset.click(
        fn=reset_form,
        inputs=[],
        outputs=[
            diem_thpt, to_hop_thpt, diem_dgnl_input, loai_cc_dgnl, diem_cc_dgnl,
            ky_thi_hb, mon_hoc_hb, giai_hb, top_k, output_all
        ]
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
