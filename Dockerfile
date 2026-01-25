ARG IMAGE_NAME
ARG IMAGE_VERSION

FROM ${IMAGE_NAME}:${IMAGE_VERSION}

WORKDIR /opt/decision

COPY pyproject.toml .
COPY README.md .
COPY setup.py .
COPY decision decision
COPY tests tests

RUN pip install -e .[tests]
