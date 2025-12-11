"""
⚙️ Admin Paneli Sayfası
İçerik moderasyonu ve kullanıcı yönetimi
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Admin Panel - Lingua-AI",
    page_icon="⚙️",
    layout="wide"
)

# Auth check - Admin Login Gate
import components.auth as auth
auth.require_admin_access()

# Imports (sadece admin ise buraya gelir)
from services.firebase_service import (
    get_pending_words, 
    get_pending_tricks,
    approve_word,
    reject_word,
    approve_trick,
    update_word,
    get_leaderboard
)
from services.gamification_service import update_user_after_word_approved
from utils.constants import WORD_TYPES, EXAM_TYPES, DIFFICULTY_LEVELS, TRICK_CATEGORIES
from utils.helpers import init_session_state, format_date

# Session state başlat
init_session_state()

admin = auth.get_current_user()

# Ana içerik
st.title("⚙️ Admin Paneli")
st.markdown("İçerik moderasyonu ve yönetim")

st.markdown("---")

# Tab'lar
tab1, tab2, tab3 = st.tabs(["📝 Bekleyen Kelimeler", "💡 Bekleyen Trick'ler", "👥 Kullanıcılar"])

# ==================== BEKLEYEN KELİMELER ====================
with tab1:
    st.subheader("📝 Bekleyen Kelimeler")
    
    # Yenile butonu
    if st.button("🔄 Yenile", key="refresh_words"):
        st.rerun()
    
    pending_words = get_pending_words(limit=50)
    
    if not pending_words:
        st.success("✅ Bekleyen kelime yok!")
    else:
        st.info(f"📨 {len(pending_words)} kelime onay bekliyor")
        
        for word in pending_words:
            word_type_info = WORD_TYPES.get(word.get("type", "noun"), WORD_TYPES["noun"])
            diff_info = DIFFICULTY_LEVELS.get(word.get("difficulty", 3), DIFFICULTY_LEVELS[3])
            
            with st.expander(f"**{word.get('english', '')}** - {word.get('turkish', '')} (Ekleyen: {word.get('addedByName', 'Anonim')})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **İngilizce:** {word.get('english', '')}
                    
                    **Türkçe:** {word.get('turkish', '')}
                    
                    **Tür:** {word_type_info['abbr']} {word_type_info['name']}
                    
                    **Zorluk:** {diff_info['icon']} {diff_info['name']}
                    """)
                
                with col2:
                    synonyms = word.get('synonyms', [])
                    antonyms = word.get('antonyms', [])
                    exam_types = word.get('examTypes', [])
                    
                    st.markdown(f"""
                    **Eş Anlamlılar:** {', '.join(synonyms) if synonyms else '-'}
                    
                    **Zıt Anlamlılar:** {', '.join(antonyms) if antonyms else '-'}
                    
                    **Sınavlar:** {', '.join([EXAM_TYPES.get(e, {}).get('name', e) for e in exam_types])}
                    """)
                
                example = word.get('exampleSentence', '')
                if example:
                    st.markdown(f"**Örnek Cümle:** _{example}_")
                
                st.markdown(f"_Eklenme: {format_date(word.get('createdAt'), 'relative')}_")
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.button("✅ Onayla", key=f"approve_{word.get('id')}", type="primary"):
                        if approve_word(word.get("id"), admin["id"]):
                            # Kullanıcıya puan ver
                            update_user_after_word_approved(word.get("addedBy"))
                            st.success("Kelime onaylandı!")
                            st.rerun()
                        else:
                            st.error("Onaylama başarısız!")
                
                with col2:
                    if st.button("❌ Reddet", key=f"reject_{word.get('id')}"):
                        if reject_word(word.get("id"), admin["id"], "Admin tarafından reddedildi"):
                            st.warning("Kelime reddedildi.")
                            st.rerun()
                        else:
                            st.error("Reddetme başarısız!")
                
                with col3:
                    with st.popover("✏️ Düzenle"):
                        new_english = st.text_input("İngilizce", value=word.get("english", ""), key=f"edit_en_{word.get('id')}")
                        new_turkish = st.text_input("Türkçe", value=word.get("turkish", ""), key=f"edit_tr_{word.get('id')}")
                        
                        if st.button("💾 Kaydet ve Onayla", key=f"save_{word.get('id')}"):
                            updates = {}
                            if new_english != word.get("english"):
                                updates["english"] = new_english.lower().strip()
                            if new_turkish != word.get("turkish"):
                                updates["turkish"] = new_turkish.strip()
                            
                            if updates:
                                update_word(word.get("id"), updates)
                            
                            approve_word(word.get("id"), admin["id"])
                            update_user_after_word_approved(word.get("addedBy"))
                            st.success("Düzenlendi ve onaylandı!")
                            st.rerun()

# ==================== BEKLEYEN TRICK'LER ====================
with tab2:
    st.subheader("💡 Bekleyen Trick'ler")
    
    if st.button("🔄 Yenile", key="refresh_tricks"):
        st.rerun()
    
    pending_tricks = get_pending_tricks(limit=50)
    
    if not pending_tricks:
        st.success("✅ Bekleyen trick yok!")
    else:
        st.info(f"📨 {len(pending_tricks)} trick onay bekliyor")
        
        for trick in pending_tricks:
            cat_info = TRICK_CATEGORIES.get(trick.get("category", "grammar"), TRICK_CATEGORIES["grammar"])
            
            with st.expander(f"**{trick.get('title', '')}** ({cat_info['icon']} {cat_info['name']}) - Ekleyen: {trick.get('addedByName', 'Anonim')}"):
                st.markdown(f"**Kategori:** {cat_info['icon']} {cat_info['name']}")
                
                related = trick.get('relatedWords', [])
                if related:
                    st.markdown(f"**İlgili Kelimeler:** {', '.join(related)}")
                
                exam_types = trick.get('examTypes', [])
                st.markdown(f"**Sınavlar:** {', '.join([EXAM_TYPES.get(e, {}).get('name', e) for e in exam_types])}")
                
                st.markdown("---")
                st.markdown("**İçerik:**")
                st.markdown(trick.get('content', ''))
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Onayla", key=f"approve_trick_{trick.get('id')}", type="primary"):
                        if approve_trick(trick.get("id"), admin["id"]):
                            st.success("Trick onaylandı!")
                            st.rerun()
                        else:
                            st.error("Onaylama başarısız!")
                
                with col2:
                    if st.button("❌ Reddet", key=f"reject_trick_{trick.get('id')}"):
                        # Trick reddetme işlemi
                        st.warning("Trick reddedildi.")

# ==================== KULLANICILAR ====================
with tab3:
    st.subheader("👥 Kullanıcı Yönetimi")
    
    # Import güncelleme
    from services.firebase_service import update_user_role
    
    users = get_leaderboard(limit=50)
    current_user_id = admin.get("id") if admin else None
    
    if not users:
        st.info("Henüz kullanıcı yok.")
    else:
        st.info(f"👥 {len(users)} kullanıcı")
        
        # Tablo başlıkları
        header_cols = st.columns([0.5, 2, 1.5, 1, 1, 1.5])
        
        with header_cols[0]:
            st.markdown("**#**")
        with header_cols[1]:
            st.markdown("**Kullanıcı**")
        with header_cols[2]:
            st.markdown("**E-posta**")
        with header_cols[3]:
            st.markdown("**Puan**")
        with header_cols[4]:
            st.markdown("**Rol**")
        with header_cols[5]:
            st.markdown("**Eylem**")
        
        st.markdown("---")
        
        for i, user in enumerate(users, 1):
            user_id = user.get("id", "")
            is_self = user_id == current_user_id
            role = user.get("role", "user")
            
            cols = st.columns([0.5, 2, 1.5, 1, 1, 1.5])
            
            with cols[0]:
                st.write(i)
            
            with cols[1]:
                name = user.get("displayName", "Anonim")
                if is_self:
                    st.markdown(f"**{name}** 🔹")
                else:
                    st.write(name)
            
            with cols[2]:
                email = user.get("email", "")
                st.write(email[:18] + "..." if len(email) > 18 else email)
            
            with cols[3]:
                st.write(user.get("points", 0))
            
            with cols[4]:
                if role == "admin":
                    st.markdown("👑 **Admin**")
                else:
                    st.markdown("👤 User")
            
            with cols[5]:
                if is_self:
                    st.caption("(Sen)")
                elif role == "user":
                    if st.button("⬆️ Admin Yap", key=f"promote_{user_id}", type="primary"):
                        if update_user_role(user_id, "admin"):
                            st.success(f"✅ {user.get('displayName')} artık admin!")
                            st.rerun()
                        else:
                            st.error("❌ İşlem başarısız!")
                else:  # admin
                    if st.button("⬇️ Yetkiyi Al", key=f"demote_{user_id}"):
                        if update_user_role(user_id, "user"):
                            st.success(f"✅ {user.get('displayName')} artık normal kullanıcı!")
                            st.rerun()
                        else:
                            st.error("❌ İşlem başarısız!")

# Sistem bilgisi
st.markdown("---")
st.subheader("ℹ️ Sistem Bilgisi")

from services.firebase_service import get_app_stats
from services.groq_service import check_groq_availability
from services.moderation_service import check_moderation_availability

stats = get_app_stats()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📊 Veritabanı**")
    st.write(f"Toplam Kelime: {stats.get('total_words', 0)}")
    st.write(f"Bekleyen: {stats.get('pending_words', 0)}")
    st.write(f"Kullanıcı: {stats.get('total_users', 0)}")

with col2:
    st.markdown("**🤖 AI Servisleri**")
    groq_status = "✅ Aktif" if check_groq_availability() else "❌ Devre Dışı"
    moderation_status = "✅ Aktif" if check_moderation_availability() else "❌ Devre Dışı"
    st.write(f"Groq API: {groq_status}")
    st.write(f"Moderasyon: {moderation_status}")

with col3:
    st.markdown("**👤 Admin Bilgisi**")
    st.write(f"Giriş: {admin.get('displayName', 'Admin')}")
    st.write(f"E-posta: {admin.get('email', '')}")

# Kelime yükleme bölümü
st.markdown("---")
st.subheader("📚 Başlangıç Kelimeleri Yükle")

col1, col2 = st.columns([2, 1])

with col1:
    st.info("**initial_words.json** dosyasından 50 YDS kelimesini Firebase'e yükler. Sadece veritabanı boşsa veya kelime eksikse çalışır.")

with col2:
    if st.button("📥 Kelimeleri Yükle", type="primary", use_container_width=True):
        from services.firebase_service import initialize_words_from_json, get_words
        import os
        
        with st.spinner("Kelimeler yükleniyor..."):
            json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "initial_words.json")
            
            if os.path.exists(json_path):
                loaded_count = initialize_words_from_json(json_path)
                if loaded_count > 0:
                    st.success(f"✅ {loaded_count} kelime başarıyla yüklendi!")
                    # Cache'i temizle
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.warning("Tüm kelimeler zaten mevcut veya yükleme yapılamadı.")
            else:
                st.error(f"JSON dosyası bulunamadı: {json_path}")
