FROM "python:3.6.3"

ENV HOME=/usr/src/app/

VOLUME $HOME
WORKDIR $HOME

COPY main.py automata.py requirements.txt weighttp.zip $HOME

RUN apt-get update -qq && \
	apt-get install libev-dev automake autoconf unzip -yqq --no-install-recommends && \
	pip install -r requirements.txt && \
	chmod +x main.py && \
	unzip weighttp.zip -d /tmp

WORKDIR /tmp/weighttp
RUN ./autogen.sh && \
	./configure && \
	make && \
	make install

WORKDIR $HOME

EXPOSE 3000
EXPOSE 3333

CMD [ "./main.py" ]
