FROM node:24.21.0-alpine3.24

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY server.js ./

EXPOSE 3001

CMD ["node", "server.js"]
