# Use Node 18 image based on Alpine Linux
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm ci --silent


# Add the rest of the app
COPY . ./

# Start the app
CMD ["npm", "run", "dev"]

EXPOSE 3000