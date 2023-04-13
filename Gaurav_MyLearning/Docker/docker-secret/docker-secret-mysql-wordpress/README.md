! https://docs.docker.com/engine/swarm/secrets/#build-support-for-docker-secrets-into-your-images

! https://stackoverflow.com/questions/42139605/how-do-you-manage-secret-values-with-docker-compose-v3-1

##### To use secrets you need to add two things into your docker-compose.yml file. First, a top-level secrets: block that defines all of the secrets. Then, another secrets: block under each service that specifies which secrets the service should receive.

##### As an example, create the two types of secrets that Docker will understand: external secrets and file secrets.

#### 1. Create an 'external' secret using docker secret create
	First thing: to use secrets with Docker, the node you are on must be part of a swarm.

	$ docker swarm init
	Next, create an 'external' secret:

	$ echo "This is an external secret" | docker secret create my_external_secret -
	(Make sure to include the final dash, -. It's easy to miss.)

#### 2. Write another secret into a file
	$ echo "This is a file secret." > my_file_secret.txt

#### 3. Create a docker-compose-nginx.yml file that uses both secrets
	Now that both types of secrets are created, here is the docker-compose-nginx.yml file that will read both of those and write them to the web service:

	version: '3.1'

	services:
  		web:
    		image: nginxdemos/hello
    		secrets:                    # secrets block only for 'web' service
     			- my_external_secret
     			- my_file_secret

	secrets:                        # top level secrets block
  		my_external_secret:
    		external: true
  		my_file_secret:
    		file: my_file_secret.txt
	
	Docker can read secrets either from its own database (e.g. secrets made with docker secret create) or from a file. The above shows both examples.

#### 4. Deploy your test stack
	Deploy the stack using:

	$ docker stack deploy --compose-file=docker-compose-nginx.yml secret_test

	This will create one instance of the web service, named secret_test_web.

#### 5. Verify that the container created by the service has both secrets
	Use docker exec -ti [container] /bin/sh to verify that the secrets exist.

	(Note: in the below docker exec command, the m2jgac... portion will be different on your machine. Run docker ps to find your container name.)

	$ docker exec -ti secret_test_web.1.m2jgacogzsiaqhgq1z0yrwekd /bin/sh

	Now inside secret_test_web; secrets are contained in /run/secrets/
	root@secret_test_web:~$ cd /run/secrets/

	root@secret_test_web:/run/secrets$ ls
	my_external_secret  my_file_secret

	root@secret_test_web:/run/secrets$ cat my_external_secret
	This is an external secret

	root@secret_test_web:/run/secrets$ cat my_file_secret
	This is a file secret.
	If all is well, the two secrets we created in steps 1 and 2 should be inside the web container that was created when we deployed our stack.

#### My Experiment
	$ vi docker-compose-nginx.yml
	$ echo "This is an external secret" | docker secret create my_external_secret -
	$ echo "This is a file secret." > my_file_secret.txt
	$ docker stack deploy --compose-file=docker-compose-nginx.yml secret_test
	$ docker exec -ti secret_test_web.1.4k8o60679j3nsdma61u08m0ys /bin/sh
	$ docker ps
	$ docker service ls
	$ docker service ps secret_test_web
	$ docker service rm secret_test_web
	$ docker secret rm my_external_secret secret_test_my_file_secret
