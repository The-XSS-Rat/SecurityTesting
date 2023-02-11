package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

func scanPort(address string, port int, wg *sync.WaitGroup) {
	defer wg.Done()

	conn, err := net.DialTimeout("tcp", fmt.Sprintf("%s:%d", address, port), time.Second*10)
	if err != nil {
		return
	}
	conn.Close()
	fmt.Println(address, "Port", port, "is open.")
}

func main() {
	fmt.Println("Enter IPs or a range of IPs (e.g. 192.168.1.1-192.168.1.100)")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	input := scanner.Text()

	var ipAddresses []string
	if strings.Contains(input, "-") {
		ipRange := strings.Split(input, "-")
		startIP := net.ParseIP(ipRange[0])
		endIP := net.ParseIP(ipRange[1])

		start := net.IPToBigInt(startIP)
		end := net.IPToBigInt(endIP)
		for i := start; i <= end; i++ {
			ipAddresses = append(ipAddresses, net.BigIntToIP(i).String())
		}
	} else {
		ipAddresses = strings.Split(input, " ")
	}

	start := time.Now()

	fmt.Println("Starting port scan on targets:", ipAddresses)

	var wg sync.WaitGroup
	for _, address := range ipAddresses {
		for port := 1; port <= 65535; port++ {
			wg.Add(1)
			go scanPort(address, port, &wg)
		}
	}
	wg.Wait()

	elapsed := time.Since(start)
	fmt.Println("Port scan completed in", elapsed)
}
