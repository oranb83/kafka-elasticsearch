FROM python:3.7-alpine

LABEL maintainer="Oran"
WORKDIR /code

# Flask Setup
# ----------------
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

# Install requirements
# ----------------
RUN pip install -U pip
RUN pip install -r requirements.txt

# Run Application
# ----------------
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
