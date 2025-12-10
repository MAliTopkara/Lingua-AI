"""
🏆 Liderlik Tablosu Sayfası
Puan sıralaması ve rozetler
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Liderlik - Lingua-AI",
    page_icon="🏆",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Imports (sadece giriş yapılmışsa)
from components.badges import (
    render_badges_grid, 
    render_badge_showcase, 
    render_user_profile_card,
    render_leaderboard_row,
    get_badge_styles
)
from services.firebase_service import get_leaderboard
from utils.constants import LEADERBOARD_PERIODS, BADGES
from utils.helpers import init_session_state

# Session state başlat
init_session_state()

user = auth.get_current_user()

# CSS
st.markdown(get_badge_styles(), unsafe_allow_html=True)

# Ana içerik
st.title("🏆 Liderlik Tablosu")
st.markdown("En aktif kullanıcılar ve rozetler")

st.markdown("---")

# Kullanıcı profili
with st.expander("👤 Profilim", expanded=True):
    render_user_profile_card(user)
    
    st.markdown("---")
    
    st.subheader("🏅 Rozetlerim")
    render_badge_showcase(user.get("badges", []))

st.markdown("---")

# Liderlik tablosu
st.subheader("📊 Sıralama")

# Dönem seçimi
period_cols = st.columns(len(LEADERBOARD_PERIODS))
selected_period = "all_time"

for i, (period_key, period_info) in enumerate(LEADERBOARD_PERIODS.items()):
    with period_cols[i]:
        if st.button(period_info["name"], use_container_width=True, type="primary" if period_key == "all_time" else "secondary"):
            selected_period = period_key

# Liderlik tablosu
st.markdown("---")

leaders = get_leaderboard(period=selected_period, limit=20)

if not leaders:
    st.info("📭 Henüz liderlik tablosunda kimse yok. İlk siz olun!")
else:
    # Tablo başlıkları
    header_cols = st.columns([0.5, 0.5, 3, 1.5, 1.5, 1])
    
    with header_cols[0]:
        st.markdown("**#**")
    with header_cols[1]:
        st.markdown("")
    with header_cols[2]:
        st.markdown("**Kullanıcı**")
    with header_cols[3]:
        st.markdown("**Puan**")
    with header_cols[4]:
        st.markdown("**Streak**")
    with header_cols[5]:
        st.markdown("**Rozetler**")
    
    st.markdown("---")
    
    # Kullanıcı listesi
    current_user_id = user.get("id") if user else None
    
    for rank, leader in enumerate(leaders, 1):
        is_current = leader.get("id") == current_user_id
        render_leaderboard_row(rank, leader, is_current)
        
        if rank < len(leaders):
            st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)

# Rozet koleksiyonu
st.markdown("---")
st.subheader("🏅 Tüm Rozetler")

st.markdown("Kazanabileceğiniz tüm rozetler:")

# Rozet kategorileri
badge_categories = {
    "contribution": {"name": "Katkı Rozetleri", "icon": "✍️"},
    "learning": {"name": "Öğrenme Rozetleri", "icon": "📚"},
    "streak": {"name": "Streak Rozetleri", "icon": "🔥"},
    "quiz": {"name": "Quiz Rozetleri", "icon": "🎯"}
}

for cat_key, cat_info in badge_categories.items():
    with st.expander(f"{cat_info['icon']} {cat_info['name']}", expanded=False):
        cat_badges = {k: v for k, v in BADGES.items() if v.get("type") == cat_key}
        
        cols = st.columns(len(cat_badges))
        
        for i, (badge_id, badge) in enumerate(cat_badges.items()):
            with cols[i]:
                # Kullanıcının bu rozeti var mı kontrol et
                has_badge = False
                if auth.is_authenticated():
                    user_badges = auth.get_current_user().get("badges", [])
                    has_badge = badge_id in user_badges
                
                bg_style = "background: rgba(102, 126, 234, 0.2);" if has_badge else "background: rgba(255,255,255,0.05); opacity: 0.6;"
                
                st.markdown(f"""
                <div style="{bg_style} border-radius: 12px; padding: 20px; text-align: center;">
                    <div style="font-size: 40px;">{badge.get('emoji', '🏅')}</div>
                    <div style="font-weight: 600; margin-top: 8px;">{badge.get('name', '')}</div>
                    <div style="font-size: 12px; color: #a0aec0; margin-top: 4px;">{badge.get('description', '')}</div>
                    <div style="font-size: 11px; color: #667eea; margin-top: 8px;">{badge.get('condition', '')}</div>
                </div>
                """, unsafe_allow_html=True)

# İstatistikler
st.markdown("---")
st.subheader("📈 Genel İstatistikler")

from services.firebase_service import get_app_stats

stats = get_app_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 16px; text-align: center;">
        <div style="font-size: 36px; font-weight: bold; color: white;">{}</div>
        <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 5px;">Toplam Kelime</div>
    </div>
    """.format(stats.get("total_words", 0)), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 16px; text-align: center;">
        <div style="font-size: 36px; font-weight: bold; color: white;">{}</div>
        <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 5px;">Kullanıcı</div>
    </div>
    """.format(stats.get("total_users", 0)), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; border-radius: 16px; text-align: center;">
        <div style="font-size: 36px; font-weight: bold; color: white;">{}</div>
        <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 5px;">Quiz Çözüldü</div>
    </div>
    """.format(stats.get("total_quizzes", 0)), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 25px; border-radius: 16px; text-align: center;">
        <div style="font-size: 36px; font-weight: bold; color: white;">{}</div>
        <div style="font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 5px;">Bekleyen Kelime</div>
    </div>
    """.format(stats.get("pending_words", 0)), unsafe_allow_html=True)
