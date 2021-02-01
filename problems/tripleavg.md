# Triple Average
* Test cases: 20
* Author: Patrick Huang
* License: GPL
* Difficulty: 2

## Description
You are given a list, `S`, of integers. Apply this process until only one element remains:
* Take every pair of neighboring elements in `S`
* Compute the first plus 2 times the second all divided by three: `(one + 2*two) / 3`
* Take all the results in order of index and apply this operation again (if the resulting list is not empty)
Print the floor of the remaining integer.

## Input Format
The first line contains the size, `N`, of `S`
The next line contains `N` integers, each an element of `S`

## Output Format
A single integer specifying the remaining value from the operations described above.</br>
Please print the output without the decimal point. The grader will mark it wrong otherwise.

## Constraints
`0 <= N <= 5` for cases 1-10<br>
`0 <= N <= 999` for cases 11-20<br>
`0 <= Si < 1000` for cases 1-10<br>
`0 <= Si < 100000` for cases 11-20<br>

## Sample Input
```
4
1 2 3 4
```

## Sample Output
```
3
```
