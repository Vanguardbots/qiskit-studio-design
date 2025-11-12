FROM ghcr.io/ai4quantum/maestro:latest

COPY ./agents.yaml /usr/src/app/
COPY ./workflow.yaml /usr/src/app/
COPY ./system-prompt.md /usr/src/app/

ENTRYPOINT [ "maestro", "serve", "agents.yaml", "workflow.yaml", "--host", "0.0.0.0" ]