# `# Getting Started with Create React App`

## The Project will run through Docker

## `01. Create the image through Dockerfile and Run the image`

```
docker build -t movie_app .
docker run -d -p 3333:3000 movie_app
```

## `02. Directly use docker-compose.yaml file(it will create image and run it)`
### docker-compose.yaml file as below

```
  version: '3'
  services:
    my-movie:
      build: .
      image: mymovieworld
      restart: always
      ports:
        - 3333:3333
```
> [!NOTE]
> ### package.json file should have PORT=3333
> ### Ex:     "start": "PORT=3333 react-scripts start"

```
docker-compose up -d
docker ps
docker-compose down
```

## `03. Run the project in Docker Swarm mode(Distributed enviornment), And Run multiple instances with replicas`
### docker-compose.yaml file as below

```
  version: 3
  services:
    my-movie:
      build: .
      image: mymovieworld
      #restart: always
      deploy:
        replicas: 2
      ports:
        - 3333-3336:3333
```
```
docker stack deploy --compose-file=docker-compose.yaml movieapp-stack
docker ps
docker service ls
docker stack rm movieapp-stack
```
### This will create 4 instances of Movie Application which run on 3333, 3334, 3335 and 3336 port and it has 2 replicas
   [http://localhost:3333](http://localhost:3333)
   [http://localhost:3334](http://localhost:3334)
   [http://localhost:3335](http://localhost:3335)
   [http://localhost:3336](http://localhost:3336)


## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
