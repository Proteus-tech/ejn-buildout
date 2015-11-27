FROM abstracttechnology/plone:5.0
MAINTAINER Giorgio Borelli <giorgio@giorgioborelli.it>

USER root


# Install Plone dependencies
RUN apt-get update && \
    apt-get install -y python-mysqldb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update buildout.cfg
COPY buildout.cfg.sample buildout.cfg
COPY requirements.txt requirements.txt
COPY base.cfg base.cfg
COPY production.cfg production.cfg
COPY development.cfg development.cfg
COPY scripts scripts
COPY src src
COPY entrypoint.sh entrypoint.sh

RUN chown -R webapp:webapp .

RUN pip install -r requirements.txt

USER webapp

RUN buildout -v

ENTRYPOINT ["./entrypoint.sh"]
CMD ["run"]

