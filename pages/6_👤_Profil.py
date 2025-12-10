"""
👤 Profil Sayfası
Kullanıcı hesap yönetimi
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Profil - Lingua-AI",
    page_icon="👤",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Imports
from services.firebase_service import update_user_name, change_user_password, get_user
from utils.helpers import init_session_state

# Session state başlat
init_session_state()

user = auth.get_current_user()

# Custom CSS
st.markdown("""
<style>
.profile-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}
.profile-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    border: 4px solid white;
    margin-bottom: 15px;
}
.profile-name {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 5px;
}
.profile-email {
    font-size: 14px;
    opacity: 0.9;
}
.stat-box {
    background: rgba(102, 126, 234, 0.1);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(102, 126, 234, 0.3);
}
.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #667eea;
}
.stat-label {
    font-size: 14px;
    color: #a0aec0;
}
</style>
""", unsafe_allow_html=True)

# Ana içerik
st.title("👤 Profilim")
st.markdown("Hesap ayarlarınızı yönetin")

st.markdown("---")

# Profil başlığı
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="profile-header">
        <img src="{user.get('photoURL', '')}" class="profile-avatar">
        <div class="profile-name">{user.get('displayName', 'Kullanıcı')}</div>
        <div class="profile-email">{user.get('email', '')}</div>
    </div>
    """, unsafe_allow_html=True)

# İstatistikler
st.subheader("📊 İstatistiklerim")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-value">{user.get('points', 0)}</div>
        <div class="stat-label">⭐ Toplam Puan</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-value">{user.get('currentStreak', 0)}</div>
        <div class="stat-label">🔥 Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-value">{user.get('wordsLearned', 0)}</div>
        <div class="stat-label">📚 Öğrenilen</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-value">{user.get('quizzesTaken', 0)}</div>
        <div class="stat-label">🎯 Quiz</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sekmeler
tab1, tab2 = st.tabs(["📝 Bilgilerim", "🔒 Güvenlik"])

# ============ BİLGİLERİM SEKMESİ ============
with tab1:
    st.subheader("📝 Kişisel Bilgiler")
    
    with st.form("update_profile_form"):
        st.markdown("##### E-posta Adresi")
        st.text_input(
            "E-posta",
            value=user.get("email", ""),
            disabled=True,
            help="E-posta adresi değiştirilemez",
            label_visibility="collapsed"
        )
        
        st.markdown("##### Ad Soyad")
        new_name = st.text_input(
            "Ad Soyad",
            value=user.get("displayName", ""),
            placeholder="Adınızı girin",
            label_visibility="collapsed"
        )
        
        st.markdown("")
        
        update_submitted = st.form_submit_button(
            "💾 Bilgileri Güncelle",
            use_container_width=True,
            type="primary"
        )
        
        if update_submitted:
            if not new_name or len(new_name.strip()) < 2:
                st.error("❌ İsim en az 2 karakter olmalı.")
            elif new_name.strip() == user.get("displayName", ""):
                st.warning("⚠️ İsim aynı, değişiklik yapılmadı.")
            else:
                result = update_user_name(user.get("id"), new_name.strip())
                
                if result["success"]:
                    # Session state'i güncelle
                    st.session_state.user["displayName"] = new_name.strip()
                    st.session_state.user["photoURL"] = f"https://ui-avatars.com/api/?name={new_name.replace(' ', '+')}&background=667eea&color=fff&size=128"
                    
                    st.success("✅ Bilgiler başarıyla güncellendi!")
                    st.balloons()
                    
                    # Sayfayı yenile
                    st.rerun()
                else:
                    st.error(f"❌ Hata: {result['error']}")

# ============ GÜVENLİK SEKMESİ ============
with tab2:
    st.subheader("🔒 Şifre Değiştir")
    
    st.info("💡 Şifrenizi düzenli olarak değiştirmenizi öneririz.")
    
    with st.form("change_password_form"):
        new_password = st.text_input(
            "🔐 Yeni Şifre",
            type="password",
            placeholder="En az 6 karakter"
        )
        
        new_password_confirm = st.text_input(
            "🔐 Yeni Şifre (Tekrar)",
            type="password",
            placeholder="Şifreyi tekrar girin"
        )
        
        st.markdown("")
        
        password_submitted = st.form_submit_button(
            "🔄 Şifreyi Güncelle",
            use_container_width=True,
            type="primary"
        )
        
        if password_submitted:
            if not new_password or not new_password_confirm:
                st.error("❌ Tüm alanları doldurun.")
            elif len(new_password) < 6:
                st.error("❌ Şifre en az 6 karakter olmalı.")
            elif new_password != new_password_confirm:
                st.error("❌ Şifreler eşleşmiyor.")
            else:
                result = change_user_password(user.get("id"), new_password)
                
                if result["success"]:
                    st.success("✅ Şifre başarıyla değiştirildi! Yeniden giriş yapmanız gerekiyor.")
                    
                    # Kullanıcıyı çıkış yaptır
                    import time
                    time.sleep(1)
                    auth.logout()
                    st.rerun()
                else:
                    st.error(f"❌ Hata: {result['error']}")

# Footer
st.markdown("---")
st.caption("🔒 Tüm bilgileriniz güvenli şekilde saklanmaktadır.")
