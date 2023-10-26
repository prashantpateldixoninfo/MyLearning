## Run website through Live server
    `Run the live server on index.htm file. It will launch the website locally.`

## Local web hosting from Lenovo server(192.168.160.4)
    `1. Login as root (sudo su)`
    `2. Copy the content(index.html, bg.jpeg files) to /var/www/html/prashant`
    `3. vi /etc/nginx/sites-available/default`
    `4. Change the root /var/www/html; code and replace with your own directory path. i.e /var/www/html/prashant `
    `5. And Restart the nginx server --> systemctl restart nginx`
    `6. Access the website from windows as 192.168.160.4`
