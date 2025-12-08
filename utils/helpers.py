"""
Lingua-AI Helper Functions
Tarih formatlama, streak hesaplama, session yönetimi
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List


def format_date(date_value, format_type: str = "full") -> str:
    """
    Tarihi Türkçe formatında göster
    
    Args:
        date_value: datetime object veya timestamp
        format_type: "full", "short", "relative"
    """
    if date_value is None:
        return "Bilinmiyor"
    
    # Firestore Timestamp'ı datetime'a çevir
    if hasattr(date_value, 'seconds'):
        date_value = datetime.fromtimestamp(date_value.seconds)
    elif isinstance(date_value, str):
        try:
            date_value = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
        except:
            return date_value
    
    # Timezone-aware ise naive'e çevir (karşılaştırma için)
    if hasattr(date_value, 'tzinfo') and date_value.tzinfo is not None:
        date_value = date_value.replace(tzinfo=None)
    
    turkish_months = [
        "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ]
    
    if format_type == "full":
        return f"{date_value.day} {turkish_months[date_value.month - 1]} {date_value.year}"
    elif format_type == "short":
        return f"{date_value.day} {turkish_months[date_value.month - 1][:3]}"
    elif format_type == "relative":
        now = datetime.now()
        diff = now - date_value
        
        if diff.days == 0:
            if diff.seconds < 60:
                return "Az önce"
            elif diff.seconds < 3600:
                return f"{diff.seconds // 60} dakika önce"
            else:
                return f"{diff.seconds // 3600} saat önce"
        elif diff.days == 1:
            return "Dün"
        elif diff.days < 7:
            return f"{diff.days} gün önce"
        elif diff.days < 30:
            return f"{diff.days // 7} hafta önce"
        else:
            return format_date(date_value, "full")
    
    return str(date_value)


def calculate_streak(last_active_date: Optional[str], current_streak: int) -> tuple[int, bool]:
    """
    Streak hesapla ve güncelle
    
    Returns:
        (new_streak, is_new_day): Yeni streak değeri ve bugün ilk giriş mi
    """
    today = datetime.now().date()
    
    if last_active_date is None:
        return 1, True
    
    try:
        if isinstance(last_active_date, str):
            last_date = datetime.fromisoformat(last_active_date).date()
        elif hasattr(last_active_date, 'seconds'):
            last_date = datetime.fromtimestamp(last_active_date.seconds).date()
        else:
            last_date = last_active_date
    except:
        return 1, True
    
    diff = (today - last_date).days
    
    if diff == 0:
        # Bugün zaten giriş yapmış
        return current_streak, False
    elif diff == 1:
        # Dün giriş yapmış, streak devam
        return current_streak + 1, True
    else:
        # Streak kırıldı
        return 1, True


def calculate_quiz_score(correct: int, total: int) -> Dict[str, Any]:
    """
    Quiz skorunu hesapla
    
    Returns:
        Dict with percentage, grade, points
    """
    from utils.constants import POINTS
    
    percentage = (correct / total * 100) if total > 0 else 0
    
    if percentage == 100:
        grade = "Mükemmel! 🏆"
        points = POINTS["quiz_complete"] + POINTS["quiz_perfect"]
    elif percentage >= 90:
        grade = "Harika! 🎯"
        points = POINTS["quiz_complete"] + POINTS["quiz_high_score"]
    elif percentage >= 70:
        grade = "İyi! 👍"
        points = POINTS["quiz_complete"] + 5
    elif percentage >= 50:
        grade = "Fena Değil 📚"
        points = POINTS["quiz_complete"]
    else:
        grade = "Tekrar Çalış 💪"
        points = POINTS["quiz_complete"] // 2
    
    return {
        "correct": correct,
        "total": total,
        "percentage": round(percentage, 1),
        "grade": grade,
        "points": points
    }


def init_session_state():
    """Session state değişkenlerini başlat"""
    defaults = {
        "user": None,
        "is_authenticated": False,
        "is_admin": False,
        "current_word_index": 0,
        "quiz_questions": [],
        "quiz_answers": [],
        "quiz_current": 0,
        "quiz_score": 0,
        "filter_exam_type": "all",
        "filter_difficulty": "all",
        "search_query": "",
        "words_cache": None,
        "words_cache_time": None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_user() -> Optional[Dict[str, Any]]:
    """Oturum açmış kullanıcıyı döndür"""
    return st.session_state.get("user")


def is_authenticated() -> bool:
    """Kullanıcı oturum açmış mı kontrol et"""
    return st.session_state.get("is_authenticated", False)


def is_admin() -> bool:
    """Kullanıcı admin mi kontrol et"""
    return st.session_state.get("is_admin", False)


def require_auth(message: str = "Bu özelliği kullanmak için giriş yapmalısınız."):
    """
    Oturum açma gerektiren sayfalar için kontrol
    Returns True if authenticated, shows warning and returns False otherwise
    """
    if not is_authenticated():
        st.warning(f"⚠️ {message}")
        st.info("👆 Sol menüden 'Giriş Yap' butonuna tıklayarak Google hesabınızla giriş yapabilirsiniz.")
        return False
    return True


def require_admin():
    """
    Admin gerektiren sayfalar için kontrol
    Returns True if admin, shows error and returns False otherwise
    """
    if not is_authenticated():
        st.error("🔒 Bu sayfa için giriş yapmalısınız.")
        return False
    if not is_admin():
        st.error("🚫 Bu sayfaya erişim yetkiniz yok.")
        return False
    return True


def truncate_text(text: str, max_length: int = 100) -> str:
    """Metni belirtilen uzunlukta kes"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_difficulty_stars(difficulty: int) -> str:
    """Zorluk seviyesine göre yıldız döndür"""
    return "⭐" * difficulty + "☆" * (5 - difficulty)


def get_exam_type_badges(exam_types: List[str]) -> str:
    """Sınav türlerini badge olarak göster"""
    from utils.constants import EXAM_TYPES
    
    badges = []
    for exam_type in exam_types:
        if exam_type in EXAM_TYPES:
            info = EXAM_TYPES[exam_type]
            badges.append(f"{info['icon']} {info['name']}")
    
    return " | ".join(badges) if badges else "Genel"


def sanitize_input(text: str) -> str:
    """Kullanıcı girdisini temizle"""
    if not text:
        return ""
    # Temel temizlik
    text = text.strip()
    # HTML karakterlerini escape et
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


def validate_word_input(english: str, turkish: str) -> tuple[bool, str]:
    """
    Kelime girdisini doğrula
    
    Returns:
        (is_valid, error_message)
    """
    if not english or len(english.strip()) < 2:
        return False, "İngilizce kelime en az 2 karakter olmalıdır."
    
    if not turkish or len(turkish.strip()) < 2:
        return False, "Türkçe karşılık en az 2 karakter olmalıdır."
    
    if not english.replace(" ", "").replace("-", "").isalpha():
        return False, "İngilizce kelime sadece harf içermelidir."
    
    if len(english) > 50:
        return False, "İngilizce kelime çok uzun (max 50 karakter)."
    
    if len(turkish) > 200:
        return False, "Türkçe karşılık çok uzun (max 200 karakter)."
    
    return True, ""


def format_number(num: int) -> str:
    """Sayıyı okunabilir formatta göster"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    return str(num)


def get_level_from_points(points: int) -> Dict[str, Any]:
    """Puana göre seviye hesapla"""
    levels = [
        {"level": 1, "name": "Başlangıç", "min": 0, "max": 50, "icon": "🌱"},
        {"level": 2, "name": "Acemi", "min": 50, "max": 150, "icon": "🌿"},
        {"level": 3, "name": "Öğrenci", "min": 150, "max": 300, "icon": "📖"},
        {"level": 4, "name": "Çalışkan", "min": 300, "max": 500, "icon": "📚"},
        {"level": 5, "name": "Azimli", "min": 500, "max": 800, "icon": "🎯"},
        {"level": 6, "name": "Bilgili", "min": 800, "max": 1200, "icon": "🧠"},
        {"level": 7, "name": "Uzman", "min": 1200, "max": 2000, "icon": "🎓"},
        {"level": 8, "name": "Usta", "min": 2000, "max": 3500, "icon": "👨‍🏫"},
        {"level": 9, "name": "Efsane", "min": 3500, "max": 5000, "icon": "🏆"},
        {"level": 10, "name": "Dahi", "min": 5000, "max": float('inf'), "icon": "💎"}
    ]
    
    for level in levels:
        if level["min"] <= points < level["max"]:
            progress = (points - level["min"]) / (level["max"] - level["min"]) * 100
            return {
                **level,
                "progress": min(progress, 100),
                "points_to_next": level["max"] - points
            }
    
    return levels[-1]


def create_word_card_css():
    """Kelime kartı için CSS stilleri"""
    return """
    <style>
    .word-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .word-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4);
    }
    .word-english {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .word-turkish {
        font-size: 18px;
        opacity: 0.9;
        margin-bottom: 16px;
    }
    .word-meta {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        font-size: 14px;
        opacity: 0.8;
    }
    .badge {
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    .quiz-option {
        background: #1a1f2e;
        border: 2px solid #667eea;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .quiz-option:hover {
        background: #667eea;
        transform: scale(1.02);
    }
    .quiz-option.correct {
        background: #27ae60;
        border-color: #27ae60;
    }
    .quiz-option.wrong {
        background: #e74c3c;
        border-color: #e74c3c;
    }
    .stats-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stats-number {
        font-size: 32px;
        font-weight: bold;
        color: #667eea;
    }
    .stats-label {
        font-size: 14px;
        color: #a0aec0;
        margin-top: 4px;
    }
    </style>
    """
