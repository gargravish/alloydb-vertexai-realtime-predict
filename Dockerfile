FROM python:3.7

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
WORKDIR /usr/app
COPY --chown=ravish:ravish ./requirements.txt requirements.txt
RUN pwd
RUN pip3 install -r ./requirements.txt

#RUN pip install --user -r ./requirements.txt

ENV PATH="/home/ravish/.local/bin:${PATH}"

# COPY --chown=ravish:ravish . .

# Expose port you want your app on
EXPOSE 8512
# Upgrade pip and install requirements

#RUN pip install -U pip
#RUN pip install streamlit
#RUN pip install pandas
#RUN pip install pandasql
#RUN pip install psycopg2-binary
#RUN pip install datetime

# Copy app code and set working directory
COPY --chown=ravish:ravish power-by-cloud.png power-by-cloud.png
COPY --chown=ravish:ravish cars_sale.py cars_sale.py
RUN ls -ltr
RUN ls -ltr /home/ravish/.local/bin/streamlit
# Run
ENTRYPOINT [“/home/ravish/.local/bin/streamlit”, “run”, “cars_sale.py”, “–server.port=8512”, “–server.address=0.0.0.0”]