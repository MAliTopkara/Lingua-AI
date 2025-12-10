"""
Lingua-AI - İngilizce Sınav Hazırlık Uygulaması
Ana uygulama dosyası
"""

import streamlit as st

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="Lingua-AI - İngilizce Sınav Hazırlık",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Lingua-AI - YDS, YÖKDİL, TOEFL, IELTS sınavlarına hazırlık uygulaması"
    }
)

# Auth check - Login Gate (giriş yoksa burada durur)
import components.auth as auth
auth.check_auth()

# Imports (sadece giriş yapılmışsa buraya gelir)
from services.firebase_service import get_app_stats, get_words
from utils.helpers import init_session_state, create_word_card_css
from utils.constants import UI, EXAM_TYPES

# Session state başlat
init_session_state()

# İlk çalıştırmada başlangıç kelimelerini yükle
if "initial_words_loaded" not in st.session_state:
    st.session_state.initial_words_loaded = True
    from services.firebase_service import initialize_words_from_json, get_words
    
    # Kelime var mı kontrol et
    existing_words = get_words(status="approved", limit=1)
    if not existing_words:
        # Kelime yoksa JSON'dan yükle
        import os
        json_path = os.path.join(os.path.dirname(__file__), "data", "initial_words.json")
        if os.path.exists(json_path):
            loaded_count = initialize_words_from_json(json_path)
            if loaded_count > 0:
                st.toast(f"✅ {loaded_count} başlangıç kelimesi yüklendi!", icon="📚")

# Custom CSS
st.markdown("""
<style>
/* Ana tema */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.main-title {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 10px;
}

.main-subtitle {
    font-size: 18px;
    opacity: 0.9;
}

/* Feature kartları */
.feature-card {
    background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 16px;
    padding: 25px;
    height: 100%;
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: #667eea;
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 40px;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 20px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 10px;
}

.feature-desc {
    font-size: 14px;
    color: #a0aec0;
    line-height: 1.5;
}

/* Stats */
.stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    color: white;
}

.stat-value {
    font-size: 36px;
    font-weight: 700;
}

.stat-label {
    font-size: 14px;
    opacity: 0.9;
    margin-top: 5px;
}

/* CTA Button */
.cta-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 40px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 600;
    text-decoration: none;
    display: inline-block;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.cta-button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

/* Exam badges */
.exam-badges {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.exam-badge {
    background: rgba(102, 126, 234, 0.2);
    padding: 10px 20px;
    border-radius: 25px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown("""
<div class="main-header">
    <div class="main-title">🎓 Lingua-AI</div>
    <div class="main-subtitle">Yapay Zeka Destekli İngilizce Sınav Hazırlık Platformu</div>
    <div class="exam-badges">
        <span class="exam-badge">🇹🇷 YDS</span>
        <span class="exam-badge">🎓 YÖKDİL</span>
        <span class="exam-badge">🌍 TOEFL</span>
        <span class="exam-badge">🇬🇧 IELTS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Hoş geldin mesajı
user = auth.get_current_user()
if user:
    st.success(f"👋 Hoş geldin, **{user.get('displayName', 'Kullanıcı')}**! Bugün de çalışmaya hazır mısın?")

st.markdown("---")

# İstatistikler
st.subheader("📊 Platform İstatistikleri")

stats = get_app_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{stats.get('total_words', 0)}</div>
        <div class="stat-label">📚 Kelime</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <div class="stat-value">{stats.get('total_users', 0)}</div>
        <div class="stat-label">👥 Kullanıcı</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <div class="stat-value">{stats.get('total_quizzes', 0)}</div>
        <div class="stat-label">🎯 Quiz</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <div class="stat-value">{stats.get('pending_words', 0)}</div>
        <div class="stat-label">⏳ Bekleyen</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Özellikler
st.subheader("✨ Özellikler")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Kelime Kartları</div>
        <div class="feature-desc">
            Binlerce YDS, YÖKDİL, TOEFL ve IELTS kelimesini öğrenin. 
            AI ile örnek cümleler oluşturun.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Quiz & Test</div>
        <div class="feature-desc">
            Bilginizi test edin. Çoktan seçmeli sorularla pratik yapın.
            Yanlışlarınızı takip edin.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏆</div>
        <div class="feature-title">Liderlik & Rozetler</div>
        <div class="feature-desc">
            Puan kazanın, rozetler toplayın. Arkadaşlarınızla yarışın.
            Streak'inizi koruyun.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Destekli</div>
        <div class="feature-desc">
            Yapay zeka ile örnek cümleler oluşturun.
            Akılda kalıcı hafıza teknikleri alın.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Topluluk Katkısı</div>
        <div class="feature-desc">
            Kelimeler ve trick'ler ekleyerek katkıda bulunun.
            Diğer kullanıcılara yardımcı olun.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Trick & İpuçları</div>
        <div class="feature-desc">
            Gramer kuralları, strateji ipuçları ve 
            sınav taktikleri keşfedin.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Hızlı başlangıç
st.subheader("🚀 Hızlı Başlangıç")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📚 Kelimelere Göz At", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📚_Kelime_Kartlari.py")

with col2:
    if st.button("🎯 Quiz Çöz", use_container_width=True):
        st.switch_page("pages/3_🎯_Quiz.py")

with col3:
    if st.button("🏆 Liderlik Tablosu", use_container_width=True):
        st.switch_page("pages/4_🏆_Liderlik.py")

# Günün kelimesi
st.markdown("---")
st.subheader("📅 Günün Kelimesi")

import random
from datetime import date

words = get_words(status="approved", limit=100)

if words:
    # Her gün aynı kelime için seed kullan
    today_seed = int(date.today().strftime("%Y%m%d"))
    random.seed(today_seed)
    word_of_day = random.choice(words)
    random.seed()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 20px; padding: 30px; color: white; text-align: center;">
        <div style="font-size: 36px; font-weight: bold; margin-bottom: 10px;">{word_of_day.get('english', '')}</div>
        <div style="font-size: 20px; opacity: 0.9;">{word_of_day.get('turkish', '')}</div>
        <div style="margin-top: 15px; font-size: 14px; opacity: 0.8;">
            {'⭐' * word_of_day.get('difficulty', 3)} | {word_of_day.get('type', 'noun')}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Henüz kelime eklenmemiş. İlk kelimeyi siz ekleyin!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; font-size: 14px;">
    <p>🎓 Lingua-AI - Yapay Zeka Destekli İngilizce Sınav Hazırlık Platformu</p>
    <p>© 2025 - Tamamen Ücretsiz | Streamlit + Firebase + Groq AI</p>
</div>
""", unsafe_allow_html=True)
