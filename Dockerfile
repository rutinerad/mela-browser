FROM python:3.13-slim

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

RUN useradd --create-home --home-dir /home/mela --shell /usr/sbin/nologin mela
WORKDIR /home/mela
USER mela
ENV HOME=/home/mela

EXPOSE 8080
ENTRYPOINT ["python", "-m", "mela_browser", "--host", "0.0.0.0"]
