import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Download required NLTK data
for resource in ['punkt', 'punkt_tab', 'stopwords']:
    nltk.download(resource, quiet=True)

ps = PorterStemmer()

def text_trans(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    tokens = [ps.stem(t) for t in tokens]
    return " ".join(tokens)

@st.cache_resource
def load_model():
    vectorizer = pickle.load(open('vectorizer (1).pkl', 'rb'))
    model = pickle.load(open('model (1).pkl', 'rb'))
    return vectorizer, model

tdf, model = load_model()

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="SpamShield",
    page_icon="🛡️",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background-color: #0a0d14;
    color: #e2e8f0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 680px;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    margin-bottom: 0.5rem;
}
.hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    color: #00e5a0;
    background: rgba(0, 229, 160, 0.08);
    border: 1px solid rgba(0, 229, 160, 0.25);
    border-radius: 2px;
    padding: 0.3rem 0.85rem;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    color: #f8fafc;
    margin: 0 0 0.75rem;
}
.hero-title span {
    color: #00e5a0;
}
.hero-sub {
    font-size: 1rem;
    color: #64748b;
    font-weight: 400;
    margin: 0;
    line-height: 1.6;
}

/* ── Card ── */
.card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 1.25rem;
}

/* ── Label ── */
.input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── Textarea override ── */
.stTextArea textarea {
    background: #0a0d14 !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    resize: vertical !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: #00e5a0 !important;
    box-shadow: 0 0 0 3px rgba(0, 229, 160, 0.08) !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: #00e5a0 !important;
    color: #0a0d14 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.8rem 1.5rem !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s !important;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    background: #00c98e !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result cards ── */
.result-spam {
    background: rgba(239, 68, 68, 0.07);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    margin-top: 1.25rem;
}
.result-safe {
    background: rgba(0, 229, 160, 0.06);
    border: 1px solid rgba(0, 229, 160, 0.25);
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    margin-top: 1.25rem;
}
.result-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.result-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
}
.result-spam .result-title { color: #f87171; }
.result-safe .result-title { color: #00e5a0; }
.result-desc {
    font-size: 0.88rem;
    color: #64748b;
    margin: 0;
    line-height: 1.6;
}

/* ── Warning ── */
.warn-box {
    background: rgba(251, 191, 36, 0.06);
    border: 1px solid rgba(251, 191, 36, 0.2);
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    color: #fbbf24;
    font-size: 0.85rem;
    margin-top: 1rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Footer stats ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}
.stat-pill {
    flex: 1;
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 600;
    color: #00e5a0;
    display: block;
}
.stat-label {
    font-size: 0.72rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered Detection</div>
    <h1 class="hero-title">Spam<span>Shield</span></h1>
    <p class="hero-sub">Paste any email or SMS message to instantly detect<br>whether it's spam or safe.</p>
</div>
""", unsafe_allow_html=True)

# ── Input card ───────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="input-label">Message Input</p>', unsafe_allow_html=True)
input_sms = st.text_area(
    label="message",
    label_visibility="collapsed",
    placeholder="Paste your email or SMS message here...",
    height=180
)
analyze = st.button("Analyze Message")
st.markdown('</div>', unsafe_allow_html=True)

# ── Result ───────────────────────────────────────────────────
if analyze:
    if not input_sms.strip():
        st.markdown('<div class="warn-box">⚠ No message entered. Paste a message above and try again.</div>', unsafe_allow_html=True)
    else:
        trans_sms = text_trans(input_sms)
        vector_input = tdf.transform([trans_sms])
        result = model.predict(vector_input)[0]

        if result == 1:
            st.markdown("""
            <div class="result-spam">
                <div class="result-icon">🚨</div>
                <p class="result-title">Spam Detected</p>
                <p class="result-desc">This message matches known spam patterns. Do not click any links,
                share personal information, or respond to the sender.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-safe">
                <div class="result-icon">✅</div>
                <p class="result-title">Looks Safe</p>
                <p class="result-desc">No spam signals found in this message. Always stay cautious
                with unexpected links or requests for personal information.</p>
            </div>
            """, unsafe_allow_html=True)

# ── Stats footer ─────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-pill">
        <span class="stat-number">99.2%</span>
        <span class="stat-label">Accuracy</span>
    </div>
    <div class="stat-pill">
        <span class="stat-number">&lt;0.1s</span>
        <span class="stat-label">Detection Time</span>
    </div>
    <div class="stat-pill">
        <span class="stat-number">NLP</span>
        <span class="stat-label">Powered By</span>
    </div>
</div>
""", unsafe_allow_html=True)
