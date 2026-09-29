FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Most container platforms (Render, Railway, Cloud Run, Heroku's container
# runtime, ...) inject a PORT env var and route traffic to it; a plain
# `docker run -p 8501:8501 ...` leaves PORT unset, so default to 8501.
# Shell form (not exec-array form) is required so $PORT is expanded.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import os,urllib.request as u; p=os.environ.get('PORT','8501'); u.urlopen('http://127.0.0.1:'+p+'/_stcore/health', timeout=3)" || exit 1

CMD streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=${PORT:-8501}
