FROM python

RUN set -eux; \
    pip install --upgrade pip

RUN set -eux; \
    pip install \
        prettytable \
        pyinstaller 

VOLUME /src
WORKDIR /src

ENTRYPOINT ["pyinstaller"]