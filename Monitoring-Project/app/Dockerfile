FROM node:24.21.0-alpine3.24 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY server.js ./


FROM node:24.21.0-alpine3.24 AS runtime

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/server.js ./

USER node

EXPOSE 3001

CMD ["node", "server.js"]