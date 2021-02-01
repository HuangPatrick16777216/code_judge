package main

import (
	"fmt"
	"math"
)


func main() {
	steps := 0
	var pos, target, step, target_range float64
	fmt.Scanf("%f", &pos)
	fmt.Scanf("%f", &target)
	fmt.Scanf("%f", &step)
	fmt.Scanf("%f", &target_range)
	for true {
		if math.Abs(pos - target) <= target_range {
			fmt.Println(steps)
			break;
		}
		if pos < target {
			for pos < target - target_range {
				pos += step
				steps++
			}
		} else {
			for pos > target + target_range {
				pos -= step
				steps++
			}
		}
		step /= 2
	}
}
