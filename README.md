🎬 Movie Recommender

An AI-powered movie and TV series discovery platform that helps users find content based on genre, country, mood, year, and rating — using natural language queries and an intelligent chat assistant.


Real-World Problem It Solves

People spend more time choosing what to watch than actually watching. Streaming platforms have thousands of titles but poor discovery tools. **Movie Recommender** solves this by:

- Letting users describe their mood in plain language ("I want something sad but beautiful")
- Filtering by country, genre, rating, and year simultaneously
- Using an AI agent (Ollama + llama3.2) to suggest titles by mood/occasion
- Supporting both Movies and TV Series in one unified search

---

Features

| Feature | Description |
|---|---|
| 🔍 Title Search | Search any movie or TV series by name |
| 🧙 AI Wizard | Step-by-step filter guide (genre, country, rating, year, mood) |
| 🤖 AI Chat | Ask the assistant anything — it suggests 3 bold-formatted titles |
| 💊 Quick Pills | One-click filters: Top Films, Trending, Korean, Horror, Anime... |
| 🎭 Mood Search | Type your mood and get AI-curated recommendations |
| 📺 TV Support | Toggle between movies and TV series |
| 🗂 Active Filters | Visual tags for applied filters with one-click removal |

---

System Architecture

```
User
 │
 ▼
index.html  ──── Search / Wizard / Chat
 │
 ▼
app.py (Flask)  ──── /api/search · /api/agent
 │               │
 ▼               ▼
api.py        agent.py
(TMDB API)    (Ollama llama3.2)
 │
 ▼
parser.py  (NLP filter extraction)
```

---


Diagram
<img width="1327" height="916" alt="image" src="https://github.com/user-attachments/assets/39252c06-dbc4-451e-b5fa-9ff805addd6e" />


Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3, Flask, Flask-CORS
- **Movie Data**: [TMDB API](https://www.themoviedb.org/documentation/api)
- **AI Agent**: [Ollama](https://ollama.com/) with `llama3.2` model
- **NLP Parser**: Custom regex-based query parser (`parser.py`)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/movie-recommender.git
cd movie-recommender
```

### 2. Install Python dependencies

```bash
pip install flask flask-cors requests
```

### 3. Install and run Ollama (for AI chat)

```bash
# Install Ollama from https://ollama.com
ollama pull llama3.2
ollama serve
```

### 4. Start the Flask server

```bash
python app.py
```

### 5. Open in browser

```
http://localhost:5000
```

---

## 📁 File Structure

```
movie-recommender/
├── index.html      # Frontend UI
├── app.py          # Flask server + routes
├── api.py          # TMDB API wrapper
├── parser.py       # NLP query parser
├── agent.py        # Ollama AI agent
└── README.md
```

---

## 🔑 API Key

The project uses the TMDB API. The key is already included in `api.py` for demo purposes. For production, replace it with your own key from [themoviedb.org](https://www.themoviedb.org/settings/api).

---


Made with using Claude (Anthropic), Flask, and TMDB API.

---

## 📄 License

MIT License — free to use and modify.
