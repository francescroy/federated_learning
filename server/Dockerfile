FROM tensorflow/tensorflow:2.7.0

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

#RUN apt-get update --fix-missing && \
#apt-get install -y build-essential && \
#apt-get clean && \
#rm -rf /var/lib/apt/lists/*

RUN pip install python-dotenv \
&& pip install aiohttp[speedups] \
&& pip install flask

#RUN apt-get purge -y --auto-remove build-essential

CMD ["/usr/local/bin/flask", "run"]



