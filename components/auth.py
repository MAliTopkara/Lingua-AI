"""
Authentication Component
Simple Firebase Email/Password Login Gate Pattern
"""

import streamlit as st
from typing import Optional, Dict, Any
import hashlib
import time


def _init_auth_state():
    """Auth session state'lerini başlat"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False


def _render_login_form():
    """Şık login/register formu render et"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .login-title {
        font-size: 32px;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .login-subtitle {
        color: #a0aec0;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Ortalanmış container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-header">
            <div class="login-title">🎓 Lingua-AI</div>
            <div class="login-subtitle">İngilizce Sınav Hazırlık Platformu</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sekmeler
        tab_login, tab_register = st.tabs(["🔐 Giriş Yap", "📝 Kayıt Ol"])
        
        # ============ GİRİŞ YAP SEKMESİ ============
        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("##### Hesabınıza giriş yapın")
                
                login_email = st.text_input(
                    "📧 E-posta",
                    placeholder="ornek@gmail.com",
                    key="login_email"
                )
                
                login_password = st.text_input(
                    "🔒 Şifre",
                    type="password",
                    placeholder="••••••••",
                    key="login_password"
                )
                
                st.markdown("")
                
                login_submitted = st.form_submit_button(
                    "🚀 Giriş Yap",
                    use_container_width=True,
                    type="primary"
                )
                
                if login_submitted:
                    if _process_login(login_email, login_password):
                        st.rerun()
        
        # ============ KAYIT OL SEKMESİ ============
        with tab_register:
            with st.form("register_form", clear_on_submit=False):
                st.markdown("##### Yeni hesap oluşturun")
                
                reg_name = st.text_input(
                    "👤 Ad Soyad",
                    placeholder="Ad Soyad",
                    key="reg_name"
                )
                
                reg_email = st.text_input(
                    "📧 E-posta",
                    placeholder="ornek@gmail.com",
                    key="reg_email"
                )
                
                reg_password = st.text_input(
                    "🔒 Şifre",
                    type="password",
                    placeholder="En az 6 karakter",
                    key="reg_password"
                )
                
                reg_password2 = st.text_input(
                    "🔒 Şifre Tekrar",
                    type="password",
                    placeholder="Şifreyi tekrar girin",
                    key="reg_password2"
                )
                
                st.markdown("")
                
                reg_submitted = st.form_submit_button(
                    "📝 Kayıt Ol",
                    use_container_width=True,
                    type="primary"
                )
                
                if reg_submitted:
                    _process_register(reg_name, reg_email, reg_password, reg_password2)
        
        st.markdown("---")
        st.caption("🔒 Şifreniz güvenli şekilde şifrelenerek saklanır.")


def _process_login(email: str, password: str) -> bool:
    """Login işlemini gerçekleştir"""
    from services.firebase_service import authenticate_user, is_user_admin
    from services.gamification_service import update_user_streak
    
    # Validasyon
    if not email or not password:
        st.error("❌ E-posta ve şifre gereklidir.")
        return False
    
    email = email.strip().lower()
    
    if "@" not in email or "." not in email.split("@")[-1]:
        st.error("❌ Geçerli bir e-posta adresi girin.")
        return False
    
    # Firebase ile doğrula
    result = authenticate_user(email, password)
    
    if not result["success"]:
        st.error(f"❌ {result['error']}")
        return False
    
    user_data = result["user"]
    
    # Session'a kaydet
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.is_admin = is_user_admin(email)
    
    # Streak güncelle
    try:
        update_user_streak(user_data["id"])
    except:
        pass
    
    st.success("✅ Giriş başarılı!")
    time.sleep(0.3)
    return True


def _process_register(name: str, email: str, password: str, password2: str) -> bool:
    """Kayıt işlemini gerçekleştir"""
    from services.firebase_service import signup_user
    
    # Validasyon
    if not name or not email or not password or not password2:
        st.error("❌ Tüm alanları doldurun.")
        return False
    
    name = name.strip()
    email = email.strip().lower()
    
    if len(name) < 2:
        st.error("❌ İsim en az 2 karakter olmalı.")
        return False
    
    if "@" not in email or "." not in email.split("@")[-1]:
        st.error("❌ Geçerli bir e-posta adresi girin.")
        return False
    
    if len(password) < 6:
        st.error("❌ Şifre en az 6 karakter olmalı.")
        return False
    
    if password != password2:
        st.error("❌ Şifreler eşleşmiyor.")
        return False
    
    # Firebase'e kaydet
    result = signup_user(email, password, name)
    
    if not result["success"]:
        st.error(f"❌ {result['error']}")
        return False
    
    st.success("✅ Kayıt başarılı! Şimdi 'Giriş Yap' sekmesinden giriş yapabilirsiniz.")
    st.balloons()
    return True


def _render_user_sidebar():
    """Sidebar'da kullanıcı bilgilerini göster"""
    user = st.session_state.get("user", {})
    
    st.sidebar.markdown("---")
    
    # Kullanıcı kartı
    col1, col2 = st.sidebar.columns([1, 3])
    
    with col1:
        photo_url = user.get("photoURL", "")
        if photo_url:
            st.image(photo_url, width=50)
    
    with col2:
        st.markdown(f"**{user.get('displayName', 'Kullanıcı')}**")
        role = "👑 Admin" if st.session_state.get("is_admin") else "👤 Kullanıcı"
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
        if badge_emojis.strip():
            st.sidebar.markdown(f"**Rozetler:** {badge_emojis}")
    
    st.sidebar.markdown("---")
    
    # Çıkış butonu
    if st.sidebar.button("🚪 Çıkış Yap", use_container_width=True):
        logout()
        st.rerun()


# Public alias for backward compatibility
def render_user_sidebar(key: str = None):
    """
    Sidebar'da kullanıcı bilgilerini göster (public alias)
    Eski kodlarla uyumluluk için
    """
    _render_user_sidebar()


def logout():
    """Kullanıcı çıkışı - session temizle"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.is_admin = False


def check_auth(require_login: bool = True) -> bool:
    """
    Ana authentication kontrolü - Login Gate Pattern
    
    Her sayfanın en başında çağrılmalı:
        import components.auth as auth
        auth.check_auth()
    
    Args:
        require_login: True ise giriş zorunlu, False ise opsiyonel
    
    Returns:
        True: Kullanıcı giriş yapmış
        False: Kullanıcı giriş yapmamış (require_login=False ise)
    
    Not: require_login=True ise ve kullanıcı giriş yapmamışsa,
         login formu gösterilir ve st.stop() çağrılır.
    """
    _init_auth_state()
    
    # DURUM A: Kullanıcı giriş yapmış
    if st.session_state.authenticated:
        _render_user_sidebar()
        return True
    
    # DURUM B: Kullanıcı giriş yapmamış
    if require_login:
        _render_login_form()
        st.stop()  # Sayfa içeriği gösterilmez
    
    return False


def is_admin() -> bool:
    """Kullanıcı admin mi?"""
    return st.session_state.get("is_admin", False)


def get_current_user() -> Optional[Dict[str, Any]]:
    """Mevcut kullanıcıyı döndür"""
    return st.session_state.get("user")


def is_authenticated() -> bool:
    """Kullanıcı giriş yapmış mı?"""
    return st.session_state.get("authenticated", False)


# Backward compatibility alias
def is_logged_in() -> bool:
    """Kullanıcı giriş yapmış mı? (eski isim)"""
    return is_authenticated()


def require_admin_access() -> bool:
    """
    Admin sayfaları için kontrol
    
    Returns:
        True: Admin erişimi var
        False: Erişim yok (hata mesajı gösterilir ve st.stop())
    """
    if not check_auth():
        return False
    
    if not is_admin():
        st.error("🚫 Bu sayfaya erişim yetkiniz yok.")
        st.info("Bu sayfa sadece admin kullanıcılar içindir.")
        st.stop()
        return False
    
    return True
