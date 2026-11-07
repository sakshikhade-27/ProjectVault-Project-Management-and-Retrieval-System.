import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Change this before using the app on a shared machine
SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")

DATABASE = os.path.join(BASE_DIR, "database", "projectvault.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB per upload

ALLOWED_EXTENSIONS = {
    "zip", "rar", "7z", "pdf", "doc", "docx", "ppt", "pptx",
    "xls", "xlsx", "txt", "py", "java", "c", "cpp", "png", "jpg", "jpeg",
}
