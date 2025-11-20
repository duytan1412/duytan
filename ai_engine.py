import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Tải các biến môi trường
load_dotenv()

class AITutor:
    def __init__(self):
        # Khởi tạo Google Gemini Client
        # Sử dụng cấu trúc client mới nhất có sẵn vào cuối năm 2025 
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Định nghĩa ID mô hình dựa trên độ phức tạp của tác vụ
        # "Flash" cho trò chuyện nhanh, "Pro" cho suy luận sâu
        self.fast_model = "gemini-2.0-flash-exp" 
        self.deep_model = "gemini-3.0-pro-preview"

    def get_chat_response(self, message, history, system_instruction):
        """
        Xử lý cuộc trò chuyện tiêu chuẩn bằng mô hình nhanh.
        """
        try:
            # Tạo phiên trò chuyện
            chat = self.client.chats.create(
                model=self.fast_model,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7, # Cân bằng sự sáng tạo
                    max_output_tokens=1000
                ),
                history=history
            )
            
            # Truyền phản hồi (stream) để giao diện phản hồi nhanh
            response = chat.send_message_stream(message)
            return response
            
        except Exception as e:
            return f"Lỗi: {str(e)}"

    def grade_essay(self, topic, essay, level="IELTS"):
        """
        Sử dụng mô hình Tư duy Sâu (Deep Thinking) để chấm điểm bài luận.
        Mô phỏng quy trình làm việc của giám khảo.
        """
        if level == "IELTS":
            prompt = self._get_ielts_rubric_prompt(topic, essay)
        else:
            prompt = self._get_german_correction_prompt(topic, essay)

        try:
            # Yêu cầu không stream cho các tác vụ suy luận sâu
            # Chúng ta muốn mô hình "nghĩ" xong mới hiện kết quả
            response = self.client.models.generate_content(
                model=self.deep_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    # Bật chế độ tư duy nếu có qua cờ API 
                    # thinking_mode="deep", 
                    temperature=0.4 # Nhiệt độ thấp hơn cho các tác vụ phân tích
                )
            )
            return response.text
        except Exception as e:
            return f"Lỗi chấm điểm: {str(e)}"

    def _get_ielts_rubric_prompt(self, topic, essay):
        """
        Xây dựng prompt dựa trên Bảng mô tả điểm IELTS chính thức.[18]
        """
        return f"""
        VAI TRÒ: Giám khảo IELTS được chứng nhận.
        NHIỆM VỤ: Đánh giá bài luận Writing Task 2 sau đây.
        CHỦ ĐỀ: {topic}
        BÀI LUẬN: {essay}
        
        HƯỚNG DẪN:
        1. SUY NGHĨ TỪNG BƯỚC: Phân tích bài luận dựa trên 4 tiêu chí:
           - Task Response (TR): Quan điểm có rõ ràng không? Ý tưởng có được mở rộng không?
           - Coherence & Cohesion (CC): Phân đoạn logic, từ nối.
           - Lexical Resource (LR): Collocations, từ vựng ít phổ biến.
           - Grammatical Range & Accuracy (GRA): Cấu trúc phức tạp, mật độ lỗi.
        
        2. CUNG CẤP ĐẦU RA DƯỚI DẠNG MARKDOWN:
           - Điểm Band ước tính (Tổng thể & theo từng tiêu chí).
           - Điểm mạnh chính.
           - Điểm yếu quan trọng (Cụ thể).
           - Phản hồi hành động: Viết lại 3 câu để nâng cấp chúng lên trình độ Band 8.0.
        """

    def _get_german_correction_prompt(self, topic, essay):
        """
        Xây dựng prompt sửa lỗi ngữ pháp tiếng Đức (A1-B2).
        """
        return f"""
        VAI TRÒ: Giáo viên tiếng Đức (tiêu chuẩn Viện Goethe).
        NHIỆM VỤ: Sửa văn bản tiếng Đức sau đây.
        VĂN BẢN: {essay}
        
        HƯỚNG DẪN:
        1. Xác định lỗi về Cách (Nominativ/Akkusativ/Dativ/Genitiv), Giống, và Trật tự từ.
        2. GIẢI THÍCH cụ thể *tại sao* lại sai (ví dụ: "Vì giới từ 'mit' luôn đi với Dativ...").
        3. Cung cấp phiên bản đã sửa.
        """

    def analyze_speech(self, audio_bytes, language="English"):
        """
        Phân tích đa phương thức của giọng nói.
        """
        prompt = f"""Hãy nghe đoạn âm thanh này.
        1. Chép lại chính xác những gì đã nói.
        2. Xác định lỗi phát âm hoặc ngữ điệu kỳ lạ.
        3. Phản hồi lại nội dung để duy trì cuộc trò chuyện."""
        
        try:
            response = self.client.models.generate_content(
                model=self.deep_model,  # Sử dụng mô hình Pro để hiểu âm thanh tốt nhất
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=prompt),
                            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
                        ]
                    )
                ]
            )
            return response.text
        except Exception as e:
            return f"Lỗi phân tích âm thanh: {str(e)}"