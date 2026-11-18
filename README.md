# BioAttend Backend

API của BioAttend, viết bằng FastAPI, SQLAlchemy và MySQL.

Sau khi pull code, làm lần lượt các bước dưới đây trong thư mục `backend`.

## Yêu cầu

- Python 3.12
- MySQL 8 (hoặc MariaDB tương thích), đang chạy trên máy

## 1. Tạo database

Mở MySQL và tạo database (bảng sẽ được tạo tự động khi server khởi động):

```sql
CREATE DATABASE BioAttend CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Tạo file `.env`

File `.env` không được đẩy lên git. Tạo file `backend/.env` với nội dung:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=mat_khau_mysql
DB_NAME=BioAttend
```

Đổi `DB_USER` và `DB_PASSWORD` cho đúng tài khoản MySQL trên máy bạn.

## 3. Tạo môi trường ảo và cài thư viện

Mở terminal tại thư mục `backend`.

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Nếu PowerShell chặn script activate, chạy một lần:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## 4. Chạy server

Vẫn đứng trong thư mục `backend`, với virtualenv đã bật:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Khi chạy, ứng dụng kết nối MySQL và tạo các bảng còn thiếu (hiện có bảng `faculties`).

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

Ví dụ endpoint hiện có:

```text
GET http://127.0.0.1:8000/api/v1/university/faculty/
```

Dừng server bằng `Ctrl + C`.

## 5. (Tuỳ chọn) Nạp dữ liệu khoa

Chỉ chạy khi bảng `faculties` còn trống. Seeder chèn sẵn 10 khoa; chạy lại khi đã có dữ liệu sẽ lỗi trùng mã khoa.

```powershell
python -m app.seeders
```

Thành công khi terminal in `Seed faculties successfully!`.

## Lỗi thường gặp

- **Không kết nối được MySQL:** kiểm tra MySQL đang chạy, và `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` trong `.env`.
- **`Unknown database 'BioAttend'`:** chưa tạo database ở bước 1.
- **`ModuleNotFoundError: No module named 'app'`:** lệnh uvicorn hoặc seeder phải chạy từ thư mục `backend`, không phải từ thư mục gốc của repo.
- **`ModuleNotFoundError` với fastapi / uvicorn / dotenv:** chưa activate virtualenv, hoặc chưa chạy `pip install -r requirements.txt`.
