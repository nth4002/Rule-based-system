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
            # Gọi phương thức tương ứng với category
            if category == 'tra_cuu_theo_diem':
                output = self.inference_engine.find_majors_by_score(
                    input_data.get('diem_thi'),
                    input_data.get('phuong_thuc')
                )
            elif category == 'tra_cuu_dgnl':
                output = self.inference_engine.find_majors_by_dgnl(
                    input_data.get('diem_dgnl'),
                    input_data.get('chung_chi_ngoai_ngu')
                )
            elif category == 'forward_chaining':
                output = self.inference_engine.recommend_by_interests(
                    input_data.get('so_thich'),
                    input_data.get('diem_thi')
                )
            elif category == 'faq':
                output = self.inference_engine.search_faq(
                    input_data.get('tu_khoa')
                )
            elif category == 'hoc_bong':
                output = self.inference_engine.search_scholarships(input_data)
            elif category == 'phuong_thuc_tuyen_sinh':
                output = self.inference_engine.get_admission_methods(
                    input_data.get('phuong_thuc'),
                    input_data.get('loai_truy_van')
                )
            elif category == 'complex_query':
                output = self.inference_engine.complex_search(input_data)
            elif category == 'comprehensive':
                output = self.inference_engine.comprehensive_consultation(
                    input_data.get('thong_tin_ca_nhan')
                )
            else:
                raise ValueError(f"Unknown category: {category}")
            
            result['output'] = output
            
            # Validate output dựa trên expected
            result['passed'] = self.validate_output(output, expected)
            
        except Exception as e:
            result['error'] = str(e)
            result['passed'] = False
        
        return result
    
    def validate_output(self, output, expected):
        """Kiểm tra output có đúng với expected không"""
        try:
            if expected.get('status') == 'success':
                if not output or output.get('error'):
                    return False
                
                # Kiểm tra số lượng ngành tối thiểu
                if 'min_majors' in expected:
                    majors = output.get('danh_sach_nganh', [])
                    if len(majors) < expected['min_majors']:
                        return False
                
                # Kiểm tra có chứa các ngành cụ thể
                if 'should_include' in expected:
                    majors = output.get('danh_sach_nganh', [])
                    major_ids = [m.get('ma_nganh') for m in majors]
                    for ma_nganh in expected['should_include']:
                        if ma_nganh not in major_ids:
                            return False
                
                # Kiểm tra pattern trong thông báo
                if 'thong_bao_pattern' in expected:
                    thong_bao = output.get('thong_bao', '')
                    if expected['thong_bao_pattern'].lower() not in thong_bao.lower():
                        return False
            
            elif expected.get('status') == 'fail':
                if 'majors_count' in expected:
                    majors = output.get('danh_sach_nganh', [])
                    if len(majors) != expected['majors_count']:
                        return False
                
                if expected.get('should_have_suggestions'):
                    if not output.get('goi_y'):
                        return False
            
            return True
            
        except Exception:
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
