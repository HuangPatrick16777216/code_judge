package main

import "fmt"

func main() {
	var n, curr int
	fmt.Scanf("%d", &n)
	max := -1
	for i := 0; i < n; i++ {
		fmt.Scanf("%d", &curr)
		if curr > max {
			curr = n
		}
	}
	fmt.Println(curr)
}
