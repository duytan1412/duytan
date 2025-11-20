# LinguaPro AI Tutor

Ứng dụng gia sư AI đa ngôn ngữ sử dụng Google Gemini.

## Triển khai lên Streamlit Cloud

1. Push code lên GitHub repository: https://github.com/duytan1412/duytan.git
2. Đăng nhập vào [share.streamlit.io](https://share.streamlit.io)
3. Kết nối tài khoản GitHub và chọn repository
4. **Quan trọng**: Trong phần "Advanced settings" > "Secrets", thêm:

```toml
GOOGLE_API_KEY = "your-google-api-key-here"
OPENAI_API_KEY = "your-openai-api-key-here"
```

5. Deploy!

## Chạy local

```bash
pip install -r requirements.txt
streamlit run app.py
```
