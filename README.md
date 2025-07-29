# 🀄 Chinese Dictionary Flashcard App

A lightweight web app to review and rehearse **Pleco flashcards** on your PC at a higher frequency than Pleco would normally allow. Designed for focused, desktop-based study using your exported Pleco database.

---

## 📦 Features

- Review flashcards with **category-based filtering**
- Reveal Pinyin & Definition on click (toggle on/off)
- View cards by category and score
- Designed to use your **Pleco flashcard database export**
- Built with **FastAPI + Jinja2 templates**

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/TF338/PlecoFlashCardViewer.git
cd PlecoFlashCardViewer
```

### 2. Create a Virtual Environment
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Add Your Flashcard Database

Export your flashcards from Pleco and place the .db file under: database_export/
This app expects a SQLite database export from Pleco.

## 🚀 Run the Application
You can configure the host/port via environment variables or defaults will be used.

Option A: Default Run
```
uvicorn app.main:app --reload
````

Option B: Use .env for Config

Create a .env file in the root directory:
```
HOST=127.0.0.1
PORT=8000
DEBUG=True
```

Then run:
```
source .env
uvicorn app.main:app --host $HOST --port $PORT --reload
```

## 🌐 How to Use

	1. Start the app and visit: http://127.0.0.1:8000
	2. Select a flashcard category and max score
	3. Click Filter to see matching cards
	4. Click on Pinyin or Definition cells to reveal or hide them
	5. Use the scores to prioritize low-performing cards
	
	
## 📚 Credits

    CC-CEDICT
    This project uses data from the CC-CEDICT Chinese-English dictionary.
    Licensed under the Creative Commons Attribution-ShareAlike 4.0 International License.

    Pleco
    This project can use exported flashcards from Pleco, a popular mobile Chinese dictionary app.
    Note: The Pleco dictionary content is proprietary. The exported flashcards are only meant to be used for personal use.