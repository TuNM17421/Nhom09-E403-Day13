from __future__ import annotations

import hashlib
import re

PII_PATTERNS: dict[str, str] = {
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "phone_vn": r"(?:\+84|0)[ \.-]?\d{3}[ \.-]?\d{3}[ \.-]?\d{3,4}",
    "cccd": r"\b\d{12}\b",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "passport": r"\b[A-Z]\d{7,8}\b", # Định dạng hộ chiếu Việt Nam (1 chữ cái + 7 hoặc 8 số)
    "address_vn": r"(?i)\b(số|đường|phường|quận|huyện|thành phố|tỉnh|thôn|xóm|ấp|số nhà)\b.*?\d+", # Nhận diện từ khóa địa chỉ đi kèm số
}


def scrub_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    safe = text
    for name, pattern in PII_PATTERNS.items():
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def summarize_text(text: str, max_len: int = 80) -> str:
    # Scrub PII trước khi summarize để đảm bảo an toàn
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_user_id(user_id: str) -> str:
    if not user_id:
        return "anonymous"
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12]
