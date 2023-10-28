## Runt the multiple host from same server(IP Address)

### Start the Docker Compose
    `docker-compose up -d`

### Stop the Docker Compose
    `docker-compose down`

### Verify from Ubuntu
    Edit the /etc/hosts file
    `sudo vi /etc/hosts`
        `192.168.99.8    website1.com
         192.168.99.8    website2.com`

    Access the Website through browser 
    `http://website1.com`
    `http://website2.com`

### Verify from Window
    `192.168.99.8:8080` for website1
    `192.168.99.8:8081` for website2
    
    Edit the C:\Windows\System32\drivers\etc\hosts file as Administrator
        `192.168.99.8    website1.com
         192.168.99.8    website2.com`

    Access the Website through browser 
    `http://website1.com:8080`
    `http://website2.com:8081`


