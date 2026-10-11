import sys
import io
import traceback

def execute_user_code(user_code: str):
    """
    Chạy code Python do người dùng nhập và bắt toàn bộ output in ra màn hình.
    Trả về: (output_text, success_bool, error_message)
    """
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer  # Chuyển hướng stdout để bắt lệnh print()
    
    error_msg = None
    success = True
    
    try:
        # Giới hạn môi trường thực thi an toàn cơ bản
        safe_globals = {
            "__builtins__": __builtins__,
        }
        exec(user_code, safe_globals)
    except Exception as e:
        success = False
        error_msg = traceback.format_exc()
    finally:
        sys.stdout = old_stdout  # Trả lại stdout mặc định
        
    output_text = buffer.getvalue()
    return output_text, success, error_msg

def check_exercise(user_output: str, expected_output: str):
    """
    So sánh kết quả chạy code với kết quả mong đợi.
    """
    # Chuẩn hóa khoảng trắng và dòng trống ở đầu/cuối
    clean_user = user_output.strip()
    clean_expected = expected_output.strip()
    
    if clean_user == clean_expected:
        return True, " Chúc mừng! Bạn đã hoàn thành bài tập chính xác."
    else:
        return False, f" Kết quả chưa chính xác.\n- Output của bạn: '{clean_user}'\n- Output mong đợi: '{clean_expected}'"