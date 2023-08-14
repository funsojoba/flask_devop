# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "src.page_tracker/app:app"]



FROM python:3.11.2-slim-bullseye

RUN apt-get update && apt-get upgrade -y

RUN useradd --create-home realpython
USER realpython
WORKDIR /home/realpython

ENV VIRTUALENV=/home/realpython/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=realpython pyproject.toml constraints.txt ./

RUN python -m pip install --upgrade pip setuptools && \
    python -m pip install --no-cache-dir -c constraints.txt ".[dev]"


COPY --chown=realpython src/ src/
COPY --chown=realpython test/ test/

RUN python -m pip install -c constraints.txt . 

CMD ["flask", "--app", "page_tracker.app", "run", \
     "--host", "0.0.0.0", "--port", "5000"]
