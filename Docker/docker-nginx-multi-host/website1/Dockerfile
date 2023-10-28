# Use an official Nginx runtime as the base image
FROM nginx:alpine

# Copy the HTML, CSS, and JavaScript files to the Nginx document root
COPY ./index.html /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
