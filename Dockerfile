FROM debian:bookworm AS base

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y python3-librdf python3-venv

RUN adduser lodstats

FROM base AS builder

RUN mkdir /src
RUN chown lodstats /src
COPY . /src

USER lodstats

WORKDIR /src
RUN python3 -m venv --system-site-packages /home/lodstats/venv
RUN --mount=type=cache,target=/home/lodstats/.cache/pip,uid=1000 \
  /home/lodstats/venv/bin/pip install .
#RUN /home/lodstats/venv/bin/python -m unittest discover -s test

FROM base
COPY --from=builder --chown=lodstats /home/lodstats/venv /home/lodstats/venv

USER lodstats

ENTRYPOINT ["/home/lodstats/venv/bin/lodstats"]
CMD ["--help"]
