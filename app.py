import gradio as gr
from inference.rule_based import RuleBasedInference

# Khởi tạo inference engine
inference_engine = RuleBasedInference()

def format_major_output(major):
    """Định dạng thông tin một ngành học"""
    output = f"### {major.get('ten', 'N/A')}\n\n"
    output += f"**Mã ngành:** {major.get('ma_nganh', 'N/A')}\n\n"
    output += f"**Mô tả:** {major.get('mo_ta', 'N/A')}\n\n"
    
    diem_chuan = major.get('diem_trung_tuyen')
    if diem_chuan:
        output += f"**Điểm chuẩn:** {diem_chuan}\n\n"
    
    co_hoi = major.get('co_hoi_nghe_nghiep', [])
    if co_hoi:
        output += f"**Cơ hội nghề nghiệp:** {', '.join(co_hoi)}\n\n"
    
    chi_tieu = major.get('chi_tieu')
    if chi_tieu:
        output += f"**Chỉ tiêu:** {chi_tieu}\n\n"
    
    to_hop = major.get('to_hop_mon', [])
    if to_hop:
        output += f"**Tổ hợp môn:** {', '.join(to_hop)}\n\n"
    
    output += "---\n\n"
    return output

def find_majors(to_hop_mon, diem):
    """
    Hàm xử lý forward inference và trả về kết quả
    """
    # Chuyển đổi input
    to_hop_mon = to_hop_mon if to_hop_mon else None
    diem = float(diem) if diem else None
    
    # Forward inference
    majors = inference_engine.forward_inference(to_hop_mon=to_hop_mon, diem=diem)
    
    # Định dạng kết quả
    if not majors:
        return "❌ Không tìm thấy ngành học phù hợp với tiêu chí của bạn."
    
    output = f"## 🎓 Tìm thấy {len(majors)} ngành học phù hợp:\n\n"
    
    for major in majors:
        output += format_major_output(major)
    
    return output

# Tạo giao diện Gradio
with gr.Blocks(title="Hệ thống Tư vấn Ngành học - UIT") as app:
    gr.Markdown(
        """
        # 🎓 Hệ thống Tư vấn Ngành học
        ## Đại học Công nghệ Thông tin - ĐHQG-HCM
        
        Hệ thống sử dụng forward inference với 2 rules:
        - **Rule 1:** Lọc ngành theo tổ hợp môn thi
        - **Rule 2:** Lọc ngành theo điểm chuẩn (nếu điểm >= điểm chuẩn)
        """
    )
    
    with gr.Row():
        with gr.Column():
            to_hop_mon = gr.Dropdown(
                choices=[
                    ("A00 - Toán, Vật lý, Hóa học", "A00"),
                    ("A01 - Toán, Vật lý, Tiếng Anh", "A01"),
                    ("D01 - Toán, Văn, Tiếng Anh", "D01"),
                    ("D07 - Toán, Hóa học, Tiếng Anh", "D07"),
                    ("D08 - Toán, Sinh học, Tiếng Anh", "D08"),
                    ("X06 - Toán, Vật lý, Tin học", "X06"),
                    ("X26 - Toán, Tiếng Anh, Tin học", "X26"),
                ],
                label="Tổ hợp môn thi",
                info="Chọn tổ hợp môn bạn đã thi",
                allow_custom_value=False
            )
            
            diem = gr.Number(
                label="Điểm thi (tùy chọn)",
                info="Nhập điểm thi của bạn (0-30)",
                minimum=0,
                maximum=30,
                step=0.1,
                precision=1
            )
            
            submit_btn = gr.Button("🔍 Tìm ngành học phù hợp", variant="primary", size="lg")
        
        with gr.Column():
            output = gr.Markdown(
                label="Kết quả",
                value="Nhập thông tin và nhấn nút để tìm ngành học phù hợp."
            )
    
    # Xử lý sự kiện
    submit_btn.click(
        fn=find_majors,
        inputs=[to_hop_mon, diem],
        outputs=output
    )
    
    # Tự động cập nhật khi thay đổi giá trị (tùy chọn)
    to_hop_mon.change(
        fn=find_majors,
        inputs=[to_hop_mon, diem],
        outputs=output
    )
    diem.change(
        fn=find_majors,
        inputs=[to_hop_mon, diem],
        outputs=output
    )
    
    gr.Markdown(
        """
        ---
        ### 📝 Lưu ý:
        - Bạn có thể chỉ chọn tổ hợp môn hoặc chỉ nhập điểm, hoặc cả hai
        - Hệ thống sẽ tự động lọc các ngành phù hợp dựa trên thông tin bạn cung cấp
        """
    )

if __name__ == "__main__":
    print("🚀 Khởi động hệ thống tư vấn ngành học với Gradio...")
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)

