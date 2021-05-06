# docker build --no-cache -t pepitoenpeligro/cc2_weatherpredictor_v1 -f Dockerfile .
# docker run -p 3005:3005 pepitoenpeligro/cc2_weatherpredictor_v1
# docker run -it -p 3005:3005 pepitoenpeligro/cc2_weatherpredictor_v1 /bin/bash
FROM python:3.8.5-slim

LABEL pepitoenpeligro.cc2_weatherprediction_v1.version="0.1.0"
LABEL pepitoenpeligro.cc2_weatherprediction_v1.release-date="2021-05-05"
LABEL pepitoenpeligro.cc2_weatherprediction_v1.url="https://github.com/pepitoenpeligro/cc2_weatherpredictor_v1"

WORKDIR /app

COPY . ./

EXPOSE 3005

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install --requirement requirements.txt

CMD gunicorn --bind 0.0.0.0:3005 server:app --timeout 60000 --workers=1 --capture-output