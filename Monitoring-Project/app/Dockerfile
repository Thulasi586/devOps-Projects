FROM node:24.21.0-alpine3.24

WORKDIR /app

RUN npm install -g npm@12.1.0

COPY package*.json ./

RUN npm install

COPY server.js ./

EXPOSE 3001

CMD ["node", "server.js"]
