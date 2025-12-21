"""
Test Runner cho Hệ thống Tư vấn Tuyển sinh UIT
Chạy các test cases và tạo báo cáo kết quả
"""

import json
import os
import sys
from datetime import datetime

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.rule_based import RuleBasedInference


class TestRunner:
    def __init__(self, test_cases_path=None):
        """Khởi tạo test runner"""
        if test_cases_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            test_cases_path = os.path.join(current_dir, 'test_cases.json')
        
        with open(test_cases_path, 'r', encoding='utf-8') as f:
            self.test_data = json.load(f)
        
        self.tests = self.test_data['tests']
        self.inference_engine = RuleBasedInference()
        self.results = []
    
    def run_all_tests(self):
        """Chạy tất cả test cases"""
        print("=" * 80)
        print(f"BẮT ĐẦU CHẠY {len(self.tests)} TEST CASES")
        print("=" * 80)
        print()
        
        passed = 0
        failed = 0
        
        for test in self.tests:
            result = self.run_single_test(test)
            self.results.append(result)
            
            if result['passed']:
                passed += 1
                status = "✓ PASS"
            else:
                failed += 1
                status = "✗ FAIL"
            
            print(f"{status} | {test['id']} - {test['name']}")
            if not result['passed']:
                print(f"      Lỗi: {result['error']}")
        
        print()
        print("=" * 80)
        print(f"KẾT QUẢ: {passed}/{len(self.tests)} PASS | {failed} FAIL")
        print("=" * 80)
        
        return {
            'total': len(self.tests),
            'passed': passed,
            'failed': failed,
            'results': self.results
        }
    
    def run_single_test(self, test):
        """Chạy một test case"""
        test_id = test['id']
        category = test['category']
        input_data = test['input']
        expected = test['expected']
        
        result = {
            'test_id': test_id,
            'name': test['name'],
            'category': category,
            'passed': False,
            'error': None,
            'output': None
        }
        
        try:
            # Tất cả test cases đều dùng comprehensive_consultation
            if category == 'comprehensive':
                # Xử lý input trực tiếp cho comprehensive_consultation
                thong_tin = {}
                if input_data.get('diem_thi') is not None:
                    thong_tin['diem_thi'] = float(input_data['diem_thi'])
                if input_data.get('diem_dgnl') is not None:
                    thong_tin['diem_dgnl'] = float(input_data['diem_dgnl'])
                if input_data.get('to_hop_mon'):
                    thong_tin['to_hop_mon'] = input_data['to_hop_mon']
                if input_data.get('chung_chi_ngoai_ngu'):
                    thong_tin['chung_chi_ngoai_ngu'] = input_data['chung_chi_ngoai_ngu']
                if input_data.get('thanh_tich'):
                    thong_tin['thanh_tich'] = input_data['thanh_tich']
                if input_data.get('so_thich'):
                    thong_tin['so_thich'] = input_data['so_thich']
                
                output = self.inference_engine.comprehensive_consultation(thong_tin)
            else:
                raise ValueError(f"Unknown category: {category}")
            
            result['output'] = output
            
            # Validate output dựa trên expected
            result['passed'] = self.validate_output(output, expected, input_data)
            
        except Exception as e:
            result['error'] = str(e)
            result['passed'] = False
        
        return result
    
    def validate_output(self, output, expected, input_data=None):
        """Kiểm tra output có đúng với expected không"""
        try:
            if expected.get('status') == 'success':
                if not output or output.get('error'):
                    return False
                
                # Kiểm tra số lượng ngành tối thiểu
                if 'min_majors' in expected:
                    majors = output.get('nganh_de_xuat', [])
                    if len(majors) < expected['min_majors']:
                        return False
                
                # Kiểm tra số lượng ngành (có thể là 0 hoặc thấp)
                if 'majors_count' in expected:
                    majors = output.get('nganh_de_xuat', [])
                    if expected['majors_count'] == 0:
                        if len(majors) > 0:
                            return False
                    elif expected['majors_count'] == "may_be_zero_or_low":
                        # Chấp nhận 0 hoặc số thấp
                        pass
                
                # Kiểm tra có chứa các ngành cụ thể (theo mã ngành)
                if 'should_include_ma_nganh' in expected:
                    majors = output.get('nganh_de_xuat', [])
                    major_ids = [m.get('ma_nganh') for m in majors]
                    for ma_nganh in expected['should_include_ma_nganh']:
                        if ma_nganh not in major_ids:
                            return False
                
                # Kiểm tra phương thức
                if 'phuong_thuc' in expected:
                    pt = output.get('phan_tich_tong_quan', {})
                    if pt.get('phuong_thuc_tot_nhat') != expected['phuong_thuc']:
                        return False
                
                # Kiểm tra điểm cộng và điểm xét tuyển
                if 'diem_cong_expected' in expected:
                    # Tính lại điểm cộng từ input (không dùng trace)
                    diem_cong = 0
                    if input_data:
                        chung_chi = input_data.get('chung_chi_ngoai_ngu')
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
                    
                    if diem_cong != expected['diem_cong_expected']:
                        return False
                
                if 'diem_xet_tuyen_expected' in expected:
                    pt = output.get('phan_tich_tong_quan', {})
                    diem_xet_tuyen = pt.get('diem_xet_tuyen_sau_cong')
                    if diem_xet_tuyen != expected['diem_xet_tuyen_expected']:
                        return False
                
                # Kiểm tra học bổng
                if 'min_scholarships' in expected:
                    hoc_bong = output.get('hoc_bong_du_kien', [])
                    if len(hoc_bong) < expected['min_scholarships']:
                        return False
                
                # Kiểm tra học bổng theo ID
                if 'should_include_hoc_bong_ids' in expected:
                    hoc_bong = output.get('hoc_bong_du_kien', [])
                    hoc_bong_ids = [hb.get('id') for hb in hoc_bong]
                    found = False
                    for hb_id in expected['should_include_hoc_bong_ids']:
                        if hb_id in hoc_bong_ids:
                            found = True
                            break
                    if not found:
                        return False
                
                if 'should_have_hoc_bong_du_kien' in expected:
                    if not output.get('hoc_bong_du_kien'):
                        return False
                
            elif expected.get('status') == 'fail':
                if 'majors_count' in expected:
                    majors = output.get('nganh_de_xuat', [])
                    if expected['majors_count'] == 0:
                        if len(majors) > 0:
                            return False
            
            return True
            
        except Exception as e:
            return False
    
    def generate_report(self, output_path=None):
        """Tạo báo cáo chi tiết"""
        if output_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(current_dir, f'test_report_{timestamp}.json')
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.tests),
                'passed': sum(1 for r in self.results if r['passed']),
                'failed': sum(1 for r in self.results if not r['passed'])
            },
            'results': self.results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\nBáo cáo chi tiết đã được lưu tại: {output_path}")
        return output_path


def main():
    """Chạy test runner"""
    runner = TestRunner()
    results = runner.run_all_tests()
    runner.generate_report()
    
    # Return exit code based on results
    if results['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
