"""
📚 Gramer Modülü - Ders Çalışma
YDS/YÖKDİL gramer konuları ve konu anlatımları
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="Gramer - Lingua-AI",
    page_icon="📚",
    layout="wide"
)

# Auth check - Login Gate
import components.auth as auth
auth.check_auth()

# Session state
from utils.helpers import init_session_state
init_session_state()

# ==================== GRAMER KONULARI ====================
GRAMMAR_TOPICS = {
    "tenses": {
        "name": "Tenses (Zamanlar)",
        "icon": "⏰",
        "summary": """
## ⏰ Tenses (Zamanlar)

### Present Tenses
| Tense | Form | Kullanım | Zaman Belirteçleri |
|-------|------|----------|-------------------|
| Simple Present | V1 / V1+s | Alışkanlık, genel doğrular | always, usually, often |
| Present Continuous | am/is/are + Ving | Şu anki eylem | now, at the moment |
| Present Perfect | have/has + V3 | Geçmiş-şimdi bağlantısı | just, already, yet, since, for |
| Present Perfect Cont. | have/has been + Ving | Devam eden eylem | for, since |

### Past Tenses
| Tense | Form | Kullanım | Zaman Belirteçleri |
|-------|------|----------|-------------------|
| Simple Past | V2 | Biten geçmiş eylem | yesterday, ago, last week |
| Past Continuous | was/were + Ving | Geçmişte devam eden | while, when |
| Past Perfect | had + V3 | Geçmişten önce | before, after, by the time |

### Future Tenses
| Tense | Form | Kullanım |
|-------|------|----------|
| Will | will + V1 | Anlık karar, tahmin |
| Be going to | am/is/are going to + V1 | Plan, niyet |
| Future Continuous | will be + Ving | Gelecekte devam eden |
| Future Perfect | will have + V3 | Gelecekte tamamlanmış |

### 💡 Sınav İpuçları
- Zaman belirteçlerine dikkat et - doğru tense'i bulmana yardımcı olur
- "Since" ve "for" gördüğünde Perfect tense düşün
- "While" genellikle Past Continuous ile kullanılır
"""
    },
    "modals": {
        "name": "Modals (Kiplik Fiiller)",
        "icon": "🔧",
        "summary": """
## 🔧 Modals (Kiplik Fiiller)

### Temel Modals ve Anlamları
| Modal | Anlam | Örnek |
|-------|-------|-------|
| **can** | yetenek, izin | I can swim. |
| **could** | geçmiş yetenek, rica | Could you help me? |
| **may** | izin, olasılık | It may rain. |
| **might** | düşük olasılık | He might come. |
| **must** | zorunluluk, kesin çıkarım | You must study. |
| **should** | tavsiye | You should rest. |
| **would** | geçmiş alışkanlık, rica | Would you like tea? |

### Modal Perfect Yapılar
| Yapı | Anlam | Örnek |
|------|-------|-------|
| must have V3 | Kesin yapmıştır | He must have left. |
| may/might have V3 | Yapmış olabilir | She may have forgotten. |
| could have V3 | Yapabilirdi (yapmadı) | You could have helped. |
| should have V3 | Yapmalıydı (yapmadı) | I should have studied. |
| needn't have V3 | Gereksiz yaptı | You needn't have waited. |

### 💡 Sınav İpuçları
- "Must have V3" geçmiş kesinlik, "must V1" şimdiki zorunluluk
- "Could" hem geçmiş yetenek hem de şu anki olasılık olabilir
- "Should have V3" pişmanlık ifade eder
"""
    },
    "conditionals": {
        "name": "Conditionals (Koşul Cümleleri)",
        "icon": "🔀",
        "summary": """
## 🔀 Conditionals (Koşul Cümleleri)

### Dört Temel Conditional Türü

| Type | If Clause | Main Clause | Kullanım |
|------|-----------|-------------|----------|
| **Type 0** | Simple Present | Simple Present | Genel doğrular |
| **Type 1** | Simple Present | will + V1 | Gerçek olasılık |
| **Type 2** | Simple Past | would + V1 | Hayali (şimdi) |
| **Type 3** | Past Perfect | would have + V3 | Hayali (geçmiş) |

### Örnekler
- **Type 0:** If you heat water, it boils.
- **Type 1:** If it rains, I **will stay** home.
- **Type 2:** If I **had** money, I **would buy** a car.
- **Type 3:** If I **had studied**, I **would have passed**.

### Mixed Conditionals
- **Type 3 → Type 2:** If I **had studied** (geçmiş), I **would be** successful (şimdi).
- **Type 2 → Type 3:** If I **were** rich (şimdi), I **would have bought** it (geçmiş).

### 💡 Sınav İpuçları
- Type 2'de "was" yerine "were" kullanımı daha formal
- "Unless" = "If...not" anlamına gelir
- "Provided that", "as long as" = If anlamında kullanılır
"""
    },
    "passive": {
        "name": "Passive Voice (Edilgen Yapı)",
        "icon": "🔄",
        "summary": """
## 🔄 Passive Voice (Edilgen Yapı)

### Dönüşüm Formülü
**Active:** Subject + Verb + Object
**Passive:** Object + be + V3 (+ by Subject)

### Zamanlarla Passive
| Tense | Active | Passive |
|-------|--------|---------|
| Simple Present | writes | is written |
| Simple Past | wrote | was written |
| Present Perfect | has written | has been written |
| Past Perfect | had written | had been written |
| Future | will write | will be written |
| Modal | can write | can be written |

### 💡 Sınav İpuçları
- Geçişsiz fiiller (intransitive) pasif yapılamaz: die, arrive, happen, occur
- "by + agent" genellikle yazılmaz (biliniyorsa veya önemsizse)
- "Get + V3" informal passive olarak kullanılır
"""
    },
    "clauses": {
        "name": "Relative Clauses",
        "icon": "🔗",
        "summary": """
## 🔗 Relative Clauses (İlgi Cümlecikleri)

### Relative Pronouns
| Pronoun | Kullanım | Örnek |
|---------|----------|-------|
| **who** | İnsanlar (özne) | The man **who** called... |
| **whom** | İnsanlar (nesne) | The man **whom** I met... |
| **which** | Nesneler/Hayvanlar | The book **which** I read... |
| **that** | Her ikisi için | The car **that** I bought... |
| **whose** | Sahiplik | The woman **whose** car... |
| **where** | Yer | The city **where** I live... |
| **when** | Zaman | The day **when** we met... |

### Defining vs Non-defining
| Tür | Virgül | That Kullanımı |
|-----|--------|----------------|
| Defining | Yok | Kullanılabilir |
| Non-defining | Var | Kullanılamaz |

### 💡 Sınav İpuçları
- Virgülden sonra "that" KULLANILMAZ, "which" kullanılır
- "Whom" nesne pozisyonunda kullanılır (formal)
- Preposition + whom/which yapısına dikkat
"""
    },
    "conjunctions": {
        "name": "Conjunctions (Bağlaçlar)",
        "icon": "🔗",
        "summary": """
## 🔗 Conjunctions (Bağlaçlar)

### Coordinating Conjunctions (FANBOYS)
| Bağlaç | Anlam | Örnek |
|--------|-------|-------|
| **For** | çünkü | I stayed home, for I was tired. |
| **And** | ve | She sings and dances. |
| **Nor** | ne de | He doesn't smoke, nor does he drink. |
| **But** | ama | I tried, but I failed. |
| **Or** | veya | Tea or coffee? |
| **Yet** | ama, yine de | It's small, yet comfortable. |
| **So** | bu yüzden | It rained, so I stayed home. |

### Subordinating Conjunctions
| Kategori | Bağlaçlar |
|----------|-----------|
| **Zaman** | when, while, before, after, until, as soon as |
| **Neden** | because, since, as |
| **Zıtlık** | although, though, even though, whereas, while |
| **Koşul** | if, unless, provided that, as long as |
| **Amaç** | so that, in order that |

### 💡 Sınav İpuçları
- "Although/Though" + clause, "Despite/In spite of" + noun/gerund
- "Whereas" ve "While" zıtlık belirtir
- "Unless" = "If...not"
"""
    },
    "prepositions": {
        "name": "Prepositions (Edatlar)",
        "icon": "📍",
        "summary": """
## 📍 Prepositions (Edatlar)

### Sık Karıştırılan Edat Kalıpları

#### Sıfat + Edat
| Kalıp | Örnek |
|-------|-------|
| afraid **of** | She is afraid of spiders. |
| interested **in** | I'm interested in music. |
| good/bad **at** | He's good at math. |
| responsible **for** | She's responsible for the project. |
| similar **to** | This is similar to that. |
| different **from** | A is different from B. |

#### Fiil + Edat
| Kalıp | Örnek |
|-------|-------|
| depend **on** | It depends on you. |
| consist **of** | Water consists of H2O. |
| belong **to** | This belongs to me. |
| result **in** | It resulted in failure. |
| succeed **in** | She succeeded in passing. |
| apologize **for** | I apologize for being late. |

### Zaman Edatları
| Edat | Kullanım | Örnek |
|------|----------|-------|
| **at** | saat, gece, hafta sonu | at 5 o'clock, at night |
| **on** | gün, tarih | on Monday, on June 5th |
| **in** | ay, yıl, mevsim | in May, in 2024, in summer |

### 💡 Sınav İpuçları
- Bu kalıpları ezberle, boşluk doldurmada çok çıkar!
- "On time" (tam zamanında) vs "In time" (yetişerek)
- "At the end" (sonunda-fiziksel) vs "In the end" (sonunda-sonuç)
"""
    }
}

# ==================== ANA İÇERİK ====================
st.title("📚 Gramer Modülü")
st.markdown("YDS/YÖKDİL gramer konuları ve ders notları")

st.markdown("---")

# Konu seçimi - sidebar tarzı kartlar
st.subheader("📖 Konu Seç")

# Konu butonları
topic_keys = list(GRAMMAR_TOPICS.keys())
cols = st.columns(len(topic_keys))

# Session state for selected topic
if "selected_grammar_topic" not in st.session_state:
    st.session_state.selected_grammar_topic = "tenses"

for i, key in enumerate(topic_keys):
    topic = GRAMMAR_TOPICS[key]
    with cols[i]:
        if st.button(
            f"{topic['icon']}\n{topic['name'].split(' (')[0]}", 
            key=f"topic_{key}",
            use_container_width=True,
            type="primary" if st.session_state.selected_grammar_topic == key else "secondary"
        ):
            st.session_state.selected_grammar_topic = key
            st.rerun()

st.markdown("---")

# Seçili konu içeriği
selected = st.session_state.selected_grammar_topic
topic_info = GRAMMAR_TOPICS[selected]

# Konu başlığı
st.markdown(f"## {topic_info['icon']} {topic_info['name']}")

# Konu özeti
st.markdown(topic_info["summary"])

# Alt bilgi
st.markdown("---")
st.info("💡 **İpucu:** Gramer konularını öğrendikten sonra **Sınav Merkezi**'ndeki AI Quiz ile pratik yapabilirsiniz!")

# Footer
st.markdown("---")
st.caption("📚 Gramer çalışarak sınavda fark yarat!")
