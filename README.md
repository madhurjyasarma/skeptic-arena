# ⚔️ The Skeptic Arena

> **Stress-test your startup ideas, feature proposals, and pitches against an adversarial vector memory bank.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://skeptic-arena.streamlit.app/)

---

## Deployment link - https://skeptic-arena.streamlit.app/
# Click above link to view the app

## 💡 What is The Skeptic Arena?

Most AI pitch feedback is polite, accommodating, and generic. **The Skeptic Arena** is engineered to do the exact opposite: ruthlessly expose structural weaknesses before the market does.

When you submit a concept, the app doesn't just prompt an LLM blindly. It queries an embedded **ChromaDB vector database** loaded with real-world failure patterns (defensibility moats, customer acquisition traps, enterprise inertia, retention leaks). It retrieves the exact fatal flaw matching your idea's semantic coordinates, delivers a biting critique, and challenges you to defend your thesis in an interactive survival duel.

---

## ⚡ Architecture

```text
       User Pitch
           │
           ▼
┌──────────────────────┐
│  ChromaDB Vector DB  │ ──► Cosine Similarity Search for Nearest
└──────────────────────┘     Failure Archetype (Objection Vector)
           │
           ▼
┌──────────────────────┐
│   Groq LPU Engine    │ ──► Synthesizes Tactical Attack
│ (openai/gpt-oss-120b)│
└──────────────────────┘
           │
           ▼
┌──────────────────────┐
│ Streamlit Interface  │ ──► Interactive Combat Floor &
└──────────────────────┘     Survival Score Rating (0-100%)
```

- **Frontend & UI:** Streamlit
- **Vector Engine:** ChromaDB (`all-MiniLM-L6-v2` embeddings)
- **Cloud LLM Inference:** Groq Cloud API (`openai/gpt-oss-120b` or `llama-3.1-8b-instant`)
- **Local LLM Inference (Optional):** Ollama (`llama3.2`)

---

## 🚀 Quickstart (Local Development)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/skeptic-arena.git
cd skeptic-arena
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.streamlit/secrets.toml` file or set an environment variable:

```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"
```

*(Get a free key with no credit card at [console.groq.com](https://console.groq.com).)*

### 4. Run Locally
```bash
streamlit run app.py
```

---

## 🌐 Deploy to Streamlit Cloud ($0 Stack)

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and click **"New app"**.
3. Select your repo, branch (`main`), and target file (`app.py`).
4. Under **Advanced settings > Secrets**, paste your key:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key"
   ```
5. Click **Deploy!**

---

## 🧠 Core Failure Vectors Indexed

ChromaDB evaluates pitches across key vector archetypes:
* **Defensibility:** Thin API wrapper vulnerability and native platform risk.
* **Go-To-Market:** Customer Acquisition Cost (CAC) outstripping Lifetime Value (LTV).
* **Behavior Change:** User habit inertia vs. marginal improvement.
* **Product-Market Fit:** "Vitamin vs. Painkiller" discretionary spending risks.
* **Retention Leaks:** Initial novelty spike masking 60-day cohort churn.
* **Trust & Liability:** Hallucination tolerance in critical workflows.


Evaluate this defense:
1. Did they genuinely solve the vulnerability or just deflect?
2. Give a Survival Rating between 0% and 100%.

Format output strictly as:
SURVIVAL RATING: [Score]%
VERDICT: [1 sentence blunt verdict]
TACTICAL FIX: [1 concrete piece of advice]
"""
                    eval_response = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": eval_prompt}],
                        model="openai/gpt-oss-120b",
                        temperature=0.2
                    )
                    st.divider()
                    st.markdown("### Combat Evaluation")
                    st.write(eval_response.choices[0].message.content)
```

---

## 📦 Requirements (`requirements.txt`)

```text
streamlit>=1.35.0
chromadb>=0.5.0
groq>=0.9.0
```

---

## 📄 License

MIT License. Free for personal, commercial, and educational use.
