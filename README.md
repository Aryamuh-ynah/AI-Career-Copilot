# AI Career Copilot 🚀

AI Career Copilot is a Python-based web application developed using the Flask framework. The platform assists users in optimizing their career trajectories by integrating essential authentication features, custom page rendering, and internal module architectures to manage data efficiently.

---

## 🛠️ Tech Stack & Prerequisites

- **Backend Framework:** Python (Flask)
- **Database Architecture:** SQLite / Custom Data Persistence (`db.py`)
- **Frontend Template Engine:** Jinja2 (HTML/CSS)
- **Environment Management:** Virtualenv (`venv`)

---

## 📂 Project Structure

As shown in the local layout configurations, the workspace is organized as follows:

```text
AI-CAREER-COPILOT/
│
├── templates/              # HTML Frontend layouts and views
│   ├── base.html           # Core layout containing shared components
│   ├── dashboard.html       # User dashboard view interface
│   ├── history.html        # Historical generation logging tracking page
│   ├── login.html          # Authentication login portal
│   └── signup.html         # Main user registration portal
│
├── venv/                   # Python Virtual Environment
├── .gitignore              # Files and directories ignored by Git version control
├── app.py                  # Main entry point and Flask routing configurations
├── dbexample.py            # Sample operations and query execution example file
├── learn.txt               # Developer guidelines and notes
└── models.py               # Application object schemas and database configurations

```

---

## 🚀 Getting Started & Installation

Follow these steps to set up and run the application locally on your system:

### 1. Clone the Repository

```bash
git clone [https://github.com/Aryamuh-ynah/AI-Career-Copilot.git](https://github.com/Aryamuh-ynah/AI-Career-Copilot.git)
cd AI-Career-Copilot

```

### 2. Activate the Virtual Environment

Ensure your configurations are set properly within your local environment wrapper before initializing dependencies.

* **On Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1

```


* **On Linux / Ubuntu:**
```bash
source venv/bin/activate

```



### 3. Install Required Dependencies

Initialize your application server requirements framework (make sure Flask is installed in your workspace).

```bash
pip install flask sqlalchemy openai PuPDF2 python-docs pymsql

```

### 4. Initialize Database & Run the Project

Launch your backend web server pipeline tracking:

```bash
python app.py

```

Once initialized, visit your local server deployment address in your web browser: `http://127.0.0.1:5000/`

---

## 📌 Development Features Built From This Course

* **User Authentication:** Fully structured `login.html` and `signup.html` modules rendering through Jinja templates routing.
* **Persistent Data Tracking:** Structural models mapped natively utilizing Python hooks to persist profile and interaction states.
* **Base Extension Templates:** Component management patterns matching modular architecture styles to prevent duplicate code configurations.
