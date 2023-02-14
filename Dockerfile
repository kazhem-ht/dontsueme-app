FROM python:3.10-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

# Install requiremets (fat layer)
COPY requirements.txt ${APP_HOME}/

RUN pip install --no-cache-dir -r ${APP_HOME}/requirements.txt


COPY scripts/run.sh /run.sh
RUN chmod +x /run.sh
COPY ./project /app
EXPOSE 8000

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/run.sh"]
