# 🔮 TarotTara - AI-Powered Tarot Reading System

**TarotTara** is an intelligent tarot reading system powered by AI that provides personalized tarot card readings and interpretations. The system understands user questions, classifies intent, draws appropriate cards, and returns insightful readings in both text and voice — with support for multiple languages.

---

## 🌟 Features

- 🧠 **Smart Intent Detection** — Classifies questions (yes/no, timeline, insight, etc.)
- 🃏 **Dynamic Tarot Card Readings** — Randomized draws with AI-based interpretations
- 📅 **Timeline Predictions** — Date-range predictions using numeric cards
- 🌐 **Multilingual Support** — English, Hindi, Spanish, French (input & output)
- 🔊 **Voice Input & Output** — Ask questions using voice; get voice answers
- 📁 **PDF Log Generation** — Stores user session info in a downloadable PDF
- ⚡ **Streamlit UI Support** — Web interface with voice, audio upload, and more

---

## 🛠️ Prerequisites

- Python 3.10 or above
- [Ollama](https://ollama.com/) (to run the LLaMA 3 model locally)
- PDF files containing tarot card meanings (e.g., `1.pdf`, `2.pdf`)

---

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd AI-Tarot

# Install dependencies
pip install -r requirements.txt
⚙️ Ollama Setup
bash
Copy
Edit
# Download and install Ollama (https://ollama.com/)
# Then pull the LLaMA 3 model
ollama pull llama3
🚀 Usage
🔸 Terminal-based App
bash
Copy
Edit
python main.py
Sample Questions:

"Will I get a promotion this year?"

"When will I find true love?"

"What should I focus on in my career?"

"Why am I feeling stuck?"

🔸 Web App with Streamlit
bash
Copy
Edit
streamlit run temp_main.py
Features:

Upload voice or type questions

Display tarot results with card visuals, voice playback, multilingual support

📚 Project Structure
graphql
Copy
Edit
AI-Tarot/
├── main.py                  # Terminal-based chatbot
├── temp_main.py            # Streamlit-based web UI
├── config.py               # Model and path configs
├── requirements.txt        # Required libraries
├── README.md               # Project documentation

├── deck.py                 # Tarot deck definitions & date logic
├── decorators.py           # Utility decorators (e.g., log_timing)

├── intent/
│   └── intent.py           # Intent classification using LLaMA + rules

├── tarot/
│   └── tarot_reader.py     # Reading engine: draw cards + generate interpretation

├── user_info/
│   ├── user_info.py        # User info collection (terminal)
│   └── pdf_export.py       # Save user info as PDF

├── voice/
│   ├── input.py            # Audio recording/transcription
│   └── output.py           # Text-to-speech and replay

├── data/
│   ├── tarot_cards/        # Individual PDF files for each card
│   └── tarot_guide.pdf     # Merged PDF file for reference

├── rag/
│   ├── rag.py              # Vector DB & card meaning retrieval

└── utils/
    └── merge_tarot_pdfs.py # Merges individual card PDFs
💻 Core Components
🧠 Intent Classification (intent/intent.py)
Classifies natural language into categories like:

yes_no, timeline, guidance, general, factual

🔮 Tarot Reading Engine (tarot/tarot_reader.py)
Draws cards (1 for timeline, 3 for general)

Uses LangChain + LLaMA to interpret cards

Adds context from PDF-based RAG if needed

📘 Knowledge Base RAG (rag/rag.py)
Processes PDFs (1.pdf, 2.pdf)

Uses sentence embeddings + ChromaDB for similarity search

🗣️ Voice Interaction (voice/)
input.py: record from mic or transcribe uploaded audio

output.py: synthesize voice from text, replay on demand

🧾 User Logging (user_info/)
Captures user session info

Stores as PDF using fpdf

🤝 Contributing
We welcome contributions from the open-source community!
Create an issue or open a Pull Request.

📝 License
This project is licensed under the MIT License — see the LICENSE file for details.

⚠️ Disclaimer
TarotTara is intended for entertainment and self-reflection only. It should not replace professional legal, medical, or psychological advice.

yaml
Copy
Edit

---

### ✅ Next Steps

Once you save this:

```bash
