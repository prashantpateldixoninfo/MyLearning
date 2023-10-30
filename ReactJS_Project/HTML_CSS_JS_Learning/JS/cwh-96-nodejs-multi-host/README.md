## Refere the github code for multi host website
    https://github.com/prashantpateldixoninfo/MyLearning/tree/main/Docker/docker-nginx-multi-host

## Steps to add mutilple host in Nginx server(192.168.160.4)

### Check the nginx status
    sudo systemctl status nginx

### Create the directory
    mkdir /var/www/html/prashant

### Open the index.html file
    vi /var/www/html/prashant/index.html

### Copy the html code inside index.html or copy all content under folder
    <html>
        <title>Prashant Web</title>
        <h1>Welcome to the prashant.com with Nginx webserver.</h1>
    </html>

### Create virtual host configuration file
    vi /etc/nginx/sites-available/prashant.conf

### Add the below lines in virtal host configuration file
    server {
        listen 80;
        listen [::]:80;

        root /var/www/html/prashant;
        index index.html index.htm;

        server_name prashant.com;

        location / {
            try_files $uri $uri/ =404;
        }
    }

### Create the soft link for available site
    ln -s /etc/nginx/sites-available/prashant.conf /etc/nginx/sites-enabled/

### Verify your nginx syntax. You should able to see the syntax is OK.
    nginx -t

### Restart the nginx server
    systemctl restart nginx

### Verify the your website by adding host name into your DNS
    For Windows Modify file C:\Windows\System32\drivers\etc\hosts file as Administrator
    192.168.160.4    prashant.com

    For Ubuntu Modify the file /etc/hosts as sudo
    192.168.160.4    prashant.com
