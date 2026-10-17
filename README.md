# StudyLens — AI Study Companion

StudyLens turns lecture notes, screenshots, and pasted text into clear explanations, revision notes, practice quizzes, and concept summaries. It uses Gemma 4 through the Gemini API and provides a small, usable Streamlit interface.

## Features

- Upload a photo or screenshot of study material
- Paste text or combine text with an image
- Choose an output: simple explanation, revision notes, practice quiz, key concepts, or diagram explanation
- Choose the learner level and response language
- Download the generated study guide as Markdown
- Prompt instructions ask the model to flag unreadable content rather than invent details

## Requirements

- Python 3.10 or newer
- A Google AI Studio API key with access to the selected Gemma model
- Internet connection while making API requests

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then add your API key. The app automatically loads the `.env` file. Then run:

```bash
streamlit run app.py
```

Default model: `gemma-4-26b-a4b-it`. If the challenge instructions specify another model, or your API account cannot access this one, set `GEMMA_MODEL` to a supported Gemma 4 model.

## Security

- Never commit `.env`, API keys, or private study documents.
- The uploaded image and text are sent to the configured model API for processing.
- Avoid uploading personal, confidential, or sensitive information.

## Demo script (about 60–90 seconds)

1. Upload a clear photo of a page of notes or a lecture diagram.
2. Select **Explain simply** and choose **Beginner**.
3. Click **Create my study guide** and show the explanation grounded in the uploaded material.
4. Switch to **Make a practice quiz**, run it again, and show the answer key.
5. Download the guide as Markdown.

## Project status

This is a prototype starter, not a verified production deployment. Test it with your own API key, inspect the generated output, and record a real demo before submitting it. Add your name, screenshots, and any improvements you personally make to the repository.

## Open source

Released under the MIT License. See `LICENSE`.

## Acknowledgements

- Google DeepMind for the Gemma open-weight model family
- Google Gen AI Python SDK
- Streamlit
