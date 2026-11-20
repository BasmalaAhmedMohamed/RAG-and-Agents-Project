# 🤖 RAG and Agents Project

A collection of two practical projects built using Python, LangChain, OpenAI, and ChromaDB. These projects demonstrate fundamental concepts of **Retrieval-Augmented Generation (RAG), AI Agents, Tool Calling, and Conversational Memory**.

---

## 📌 Projects Overview

| Project | Description | Main Concepts |
|---|---|---|
| **RAG project: Ask Your Documents (RAG)** | A chatbot that answers questions using your own PDF and TXT documents and provides source references. | RAG, Embeddings, Vector Databases, Semantic Search |
| **Assistant Agent project: Teaching-Assistant Agent** | An AI agent that decides when to call Python tools and remembers previous conversations. | AI Agents, Tool Calling, Conversational Memory |

---

# 📚 RAG project: Ask Your Documents (RAG)

## 🎯 Overview

Ask Your Documents is a command-line chatbot that allows users to interact with their own PDF and TXT documents.

Instead of relying on the LLM's general knowledge, the chatbot retrieves relevant information from the provided documents and generates answers based only on the retrieved context.

It also provides source references after every answer, making the responses more transparent and traceable.

## ⚙️ How It Works

The project consists of two main processes:

### 1. Document Ingestion

Documents are processed and stored in a ChromaDB vector database.

**Pipeline:**

`Load Documents → Split into Chunks → Generate Embeddings → Store in ChromaDB`

- Load PDF files using PyPDFLoader.
- Load TXT files using TextLoader.
- Split documents into smaller chunks using RecursiveCharacterTextSplitter.
- Convert chunks into vector embeddings.
- Store the embeddings and metadata in ChromaDB.

### 2. Question Answering

When a user asks a question, the system retrieves relevant document chunks and passes them to the LLM.

**Pipeline:**

`User Question → Retriever → Relevant Chunks → Prompt → LLM → Answer + Sources`

Two retrieval strategies are supported:

- **Similarity Search:** Retrieves chunks based on semantic similarity.
- **MMR (Maximum Marginal Relevance):** Retrieves relevant chunks while encouraging diversity and reducing redundancy.

## ✨ Features

- Supports PDF and TXT documents.
- Automatic document loading and chunking.
- Vector embeddings and persistent ChromaDB storage.
- Similarity and MMR retrieval strategies.
- Context-based answer generation.
- Source file references in every answer.
- Page-level citations for PDF documents.
- Prevents unsupported answers using a strict prompt.

If the answer cannot be found in the provided documents, the chatbot responds:

`I don't know from the provided documents.`

### Additional Features
- Command-Line Search:Add a `--search` argument using argparse instead of relying only on `input()`.
- Page-Level Sources: Display the page number alongside each source when answering questions from PDFs.

## 🛠️ Technologies

- Python
- LangChain
- OpenAI API
- ChromaDB
- PyPDF
- RecursiveCharacterTextSplitter
- Vector Embeddings

## 📂 Project Structure

```text
RAG_project/
│
├── data/
│   ├── transformers_notes.txt
│   └── your_document.pdf
│
├── chroma_db/          # Generated automatically
│
├── config.py           # Configuration and settings
├── ingest.py           # Document ingestion pipeline
├── rag_chain.py        # Retriever, prompt, and RAG chain
└── ask.py              # Interactive chatbot
```

---

# 🧑‍🏫 Assistant Agent project: Teaching-Assistant Agent

## 🎯 Overview

Teaching-Assistant Agent is an intelligent command-line assistant that can understand user requests, decide when external tools are needed, execute Python functions, and remember previous messages within a conversation.

Unlike a basic chatbot, this agent can perform calculations, retrieve student grades, check the current date and time, and save notes.

It uses LangChain's agent capabilities and LangGraph's checkpointing mechanism to maintain conversational memory.

## ⚙️ How It Works

The agent follows a tool-calling workflow:

`User Message → LLM → Decision → Tool Execution → LLM → Final Answer`

For example:

**User:** What's the average of Mona's marks?

1. The agent identifies that it needs Mona's grades.
2. It calls `get_student_grades("mona")`.
3. It receives Math = 92 and AI = 81.
4. It decides to perform a calculation.
5. It calls `calculator("(92+81)/2")`.
6. It returns the final answer: **86.5**.

The agent also maintains conversation history using a thread ID.

## ✨ Features

### Built-in Python Tools

| Tool | Functionality |
|---|---|
| `calculator(expression)` | Performs safe mathematical calculations using Python AST. |
| `current_datetime()` | Returns the current date and time. |
| `get_student_grades(name)` | Retrieves student grades from a predefined dictionary. |
| `save_note(note)` | Saves notes to a local TXT file. |

### Conversational Memory

- Remembers previous messages within the same conversation.
- Uses `thread_id` to identify individual conversations.
- Understands references to previous messages.
- Supports multiple independent conversation threads.
- Uses `InMemorySaver` as the checkpointing mechanism.

### Additional Features
- Automatic tool selection by the LLM.
- Tool execution and result tracking.
- Verbose mode to display tool calls and their results.
- Safe mathematical calculations without using `eval()`.
- Interactive command-line chat interface.
- Read Notes Tool: Implement `read_notes()` to retrieve all previously saved notes. 
- Add Student Tool: Implement `add_student(name, math, ai)` to dynamically add students and their grades. 
- Persistent Memory: Replace `InMemorySaver` with `SqliteSaver` so conversation memory survives application restarts. 
- Project Integration: Connect the RAG project to the agent by implementing an `ask_documents(question)` tool. 

## 🔗 Connecting Both Projects

The integration bonus allows the Teaching-Assistant Agent to answer questions using the document knowledge base from Project 1.

Add a new tool:

```python
ask_documents(question)
```

This tool uses the RAG chain from Project 1 to retrieve information and generate document-grounded answers.

After integration, the agent can:

- Answer general conversational questions.
- Perform calculations.
- Retrieve student grades.
- Save and read notes.
- Answer questions using external documents through RAG.
- Decide automatically which tool is appropriate for each request.

This transforms the two independent projects into a more capable AI Teaching Assistant.

## 🛠️ Technologies

- Python
- LangChain
- OpenAI API
- Python AST
- InMemorySaver
- python-dotenv

## 📂 Project Structure

```text
Assistant Agent project/
│
├── tools.py       # Python functions available to the agent
├── agent.py       # Agent construction and configuration
├── main.py        # Interactive chatbot interface
└── notes.txt      # Generated automatically by save_note
```

---

## Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
```

# 🧪 Testing

## RAG project: RAG Test Cases

| Question | Expected Result |
|---|---|
| What is multi-head attention? | Answer from the provided notes with sources. |
| How many layers does the encoder have? | 6 layers with a source reference. |
| Why do we need positional encoding? | Attention has no notion of word order. |
| Who won the 2022 World Cup? | I don't know from the provided documents. |
| Empty input | Skip the question and ask again. |
| `exit` | Terminate the program. |

Test both MMR and Similarity retrieval modes.

## Assistant Agent project: Agent Test Cases

| User Input | Expected Result |
|---|---|
| My name is Ali. | Agent remembers the user's name. |
| What are Mona's grades? | Retrieves Math = 92 and AI = 81. |
| What's the average of her two marks? | Calculates 86.5 using the calculator. |
| What is my name? | Answers Ali using conversation memory. |
| What day is it today? | Calls `current_datetime`. |
| Save a note: revise RAG tomorrow. | Saves the note in notes.txt. |
| Grades for Omar? | Returns a polite message that Omar was not found. |
| Calculate 2 ** 10. | Returns 1024. |

*Built with Python, LangChain, LangGraph, OpenAI, and ChromaDB.*
