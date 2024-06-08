package main

import (
	"strings"
	"regexp"
	"fmt"
	"net"
	"os"
)

func getIP() string {
	var ip string

	regex, err := regexp.Compile(`^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}$`)
	if err != nil {
		fmt.Println("Error compiling regex:", err)
		os.Exit(1)
	}

	for {
		fmt.Print("IP: ")
		fmt.Scan(&ip)
		ip = strings.TrimSpace(ip)

		if regex.MatchString(ip) {
			fmt.Println("Sending packet now...")
			return ip
		}

		fmt.Println("Invalid IP address format. Try again...")
	}
}

func main() {
	conn, err := net.Dial("tcp", getIP())
	if err != nil {
		fmt.Println("Error connecting:", err)
		os.Exit(1)
	}
	defer conn.Close()

	_, err = conn.Write([]byte("Hello, Server!"))
	if err != nil {
		fmt.Println("Error sending message:", err)
		return
	}

	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		fmt.Println("Error reading response:", err)
		return
	}

	fmt.Println("Received from server:", string(buffer[:n]))
}
