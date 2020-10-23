FROM python:3.7-alpine

LABEL maintainer="Oran"
ADD . /code
WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers

# Install requirements
# --------------------
RUN pip install -U pip
RUN pip install -r requirements.txt

# Run Application
# ---------------
EXPOSE 5000
CMD ["python", "/code/app.py"]
