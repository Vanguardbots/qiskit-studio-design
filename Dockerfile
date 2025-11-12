FROM registry.access.redhat.com/ubi9/nodejs-22

COPY --chown=1001:1001 . /app

WORKDIR /app

USER 1001:1001

RUN npm install

ENV PATH=/app/node_modules/.bin:$PATH \
	NEXT_TELEMETRY_DISABLED=1

ENTRYPOINT [ "npm", "run", "dev", "--", "-H", "0.0.0.0", "-p", "3000" ]
