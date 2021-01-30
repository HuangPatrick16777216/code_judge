# Path Find
* Test cases: 10
* Author: Patrick Huang
* License: GPL

## Description
You are given the number of points, `N`. The points are numbered `1...N`
You are also given `M` paths, each with a start and end point in `1...N`. Each path also has a length which is an integer.
You are also given `Q` queries. Each query consists of two points, `A` and `B`.
Find the shortest length between `A` and `B`, only traveling along given paths.

## Input Format
The first line contains `N`, `M`, and `Q`, space separated.
The next `M` lines each contain a path with the start point, end point, and length space separated.
The next `Q` lines contain two integers, `A` and `B`.

## Output Format
Output `Q` lines, each specifying the shortest distance for each query. It is guarenteed that such a path exists.
Make sure each answer is on a new line.

## Constraints
`2 <= N <= 100`
`1 <= M < 100`
`1 <= Q <= 10`

## Sample Input
```
5 4 2
1 2 1
2 3 3
3 4 2
4 5 1
1 4
3 5
```

## Sample Output
```
6
3
```
