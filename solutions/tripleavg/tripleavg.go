package main

import (
	"fmt"
	"math"
)

func main() {
	var n int
	fmt.Scanf("%d", &n)
	nums := []int{}
	for i := 0; i < n; i++ {
		var tmp int
		fmt.Scanf("%d", &tmp)
		nums = append(nums, tmp)
	}
	for len(nums) > 1 {
		new_nums := []int{}
		for i := 0; i < len(nums)-1; i++ {
			new_nums = append(new_nums, (nums[i]+2*nums[i+1]) / 3)
		}
		nums := new_nums
	}
	fmt.Println(math.Floor(float64(nums[0])))
}
