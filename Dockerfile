FROM alpine:3.10

RUN apk -v --update add \
        python \
        py-pip \
        groff \
        less \
        mailcap \
        jq \
        && \
    pip install --upgrade awscli python-magic && \
    apk -v --purge del py-pip && \
    rm /var/cache/apk/*

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
