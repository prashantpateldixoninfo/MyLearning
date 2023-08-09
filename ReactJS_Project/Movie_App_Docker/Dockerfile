FROM node:13-alpine

RUN mkdir -p /home/app/src
RUN mkdir -p /home/app/public

COPY ./src /home/app/src

COPY ./public /home/app/public

COPY ./package.json /home/app/

COPY ./package-lock.json /home/app/

# set default dir so that next commands executes in /home/app dir
WORKDIR /home/app

# will execute npm install in /home/app because of WORKDIR
RUN npm install react-scripts

RUN npm install axios

# Installing vim editor
RUN apk add vim

# no need for /home/app/server.js because of WORKDIR
CMD ["npm", "start"]

