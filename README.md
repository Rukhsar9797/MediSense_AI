# MediSense AI 💊
### AI-Powered Medication Adherence Monitoring

MediSense AI is an AI-powered medication adherence monitoring application built for **ForgeHacks**. It helps users understand medication-taking patterns through adherence statistics, risk indicators, missed-dose alerts, interactive visualizations, and AI-generated recommendations.

## ✨ Features

- **Adherence Tracking:** Calculates medication adherence percentages and summarizes taken, missed, and pending doses.
- **Risk Assessment:** Uses a rule-based engine to assess recent medication adherence patterns.
- **Missed-Dose Alerts:** Flags days when more than one dose record is marked as missed.
- **Interactive Dashboard:** Displays patient summaries, medication statistics, and visualizations using Streamlit and Plotly.
- **AI-Powered Insights:** Generates adherence summaries and general habit-building recommendations using the Groq API.
- **Synthetic Demo Data:** Uses sample patient profiles and medication records for demonstration.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Data Processing:** Pandas
- **Visualizations:** Plotly
- **AI Integration:** Groq API
- **Data Storage:** CSV files

## 📁 Project Structure

```text
MediSense AI/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── data/
│   ├── patient_profiles.csv
│   └── medication_data_with_dates.csv
├── src/
│   ├── __init__.py
│   ├── adherence.py
│   ├── risk_engine.py
│   └── ai_advisor.py
└── test_backend_new.py
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd "MediSense AI"
```

Alternatively, download and extract the project folder.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API

Create a `.env` file in the project root using `.env.example` as a template:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Replace the placeholder with your own valid API key. Keep `.env` private and never commit it to GitHub.

## ▶️ Run the Application

Start the Streamlit dashboard from the project root:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to use MediSense AI.

## 🧠 How It Works

1. The application loads synthetic patient profiles and medication records.
2. The adherence module calculates medication-taking statistics.
3. The risk engine analyzes recent records and generates rule-based risk indicators and alerts.
4. The Groq-powered AI advisor generates readable summaries and general habit-building suggestions.
5. Streamlit displays the results through dashboard metrics, charts, and alerts.

## 🧪 Run Backend Tests

To test the backend independently, run:

```bash
python test_backend_new.py
```

Ensure the datasets and `.env` configuration are available before testing. AI functionality requires a valid Groq API key unless a fallback response is used.

## 🔮 Future Improvements

- More detailed adherence trend analysis.
- Improved detection of recurring missed-dose patterns.
- Customizable date ranges and reminders.
- Enhanced dashboard visualizations.
- Expanded automated testing and data validation.

## 🔐 Privacy and Disclaimer

This project uses synthetic data for demonstration. Do not upload real patient information to public repositories.

MediSense AI is an educational hackathon prototype, not a medical device. Its risk indicators are rule-based and are not clinically validated. It does not provide medical diagnosis or recommend medication changes.

## 👥 Team

Developed collaboratively for **ForgeHacks**, combining backend development, AI integration, data processing, and Streamlit dashboard design.

**MediSense AI — turning medication records into clearer adherence insights.**
