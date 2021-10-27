FROM python:3.8-slim

WORKDIR /federated-learning-network/
COPY . node
COPY ./docker-client-config.py node/config.py

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && \
apt-get install -y build-essential && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

RUN pip install torch torchvision \
#&& pip install --ignore-installed --upgrade ./node/tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl \
&& pip install ./node/tensorflow-2.5.0-cp38-cp38-linux_x86_64.whl \
&& pip uninstall tensorflow-cpu \
&& pip install fastai \
&& pip install python-dotenv \
&& pip install aiohttp[speedups] \
&& pip install flask

RUN apt-get purge -y --auto-remove build-essential

WORKDIR /federated-learning-network/node

EXPOSE 5000
CMD ["/usr/local/bin/flask", "run"]