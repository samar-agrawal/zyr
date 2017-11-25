FROM samar/alpine-sanic-aiomysql
MAINTAINER sagrawal@noon.com

WORKDIR /src
EXPOSE 5199

CMD ["python3", "-m", "zyr.app"]

RUN pip3 install hirlite==0.3.1 requests flask

COPY . /src
RUN cd /src && python3 setup.py develop
