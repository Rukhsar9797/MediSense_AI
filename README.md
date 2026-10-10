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

## 🔮 Future Improvements

- More detailed adherence trend analysis.
- Improved detection of recurring missed-dose patterns.
- Customizable date ranges and reminders.
- Enhanced dashboard visualizations.
- Expanded automated testing and data validation.


## 👥 Team

Developed collaboratively for **ForgeHacks**, combining backend development, AI integration, data processing, and Streamlit dashboard design.

**MediSense AI — turning medication records into clearer adherence insights.**
