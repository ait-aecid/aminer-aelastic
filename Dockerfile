# aminer-aelastic Dockerfile
#
# Build:
#    docker build -t aecid/aelastic:latest -t aecid/aelastic:$(grep '__version__ =' aelastic/metadata.py | awk -F '"' '{print $2}') .
#

# Pull base image.
FROM python:3.8
LABEL maintainer="wolfgang.hotwagner@ait.ac.at"

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN make install

ENTRYPOINT ["/usr/lib/aelastic/aelasticd.py"]
