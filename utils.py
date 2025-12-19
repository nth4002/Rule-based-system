



# ============= HELPER FUNCTIONS =============

def format_major_simple(major_info):
    """Định dạng thông tin ngành học đơn giản"""
    idx = major_info.get('idx', '0')
    output = f"### {idx}. {major_info.get('ten', 'N/A')}\n"
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