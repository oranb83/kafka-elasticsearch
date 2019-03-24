# I didn't use the alphine version since there was no python wheel for Kafka, so I was forced to build it on my own.
# This is obviosly something that I did many times, but it takes time and relevant when used on production.
FROM python:3.7

LABEL maintainer="Oran"

# Update pip
# ----------------
RUN pip install -U pip


# Copy application from local to WORKDIR
# ----------------
ADD . /project
WORKDIR /project

# Install requirements
# ----------------
RUN pip install -r requirements.txt


# Run Application
# ----------------
EXPOSE 5000
CMD ["python", "/project/api.py"]