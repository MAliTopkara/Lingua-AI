"""
Authentication Component
Google Sign-In simulation and user management for Streamlit
"""

import streamlit as st
from typing import Optional, Dict, Any
import hashlib
import time


def init_auth():
    """Auth session state'lerini başlat"""
    if "user" not in st.session_state:
        st.session_state.user = None
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False


def get_current_user() -> Optional[Dict[str, Any]]:
    """Oturum açmış kullanıcıyı döndür"""
    return st.session_state.get("user")


def is_logged_in() -> bool:
    """Kullanıcı giriş yapmış mı?"""
    return st.session_state.get("is_authenticated", False)


def is_admin() -> bool:
    """Kullanıcı admin mi?"""
    return st.session_state.get("is_admin", False)


def simulate_google_login(email: str, name: str) -> Dict[str, Any]:
    """
    Google Sign-In simülasyonu
    Not: Gerçek uygulamada OAuth 2.0 kullanılmalı
    """
    # Benzersiz kullanıcı ID oluştur
    user_id = hashlib.md5(email.encode()).hexdigest()[:20]
    
    user_data = {
        "id": user_id,
        "email": email,
        "displayName": name,
        "photoURL": f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=667eea&color=fff",
    }
    
    return user_data


def login_user(user_data: Dict[str, Any]) -> bool:
    """Kullanıcıyı oturuma al"""
    from services.firebase_service import create_or_update_user, get_user, is_user_admin
    from services.gamification_service import update_user_streak
    
    try:
        # Firebase'e kaydet/güncelle
        success = create_or_update_user(user_data["id"], user_data)
        
        if success:
            # Kullanıcı bilgilerini al
            db_user = get_user(user_data["id"])
            if db_user:
                user_data = {**user_data, **db_user}
            
            # Session'a kaydet
            st.session_state.user = user_data
            st.session_state.is_authenticated = True
            st.session_state.is_admin = is_user_admin(user_data.get("email", ""))
            
            # Streak güncelle
            update_user_streak(user_data["id"])
            
            return True
    except Exception as e:
        st.error(f"Giriş hatası: {str(e)}")
    
    return False


def logout_user():
    """Kullanıcı çıkışı"""
    st.session_state.user = None
    st.session_state.is_authenticated = False
    st.session_state.is_admin = False


def render_login_button():
    """Google giriş butonu göster"""
    init_auth()
    
    if is_logged_in():
        return
    
    st.markdown("""
    <style>
    .google-btn {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: white;
        color: #333;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 500;
        text-decoration: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .google-btn:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Demo login formu
    with st.expander("🔐 Giriş Yap", expanded=False):
        st.markdown("#### Google ile Giriş Simülasyonu")
        st.caption("Not: Bu demo moddur. Gerçek uygulamada OAuth 2.0 kullanılır.")
        
        with st.form("login_form"):
            email = st.text_input("E-posta", placeholder="ornek@gmail.com")
            name = st.text_input("İsim", placeholder="Ad Soyad")
            
            submitted = st.form_submit_button("🚀 Giriş Yap", use_container_width=True)
            
            if submitted:
                if email and name:
                    if "@" in email and "." in email.split("@")[1]:
                        user_data = simulate_google_login(email, name)
                        if login_user(user_data):
                            st.success("✅ Giriş başarılı!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Giriş yapılamadı. Lütfen tekrar deneyin.")
                    else:
                        st.error("Geçerli bir e-posta adresi girin.")
                else:
                    st.error("Tüm alanları doldurun.")


def render_user_sidebar():
    """Sidebar'da kullanıcı bilgilerini göster"""
    init_auth()
    
    st.sidebar.markdown("---")
    
    if is_logged_in():
        user = get_current_user()
        
        # Kullanıcı kartı
        col1, col2 = st.sidebar.columns([1, 3])
        
        with col1:
            st.image(user.get("photoURL", ""), width=50)
        
        with col2:
            st.markdown(f"**{user.get('displayName', 'Kullanıcı')}**")
            role = "👑 Admin" if is_admin() else "👤 Kullanıcı"
            st.caption(role)
        
        # İstatistikler
        st.sidebar.markdown("---")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("🔥 Streak", user.get("currentStreak", 0))
        with col2:
            st.metric("⭐ Puan", user.get("points", 0))
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("📚 Öğrenilen", user.get("wordsLearned", 0))
        with col2:
            st.metric("✍️ Eklenen", user.get("wordsContributed", 0))
        
        # Rozetler
        badges = user.get("badges", [])
        if badges:
            from utils.constants import BADGES
            badge_emojis = " ".join([BADGES.get(b, {}).get("emoji", "") for b in badges])
            st.sidebar.markdown(f"**Rozetler:** {badge_emojis}")
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 Çıkış Yap", use_container_width=True):
            logout_user()
            st.rerun()
    else:
        st.sidebar.info("👋 Hoş geldiniz! Tüm özellikleri kullanmak için giriş yapın.")
        render_login_button()


def require_auth(redirect_message: str = "Bu özelliği kullanmak için giriş yapmalısınız.") -> bool:
    """
    Sayfa için auth kontrolü
    
    Returns:
        True if authenticated, False otherwise (also shows message)
    """
    init_auth()
    
    if not is_logged_in():
        st.warning(f"⚠️ {redirect_message}")
        st.markdown("---")
        render_login_button()
        return False
    
    return True


def require_admin() -> bool:
    """
    Admin sayfaları için kontrol
    
    Returns:
        True if admin, False otherwise
    """
    if not require_auth("Admin paneline erişmek için giriş yapmalısınız."):
        return False
    
    if not is_admin():
        st.error("🚫 Bu sayfaya erişim yetkiniz yok.")
        st.info("Bu sayfa sadece admin kullanıcılar içindir.")
        return False
    
    return True


def get_user_display_name() -> str:
    """Kullanıcı adını döndür"""
    user = get_current_user()
    if user:
        return user.get("displayName", "Kullanıcı")
    return "Misafir"


def refresh_user_data():
    """Kullanıcı verilerini yenile"""
    if not is_logged_in():
        return
    
    from services.firebase_service import get_user
    
    user = get_current_user()
    if user and user.get("id"):
        db_user = get_user(user["id"])
        if db_user:
            st.session_state.user = {**user, **db_user}
