https://docs.docker.com/engine/swarm/secrets/#build-support-for-docker-secrets-into-your-images


Simple example: Get started with secrets
This simple example shows how secrets work in just a few commands. For a real-world example, continue to Intermediate example: Use secrets with a Nginx service.



Add a secret to Docker. The docker secret create command reads standard input because the last argument, which represents the file to read the secret from, is set to -.


 printf "This is a secret" | docker secret create my_secret_data -
Create a redis service and grant it access to the secret. By default, the container can access the secret at /run/secrets/<secret_name>, but you can customize the file name on the container using the target option.


 docker service  create --name redis --secret my_secret_data redis:alpine
Verify that the task is running without issues using docker service ps. If everything is working, the output looks similar to this:


 docker service ps redis
If there were an error, and the task were failing and repeatedly restarting, you would see something like this:


 docker service ps redis
Get the ID of the redis service task container using docker ps , so that you can use docker container exec to connect to the container and read the contents of the secret data file, which defaults to being readable by all and has the same name as the name of the secret. The first command below illustrates how to find the container ID, and the second and third commands use shell completion to do this automatically.


 docker ps --filter name=redis -q
 docker container exec $(docker ps --filter name=redis -q) ls -l /run/secrets
 docker container exec $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data
Verify that the secret is not available if you commit the container.

$ docker commit $(docker ps --filter name=redis -q) committed_redis

$ docker run --rm -it committed_redis cat /run/secrets/my_secret_data

cat: can't open '/run/secrets/my_secret_data': No such file or directory
Try removing the secret. The removal fails because the redis service is running and has access to the secret.


 docker secret ls
 docker secret rm my_secret_data
Remove access to the secret from the running redis service by updating the service.


 docker service update --secret-rm my_secret_data redis
Repeat steps 3 and 4 again, verifying that the service no longer has access to the secret. The container ID is different, because the service update command redeploys the service.

$ docker container exec -it $(docker ps --filter name=redis -q) cat /run/secrets/my_secret_data

cat: can't open '/run/secrets/my_secret_data': No such file or directory
Stop and remove the service, and remove the secret from Docker.


 docker service rm redis
 docker secret rm my_secret_data

----------------------------------------------------------------------------------------------------

Intermediate example: Use secrets with a Nginx service
This example is divided into two parts. The first part is all about generating the site certificate and does not directly involve Docker secrets at all, but it sets up the second part, where you store and use the site certificate and Nginx configuration as secrets.

Generate the site certificate
Generate a root CA and TLS certificate and key for your site. For production sites, you may want to use a service such as Let’s Encrypt to generate the TLS certificate and key, but this example uses command-line tools. This step is a little complicated, but is only a set-up step so that you have something to store as a Docker secret. If you want to skip these sub-steps, you can use Let’s Encrypt to generate the site key and certificate, name the files site.key and site.crt, and skip to Configure the Nginx container.

Generate a root key.


 openssl genrsa -out "root-ca.key" 4096
Generate a CSR using the root key.


 openssl req \
          -new -key "root-ca.key" \
          -out "root-ca.csr" -sha256 \
          -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=Swarm Secret Example CA'
Configure the root CA. Edit a new file called root-ca.cnf and paste the following contents into it. This constrains the root CA to signing leaf certificates and not intermediate CAs.

[root_ca]
basicConstraints = critical,CA:TRUE,pathlen:1
keyUsage = critical, nonRepudiation, cRLSign, keyCertSign
subjectKeyIdentifier=hash
Sign the certificate.


 openssl x509 -req  -days 3650  -in "root-ca.csr" \
               -signkey "root-ca.key" -sha256 -out "root-ca.crt" \
               -extfile "root-ca.cnf" -extensions \
               root_ca
Generate the site key.


 openssl genrsa -out "site.key" 4096
Generate the site certificate and sign it with the site key.


 openssl req -new -key "site.key" -out "site.csr" -sha256 \
          -subj '/C=US/ST=CA/L=San Francisco/O=Docker/CN=localhost'
Configure the site certificate. Edit a new file called site.cnf and paste the following contents into it. This constrains the site certificate so that it can only be used to authenticate a server and can’t be used to sign certificates.

[server]
authorityKeyIdentifier=keyid,issuer
basicConstraints = critical,CA:FALSE
extendedKeyUsage=serverAuth
keyUsage = critical, digitalSignature, keyEncipherment
subjectAltName = DNS:localhost, IP:127.0.0.1
subjectKeyIdentifier=hash
Sign the site certificate.


 openssl x509 -req -days 750 -in "site.csr" -sha256 \
    -CA "root-ca.crt" -CAkey "root-ca.key"  -CAcreateserial \
    -out "site.crt" -extfile "site.cnf" -extensions server
The site.csr and site.cnf files are not needed by the Nginx service, but you need them if you want to generate a new site certificate. Protect the root-ca.key file.

Configure the Nginx container
Produce a very basic Nginx configuration that serves static files over HTTPS. The TLS certificate and key are stored as Docker secrets so that they can be rotated easily.

In the current directory, create a new file called site.conf with the following contents:

server {
    listen                443 ssl;
    server_name           localhost;
    ssl_certificate       /run/secrets/site.crt;
    ssl_certificate_key   /run/secrets/site.key;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
Create three secrets, representing the key, the certificate, and the site.conf. You can store any file as a secret as long as it is smaller than 500 KB. This allows you to decouple the key, certificate, and configuration from the services that use them. In each of these commands, the last argument represents the path to the file to read the secret from on the host machine’s filesystem. In these examples, the secret name and the file name are the same.


 docker secret create site.key site.key
 docker secret create site.crt site.crt
 docker secret create site.conf site.conf

 docker secret ls
Create a service that runs Nginx and has access to the three secrets. The last part of the docker service create command creates a symbolic link from the location of the site.conf secret to /etc/nginx.conf.d/, where Nginx looks for extra configuration files. This step happens before Nginx actually starts, so you don’t need to rebuild your image if you change the Nginx configuration.

Note: Normally you would create a Dockerfile which copies the site.conf into place, build the image, and run a container using your custom image. This example does not require a custom image. It puts the site.conf into place and runs the container all in one step.

Secrets are located within the /run/secrets/ directory in the container by default, which may require extra steps in the container to make the secret available in a different path. The example below creates a symbolic link to the true location of the site.conf file so that Nginx can read it:


 docker service create \
     --name nginx \
     --secret site.key \
     --secret site.crt \
     --secret site.conf \
     --publish published=3000,target=443 \
     nginx:latest \
     sh -c "ln -s /run/secrets/site.conf /etc/nginx/conf.d/site.conf && exec nginx -g 'daemon off;'"
Instead of creating symlinks, secrets allow you to specify a custom location using the target option. The example below illustrates how the site.conf secret is made available at /etc/nginx/conf.d/site.conf inside the container without the use of symbolic links:


 docker service create \
     --name nginx \
     --secret site.key \
     --secret site.crt \
     --secret source=site.conf,target=/etc/nginx/conf.d/site.conf \
     --publish published=3000,target=443 \
     nginx:latest \
     sh -c "exec nginx -g 'daemon off;'"
The site.key and site.crt secrets use the short-hand syntax, without a custom target location set. The short syntax mounts the secrets in `/run/secrets/ with the same name as the secret. Within the running containers, the following three files now exist:

/run/secrets/site.key
/run/secrets/site.crt
/etc/nginx/conf.d/site.conf
Verify that the Nginx service is running.


 docker service ls
 docker service ps nginx
Verify that the service is operational: you can reach the Nginx server, and that the correct TLS certificate is being used.


 curl --cacert root-ca.crt https://localhost:3000



Welcome to nginx!</title>







Welcome to nginx!</h1>
If you see this page, the nginx web server is successfully installed and

For online documentation and support. refer to
nginx.org</a>.<br/>
nginx.com</a>.</p>
<em>Thank you for using nginx.</em></p>



 openssl s_client -connect localhost:3000 -CAfile root-ca.crt
To clean up after running this example, remove the nginx service and the stored secrets.


 docker service rm nginx
 docker secret rm site.crt site.key site.conf


------------------------------------------------------------------------------------------------
https://stackoverflow.com/questions/42139605/how-do-you-manage-secret-values-with-docker-compose-v3-1

To use secrets you need to add two things into your docker-compose.yml file. First, a top-level secrets: block that defines all of the secrets. Then, another secrets: block under each service that specifies which secrets the service should receive.

As an example, create the two types of secrets that Docker will understand: external secrets and file secrets.

1. Create an 'external' secret using docker secret create
First thing: to use secrets with Docker, the node you are on must be part of a swarm.

$ docker swarm init
Next, create an 'external' secret:

$ echo "This is an external secret" | docker secret create my_external_secret -
(Make sure to include the final dash, -. It's easy to miss.)

2. Write another secret into a file
$ echo "This is a file secret." > my_file_secret.txt
3. Create a docker-compose.yml file that uses both secrets
Now that both types of secrets are created, here is the docker-compose.yml file that will read both of those and write them to the web service:

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

4. Deploy your test stack
Deploy the stack using:

$ docker stack deploy --compose-file=docker-compose.yml secret_test
This will create one instance of the web service, named secret_test_web.

5. Verify that the container created by the service has both secrets
Use docker exec -ti [container] /bin/sh to verify that the secrets exist.

(Note: in the below docker exec command, the m2jgac... portion will be different on your machine. Run docker ps to find your container name.)

$ docker exec -ti secret_test_web.1.m2jgacogzsiaqhgq1z0yrwekd /bin/sh

# Now inside secret_test_web; secrets are contained in /run/secrets/
root@secret_test_web:~$ cd /run/secrets/

root@secret_test_web:/run/secrets$ ls
my_external_secret  my_file_secret

root@secret_test_web:/run/secrets$ cat my_external_secret
This is an external secret

root@secret_test_web:/run/secrets$ cat my_file_secret
This is a file secret.
If all is well, the two secrets we created in steps 1 and 2 should be inside the web container that was created when we deployed our stack.

$vi docker-compose.yml
$openssl rand -base64 20 > db_password.txt
$vi db_password.txt
$openssl rand -base64 20 > db_root_password.txt
$vi db_root_password.txt
$docker stack deploy --compose-file=docker-compose.yml secret_test
$docker ps
$docker secret ls
$docker secret inspect secret_test_db_password



---------------------------------------------------------------------------------------------------------------------
