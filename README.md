# Fligh delay prediction service 

This is a simple service that predicts will a flight be delayed for more than 15 minutes or not.
The idea was inspired by Kaggle competition: https://www.kaggle.com/competitions/flight-delays-fall-2018/overview
Dataset is also from provided in the competition: https://www.kaggle.com/competitions/flight-delays-fall-2018/data.

### Tech Stack:
**Backend**: Docker, Python, FastAPI, Uvicorn
**Frontend**: Streamlit

### How to run:
1. Clone the repository
2. Run:
```bash
docker-compose build
docker-compose up
```

Backend: http://localhost:8000/docs, and Streamlit at http://localhost:8501

To run airflow tasks simply run the usual airflow launch commands, the data_engineering_dag.py will start automatically.

