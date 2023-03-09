FROM python:3.9-slim-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY milli_project.py .
CMD ["python", "milli_project.py"]