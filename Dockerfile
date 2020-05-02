FROM python:3

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip -q awscliv2.zip \
  && ./aws/install

RUN apt-get update \
  && apt-get install -y less jq

COPY entrypoint.sh /entrypoint.sh
COPY pretty_format.py /pretty_format.py

ENTRYPOINT ["/entrypoint.sh"]
