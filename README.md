# Meeting Summarizer

Upload a meeting audio file. The app transcribes it and produces a summary with
key decisions and action items.

## How it works

1. Audio is uploaded through a Streamlit page.
2. The file is sent to the OpenAI Whisper API for transcription.
3. The transcript is sent to an LLM with a prompt that asks for a summary,
   key decisions, and action items.
4. The transcript and summary are shown on the page and can be downloaded.

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
streamlit run app.py
```

## Files

- `app.py` — the whole application (upload, transcription, summarization, display)
- `requirements.txt` — dependencies

## Prompt used

```
Summarize this meeting transcript.

Return three sections:
1. Summary
2. Key Decisions
3. Action Items (include owner and deadline if mentioned)
```

## Supported formats

mp3, wav, m4a

## Limitations

- No database. Results are not stored between sessions.
- No speaker diarization.
- Long audio files are sent in a single request and may hit API size limits.
