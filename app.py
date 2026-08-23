import os
import tempfile

import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    timeout=180.0,
    max_retries=3,
)

PROMPT = """Summarize this meeting transcript.

Return three sections:
1. Summary
2. Key Decisions
3. Action Items (include owner and deadline if mentioned)

Transcript:
{transcript}
"""


def transcribe(audio_path):
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f,
        )
    return result.text


def summarize(transcript):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": PROMPT.format(transcript=transcript)}],
    )
    return response.choices[0].message.content


st.title("Meeting Summarizer")

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY is not set. Set it and restart the app.")
    st.stop()

uploaded = st.file_uploader("Upload meeting audio", type=["mp3", "wav", "m4a"])

if uploaded is not None:
    if st.button("Process"):
        suffix = os.path.splitext(uploaded.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        try:
            with st.spinner("Transcribing..."):
                transcript = transcribe(tmp_path)

            with st.spinner("Summarizing..."):
                summary = summarize(transcript)
        except Exception as e:
            st.error(f"{type(e).__name__}: {e}")
            st.error(f"Cause: {e.__cause__!r}")
            st.stop()
        finally:
            os.remove(tmp_path)

        st.subheader("Summary")
        st.write(summary)

        with st.expander("Full transcript"):
            st.write(transcript)

        st.download_button("Download transcript", transcript, "transcript.txt")
        st.download_button("Download summary", summary, "summary.txt")