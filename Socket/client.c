// Client side C/C++ program to demonstrate Socket
// programming
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080

int main(int argc, char const* argv[])
{
    int sock = 0, valread, client_fd;
    struct sockaddr_in serv_addr;
    char ip_addr_str[INET_ADDRSTRLEN];
    char buffer[1024] = { 0 };
    char* hello = "Hello message from Prashant Patel";

    printf("==> Create the socket descriptor for SOCK_STREAM <==\n");
    if((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
    	printf("Socket creation error\n");
    	return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IPv4 and IPv6 addresses from text to binary form
    printf("==> Convert IPv4 and IPv6 addresses from text to binary form <==\n");
    if(inet_pton(AF_INET, "192.168.160.4", &serv_addr.sin_addr) <= 0)
    {
    	printf("Invalid address/ Address not supported\n");
    	return -1;
    }

    inet_ntop(AF_INET, &serv_addr.sin_addr, ip_addr_str, INET_ADDRSTRLEN);
    printf("Server IP Family ==> %d\n", serv_addr.sin_family);
    printf("Server IP Address ==> %s\n", ip_addr_str);
    printf("Server Port Number ==> %d\n", htons(serv_addr.sin_port));
    printf("==> Connect the TCP connection to Remote <==\n");
    if((client_fd = connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0)
    {
    	printf("Connection Failed\n");
    	return -1;
    }

    printf("==> Send 'Hello message from client' to Server <==\n");
    send(sock, hello, strlen(hello), 0);
    printf("==> Going to Receiving message from Server <==\n");
    valread = read(sock, buffer, 1024);
    printf("Message received from Server is ==>  %s\n", buffer);

    // closing the connected socket
    printf("==> Closing the connected socket <==\n");
    close(client_fd);
    return 0;
}

