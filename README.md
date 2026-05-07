# Centrix

A natural language query system for PostgreSQL databases, powered by LLM.

> Ask a question in plain language. Get a formatted answer. No SQL, no spreadsheets.

---

## How it works

```
User types a question in natural language
        ↓
LLM (Claude) interprets it and generates the corresponding SQL
        ↓
Query is executed against the PostgreSQL database
        ↓
Result is formatted and returned in natural language
```

---

## Tech stack

- **Python** — core language
- **FastAPI** — async API framework
- **asyncpg** — async PostgreSQL driver
- **Pydantic** — data validation and settings management
- **Anthropic API** — SQL generation via Claude

---

## Prerequisites

- Python 3.10+
- A running PostgreSQL instance (local or cloud)
- An Anthropic API key ([get one here](https://console.anthropic.com/))

---

## Installation

```bash
# Clone the repository
git clone https://github.com/guisomera/Centrix.git
cd Centrix

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file at the project root:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_user
DB_PASSWORD=your_password

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## Usage

```bash
python main.py
```

Once running, just type your question in the terminal:

```
You: Which contracts are currently active?
Centrix: There are 8 active contracts. The services include...

You: Who manages Condomínio Central?
Centrix: The manager responsible for Condomínio Central is João Silva...
```

---

## Project structure

```
Centrix/
├── main.py          # Entry point, user interface
├── llm.py           # Anthropic API integration, SQL generation
├── database.py      # PostgreSQL connection via asyncpg
├── validacao.py     # Query validation layer
├── .env.example     # Configuration template (copy to .env)
├── requirements.txt
└── README.md
```

---

## Adapting to your own database

Centrix was built around a specific schema for condominium management, but it can be adapted to any PostgreSQL database.

To do so, edit `llm.py` and replace the schema injected into the LLM prompt with your own. The more detailed the schema (table names, columns, relationships), the better the generated SQL will be.

---

## Project status

MVP complete — terminal interface, full pipeline working end-to-end.

**Planned next steps:**
- [ ] SQL validation layer before execution
- [ ] Authentication and access control
- [ ] Web frontend

---

## Author

**Gui Somera**
[LinkedIn](https://linkedin.com/in/guisomera) · [GitHub](https://github.com/guisomera)
