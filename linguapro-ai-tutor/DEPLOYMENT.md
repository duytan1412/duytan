# Hướng dẫn Triển khai Streamlit Cloud

## Bước 1: Chuẩn bị Repository

1. Đảm bảo tất cả file đã được commit (trừ .env và venv/)
2. Push code lên GitHub:

```bash
git add .
git commit -m "Prepare for Streamlit deployment"
git push origin main
```

## Bước 2: Triển khai trên Streamlit Cloud

1. Truy cập: https://share.streamlit.io
2. Đăng nhập bằng tài khoản GitHub
3. Click "New app"
4. Chọn repository: `duytan1412/duytan`
5. Chọn branch: `main` (hoặc branch bạn đang dùng)
6. Chọn file chính: `linguapro-ai-tutor/app.py`

## Bước 3: Cấu hình Secrets (QUAN TRỌNG!)

Trong phần "Advanced settings" > "Secrets", thêm nội dung sau:

```toml
GOOGLE_API_KEY = "AIzaSyAIzaSyCfKMPBLCrfFqjZ6Q4tsDWHpb101pubj2oO"
OPENAI_API_KEY = "sk-proj-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"
```

**Lưu ý**: 
- Không bao giờ commit file .env lên GitHub
- Secrets trên Streamlit Cloud được mã hóa an toàn
- Bạn có thể cập nhật secrets bất cứ lúc nào từ dashboard

## Bước 4: Deploy

Click "Deploy!" và đợi vài phút để ứng dụng khởi động.

## Cập nhật Ứng dụng

Mỗi khi bạn push code mới lên GitHub, Streamlit Cloud sẽ tự động deploy lại ứng dụng.

## Xử lý Lỗi

Nếu gặp lỗi:
1. Kiểm tra logs trong Streamlit Cloud dashboard
2. Đảm bảo requirements.txt có đầy đủ dependencies
3. Kiểm tra secrets đã được cấu hình đúng
4. Restart app từ dashboard nếu cần
