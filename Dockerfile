FROM python:3.7.11-alpine3.14 as base
FROM base as builder

RUN apk --no-cache upgrade && pip install --upgrade pip

WORKDIR /code
COPY setup.py ./
RUN pip install --prefix=/install .

FROM base
COPY --from=builder /install /usr/local

WORKDIR /code
COPY main.py ./
COPY linkedin_token ./linkedin_token

ENTRYPOINT ["python", "/code/main.py"]

LABEL version=0.1.0
LABEL name=linkedin-token-generator
