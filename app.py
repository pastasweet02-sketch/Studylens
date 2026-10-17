import os
from io import BytesIO

import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.set_page_config(page_title="StudyLens | AI Study Companion", page_icon="📚", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1050px; padding-top: 2rem;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#18233d,#354f7d); color: white; margin-bottom: 1.2rem;}
.hero h1 {font-size: 2.4rem; margin: 0; color: white;}
.hero p {font-size: 1.05rem; margin: .5rem 0 0 0; color: #e7edfa;}
</style>
<div class="hero"><h1>StudyLens</h1><p>Turn lecture material into understanding — not just more pages to memorize.</p></div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Study settings")
    task = st.selectbox("What do you need?", [
        "Explain simply", "Create revision notes", "Make a practice quiz", "Find key concepts", "Explain a diagram"
    ])
    level = st.selectbox("Explanation level", ["Beginner", "Intermediate", "Detailed"])
    language = st.selectbox("Answer language", ["English", "Simple English", "Urdu", "Roman Urdu"])
    st.caption("StudyLens uses Gemma 4 through the Gemini API. Your API key stays on your device when running locally; never publish it.")

st.write("Upload a photo or screenshot of your notes, or paste the text below. You can use both.")
col1, col2 = st.columns([1, 1])
with col1:
    uploaded = st.file_uploader("Upload notes or a lecture screenshot", type=["png", "jpg", "jpeg", "webp"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded study material", use_container_width=True)
with col2:
    text_input = st.text_area("Or paste lecture text", height=190, placeholder="Paste your notes, textbook excerpt, or a topic here…")
    extra = st.text_input("Optional focus", placeholder="e.g. explain the confusing part about contraposition")

st.info("Tip: For the best results, upload a clear, well-lit photo showing one page at a time.")

if st.button("Create my study guide", type="primary", use_container_width=True):
    if not uploaded and not text_input.strip():
        st.warning("Upload an image or paste some text first.")
        st.stop()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        st.error("No API key found. Add GEMINI_API_KEY to a .env file or your environment, then restart the app.")
        st.stop()

    task_instructions = {
        "Explain simply": "Explain the material in small, clear steps. Define unfamiliar terms and give one everyday example.",
        "Create revision notes": "Create concise, well-organized revision notes with headings, definitions, key facts, and common mistakes.",
        "Make a practice quiz": "Create 8 questions from the supplied material: a mix of multiple choice and short answer. Put the answer key in a separate section at the end.",
        "Find key concepts": "Identify the most important concepts, explain why they matter, and show how they connect.",
        "Explain a diagram": "Describe what is visible, explain the diagram's parts and relationships, and flag anything unreadable instead of guessing."
    }
    prompt = f"""You are StudyLens, a careful and supportive study assistant.
Use ONLY the supplied study material as the source for claims about its contents. If a word or detail is unreadable or missing, say so rather than inventing it. Clearly label any general background knowledge you add.

Requested task: {task_instructions[task]}
Learner level: {level}
Answer language: {language}
Additional focus: {extra or 'None'}

Structure the answer with useful headings and bullets. Keep it genuinely educational, not vague. End with a short 'Check your understanding' section containing two questions (unless the requested task is a quiz, in which case use the quiz format)."""

    with st.spinner("Reading your material and preparing your study guide…"):
        try:
            client = genai.Client(api_key=api_key)
            contents = [prompt]
            if uploaded:
                image_bytes = uploaded.getvalue()
                contents.append(types.Part.from_bytes(data=image_bytes, mime_type=uploaded.type))
            if text_input.strip():
                contents.append("Additional pasted notes:\n" + text_input.strip())
            response = client.models.generate_content(
                model=os.getenv("GEMMA_MODEL", "gemma-4-26b-a4b-it"),
                contents=contents,
                config=types.GenerateContentConfig(temperature=0.3),
            )
            answer = (response.text or "The model returned an empty answer. Please try again.").strip()
            st.session_state["studylens_answer"] = answer
            st.session_state["studylens_task"] = task
        except Exception as exc:
            st.error("The AI request failed. Check your API key, model access, internet connection, and try again.")
            st.caption(f"Technical detail: {exc}")

if st.session_state.get("studylens_answer"):
    st.divider()
    st.subheader("Your study guide")
    st.markdown(st.session_state["studylens_answer"])
    st.download_button(
        "Download study guide (.md)",
        data=st.session_state["studylens_answer"],
        file_name="studylens-study-guide.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.divider()
st.caption("StudyLens is a learning aid, not an authority. Verify important facts against your course materials. Do not upload private or sensitive documents.")
