import streamlit as st
import json
import os
from coder_engine import execute_user_code, check_exercise

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="App Học Python - Chặng 1",
    page_icon="🐍",
    layout="wide"
)

# Dữ liệu dự phòng nếu không tìm thấy file JSON
DEFAULT_LESSONS = [
    {
        "id": "bai_1",
        "title": "Bài 1: Chào mừng tới Python & Chương trình đầu tiên",
        "theory": "### 1. Hàm `print()`\nHàm `print()` dùng để xuất dữ liệu ra màn hình.\n\n### 2. Ví dụ:\n```python\nprint('Xin chào thế giới!')\n```\n\n### 3. Quy tắc:\n- Phân biệt chữ hoa/chữ thường (`print` khác `Print`).\n- Chuỗi văn bản phải đặt trong cặp dấu ngoặc đơn `''` hoặc ngoặc kép `\"\"`.",
        "initial_code": "# Viết code của bạn ở đây\n",
        "exercise": {
            "prompt": "**Thử thách:** Dùng hàm `print()` để in ra chính xác dòng chữ: `Chào mừng bạn đến với Python!`",
            "expected_output": "Chào mừng bạn đến với Python!\n"
        }
    },
    {
        "id": "bai_2",
        "title": "Bài 2: Biến & Các kiểu dữ liệu cơ bản",
        "theory": "### 1. Biến (Variable)\nBiến là hộp chứa dữ liệu. Khai báo biến bằng cách gán giá trị: `ten_bien = gia_tri`.\n\n### 2. Các kiểu dữ liệu cơ bản:\n- `int`: Số nguyên (VD: `age = 25`)\n- `float`: Số thực (VD: `gpa = 8.5`)\n- `str`: Chuỗi ký tự (VD: `name = 'Công'`)\n- `bool`: Đúng/Sai (`True` hoặc `False`)",
        "initial_code": "# Tạo biến name và age\nname = 'Công'\nage = 37\nprint(name)\nprint(age)\n",
        "exercise": {
            "prompt": "**Thử thách:** Tạo biến `so_a = 10` và `so_b = 20`. In ra tổng của 2 số này.",
            "expected_output": "30\n"
        }
    },
    {
        "id": "bai_3",
        "title": "Bài 3: Định dạng chuỗi với f-string",
        "theory": "### f-string trong Python\nf-string giúp ghép biến vào chuỗi dễ dàng bằng cách đặt chữ `f` trước dấu ngoặc bọc chuỗi và đặt tên biến trong `{}`.\n\n### Ví dụ:\n```python\nten = 'Nam'\ntuoi = 15\nprint(f'{ten} năm nay {tuoi} tuổi.')\n```",
        "initial_code": "mon_hoc = 'Python'\ndiem = 10\n# In ra: Môn Python đạt 10 điểm!\n",
        "exercise": {
            "prompt": "**Thử thách:** Dùng f-string in ra chuỗi: `Môn Python đạt 10 điểm!` dựa trên 2 biến `mon_hoc = 'Python'` và `diem = 10`.",
            "expected_output": "Môn Python đạt 10 điểm!\n"
        }
    }
]

# Hàm tải dữ liệu bài học an toàn
# Bỏ dòng @st.cache_data để ứng dụng luôn đọc file mới nhất
def load_lessons():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "data", "lessons_chang1.json")
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception as e:
            st.error(f"Lỗi đọc file JSON: {e}")
            
    # Báo lỗi nếu không đọc được file JSON thay vì tự trả về 3 bài mẫu
    st.error(f"Không tìm thấy file bài học tại: {json_path}")
    return []

lessons = load_lessons()

# --- HEADER APP ---
st.title("🐍 Ứng Dụng Học Python Từ Zero Đến Thành Thạo")
st.caption("Chặng 1: Nhập môn & Cấu trúc cơ bản")
st.divider()

# --- SIDEBAR: DANH SÁCH BÀI HỌC ---
st.sidebar.header("📚 Danh sách bài học")
lesson_titles = [f"{i+1}. {l['title']}" for i, l in enumerate(lessons)]

# Quản lý bài học chọn
selected_lesson = st.sidebar.radio(
    "Chọn bài học:",
    lesson_titles,
    index=0
)

current_idx = lesson_titles.index(selected_lesson)
current_lesson = lessons[current_idx]

# --- CHIA MÀN HÌNH THÀNH 2 CỘT ---
col_left, col_right = st.columns([1, 1], gap="large")

# --- CỘT TRÁI: LÝ THUYẾT & ĐỀ BÀI ---
with col_left:
    st.subheader(current_lesson["title"])
    
    tab_theory, tab_exercise = st.tabs(["📖 Lý thuyết", "🎯 Bài tập thực hành"])
    
    with tab_theory:
        st.markdown(current_lesson["theory"])
        
    with tab_exercise:
        st.markdown(current_lesson["exercise"]["prompt"])

# --- CỘT PHẢI: TRÌNH BIÊN DỊCH & CHẤM ĐIỂM ---
with col_right:
    st.subheader("💻 Môi trường gõ code")
    
    user_code = st.text_area(
        "Viết code Python của bạn tại đây:",
        value=current_lesson["initial_code"],
        height=220,
        key=f"editor_{current_lesson['id']}"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        run_pressed = st.button("▶️ Chạy Code", use_container_width=True)
    with col_btn2:
        submit_pressed = st.button("✅ Nộp Bài Chấm Điểm", type="primary", use_container_width=True)
        
    st.divider()
    st.subheader("🖥️ Kết quả đầu ra (Output):")
    
    if run_pressed:
        output, success, error_msg = execute_user_code(user_code)
        if success:
            st.code(output if output else "[Chương trình chạy thành công và không in ra kết quả]", language="text")
        else:
            st.error(" Lỗi khi chạy code:")
            st.code(error_msg, language="python")
            
    if submit_pressed:
        output, success, error_msg = execute_user_code(user_code)
        if not success:
            st.error(" Code bị lỗi, không thể chấm điểm:")
            st.code(error_msg, language="python")
        else:
            is_correct, msg = check_exercise(output, current_lesson["exercise"]["expected_output"])
            if is_correct:
                st.success(msg)
                st.balloons()
            else:
                st.warning(msg)