with open("commandos.in", "r") as inp:
    T = int(inp.readline())
    for _ in xrange(T):
        a = [[[0 for _1 in xrange(15)] for _2 in xrange(15)] for _3 in xrange(15)]
        dp = [[[-1000000 for _1 in xrange(15)] for _2 in xrange(15)] for _3 in xrange(15)]
        n = int(inp.readline())
        for i in xrange(n):
            u, v, w, h = map(int, inp.readline().split())
            a[u][v][w] += h
        dp[10][1][1] = 0
        s = 10
        i = s
        for i in xrange(s, 0, -1):
            for j in xrange(1, s+1):
                for k in xrange(1, s+1):
                    dp[i][j][k] = max(max(dp[i][j][k], dp[i + 1][j][k]), max(dp[i][j - 1][k], dp[i][j][k - 1]))
                    dp[i][j][k] += a[i][j][k]
        print dp[1][s][s]

