FROM python:3.9-slim-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY apa_project.py .
CMD ["python", "apa_project.py"]