import streamlit as st
import google.generativeai as genai

# Setup page
st.set_page_config(page_title="STK-JAIM AI", page_icon="🚗")

st.title("🚗 Sistem Tempahan Kenderaan (AI)")
st.write("Tanya apa sahaja tentang tempahan kenderaan.")

# --- BAHAGIAN RAHSIA (API KEY) ---
# Kita akan set kunci ni dalam setting Streamlit nanti
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key tak jumpa. Sila set dalam Streamlit Secrets.")
    st.stop()

# --- SETUP OTAK AI ---
# Masukkan arahan system (prompt) awak di sini
system_instruction = """
Awak adalah pembantu AI untuk Sistem Tempahan Kenderaan JAIM (STK-JAIM).
Jawab soalan pengguna dengan sopan dan ringkas.
Fokus kepada tempahan kenderaan rasmi jabatan.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tunjuk chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bila user taip sesuatu
if prompt := st.chat_input("Taip soalan anda di sini..."):
    # Simpan soalan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Jawab
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        
    # Simpan jawapan AI
    st.session_state.messages.append({"role": "assistant", "content": response.text})
