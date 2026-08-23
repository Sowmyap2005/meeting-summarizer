import os
import tempfile

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
            model="whisper-1",
            file=f,
        )
    return result.text


def summarize(transcript):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT.format(transcript=transcript)}],
    )
    return response.choices[0].message.content


st.title("Meeting Summarizer")

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
        finally:
            os.remove(tmp_path)

        st.subheader("Summary")
        st.write(summary)

        with st.expander("Full transcript"):
            st.write(transcript)

        st.download_button("Download transcript", transcript, "transcript.txt")
        st.download_button("Download summary", summary, "summary.txt")
