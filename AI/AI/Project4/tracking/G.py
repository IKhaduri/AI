mod = 1000000007


def mod_inverse(a, p):
    return pow(a, p-2, p)


def c(n, k):
    if n < k or n < 0 or k < 0:
        return 0
    tmp = facts[n] * rev_fact[k] % mod;
    tmp = tmp * rev_fact[n - k] % mod;
    return tmp

facts = [1 for _ in xrange(10000)]
rev_fact = [1 for _ in xrange(10000)]
for i in xrange(1, 10000):
    facts[i] = facts[i-1]*i % mod
    rev_fact[i] = mod_inverse(facts[i], mod)


def solve(n, k, i):
    print "as  ", pow(k, i, mod) * i
    return pow(i, n, mod) * i


with open("galactic.in", "r") as inp:
    _ = int(inp.readline())
    for line in inp:
        n, k = map(int, line.split())
        if k > n:
            print 0
        else:
            ans = pow(k, n, mod)
            t = n
            for i in xrange(k-1):
                if i % 2 == 1:
                    ans += pow(k,t-1, mod)*(t-1)
                    print k, t
                    print pow(k,t-1, mod)*(t-1)
                else:
                    ans -= pow(k, t-1, mod) * (t - 1)
                    print k, t
                    print -pow(k, t-1, mod) * (t - 1)
                ans %= mod

                t -= 1

        print ans