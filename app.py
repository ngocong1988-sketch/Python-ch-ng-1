import streamlit as st
import json
import os
from coder_engine import execute_user_code, check_exercise

# Tắt cảnh báo dịch tự động của trình duyệt
st.markdown(
    """
    <html lang="vi" class="notranslate" translate="no">
    <head>
        <meta name="google" content="notranslate" />
    </head>
    """,
    unsafe_allow_html=True
)

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="App Học Python - Từ Zero Đến Thành Thạo",
    page_icon="🐍",
    layout="wide"
)

# --- 1. KHỞI TẠO SESSION STATE LƯU TIẾN ĐỘ ---
if "completed_lessons" not in st.session_state:
    st.session_state.completed_lessons = set()

# Danh sách cấu hình 5 chặng học
STAGES = {
    "Chặng 1: Nhập môn & Cấu trúc cơ bản": "lessons_chang1.json",
    "Chặng 2: Cấu trúc dữ liệu & Hàm": "lessons_chang2.json",
    "Chặng 3: OOP & Xử lý File": "lessons_chang3.json",
    "Chặng 4: Thuật toán & Thư viện": "lessons_chang4.json",
    "Chặng 5: Dự án thực tế & Định hướng": "lessons_chang5.json"
}

# Hàm tải dữ liệu bài học
def load_lessons(json_filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    json_path = os.path.join(data_dir, json_filename)
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return data
        except Exception:
            pass
            
    return [
        {
            "id": "coming_soon",
            "title": "Nội dung đang được cập nhật",
            "theory": "### 🚀 Chặng học này đang được biên soạn!\nBạn vui lòng quay lại sau hoặc chọn Chặng khác ở thanh menu bên trái.",
            "initial_code": "# Code mẫu\nprint('Nội dung sắp ra mắt!')\n",
            "exercise": {
                "prompt": "**Thử thách:** In ra dòng chữ `Nội dung sắp ra mắt!`",
                "expected_output": "Nội dung sắp ra mắt!\n"
            }
        }
    ]

# --- HEADER APP ---
st.title("🐍 Ứng Dụng Học Python Từ Zero Đến Thành Thạo")
st.caption("Hệ thống bài học tương tác & chấm điểm tự động")
st.divider()

# --- SIDEBAR: CHỌN CHẶNG & BÀI HỌC ---
st.sidebar.header("🎯 Lộ Trình Học Tập")

# 1. Chọn Chặng học
selected_stage_name = st.sidebar.selectbox(
    "Chọn Chặng học:",
    list(STAGES.keys())
)

json_file = STAGES[selected_stage_name]
lessons = load_lessons(json_file)

st.sidebar.divider()

# --- 2. HIỂN THỊ THANH TIẾN ĐỘ HỌC TẬP (PROGRESS BAR) ---
total_lessons = len(lessons)
completed_in_stage = sum(1 for l in lessons if l["id"] in st.session_state.completed_lessons)
progress_percentage = completed_in_stage / total_lessons if total_lessons > 0 else 0.0

st.sidebar.subheader("📊 Tiến độ Chặng")
st.sidebar.progress(progress_percentage)
st.sidebar.caption(f"Đã hoàn thành **{completed_in_stage}/{total_lessons}** bài học ({int(progress_percentage * 100)}%)")

st.sidebar.divider()
st.sidebar.header("📚 Danh sách bài học")

# --- 3. ĐÁNH DẤU ✅ VÀO DANH SÁCH BÀI HỌC ---
lesson_options = []
for l in lessons:
    status_icon = "✅ " if l["id"] in st.session_state.completed_lessons else "📖 "
    lesson_options.append(f"{status_icon}{l['title']}")

selected_option = st.sidebar.radio(
    "Chọn bài học:",
    lesson_options,
    index=0
)

# Lấy chỉ số bài học đang chọn
current_idx = lesson_options.index(selected_option)
current_lesson = lessons[current_idx]

# --- CHIA MÀN HÌNH THÀNH 2 CỘT ---
col_left, col_right = st.columns([1, 1], gap="large")

# --- CỘT TRÁI: LÝ THUYẾT & ĐỀ BÀI ---
with col_left:
    # Hiển thị nhãn Hoàn thành nếu bài này đã làm xong
    if current_lesson["id"] in st.session_state.completed_lessons:
        st.success("🎉 Bạn đã hoàn thành bài học này!")
        
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
        key=f"editor_{selected_stage_name}_{current_lesson['id']}"
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
                # --- 4. TỰ ĐỘNG LƯU TIẾN ĐỘ KHI NỘP ĐÚNG ---
                st.session_state.completed_lessons.add(current_lesson["id"])
                st.success(msg)
                st.balloons()
                # Tải lại trang nhẹ để cập nhật icon ✅ trên Sidebar
                st.rerun()
            else:
                st.warning(msg)