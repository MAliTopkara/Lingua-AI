"""
➕ Kelime ve Trick Ekle Sayfası
Kullanıcıların kelime ve trick ekleyebildiği sayfa
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="İçerik Ekle - Lingua-AI",
    page_icon="➕",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Imports (sadece giriş yapılmışsa)
from services.firebase_service import add_word, add_trick, check_word_exists
from services.moderation_service import check_word_submission, check_trick_submission, check_moderation_availability
from utils.constants import WORD_TYPES, EXAM_TYPES, DIFFICULTY_LEVELS, TRICK_CATEGORIES
from utils.helpers import init_session_state, validate_word_input, sanitize_input

# Session state başlat
init_session_state()

user = auth.get_current_user()

# Ana içerik
st.title("➕ Kelime veya Trick Ekle")
st.markdown("Kelime havuzuna ve bilgi bankasına katkıda bulunun!")

# Moderasyon durumu
if check_moderation_availability():
    st.success("✅ Moderasyon sistemi aktif - içerikler otomatik kontrol edilecek.")
else:
    st.warning("⚠️ Moderasyon sistemi devre dışı - içerikler manuel olarak kontrol edilecek.")

st.markdown("---")

# Tab'lar
tab1, tab2 = st.tabs(["📖 Kelime Ekle", "💡 Trick/İpucu Ekle"])

# ==================== KELİME EKLEME ====================
with tab1:
    st.subheader("📖 Yeni Kelime Ekle")
    st.markdown("Eklediğiniz kelimeler admin onayından sonra yayınlanacaktır.")
    
    with st.form("word_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            english = st.text_input(
                "İngilizce Kelime *",
                placeholder="abandon",
                help="Küçük harflerle yazın"
            )
            
            word_type = st.selectbox(
                "Kelime Türü *",
                options=list(WORD_TYPES.keys()),
                format_func=lambda x: f"{WORD_TYPES[x]['abbr']} {WORD_TYPES[x]['name']}"
            )
            
            difficulty = st.slider(
                "Zorluk Seviyesi *",
                min_value=1,
                max_value=5,
                value=3,
                help="1: Çok kolay, 5: Çok zor"
            )
            
            # Zorluk göstergesi
            diff_info = DIFFICULTY_LEVELS[difficulty]
            st.markdown(f"{diff_info['icon']} **{diff_info['name']}**")
        
        with col2:
            turkish = st.text_input(
                "Türkçe Karşılık *",
                placeholder="terk etmek, vazgeçmek",
                help="Birden fazla anlam varsa virgülle ayırın"
            )
            
            synonyms_text = st.text_input(
                "Eş Anlamlılar (İngilizce)",
                placeholder="leave, desert, forsake",
                help="Virgülle ayırarak yazın"
            )
            
            antonyms_text = st.text_input(
                "Zıt Anlamlılar (İngilizce)",
                placeholder="keep, maintain",
                help="Virgülle ayırarak yazın"
            )
        
        example_sentence = st.text_area(
            "Örnek Cümle (Opsiyonel)",
            placeholder="The sailors had to abandon the sinking ship.",
            help="İngilizce örnek cümle"
        )
        
        st.markdown("**Hangi sınavlar için?**")
        
        exam_cols = st.columns(len(EXAM_TYPES))
        selected_exams = []
        
        for i, (exam_key, exam_info) in enumerate(EXAM_TYPES.items()):
            with exam_cols[i]:
                if st.checkbox(f"{exam_info['icon']} {exam_info['name']}", value=(exam_key in ["yds", "yokdil", "genel"])):
                    selected_exams.append(exam_key)
        
        st.markdown("---")
        
        submitted = st.form_submit_button("📤 Kelime Ekle", type="primary", use_container_width=True)
        
        if submitted:
            # Validasyon
            is_valid, error_msg = validate_word_input(english, turkish)
            
            if not is_valid:
                st.error(f"❌ {error_msg}")
            elif not selected_exams:
                st.error("❌ En az bir sınav türü seçmelisiniz.")
            elif check_word_exists(english):
                st.warning("⚠️ Bu kelime zaten mevcut!")
            else:
                # Moderasyon kontrolü
                is_safe, mod_msg = check_word_submission(english, turkish, example_sentence)
                
                if not is_safe:
                    st.error(f"❌ {mod_msg}")
                else:
                    # Kelimeleri parse et
                    synonyms = [s.strip() for s in synonyms_text.split(",") if s.strip()] if synonyms_text else []
                    antonyms = [s.strip() for s in antonyms_text.split(",") if s.strip()] if antonyms_text else []
                    
                    word_data = {
                        "english": sanitize_input(english.lower().strip()),
                        "turkish": sanitize_input(turkish.strip()),
                        "type": word_type,
                        "difficulty": difficulty,
                        "synonyms": synonyms,
                        "antonyms": antonyms,
                        "exampleSentence": sanitize_input(example_sentence) if example_sentence else "",
                        "examTypes": selected_exams,
                        "addedBy": user["id"],
                        "addedByName": user.get("displayName", "Anonim")
                    }
                    
                    word_id = add_word(word_data)
                    
                    if word_id:
                        st.success("✅ Kelime başarıyla eklendi! Admin onayından sonra yayınlanacak.")
                        st.balloons()
                    else:
                        st.error("❌ Kelime eklenirken bir hata oluştu.")

# ==================== TRICK EKLEME ====================
with tab2:
    st.subheader("💡 Yeni Trick/İpucu Ekle")
    st.markdown("Sınava hazırlık için faydalı ipuçları ve stratejiler paylaşın.")
    
    with st.form("trick_form"):
        title = st.text_input(
            "Başlık *",
            placeholder="Although vs Despite Farkı",
            help="Kısa ve açıklayıcı bir başlık"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Kategori *",
                options=list(TRICK_CATEGORIES.keys()),
                format_func=lambda x: f"{TRICK_CATEGORIES[x]['icon']} {TRICK_CATEGORIES[x]['name']}"
            )
        
        with col2:
            related_words_text = st.text_input(
                "İlgili Kelimeler",
                placeholder="although, despite, however",
                help="Virgülle ayırarak yazın"
            )
        
        content = st.text_area(
            "İçerik * (Markdown desteklenir)",
            placeholder="""## Although vs Despite

**Although** + clause (özne + fiil) kullanılır:
- Although it was raining, we went out.

**Despite** + noun/gerund kullanılır:
- Despite the rain, we went out.
- Despite being tired, she continued working.

### Hatırlatma
- Although = "e rağmen" (cümle ile)
- Despite = "e rağmen" (isim ile)""",
            height=300,
            help="Markdown formatında yazabilirsiniz"
        )
        
        st.markdown("**Hangi sınavlar için?**")
        
        exam_cols = st.columns(len(EXAM_TYPES))
        selected_trick_exams = []
        
        for i, (exam_key, exam_info) in enumerate(EXAM_TYPES.items()):
            with exam_cols[i]:
                if st.checkbox(f"{exam_info['icon']} {exam_info['name']}", value=True, key=f"trick_exam_{exam_key}"):
                    selected_trick_exams.append(exam_key)
        
        st.markdown("---")
        
        trick_submitted = st.form_submit_button("📤 Trick Ekle", type="primary", use_container_width=True)
        
        if trick_submitted:
            if not title or len(title) < 5:
                st.error("❌ Başlık en az 5 karakter olmalıdır.")
            elif not content or len(content) < 20:
                st.error("❌ İçerik en az 20 karakter olmalıdır.")
            else:
                # Moderasyon kontrolü
                is_safe, mod_msg = check_trick_submission(title, content)
                
                if not is_safe:
                    st.error(f"❌ {mod_msg}")
                else:
                    related_words = [w.strip() for w in related_words_text.split(",") if w.strip()] if related_words_text else []
                    
                    trick_data = {
                        "title": sanitize_input(title),
                        "content": content,  # Markdown olduğu için sanitize etmiyoruz
                        "category": category,
                        "relatedWords": related_words,
                        "examTypes": selected_trick_exams,
                        "addedBy": user["id"],
                        "addedByName": user.get("displayName", "Anonim")
                    }
                    
                    trick_id = add_trick(trick_data)
                    
                    if trick_id:
                        st.success("✅ Trick başarıyla eklendi! Admin onayından sonra yayınlanacak.")
                        st.balloons()
                    else:
                        st.error("❌ Trick eklenirken bir hata oluştu.")

# Bilgi kutusu
st.markdown("---")
with st.expander("ℹ️ İçerik Ekleme Kuralları"):
    st.markdown("""
    ### Kelime Ekleme Kuralları
    - Kelimeler doğru yazılmalıdır
    - Türkçe karşılık anlamlı olmalıdır
    - Zorluk seviyesi gerçekçi olmalıdır
    - Mümkünse örnek cümle ekleyin
    
    ### Trick Ekleme Kuralları
    - Başlık açıklayıcı olmalıdır
    - İçerik eğitici ve faydalı olmalıdır
    - Markdown formatını kullanabilirsiniz
    - Uygunsuz içerik paylaşmayın
    
    ### Moderasyon
    - Tüm içerikler otomatik kontrolden geçer
    - Admin onayından sonra yayınlanır
    - Uygunsuz içerikler reddedilir
    
    ### Ödüller
    - Her onaylanan kelime için **10 puan** kazanırsınız
    - Her onaylanan trick için **15 puan** kazanırsınız
    - Rozetler kazanarak seviye atlayabilirsiniz
    """)
