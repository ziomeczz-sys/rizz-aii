import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACJA STRONY (Szeroki układ jak w ChatGPT) ---
st.set_page_config(page_title="RizzGPT", page_icon="💬", layout="wide", initial_sidebar_state="expanded")

# --- 2. ZAAWANSOWANY CSS (Klonowanie wyglądu ChatGPT z szarym tłem) ---
st.markdown("""
<style>
    /* Ukrycie standardowych śmieci Streamlita */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* GŁÓWNE TŁO APLIKACJI NA SZARO */
    [data-testid="stAppViewContainer"] {
        background-color: #2b2b2b !important; 
    }
    
    /* Panel boczny - trochę ciemniejszy szary dla kontrastu */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e !important;
    }
    
    /* Wyśrodkowanie okna czatu */
    .block-container {
        max-width: 800px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Pasek do wpisywania tekstu */
    [data-testid="stChatInput"] {
        background-color: #3b3b3b !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 5px 15px !important;
    }
    
    /* Użytkownik - jasnoszare, zaokrąglone tło po prawej stronie */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #3b3b3b;
        border-radius: 20px;
        padding: 10px 20px;
        margin-bottom: 15px;
    }

    /* AI - brak tła, czysty tekst */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: transparent;
        padding: 10px 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PODŁĄCZENIE "MÓZGU" ---
klucz_api = "WLEJ_TUTAJ_SWOJ_KLUCZ" # <--- PAMIĘTAJ O WKLEJENIU SWOJEGO KLUCZA!
genai.configure(api_key=klucz_api)

# --- 4. PANEL BOCZNY (Sidebar) ---
with st.sidebar:
    # Przycisk "Nowy czat"
    if st.button("➕ Nowy czat", use_container_width=True, type="primary"):
        st.session_state.chat_session = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("⚙️ **Twój RizzGPT**")
    st.info("Historia czatu resetuje się po odświeżeniu strony (wersja bez bazy danych).")
    
    # Puste linie HTML zamiast błędu st.spacer()
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("Tryb: **Pro Rizz 2.5**")

# --- 5. USTAWIENIA AI ---
system_prompt = """
Jesteś inteligentnym, wyluzowanym asystentem. Pomagasz pisać wiadomości z "rizz". 
Pisz naturalnie, konkretnie i z humorem. Odpowiadaj krótko.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    system_instruction=system_prompt
)

if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = model.start_chat(history=[])

# Jeśli czat jest pusty, wyświetl logo na środku (jak w ChatGPT)
if len(st.session_state.chat_session.history) == 0:
    st.markdown("<h1 style='text-align: center; margin-top: 10vh;'>💬 RizzGPT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>W czym mogę pomóc?</p>", unsafe_allow_html=True)

# --- 6. WYŚWIETLANIE CZATU ---
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    avatar = "👤" if role == "user" else "✨"
    with st.chat_message(role, avatar=avatar):
        st.write(message.parts[0].text)

# --- 7. WPISYWANIE WIADOMOŚCI ---
user_input = st.chat_input("Zapytaj o cokolwiek...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    with st.chat_message("assistant", avatar="✨"):
        response = st.session_state.chat_session.send_message(user_input)
        st.write(response.text)