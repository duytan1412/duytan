import streamlit as st
from ai_engine import AITutor

# Cấu hình Trang
st.set_page_config(page_title="LinguaPro AI Tutor", layout="wide", page_icon="🎓")

# Khởi tạo AI Engine
if "tutor" not in st.session_state:
    st.session_state.tutor = AITutor()

# Trạng thái phiên cho Lịch sử Chat
if "messages" not in st.session_state:
    st.session_state.messages =

# --- CẤU HÌNH SIDEBAR ---
st.sidebar.title("⚙️ Cấu hình")
track = st.sidebar.radio("Chọn Lộ trình Học:",)

# Định nghĩa Chỉ dẫn Hệ thống dựa trên Lộ trình
if "English" in track:
    sys_instruction = "Bạn là Huấn luyện viên IELTS Band 8.0. Giúp người dùng cải thiện từ vựng và sự mạch lạc. Mục tiêu Band 7.0+."
    welcome_msg = "Xin chào! Tôi là Huấn luyện viên IELTS của bạn. Chúng ta hãy luyện tập Speaking Part 1 hoặc thảo luận về chủ đề Writing Task 2 nhé. Bạn muốn làm gì?"
else:
    sys_instruction = "Du bist Deutschlehrerin. Hilf dem Schüler mit Grammatik (Akkusativ/Dativ) und Wortschatz. Erkläre Fehler auf Vietnamesisch/Englisch."
    welcome_msg = "Hallo! Wie geht es dir? Wir können heute Grammatik üben oder einfach plaudern (Chào bạn! Bạn khỏe không? Hôm nay chúng ta có thể luyện ngữ pháp hoặc trò chuyện đơn giản)."

# Đặt lại cuộc trò chuyện nếu thay đổi lộ trình
if "current_track" not in st.session_state or st.session_state.current_track!= track:
    st.session_state.messages = [{"role": "model", "parts": [welcome_msg]}]
    st.session_state.current_track = track

# --- GIAO DIỆN CHÍNH ---
st.title(f"LinguaPro: {track}")

# Các tab cho các chế độ học tập khác nhau
tab_chat, tab_essay, tab_voice = st.tabs()

# --- TAB 1: HỘI THOẠI ---
with tab_chat:
    # Hiển thị Lịch sử Chat
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["parts"])

    # Đầu vào Chat
    if user_input := st.chat_input("Nhập tin nhắn của bạn ở đây..."):
        # Hiển thị tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "parts": [user_input]})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Tạo Phản hồi AI
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Gọi Bộ não Nhanh
            response_stream = st.session_state.tutor.get_chat_response(
                user_input, 
                st.session_state.messages[:-1], # Lịch sử trừ tin nhắn hiện tại
                sys_instruction
            )
            
            # Logic Stream
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "model", "parts": [full_response]})

# --- TAB 2: CHẤM ĐIỂM BÀI LUẬN (Bộ não Sâu) ---
with tab_essay:
    st.header("Chấm điểm Bài luận Tư duy Sâu")
    st.info("Chế độ này sử dụng Gemini 3.0 Pro / GPT-5.1 Thinking để cung cấp phản hồi cấp độ giám khảo.")
    
    essay_topic = st.text_input("Nhập Chủ đề / Câu hỏi Bài luận:")
    essay_text = st.text_area("Dán bài luận của bạn vào đây:", height=300)
    
    if st.button("Chấm điểm Bài luận của tôi"):
        if essay_text and essay_topic:
            with st.spinner("Giám khảo AI đang suy nghĩ sâu... (Việc này có thể mất 15-30 giây)"):
                feedback = st.session_state.tutor.grade_essay(
                    essay_topic, 
                    essay_text, 
                    level="IELTS" if "English" in track else "German"
                )
                st.markdown(feedback)
        else:
            st.warning("Vui lòng cung cấp cả chủ đề và bài luận.")

# --- TAB 3: CHẾ ĐỘ GIỌNG NÓI (Đa phương thức) ---
with tab_voice:
    st.header("Luyện Phát âm & Nói")
    
    # Sử dụng đầu vào âm thanh gốc của Streamlit [17]
    audio_value = st.audio_input("Ghi âm giọng nói của bạn")
    
    if audio_value:
        st.audio(audio_value)
        with st.spinner("Đang phân tích giọng nói..."):
            # Trong thực tế, bạn sẽ truyền byte 'audio_value' tới Gemini
            # Gemini 3.0 chấp nhận byte âm thanh trực tiếp trong tham số 'contents'
            # Tham khảo  và [6] để biết cách sử dụng API âm thanh gốc
            st.success("Đã xử lý âm thanh! (Logic tích hợp ở backend)")
            # Placeholder cho phản hồi
            st.markdown("**Phản hồi AI:** Phát âm từ 'th' của bạn cần cải thiện. Hãy thử đặt lưỡi giữa hai hàm răng.")