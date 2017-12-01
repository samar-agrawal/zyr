FROM samar/alpine-python3-flask
MAINTAINER sagrawal@noon.com

WORKDIR /src
EXPOSE 5199

CMD ["python3", "-m", "zyr.app"]

COPY . /src
RUN cd /src && python3 setup.py develop
