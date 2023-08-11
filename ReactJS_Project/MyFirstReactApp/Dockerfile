FROM node:14-alpine
#FROM alpine

RUN mkdir -p /home/app

WORKDIR /home/app/

# Install nodejs(NPM)
#RUN apk add --update nodejs npm

# Intall create-react-app script/library
#RUN npm install -g create-react-app

# This will creat new folder i.e. my-first-react-app
RUN npx create-react-app my-first-react-app

# Set working directory as my-first-react-app
WORKDIR /home/app/my-first-react-app

# Execute the command at /home/app/my-first-react-app
CMD ["npm", "start"]

