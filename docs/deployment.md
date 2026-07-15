# Deployment

## Streamlit Community Cloud

1. Connect the GitHub repository.
2. Select `dashboard/app.py` as the app entry point.
3. Use the default Python environment and install dependencies from `requirements.txt`.
4. The app reads committed files from `outputs/`, so raw Kaggle data is not required for dashboard review.

## Docker

Build the image:

```bash
docker build -t olist-ops-analytics .
```

Run the dashboard:

```bash
docker run -p 8501:8501 olist-ops-analytics
```

Open:

```text
http://localhost:8501
```

## Local Production Check

Before deployment, run:

```bash
python scripts/validate_project.py
pytest
streamlit run dashboard/app.py
```
