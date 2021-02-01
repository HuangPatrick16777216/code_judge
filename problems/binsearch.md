# Max Num
* Test cases: 20
* Author: Patrick Huang
* License: GPL
* Difficulty: 3

## Description
You are given a sorted list, `S`, with `L` elements, of integers.<br>
You are also given `Q` not necessarily distinct queries.<br>
For each `N` in `Q`, output the position of `N` in `S`. It is guarenteed that `N` is in `S`.

## Input Format
The first line contains `L` and `Q`, space separated.<br>
The next line contains `L` space separated integers, which are elements in `S`.<br>
The last line contains `Q` space separated integers, which are the queries.

## Output Format
Output `Q` lines, each with the position of a query.

## Constraints
`10 <= L < 1,000,000`<br>
`1 <= Q < 1,000,000`<br>
`1 <= Si <= 1,000,000,000`<br>
Problem may not be completely solvable for slower languages like Python.

## Sample Input
```
10 3
1 5 12 56 89 143 567 1090 3478 10000
56 1090 1
```

## Sample Output
```
4
8
1
```
