"""
Groq Service
AI-powered sentence generation using Groq API (Llama 3.1)
"""

import streamlit as st
from typing import Optional, Dict, Any
import json

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

from utils.constants import GROQ_SETTINGS, SYSTEM_PROMPTS


@st.cache_resource
def get_groq_client():
    """Groq client'ı başlat ve cache'le"""
    if not GROQ_AVAILABLE:
        return None
    
    try:
        api_key = st.secrets.get("groq", {}).get("api_key")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Groq bağlantı hatası: {str(e)}")
        return None


def generate_example_sentence(word: str, word_type: str = "noun", turkish: str = "") -> Optional[Dict[str, str]]:
    """
    Verilen kelime için YDS formatında örnek cümle ve Türkçe çevirisi oluştur
    
    Args:
        word: İngilizce kelime
        word_type: Kelime türü (noun, verb, adj, vb.)
        turkish: Türkçe anlamı (bağlam için)
    
    Returns:
        Dict with 'english' and 'turkish' sentences or None
    """
    client = get_groq_client()
    if not client:
        return None
    
    try:
        # Bağlam bilgisi ekle
        word_context = f"Kelime: {word}"
        if word_type:
            word_context += f" (tür: {word_type})"
        if turkish:
            word_context += f" - Türkçe anlamı: {turkish}"
        
        system_prompt = """Sen bir YDS/İngilizce sınav uzmanısın. Verilen kelimeyi kullanarak akademik ve resmi dilde, sınav formatına uygun bir İngilizce cümle oluştur ve Türkçe çevirisini de yaz.

Kurallar:
1. Cümle 15-25 kelime arasında olsun
2. Akademik/resmi dil kullan
3. Cümle bağlamdan anlaşılır olsun
4. Kelimeyi doğru gramatikal yapıda kullan
5. Türkçe çeviri doğru ve akıcı olsun

SADECE aşağıdaki JSON formatında yanıt ver, başka hiçbir şey ekleme:
{"english": "İngilizce cümle buraya", "turkish": "Türkçe çeviri buraya"}"""

        response = client.chat.completions.create(
            model=GROQ_SETTINGS["model"],
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": word_context
                }
            ],
            max_tokens=250,
            temperature=GROQ_SETTINGS["temperature"]
        )
        
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content.strip()
            
            # JSON parse et
            try:
                # Bazen model JSON'u code block içinde döndürebilir
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                content = content.strip()
                result = json.loads(content)
                
                if "english" in result and "turkish" in result:
                    return result
            except json.JSONDecodeError:
                # JSON parse edilemezse, sadece İngilizce olarak döndür
                sentence = content.strip('"\'')
                return {"english": sentence, "turkish": ""}
        
        return None
    
    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg:
            st.warning("⚠️ API limit aşıldı. Lütfen biraz bekleyip tekrar deneyin.")
        elif "invalid api key" in error_msg:
            st.error("❌ Geçersiz Groq API anahtarı.")
        else:
            st.error(f"AI hatası: {str(e)}")
        return None


def generate_sentence_completion_question(word: str, word_type: str = "noun") -> Optional[Dict[str, Any]]:
    """
    Cümle tamamlama sorusu oluştur
    
    Args:
        word: Doğru cevap olacak kelime
        word_type: Kelime türü
    
    Returns:
        Dict with sentence, correct answer, and options
    """
    client = get_groq_client()
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model=GROQ_SETTINGS["model"],
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPTS["sentence_completion"]
                },
                {
                    "role": "user",
                    "content": f"Kelime: {word} (tür: {word_type})"
                }
            ],
            max_tokens=200,
            temperature=0.8
        )
        
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content.strip()
            
            # JSON parse et
            try:
                # Bazen model JSON'u code block içinde döndürebilir
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                result = json.loads(content)
                
                # Gerekli alanları kontrol et
                if all(key in result for key in ["sentence", "correct", "options"]):
                    return result
            except json.JSONDecodeError:
                pass
        
        return None
    
    except Exception as e:
        st.error(f"Soru oluşturma hatası: {str(e)}")
        return None


def generate_word_explanation(word: str, turkish: str) -> Optional[str]:
    """
    Kelime için kısa açıklama oluştur
    
    Args:
        word: İngilizce kelime
        turkish: Türkçe anlamı
    
    Returns:
        Türkçe açıklama
    """
    client = get_groq_client()
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model=GROQ_SETTINGS["model"],
            messages=[
                {
                    "role": "system",
                    "content": """Sen bir İngilizce öğretmenisin. Verilen kelime için Türkçe kısa bir açıklama yaz.
Açıklama:
- En fazla 2 cümle olsun
- Kelimenin kullanım bağlamını açıkla
- Türkçe yaz"""
                },
                {
                    "role": "user",
                    "content": f"Kelime: {word}\nTürkçe karşılık: {turkish}"
                }
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        
        return None
    
    except Exception as e:
        return None


def check_groq_availability() -> bool:
    """Groq API'nin kullanılabilir olup olmadığını kontrol et"""
    if not GROQ_AVAILABLE:
        return False
    
    client = get_groq_client()
    return client is not None


def get_ai_hint(word: str, context: str = "") -> Optional[str]:
    """
    Kelime için hafıza tekniği/ipucu oluştur
    
    Args:
        word: İngilizce kelime
        context: Ek bağlam
    
    Returns:
        Hafıza ipucu
    """
    client = get_groq_client()
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model=GROQ_SETTINGS["model"],
            messages=[
                {
                    "role": "system",
                    "content": """Sen yaratıcı bir dil öğretmenisin. Verilen İngilizce kelimeyi hatırlamak için eğlenceli ve akılda kalıcı bir Türkçe ipucu oluştur.
İpucu:
- Ses benzerliği kullanabilirsin (örn: 'abandon' = 'aban don' gibi)
- Görsel çağrışım yapabilirsin
- Kısa ve akılda kalıcı olsun
- Sadece ipucunu yaz, başka açıklama ekleme"""
                },
                {
                    "role": "user",
                    "content": f"Kelime: {word}\n{context}"
                }
            ],
            max_tokens=80,
            temperature=0.9
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        
        return None
    
    except Exception as e:
        return None
