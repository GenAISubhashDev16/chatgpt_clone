# AI Chat Assistant — ChatGPT Clone

A ChatGPT-inspired AI chatbot built using Python, Streamlit, LangChain, Groq API, and SQLite. The application supports real-time AI response streaming and persistent conversation history.

## 1. Project Overview

The goal of this project is to build an AI-powered chat application with a clean interface and reusable backend architecture.

### Features

- ChatGPT-style conversational interface.
- Create and manage multiple conversations.
- Save chat history in SQLite.
- Load previous conversations.
- Stream AI responses in real time.
- Display response-generation progress.
- Generate conversation titles automatically.
- Integrate Groq LLM through LangChain.
- Modular and reusable Python architecture.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | User interface |
| LangChain | LLM integration and prompt management |
| Groq API | AI response generation |
| SQLite | Conversation and message storage |
| python-dotenv | Environment variable management |
| uv | Python package and project management |

## 3. Project Architecture

```text
chatgpt_clone/
│
├── app.py
├── README.md
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── chat_repository.py
│
├── services/
│   ├── __init__.py
│   ├── prompt_service.py
│   ├── llm_service.py
│   └── chat_service.py
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py
│   ├── chat_interface.py
│   └── thinking_animation.py
│
└── data/
    └── chat_history.db
```

## 4. Prerequisites

Before starting, install:

- Python 3.12 or a compatible version supported by the project dependencies.
- Git.
- uv package manager.
- A Groq API key.

Install uv:

```powershell
pip install uv
```

Verify installations:

```powershell
python --version
uv --version
git --version
```

## 5. Clone the Repository

```powershell
git clone https://github.com/GenAISubhashDev16/chatgpt_clone
cd chatgpt_clone
```



## 6. Install Dependencies

```powershell
uv sync
```

## 7. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Get your API key from:

https://console.groq.com/keys



```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

**Important:** Never upload your actual `.env` file or API key to GitHub. Make sure `.env` is included in `.gitignore`.

## 8. Database

The application uses SQLite to store conversations and messages.

Database tables are created automatically when the application starts.

Database location:

```text
data/chat_history.db
```

## 9. Run the Application

Start the Streamlit application:

```powershell
uv run streamlit run app.py
```

Open your browser:

http://localhost:8501

## 10. How to Use the Application

1. Open the application in your browser.
2. Click **New Chat** in the sidebar.
3. Enter your question in the chat input.
4. Wait for the AI response to stream.
5. View your conversation in the main chat window.
6. Select an older conversation from the sidebar to continue it.
7. Refresh the browser and verify that your chat history is still available.

## 11. Application Workflow

```text
             User
               |
               v
       Streamlit Interface
               |
               v
         Sidebar / Chat UI
               |
               v
          Chat Service
               |
        +------+------+
        |             |
        v             v
   SQLite Database  Prompt Service
                      |
                      v
                  LLM Service
                      |
                      v
                   Groq API
                      |
                      v
               Streamed Response
                      |
                      v
               SQLite Database
```

## 12. Troubleshooting

### GROQ_API_KEY is missing

Check that `.env` exists in the project root and contains a valid API key.

### ModuleNotFoundError

Run commands from the project root and use module execution where appropriate:

```powershell
uv run python -m services.chat_service
```

Make sure package folders contain `__init__.py`.

### Streamlit command not found

Run Streamlit through uv:

```powershell
uv run streamlit run app.py
```

### Database errors

Check that the application has permission to create files inside the `data` directory.

## 13. GitHub: Upload Your Changes

Check Git status:

```powershell
git status
```

Add files:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Update project documentation"
```

Push to GitHub:

```powershell
git push origin main
```

## 14. Future Improvements

- Chat deletion and renaming in the sidebar.
- Custom ChatGPT-inspired CSS design.
- Markdown and code syntax highlighting.
- Copy response functionality.
- Regenerate AI responses.
- Export conversation history.
- User authentication.
- File upload and document-based RAG.
- AI agents and tool integration.
- Support for multiple LLM providers.

## 15. Learning Objectives

This project provides practical experience with:

- Python application architecture.
- Building LLM-powered applications.
- LangChain prompt templates.
- Streaming AI responses.
- SQLite database integration.
- Session state management in Streamlit.
- API integration and environment variables.
- Modular application development.

---

**Author:** Subhash Verma

**Project:** AI Chat Assistant — ChatGPT Clone

**Status:** Core application development

**License:** MIT (add a LICENSE file if you choose to distribute the project under this license).
