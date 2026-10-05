FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY cfads cfads
COPY webapp webapp
COPY scripts scripts
ENV DATABASE=/data/cfads.db TRUST_PROXY=1 PYTHONUNBUFFERED=1
RUN useradd -m app && mkdir -p /data && chown app /data
USER app
EXPOSE 8000
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:${PORT:-8000} --access-logfile - 'webapp.app:create_app()'"]
