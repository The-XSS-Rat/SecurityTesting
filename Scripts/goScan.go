package main

import (
	"fmt"
	"net"
	"sync"
	"time"
)

func scanPort(port int, wg *sync.WaitGroup) {
	defer wg.Done()
	target := "example.com"
	address := fmt.Sprintf("%s:%d", target, port)
	conn, err := net.DialTimeout("tcp", address, time.Second*10)
	if err != nil {
		return
	}
	conn.Close()
	fmt.Println("Port", port, "is open.")
}

func main() {
	target := "example.com"
	start := time.Now()

	fmt.Println("Starting port scan on target:", target)

	var wg sync.WaitGroup
	for port := 1; port <= 65535; port++ {
		wg.Add(1)
		go scanPort(port, &wg)
	}
	wg.Wait()

	elapsed := time.Since(start)
	fmt.Println("Port scan completed in", elapsed)
}
