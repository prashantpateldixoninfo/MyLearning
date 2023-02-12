## Docker Secret Simple
! https://docs.docker.com/engine/swarm/secrets/

! https://docs.docker.com/engine/swarm/secrets/#simple-example-get-started-with-secrets

##### 1. Add a secret to Docker. The docker secret create command reads standard input because the last argument, which represents the file to read the secret from, is set to -.

	$ printf "This is a secret" | docker secret create my_secret_data -

##### 2. Create a redis service and grant it access to the secret. By default, the container can access the secret at /run/secrets/<secret_name>, but you can customize the file name on the container using the target option.


	$ docker service  create --name redis --secret my_secret_data redis:alpine

##### 3. Verify that the task is running without issues using docker service ps. If everything is working, the output looks similar to this:


	$ docker service ps redis

If there were an error, and the task were failing and repeatedly restarting, you would see something like this:


	$ docker service ps redis

##### 4. Get the ID of the redis service task container using docker ps , so that you can use docker container exec to connect to the container and read the contents of the secret data file, which defaults to being readable by all and has the same name as the name of the secret. The first command below illustrates how to find the container ID, and the second and third commands use shell completion to do this automatically.


	$ docker ps --filter name=redis -q
	$ docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets
	$ docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

##### 5. Verify that the secret is not available if you commit the container.

	$ docker commit $(docker ps --filter name=redis -q) committed_redis

	$ docker run --rm -it committed_redis cat /run/secrets/my_secret_data

 cat: can't open '/run/secrets/my_secret_data': No such file or directory

##### 6. Try removing the secret. The removal fails because the redis service is running and has access to the secret.


	$ docker secret ls
	$ docker secret rm my_secret_data

##### 7. Remove access to the secret from the running redis service by updating the service.


	$ docker service update --secret-rm my_secret_data redis

##### 8. Repeat steps 3 and 4 again, verifying that the service no longer has access to the secret. The container ID is different, because the service update command redeploys the service.

	$ docker container exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

 cat: can't open '/run/secrets/my_secret_data': No such file or directory

##### 9. Stop and remove the service, and remove the secret from Docker.


	$ docker service rm redis
	$ docker secret rm my_secret_data


### My Eperiment

##### 1. Add a secret to Docker. The docker secret create command reads standard input because the last argument, which represents the file to read the secret from, is set to -.
    $ printf "This is a secret" | docker secret create my_secret_data -
    w42xjtowuewsa85ylpf00009j
    $ docker secret inspect my_secret_data
    [
        {
            "ID": "w42xjtowuewsa85ylpf00009j",
            "Version": {
                "Index": 740
            },
            "CreatedAt": "2023-02-12T11:02:46.742658837Z",
            "UpdatedAt": "2023-02-12T11:02:46.742658837Z",
            "Spec": {
                "Name": "my_secret_data",
                "Labels": {}
            }
        }
    ]
    $ docker secret ls
    ID                          NAME             DRIVER    CREATED          UPDATED
    w42xjtowuewsa85ylpf00009j   my_secret_data             35 seconds ago   35 seconds ago

##### 2. Create a redis service and grant it access to the secret. By default, the container can access the secret at /run/secrets/<secret_name>, but you can  customize the file name on the container using the target option.

    $ docker service  create --name redis --secret my_secret_data redis:alpine
    7cr3aaiw2yscdvmar23bli8w5
    overall progress: 1 out of 1 tasks
    1/1: running   [==================================================>]
    verify: Service converged


##### 3. Verify that the task is running without issues using docker service ps.If everything is working, the output looks similar to this:

    $ docker service ps redis
    ID             NAME      IMAGE          NODE               DESIRED STATE   CURRENT STATE            ERROR     PORTS
    vkk1ns7meroy   redis.1   redis:alpine   guest-VirtualBox   Running         Running 51 seconds ago

    $ docker ps
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS      NAMES
    45b252c17feb   redis:alpine   "docker-entrypoint.s…"   56 seconds ago   Up 55 seconds   6379/tcp   redis.1.vkk1ns7meroyubvql9ct2nox7
    
    $ docker images
    REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
    redis        <none>    aeeb92ae6202   22 hours ago   29.9MB
    ubuntu       bionic    5d2df19066ac   2 weeks ago    63.1MB
    nginx        latest    3964ce7b8458   2 months ago   142MB

##### 4. Get the ID of the redis service task container using docker ps , so that you can use docker container exec to connect to the container and read the contents of the secret data file, which defaults to being readable by all and has the same name as the name of the secret. The first command below illustrates how to find the container ID, and the second and third commands use shell completion to do this automatically.

    $ docker ps
    CONTAINER ID   IMAGE          COMMAND                  CREATED              STATUS              PORTS      NAMES
    45b252c17feb   redis:alpine   "docker-entrypoint.s…"   About a minute ago   Up About a minute   6379/tcp   redis.1.vkk1ns7meroyubvql9ct2nox7

    $ docker ps --filter name=redis -q
    45b252c17feb

    $ docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets
    total 4
    -r--r--r--    1 root     root            16 Feb 12 11:05 my_secret_data

    $ docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data
    This is a secret

##### 5. Verify that the secret is not available if you commit the container.

    $ docker commit $(docker ps --filter name=redis -q) committed_redis committed_redis
    sha256:8795574c050cb2826297409b0ab69e18b1bc2e435f820e77e639fd4ddbdbb0ca

    $ docker images
    REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
    committed_redis   latest    8795574c050c   17 seconds ago   29.9MB
    redis             <none>    aeeb92ae6202   22 hours ago     29.9MB
    ubuntu            bionic    5d2df19066ac   2 weeks ago      63.1MB
    nginx             latest    3964ce7b8458   2 months ago     142MB

    $ docker run --rm -it committed_redis cat /run/secrets/my_secret_data
    $
    
##### 6. Try removing the secret. The removal fails because the redis service is running and has access to the secret.

    $ docker secret ls
    ID                          NAME             DRIVER    CREATED          UPDATED
    w42xjtowuewsa85ylpf00009j   my_secret_data             20 minutes ago   20 minutes ago

    $ docker secret rm my_secret_data
    Error response from daemon: rpc error: code = InvalidArgument desc = secret 'my_secret_data' is in use by the following service: redis
    
##### 7. Remove access to the secret from the running redis service by updating the service.

    $ docker service update --secret-rm my_secret_data redis
    redis
    overall progress: 1 out of 1 tasks
    1/1: running   [==================================================>]
    verify: Service converged

    $ docker service ps redis
    ID             NAME          IMAGE          NODE               DESIRED STATE   CURRENT STATE             ERROR     PORTS
    9z68zbrn7wpx   redis.1       redis:alpine   guest-VirtualBox   Running         Running 41 seconds ago
    vkk1ns7meroy    \_ redis.1   redis:alpine   guest-VirtualBox   Shutdown        Shutdown 41 seconds ago
    
    $ docker ps
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS      NAMES
    2ec92d11fa35   redis:alpine   "docker-entrypoint.s…"   16 seconds ago   Up 13 seconds   6379/tcp   redis.1.9z68zbrn7wpxtaarpv1hau77l
    
    $ docker images
    REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
    committed_redis   latest    8795574c050c   15 minutes ago   29.9MB
    redis             <none>    aeeb92ae6202   22 hours ago     29.9MB
    ubuntu            bionic    5d2df19066ac   2 weeks ago      63.1MB
    nginx             latest    3964ce7b8458   2 months ago     142MB

##### 8. Repeat steps 3 and 4 again, verifying that the service no longer has access to the secret. The container ID is different, because the service update command redeploys the service.

    $ docker service ps redis
    ID             NAME          IMAGE          NODE               DESIRED STATE   CURRENT STATE            ERROR     PORTS
    9z68zbrn7wpx   redis.1       redis:alpine   guest-VirtualBox   Running         Running 2 minutes ago
    vkk1ns7meroy    \_ redis.1   redis:alpine   guest-VirtualBox   Shutdown        Shutdown 2 minutes ago

    $ docker ps --filter name=redis -q
    2ec92d11fa35
    
    $ docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets
    ls: /run/secrets: No such file or directory
    
    $ docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data
    cat: can't open '/run/secrets/my_secret_data': No such file or directory
    
##### 9. Stop and remove the service, and remove the secret from Docker.

    $ docker service rm redis
    redis

    $ docker secret rm my_secret_data
    my_secret_data
    
    $ docker ps
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
    
    $ docker service ps redis
    no such service: redis
    
    $ docker run --rm -it committed_redis cat /run/secrets/my_secret_data
    $
    
    $ docker rmi committed_redis:latest
    
    $ docker rmi <redis>

