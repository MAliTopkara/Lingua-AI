"""
💡 Trick İstasyonu Sayfası
YDS/YÖKDİL sınav ipuçları ve stratejiler
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Trick İstasyonu - Lingua-AI",
    page_icon="💡",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Session state
from utils.helpers import init_session_state
init_session_state()

# ==================== TRICKS VERİSİ ====================
TRICKS = [
    {
        "id": 1,
        "title": "Zaman Uyumu (Tense Harmony)",
        "content": """**Kural:** Cümlede 'when', 'while', 'before', 'after' gibi zaman bağlaçları varsa, iki tarafın zamanı uyumlu olmalıdır.

**Örnekler:**
- ✅ When he **came** home, she **was cooking**. (Past - Past Continuous)
- ✅ Before I **leave**, I **will call** you. (Present - Future)
- ❌ When he came home, she cooks. (Past - Present = YANLIŞ)

**Sınav İpucu:** Cümlede bir zaman belirteci gördüğünde, diğer fiilin zamanını ona göre ayarla.""",
        "tag": "Tenses",
        "color": "#667eea"
    },
    {
        "id": 2,
        "title": "Subject-Verb Agreement",
        "content": """**Kural:** Özne ile yüklem tekil/çoğul açısından uyumlu olmalıdır.

**Dikkat Edilecekler:**
- 'Everyone', 'somebody', 'each' → TEKİL fiil alır
- 'The number of' → TEKİL, 'A number of' → ÇOĞUL
- 'Neither...nor', 'Either...or' → Yakın özneye uyum

**Örnekler:**
- ✅ Everyone **is** happy.
- ✅ The number of students **is** increasing.
- ✅ A number of students **are** waiting.""",
        "tag": "Grammar",
        "color": "#764ba2"
    },
    {
        "id": 3,
        "title": "Relative Clause İpuçları",
        "content": """**Kim için ne kullanılır:**
- **Who/That** → İnsanlar için
- **Which/That** → Nesneler/Hayvanlar için
- **Whose** → Sahiplik (Kimin)
- **Where** → Yer belirtir
- **When** → Zaman belirtir

**Özel Durumlar:**
- Virgülden sonra 'that' KULLANILMAZ → 'which' kullanılır
- Tanımlayıcı (defining) → that tercih edilir
- Tanımlayıcı olmayan (non-defining) → which zorunlu""",
        "tag": "Clauses",
        "color": "#f39c12"
    },
    {
        "id": 4,
        "title": "Causative Yapılar",
        "content": """**Have/Get Something Done:**

| Yapı | Form | Anlam |
|------|------|-------|
| have sth done | have + obj + V3 | Yaptırmak |
| get sth done | get + obj + V3 | Yaptırmak |
| make sb do | make + sb + V1 | Zorla yaptırmak |
| let sb do | let + sb + V1 | İzin vermek |

**Örnekler:**
- I **had** my car **repaired**. (Arabamı tamir ettirdim)
- She **got** her hair **cut**. (Saçını kestirdi)
- He **made** me **wait**. (Beni bekletti)""",
        "tag": "Causatives",
        "color": "#e74c3c"
    },
    {
        "id": 5,
        "title": "Wish / If Only Yapıları",
        "content": """**Zaman Kaydırma Kuralı:**

| Durum | Wish/If only + | Örnek |
|-------|----------------|-------|
| Şimdi | Past Simple | I wish I **knew** the answer. |
| Geçmiş | Past Perfect | I wish I **had studied** more. |
| Gelecek | Would + V1 | I wish he **would stop** talking. |

**Dikkat:** 'I wish I was' yerine 'I wish I **were**' daha formal ve sınavda tercih edilir.""",
        "tag": "Conditionals",
        "color": "#27ae60"
    },
    {
        "id": 6,
        "title": "Inversion (Devrik Cümle)",
        "content": """**Olumsuz/Kısıtlayıcı İfadelerle Devrik Yapı:**

Cümle başına gelince devrik yapı gerektirir:
- **Never** have I seen such beauty.
- **Rarely** does he come here.
- **Not only** did she win, **but also** she broke the record.
- **Hardly** had I arrived **when** it started raining.
- **No sooner** had I left **than** it rained.

**Formül:** Olumsuz ifade + yardımcı fiil + özne + ana fiil""",
        "tag": "Advanced",
        "color": "#9b59b6"
    },
    {
        "id": 7,
        "title": "Gerund vs Infinitive",
        "content": """**Sadece Gerund (-ing) Alan Fiiller:**
enjoy, avoid, mind, suggest, finish, keep, consider, admit, deny

**Sadece Infinitive (to + V1) Alan Fiiller:**
want, need, decide, hope, expect, promise, refuse, agree, manage

**Her İkisini de Alan (Anlam Farkı Var!):**
- **stop to do** = yapmak için durmak
- **stop doing** = yapmayı bırakmak
- **remember to do** = yapacağını hatırlamak
- **remember doing** = yaptığını hatırlamak""",
        "tag": "Verbs",
        "color": "#3498db"
    },
    {
        "id": 8,
        "title": "Preposition Collocations",
        "content": """**Sık Çıkan Edat Kalıpları:**

| Sıfat + Edat | Fiil + Edat |
|--------------|-------------|
| afraid **of** | depend **on** |
| interested **in** | consist **of** |
| good **at** | belong **to** |
| responsible **for** | result **in** |
| similar **to** | succeed **in** |
| different **from** | apologize **for** |

**İpucu:** Bu kalıpları ezberle, boşluk doldurmada çok çıkar!""",
        "tag": "Prepositions",
        "color": "#1abc9c"
    },
    {
        "id": 9,
        "title": "Passive Voice Kuralları",
        "content": """**Aktiften Pasife Dönüşüm:**
- Nesne → Özne olur
- Fiil → be + V3 olur
- Özne → by + nesne (opsiyonel)

**Zaman Uyumu:**
| Aktif | Pasif |
|-------|-------|
| writes | is written |
| wrote | was written |
| has written | has been written |
| will write | will be written |

**Dikkat:** Geçişsiz fiiller (intransitive) pasif yapılamaz! (die, arrive, happen)""",
        "tag": "Passive",
        "color": "#e67e22"
    },
    {
        "id": 10,
        "title": "Quantifiers (Nicelik Belirteçleri)",
        "content": """**Sayılabilenler için:**
- many, few, a few, several, a number of

**Sayılamayanlar için:**
- much, little, a little, a great deal of

**Her İkisi için:**
- some, any, no, a lot of, plenty of, enough

**Dikkat:**
- few / little → olumsuz anlam (az, yetersiz)
- a few / a little → olumlu anlam (biraz, yeterli)""",
        "tag": "Quantifiers",
        "color": "#8e44ad"
    }
]

# ==================== SESSION STATE ====================
if "trick_index" not in st.session_state:
    st.session_state.trick_index = 0

# ==================== HELPER FUNCTIONS ====================
def next_trick():
    if st.session_state.trick_index < len(TRICKS) - 1:
        st.session_state.trick_index += 1

def prev_trick():
    if st.session_state.trick_index > 0:
        st.session_state.trick_index -= 1

# ==================== ANA İÇERİK ====================
st.title("💡 Trick İstasyonu")
st.markdown("YDS/YÖKDİL sınavları için altın değerinde ipuçları")

st.markdown("---")

# Mevcut trick
current_index = st.session_state.trick_index
trick = TRICKS[current_index]
total = len(TRICKS)

# Progress bar
progress = (current_index + 1) / total
st.progress(progress)
st.markdown(f"**{current_index + 1} / {total}** - {trick['tag']}")

st.markdown("---")

# Trick kartı
st.markdown(f'''
<div style="background: linear-gradient(135deg, {trick['color']} 0%, {trick['color']}99 100%); border-radius: 20px; padding: 30px; color: white; margin: 20px 0; border: 3px solid #ffd700; box-shadow: 0 10px 40px rgba(0,0,0,0.3);">
    <div style="font-size: 28px; font-weight: 700; margin-bottom: 15px;">💡 {trick['title']}</div>
    <div style="background: rgba(255,215,0,0.2); padding: 5px 15px; border-radius: 20px; display: inline-block; font-size: 14px; margin-bottom: 20px;">🏷️ {trick['tag']}</div>
</div>
''', unsafe_allow_html=True)

# İçerik
st.markdown(trick['content'])

st.markdown("---")

# Navigasyon butonları
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if current_index > 0:
        if st.button("⬅️ Önceki", use_container_width=True):
            prev_trick()
            st.rerun()
    else:
        st.button("⬅️ Önceki", use_container_width=True, disabled=True)

with col2:
    # Konu seçimi
    tags = list(set(t['tag'] for t in TRICKS))
    selected_tag = st.selectbox("🏷️ Konuya Git", ["Tümü"] + tags, label_visibility="collapsed")
    
    if selected_tag != "Tümü":
        for i, t in enumerate(TRICKS):
            if t['tag'] == selected_tag:
                st.session_state.trick_index = i
                st.rerun()

with col3:
    if current_index < total - 1:
        if st.button("Sonraki ➡️", use_container_width=True, type="primary"):
            next_trick()
            st.rerun()
    else:
        st.button("Sonraki ➡️", use_container_width=True, disabled=True)

# Footer
st.markdown("---")
st.caption("💡 Her gün bir trick öğren, sınavda fark yarat!")
