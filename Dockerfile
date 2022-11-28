FROM python:3.7
LABEL OWNER="ravishgarg@google.com"

RUN apt-get install -y gcc
RUN apt-get install -y libc-dev
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash ravish
#RUN mkdir -p /usr/app
USER ravish
RUN chown -R ravish:ravish /home/ravish
RUN chmod 755 /home/ravish
WORKDIR /home/ravish
COPY --chown=ravish:ravish ./requirements.txt requirements.txt
RUN pwd
ENV PATH="/home/ravish/.local/bin:${PATH}"

RUN pip3 install -r ./requirements.txt

EXPOSE 8512

COPY --chown=ravish:ravish power-by-cloud.png power-by-cloud.png
COPY --chown=ravish:ravish cars_sale.py cars_sale.py
RUN ls -ltr
RUN ls -ltr /home/ravish/.local/bin/streamlit
# RUN
ENTRYPOINT ["/home/ravish/.local/bin/streamlit", "run", "cars_sale.py", "--server.port=8512", "--server.address=0.0.0.0"]
