"""
Lingua-AI Constants
Rozet tanımları, sınav türleri, kelime türleri ve puan sistemi
"""

# Sınav Türleri
EXAM_TYPES = {
    "yds": {"name": "YDS", "icon": "🇹🇷", "description": "Yabancı Dil Sınavı"},
    "yokdil": {"name": "YÖKDİL", "icon": "🎓", "description": "YÖK Dil Sınavı"},
    "toefl": {"name": "TOEFL", "icon": "🌍", "description": "Test of English as a Foreign Language"},
    "ielts": {"name": "IELTS", "icon": "🇬🇧", "description": "International English Language Testing System"},
    "genel": {"name": "Genel", "icon": "📚", "description": "Genel İngilizce"}
}

# Kelime Türleri
WORD_TYPES = {
    "noun": {"name": "İsim", "abbr": "n.", "color": "#3498db"},
    "verb": {"name": "Fiil", "abbr": "v.", "color": "#e74c3c"},
    "adjective": {"name": "Sıfat", "abbr": "adj.", "color": "#2ecc71"},
    "adverb": {"name": "Zarf", "abbr": "adv.", "color": "#9b59b6"},
    "preposition": {"name": "Edat", "abbr": "prep.", "color": "#f39c12"},
    "conjunction": {"name": "Bağlaç", "abbr": "conj.", "color": "#1abc9c"},
    "pronoun": {"name": "Zamir", "abbr": "pron.", "color": "#e91e63"},
    "interjection": {"name": "Ünlem", "abbr": "interj.", "color": "#ff5722"}
}

# Trick Kategorileri
TRICK_CATEGORIES = {
    "grammar": {"name": "Gramer", "icon": "📖", "color": "#3498db"},
    "vocabulary": {"name": "Kelime", "icon": "📝", "color": "#2ecc71"},
    "strategy": {"name": "Strateji", "icon": "🎯", "color": "#e74c3c"}
}

# Zorluk Seviyeleri
DIFFICULTY_LEVELS = {
    1: {"name": "Çok Kolay", "color": "#27ae60", "icon": "🌱"},
    2: {"name": "Kolay", "color": "#2ecc71", "icon": "🌿"},
    3: {"name": "Orta", "color": "#f39c12", "icon": "🌳"},
    4: {"name": "Zor", "color": "#e67e22", "icon": "🔥"},
    5: {"name": "Çok Zor", "color": "#e74c3c", "icon": "💀"}
}

# Rozet Tanımları
BADGES = {
    "caylak": {
        "id": "caylak",
        "name": "Çaylak",
        "emoji": "🥉",
        "description": "İlk kelimeni ekledin!",
        "condition": "İlk kelime ekleme",
        "threshold": 1,
        "type": "contribution"
    },
    "katkici": {
        "id": "katkici",
        "name": "Katkıcı",
        "emoji": "🥈",
        "description": "10 kelimenin onaylandı!",
        "condition": "10 onaylanan kelime",
        "threshold": 10,
        "type": "contribution"
    },
    "uzman": {
        "id": "uzman",
        "name": "Uzman",
        "emoji": "🥇",
        "description": "50 kelimenin onaylandı!",
        "condition": "50 onaylanan kelime",
        "threshold": 50,
        "type": "contribution"
    },
    "efsane": {
        "id": "efsane",
        "name": "Efsane",
        "emoji": "💎",
        "description": "100+ kelimenin onaylandı!",
        "condition": "100+ onaylanan kelime",
        "threshold": 100,
        "type": "contribution"
    },
    "kelime_avcisi": {
        "id": "kelime_avcisi",
        "name": "Kelime Avcısı",
        "emoji": "📚",
        "description": "100 kelime öğrendin!",
        "condition": "100 kelime öğrenme",
        "threshold": 100,
        "type": "learning"
    },
    "streak_master": {
        "id": "streak_master",
        "name": "Streak Master",
        "emoji": "🎯",
        "description": "7 gün üst üste çalıştın!",
        "condition": "7 gün streak",
        "threshold": 7,
        "type": "streak"
    },
    "streak_efsanesi": {
        "id": "streak_efsanesi",
        "name": "Streak Efsanesi",
        "emoji": "🔥",
        "description": "30 gün üst üste çalıştın!",
        "condition": "30 gün streak",
        "threshold": 30,
        "type": "streak"
    },
    "quiz_sampiyonu": {
        "id": "quiz_sampiyonu",
        "name": "Quiz Şampiyonu",
        "emoji": "🏆",
        "description": "10 quiz'de %90+ başarı!",
        "condition": "10 quiz'de %90+",
        "threshold": 10,
        "type": "quiz"
    }
}

# Puan Sistemi
POINTS = {
    "word_approved": 10,      # Kelime onaylandığında
    "trick_approved": 15,     # Trick onaylandığında
    "quiz_complete": 5,       # Quiz tamamlama (base)
    "quiz_perfect": 20,       # %100 doğru quiz
    "quiz_high_score": 10,    # %90+ doğru quiz
    "daily_login": 2,         # Günlük giriş
    "streak_bonus": 5,        # Her streak günü için bonus
    "word_learned": 1         # Yeni kelime öğrenme
}

# Quiz Ayarları
QUIZ_SETTINGS = {
    "default_question_count": 10,
    "min_questions": 5,
    "max_questions": 50,
    "time_per_question": 30,  # saniye
    "options_count": 4
}

# Quiz Türleri
QUIZ_TYPES = {
    "en_to_tr": {"name": "İngilizce → Türkçe", "icon": "🔤"},
    "tr_to_en": {"name": "Türkçe → İngilizce", "icon": "🔠"},
    "sentence_completion": {"name": "Cümle Tamamlama", "icon": "📝"},
    "synonym": {"name": "Eş Anlam Bulma", "icon": "🔗"}
}

# Durum Tanımları
STATUS = {
    "pending": {"name": "Beklemede", "color": "#f39c12", "icon": "⏳"},
    "approved": {"name": "Onaylandı", "color": "#27ae60", "icon": "✅"},
    "rejected": {"name": "Reddedildi", "color": "#e74c3c", "icon": "❌"}
}

# Zaman Dilimleri (Liderlik Tablosu)
LEADERBOARD_PERIODS = {
    "weekly": {"name": "Bu Hafta", "days": 7},
    "monthly": {"name": "Bu Ay", "days": 30},
    "all_time": {"name": "Tüm Zamanlar", "days": None}
}

# UI Sabitleri
UI = {
    "page_icon": "🎓",
    "page_title": "Lingua-AI",
    "sidebar_title": "Lingua-AI 🎓",
    "footer_text": "© 2025 Lingua-AI - İngilizce Sınav Hazırlık",
    "max_cards_per_page": 12,
    "animation_duration": 0.3
}

# Groq API Ayarları
GROQ_SETTINGS = {
    "model": "llama-3.1-8b-instant",
    "max_tokens": 150,
    "temperature": 0.7
}

# Sistem Promptları
SYSTEM_PROMPTS = {
    "example_sentence": """Sen bir YDS/İngilizce sınav uzmanısın. Verilen kelimeyi kullanarak akademik ve resmi dilde, sınav formatına uygun bir İngilizce cümle oluştur.

Kurallar:
1. Cümle 15-25 kelime arasında olsun
2. Akademik/resmi dil kullan
3. Cümle bağlamdan anlaşılır olsun
4. Kelimeyi doğru gramatikal yapıda kullan

Sadece cümleyi döndür, başka açıklama ekleme.""",

    "sentence_completion": """Sen bir YDS/İngilizce sınav uzmanısın. Verilen kelimeyi kullanarak cümle tamamlama sorusu oluştur.

Format:
- Cümlenin bir kısmını boşluk (______) olarak bırak
- Doğru cevap verilen kelime olsun
- 3 yanlış şık da oluştur (benzer ama yanlış kelimeler)

JSON formatında döndür:
{
    "sentence": "The scientist had to ______ the experiment due to lack of funding.",
    "correct": "abandon",
    "options": ["abandon", "enhance", "pursue", "maintain"]
}"""
}
