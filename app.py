import os
import streamlit as st
import chromadb
from groq import Groq

st.set_page_config(page_title="Skeptic Arena", page_icon="⚔️", layout="wide")

# 1. Initialize Groq Client (Reads from Streamlit Secrets or Environment)
groq_api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

if not groq_api_key:
    st.error("Missing Groq API Key! Please configure GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

groq_client = Groq(api_key=groq_api_key)

# 2. ChromaDB Setup with Auto-Seeding for Cloud Environments
@st.cache_resource
def init_chroma():
    client = chromadb.PersistentClient(path="./chroma_store")
    collection = client.get_or_create_collection(name="skeptic_objections")
    
    if collection.count() == 0:
        objections = [
            {"id": "obj_wrapper", "cat": "Defensibility", "text": "This is a thin wrapper around a foundational model. The moment the underlying provider updates their native UI, your entire competitive advantage disappears."},
            {"id": "obj_distribution", "cat": "Go-To-Market", "text": "Building the product is easy; customer acquisition is the real bottleneck. CAC will quickly outpace lifetime value."},
            {"id": "obj_inertia", "cat": "Behavior Change", "text": "Habit and workflow inertia are undefeated. Your solution is slightly better, but switching requires 10x the effort. Users will default to old habits."},
            {"id": "obj_nice_to_have", "cat": "Product-Market Fit", "text": "This is a discretionary vitamin, not a painkiller. During budget tightening, tools like this are cancelled first."},
            {"id": "obj_retention_leak", "cat": "Economics", "text": "You will get an early novelty spike, but zero recurring daily utility. Churn will hollow out the user base within 60 days."},
            {"id": "obj_trust_liability", "cat": "Risk & Trust", "text": "AI hallucinations and edge-case errors will destroy user trust. One critical failure in high-stakes workflows ruins the brand permanently."}
        ]
        collection.upsert(
            ids=[item["id"] for item in objections],
            documents=[item["text"] for item in objections],
            metadatas=[{"category": item["cat"]} for item in objections]
        )
    return collection

collection = init_chroma()

# 3. Streamlit Interface & State
st.title("⚔️ The Skeptic Arena")
st.caption("Stress-test your pitch. ChromaDB pulls the fatal vulnerability; Llama 3 delivers the critique.")

if "objection" not in st.session_state:
    st.session_state.objection = None
if "closest_category" not in st.session_state:
    st.session_state.closest_category = None

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Enter Your Thesis")
    pitch = st.text_area(
        "Describe your product or idea:",
        placeholder="e.g., An AI note-taking extension that summarizes meetings into calendar tasks...",
        height=140
    )
    
    if st.button("Unleash the Skeptic", type="primary", use_container_width=True):
        if not pitch.strip():
            st.warning("Enter a proposal first.")
        else:
            with st.spinner("Searching semantic objection vectors..."):
                results = collection.query(query_texts=[pitch], n_results=1)
                retrieved_objection = results["documents"][0][0]
                category = results["metadatas"][0][0]["category"]
                
                st.session_state.closest_category = category

                prompt = f"""
You are an uncompromising venture partner and product strategist.
The user is pitching: "{pitch}"

Our vector intelligence detected this vulnerability:
"{retrieved_objection}" (Category: {category})

Deliver a punchy, ruthless, 3-sentence attack applying this vulnerability directly to their pitch.
"""
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-120b",
                    temperature=0.5
                )
                st.session_state.objection = chat_completion.choices[0].message.content

with col2:
    st.subheader("2. The Arena Floor")
    if st.session_state.objection:
        st.info(f"**Vulnerability Vector:** {st.session_state.closest_category}")
        st.error(f"**The Skeptic's Attack:**\n\n{st.session_state.objection}")
        
        defense = st.text_area("Your Counter-Strategy:", placeholder="How do you neutralize this flaw?", height=100)
        
        if st.button("Submit Counter-Move", use_container_width=True):
            if not defense.strip():
                st.warning("State your defense.")
            else:
                with st.spinner("Evaluating defense..."):
                    eval_prompt = f"""
Original pitch: "{pitch}"
The attack: "{st.session_state.objection}"
User defense: "{defense}"

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