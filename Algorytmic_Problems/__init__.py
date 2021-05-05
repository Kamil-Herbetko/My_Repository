

n, m = map(int, input().split())
lista = [[0, 0, 0] for i in range(2*n)]
answer = 0



def update(v, tl, tr, l, r, new_val):
    if l > r:
        return
    if l == tl and tr == r:
        lista[v][new_val - 1] = new_val
    else:
        tm = (tl + tr)//2
        update(v*2, tl, tm, l, min(r, tm), new_val)
        update(v*2 + 1, tm + 1, tr, max(l, tm + 1), r, new_val)

def check(v):
    y = 0
    b = 0
    while v > 0:
        if lista[v][2] == 3:
            return 0
        if lista[v][1] == 2:
            b = 1
        if lista[v][0] == 1:
            y = 1
        v = v//2
    return b*y

for i in range(m):
    l, r, k = map(int, input().split())
    update(1, 1, n, l, r, k)
for node in range(n, 2*n):
    answer += check(node)

print(answer)
