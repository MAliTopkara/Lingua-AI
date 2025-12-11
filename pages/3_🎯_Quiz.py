"""
🎯 Sınav ve Test Merkezi
Kelime testi ve AI destekli gramer quizi
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Sınav Merkezi - Lingua-AI",
    page_icon="🎯",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Imports
from components.quiz_card import (
    init_quiz_state, 
    render_quiz_question, 
    render_quiz_result,
)
from services.firebase_service import get_words, save_quiz_result
from services.gamification_service import update_user_after_quiz
from utils.constants import EXAM_TYPES, QUIZ_TYPES
from utils.helpers import init_session_state

# Session state başlat
init_session_state()
init_quiz_state()

user = auth.get_current_user()

# Gramer konuları
GRAMMAR_TOPICS = {
    "tenses": "Tenses (Zamanlar)",
    "modals": "Modals (Kiplik Fiiller)",
    "conditionals": "Conditionals (Koşul Cümleleri)",
    "prepositions": "Prepositions (Edatlar)",
    "conjunctions": "Conjunctions (Bağlaçlar)",
    "passive": "Passive Voice (Edilgen)",
    "clauses": "Relative Clauses"
}

# Ana içerik
st.title("🎯 Sınav ve Test Merkezi")
st.markdown("Kelime ve gramer bilginizi test edin!")

st.markdown("---")

# Sekmeler
tab1, tab2 = st.tabs(["📝 Kelime Testi", "🤖 Gramer AI Testi"])

# ==================== TAB 1: KELİME TESTİ ====================
with tab1:
    if st.session_state.quiz_completed:
        render_quiz_result()
        
        if "quiz_result_saved" not in st.session_state or not st.session_state.quiz_result_saved:
            score = st.session_state.quiz_score
            total = len(st.session_state.quiz_questions)
            
            result_data = {
                "userId": user["id"],
                "score": score,
                "totalQuestions": total,
                "percentage": round((score / total * 100) if total > 0 else 0, 1),
                "wrongAnswers": [w.get("id") for w in st.session_state.quiz_wrong_words if w]
            }
            
            save_quiz_result(result_data)
            gamification_result = update_user_after_quiz(user["id"], score, total)
            
            if gamification_result.get("points_earned", 0) > 0:
                st.info(f"🎉 **{gamification_result['points_earned']} puan** kazandınız!")
            
            new_badges = gamification_result.get("new_badges", [])
            if new_badges:
                from services.gamification_service import show_badge_earned_notification
                for badge_id in new_badges:
                    show_badge_earned_notification(badge_id)
            
            st.session_state.quiz_result_saved = True

    elif st.session_state.quiz_active:
        render_quiz_question()

    else:
        st.subheader("⚙️ Kelime Testi Ayarları")
        
        col1, col2 = st.columns(2)
        
        with col1:
            exam_filter = st.selectbox(
                "📋 Sınav Türü",
                options=["all"] + list(EXAM_TYPES.keys()),
                format_func=lambda x: "Tümü" if x == "all" else f"{EXAM_TYPES[x]['icon']} {EXAM_TYPES[x]['name']}",
                key="vocab_exam_filter"
            )
        
        with col2:
            quiz_type = st.selectbox(
                "❓ Soru Türü",
                options=list(QUIZ_TYPES.keys()),
                format_func=lambda x: f"{QUIZ_TYPES[x]['icon']} {QUIZ_TYPES[x]['name']}",
                key="vocab_quiz_type"
            )
        
        words = get_words(
            status="approved",
            exam_type=exam_filter if exam_filter != "all" else None,
            limit=200
        )
        
        if len(words) < 4:
            st.warning("⚠️ Quiz için en az 4 onaylı kelime gerekli.")
        else:
            st.success(f"✅ {len(words)} kelime hazır!")
            
            max_questions = min(50, len(words))
            question_count = st.slider(
                "📊 Soru Sayısı", 5, max_questions, min(10, max_questions),
                key="vocab_question_count"
            )
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📝 Soru", question_count)
            with col2:
                st.metric("⏱️ Süre", f"~{question_count // 2} dk")
            with col3:
                st.metric("🏆 Puan", "+25")
            
            st.markdown("---")
            
            if st.button("🚀 Kelime Testine Başla", type="primary", use_container_width=True, key="start_vocab"):
                from components.quiz_card import generate_quiz_questions, start_quiz
                
                questions = generate_quiz_questions(words, question_count, quiz_type)
                
                if questions:
                    st.session_state.quiz_result_saved = False
                    start_quiz(questions)
                    st.rerun()
                else:
                    st.error("Sorular oluşturulamadı.")

# ==================== TAB 2: GRAMER AI TESTİ (GERÇEK SINAV MODU) ====================
with tab2:
    
    # ========== SONUÇ EKRANI (DETAYLI ANALİZ) ==========
    if st.session_state.get("grammar_completed", False):
        questions = st.session_state.get("grammar_questions", [])
        user_answers = st.session_state.get("grammar_user_answers", {})
        total = len(questions)
        
        # Skoru hesapla
        score = 0
        for i, q in enumerate(questions):
            user_answer = user_answers.get(i)
            if user_answer:
                correct = q.get('correct', '')
                selected_letter = user_answer.split(")")[0].strip() if ")" in user_answer else user_answer[0]
                if selected_letter == correct:
                    score += 1
        
        percentage = round((score / total * 100) if total > 0 else 0)
        
        # Motivasyon
        if percentage >= 90:
            grade, message, color = "🏆 MÜTHİŞ!", "Harikaydın!", "#27ae60"
        elif percentage >= 70:
            grade, message, color = "🎯 BAŞARILI!", "Çok iyi gidiyorsun!", "#2ecc71"
        elif percentage >= 50:
            grade, message, color = "📚 FENA DEĞİL", "Biraz daha pratik yap.", "#f39c12"
        else:
            grade, message, color = "💪 ÇALIŞMALISIN", "Konuları tekrar gözden geçir.", "#e74c3c"
        
        # Sonuç kartı
        st.markdown(f'''
<div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%); border-radius: 20px; margin: 20px 0;">
    <div style="font-size: 72px; font-weight: 700; color: #667eea;">%{percentage}</div>
    <div style="font-size: 28px; margin-top: 10px; color: {color};">{grade}</div>
    <div style="font-size: 16px; margin-top: 15px; color: #a0aec0;">{message}</div>
</div>
        ''', unsafe_allow_html=True)
        
        # İstatistik kutucukları
        st.markdown(f'''
<div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;">
    <div style="text-align: center; padding: 20px 40px; background: rgba(39, 174, 96, 0.2); border-radius: 12px; border: 2px solid #27ae60;">
        <div style="font-size: 36px; font-weight: 700; color: #27ae60;">{score}</div>
        <div style="font-size: 14px; color: #a0aec0;">✅ Doğru</div>
    </div>
    <div style="text-align: center; padding: 20px 40px; background: rgba(231, 76, 60, 0.2); border-radius: 12px; border: 2px solid #e74c3c;">
        <div style="font-size: 36px; font-weight: 700; color: #e74c3c;">{total - score}</div>
        <div style="font-size: 14px; color: #a0aec0;">❌ Yanlış</div>
    </div>
    <div style="text-align: center; padding: 20px 40px; background: rgba(160, 174, 192, 0.2); border-radius: 12px; border: 2px solid #a0aec0;">
        <div style="font-size: 36px; font-weight: 700; color: #a0aec0;">{total}</div>
        <div style="font-size: 14px; color: #a0aec0;">📊 Toplam</div>
    </div>
</div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detaylı Analiz
        st.subheader("📋 Detaylı Analiz")
        
        for i, q in enumerate(questions):
            user_answer = user_answers.get(i, "Cevap verilmedi")
            correct = q.get('correct', '')
            
            # Kullanıcının cevabını kontrol et
            if user_answer and user_answer != "Cevap verilmedi":
                selected_letter = user_answer.split(")")[0].strip() if ")" in user_answer else user_answer[0]
                is_correct = selected_letter == correct
            else:
                is_correct = False
            
            # Expander içinde göster
            status_icon = "✅" if is_correct else "❌"
            with st.expander(f"{status_icon} Soru {i+1}: {q.get('question', '')[:50]}..."):
                st.markdown(f"**Soru:** {q.get('question', '')}")
                st.markdown("---")
                
                # Kullanıcının cevabı
                if is_correct:
                    st.success(f"**Senin Cevabın:** {user_answer}")
                else:
                    st.error(f"**Senin Cevabın:** {user_answer}")
                    
                    # Doğru cevabı bul ve göster
                    correct_option = ""
                    for opt in q.get('options', []):
                        if opt.startswith(correct + ")"):
                            correct_option = opt
                            break
                    st.success(f"**Doğru Cevap:** {correct_option if correct_option else correct}")
                
                # Açıklama
                explanation = q.get('explanation', '')
                if explanation:
                    st.info(f"📖 **Açıklama:** {explanation}")
        
        st.markdown("---")
        
        if st.button("🔄 Yeni Test Başlat", type="primary", use_container_width=True, key="new_grammar"):
            for key in list(st.session_state.keys()):
                if key.startswith("grammar_"):
                    del st.session_state[key]
            st.rerun()
    
    # ========== SORU EKRANI (SINAV MODU - GERİ BİLDİRİM YOK) ==========
    elif st.session_state.get("grammar_active", False):
        questions = st.session_state.grammar_questions
        current_idx = st.session_state.grammar_index
        total = len(questions)
        
        # Kullanıcı cevapları dict
        if "grammar_user_answers" not in st.session_state:
            st.session_state.grammar_user_answers = {}
        
        # Tüm sorular bitti mi?
        if current_idx >= total:
            st.session_state.grammar_completed = True
            st.session_state.grammar_active = False
            st.rerun()
        
        question = questions[current_idx]
        
        # Progress bar
        progress = (current_idx + 1) / total
        st.progress(progress)
        st.markdown(f"**Soru {current_idx + 1} / {total}**")
        
        st.markdown("---")
        
        # Soru kartı
        st.markdown(f'''
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 25px; color: white; margin: 20px 0;">
    <div style="font-size: 18px; line-height: 1.6;">{question.get('question', '')}</div>
</div>
        ''', unsafe_allow_html=True)
        
        # Şıklar
        options = question.get('options', [])
        answer_key = f"grammar_radio_{current_idx}"
        
        # Önceki cevabı al (varsa)
        previous_answer = st.session_state.grammar_user_answers.get(current_idx)
        default_index = None
        if previous_answer:
            try:
                default_index = options.index(previous_answer)
            except ValueError:
                default_index = None
        
        selected = st.radio(
            "Cevabınızı seçin:",
            options,
            key=answer_key,
            index=default_index
        )
        
        st.markdown("---")
        
        # Navigasyon butonları
        col1, col2 = st.columns(2)
        
        # Önceki soru butonu
        with col1:
            if current_idx > 0:
                if st.button("⬅️ Önceki Soru", use_container_width=True, key=f"prev_{current_idx}"):
                    # Cevabı kaydet
                    if selected:
                        st.session_state.grammar_user_answers[current_idx] = selected
                    st.session_state.grammar_index -= 1
                    st.rerun()
        
        # Sonraki/Bitir butonu
        with col2:
            if current_idx < total - 1:
                # Sonraki Soru
                if st.button("➡️ Sonraki Soru", type="primary", use_container_width=True, key=f"next_{current_idx}"):
                    if selected:
                        st.session_state.grammar_user_answers[current_idx] = selected
                        st.session_state.grammar_index += 1
                        st.rerun()
                    else:
                        st.warning("⚠️ Lütfen bir şık seçin!")
            else:
                # Testi Bitir
                if st.button("🏁 Testi Bitir ve Sonuçları Gör", type="primary", use_container_width=True, key="finish_grammar"):
                    if selected:
                        st.session_state.grammar_user_answers[current_idx] = selected
                    st.session_state.grammar_completed = True
                    st.session_state.grammar_active = False
                    st.rerun()
        
        # Cevaplanan soru sayısı
        answered_count = len([a for a in st.session_state.grammar_user_answers.values() if a])
        st.caption(f"📝 Cevaplanan: {answered_count} / {total}")
    
    # ========== AYARLAR EKRANI ==========
    else:
        st.subheader("🤖 AI Gramer Testi")
        st.info("🎯 **Gerçek Sınav Modu:** Tüm soruları çözene kadar doğru/yanlış gösterilmez. Sonunda detaylı analiz yapılır.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            grammar_topic = st.selectbox(
                "📚 Konu",
                list(GRAMMAR_TOPICS.keys()),
                format_func=lambda x: GRAMMAR_TOPICS[x],
                key="grammar_topic"
            )
        
        with col2:
            grammar_level = st.selectbox(
                "📊 Seviye",
                ["B1 - Orta", "B2 - İyi", "C1 - YDS"],
                index=1,
                key="grammar_level"
            )
        
        with col3:
            grammar_count = st.slider("❓ Soru Sayısı", 3, 10, 5, key="grammar_count")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Konu", GRAMMAR_TOPICS[grammar_topic].split(" (")[0])
        with col2:
            st.metric("📊 Seviye", grammar_level.split(" - ")[0])
        with col3:
            st.metric("❓ Soru", grammar_count)
        
        st.markdown("---")
        
        if st.button("🚀 Sınava Başla", type="primary", use_container_width=True, key="start_grammar"):
            from services.groq_service import get_grammar_quiz
            
            level_map = {"B1 - Orta": "intermediate", "B2 - İyi": "upper-intermediate", "C1 - YDS": "advanced"}
            
            with st.spinner("🤖 AI sorular oluşturuyor..."):
                questions = get_grammar_quiz(
                    topic=GRAMMAR_TOPICS[grammar_topic],
                    level=level_map.get(grammar_level, "intermediate"),
                    num_questions=grammar_count
                )
            
            if questions:
                st.session_state.grammar_questions = questions
                st.session_state.grammar_index = 0
                st.session_state.grammar_user_answers = {}
                st.session_state.grammar_active = True
                st.session_state.grammar_completed = False
                st.success(f"✅ {len(questions)} soru oluşturuldu!")
                st.rerun()
            else:
                st.error("❌ Sorular oluşturulamadı. Lütfen tekrar deneyin.")

# İpuçları
st.markdown("---")
with st.expander("💡 Test İpuçları"):
    st.markdown("""
    ### 📝 Kelime Testi
    - Verilen kelimenin doğru karşılığını bulun
    - Her doğru cevap puan kazandırır
    
    ### 🤖 Gramer AI Testi
    - **Gerçek Sınav Modu:** Test sırasında doğru/yanlış gösterilmez
    - Tüm soruları cevapladıktan sonra detaylı analiz yapılır
    - Her soru için açıklama ve doğru cevap gösterilir
    """)
