import math
pi = math.pi


def calc(rad):

    ar = 0
    grad = 0
    ps = [(float(rad), 0.000000000)]
    for j in xrange(0, len(v)-1):
        cur = v[j]
        if not -1.000001 < 1.000000000*(2 * rad * rad - cur * cur) / (2 * rad * rad) < 1.00000001:
            return -1, 0
        degree = math.acos(1.000000000 * (2 * rad * rad - cur * cur) / (2 * rad * rad))
        grad += degree
        if grad >= 2*pi:
            return -1, 0.000000
        ps.append((rad * math.cos(grad), rad * math.sin(grad)))
    for j in xrange(len(ps)):
        ar += ps[j][0]*ps[(j+1) % len(ps)][1] - ps[(j+1) % len(ps)][0]*ps[j][1]

    return dist((rad - ps[-1][0], 0 - ps[-1][1])) - v[-1], ar / 2


def dist(x):
    return math.sqrt(x[0]*x[0] + x[1]*x[1])

N = int(raw_input())
v = []
while N > 0:
    N -= 1
    v.append(int(raw_input()))
v.sort()
l, r, Sum, area = 0, 1000000, 0, 0
for i in xrange(100, 0, -1):
    mid = l + (r-l)/2.000000000
    p = calc(mid)
    Sum = p[0]
    area = p[1]
    if v[-1] > 2*mid or Sum < 0:
        l = mid
    else:
        r = mid
    print mid
if v[-1] >= sum(v[:-1]):
    print "0.00"
else:
    if abs(Sum) > 0.000001:
        print "0.00"
    else:
        print "%.2f" % area
