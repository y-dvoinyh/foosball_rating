FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm config set strict-ssl false \
    && npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
