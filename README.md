## MediSense AI
**MediSense AI** is an AI-powered medication adherence tracking system designed to help users monitor medication routines and understand their adherence patterns.

## Project Overview

The project combines data analytics and AI-generated insights to present medication adherence information in a simple, interactive dashboard.

## Key Features

- **Medication Adherence Tracking:** Monitors medication records and calculates adherence percentages.
- **Risk Assessment:** Evaluates adherence patterns and identifies potential concerns based on missed doses.
- **AI-Powered Insights:** Generates summaries and personalized, general recommendations using the Groq API.
- **Interactive Dashboard:** Displays medication data and adherence trends through Streamlit and Plotly visualizations.
- **Patient Profiles:** Organizes medication records by patient.
- **Synthetic Demo Dataset:** Uses sample patient profiles and medication records to demonstrate the system.

## Technology Stack

- **Python** — Core application and backend logic
- **Streamlit** — Interactive dashboard
- **Pandas** — Data processing and analysis
- **Plotly** — Data visualization
- **Groq API** — AI-generated summaries and recommendations

## Project Structure

- `app.py` — Main Streamlit application
- `src/adherence.py` — Medication adherence calculations
- `src/risk_engine.py` — Adherence risk assessment
- `src/ai_advisor.py` — AI-generated insights and recommendations
- `data/` — Synthetic patient profiles and medication records
- `test_backend_new.py` — Backend testing

## Objective

MediSense AI aims to make medication adherence data easier to understand by combining tracking, risk indicators, visual analytics, and AI-generated guidance in one platform.

*Disclaimer: MediSense AI is a demonstration project, not a medical diagnostic system. Its insights are informational and should not replace professional medical advice.*
