n, m = map(int, input().split())
lista = [[0, 0, 0] for i in range(4*n)]
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

def check(v, tl, tr,yellow, blue):
    if lista[v][2] == 3:
        return 0
    if lista[v][1] == 2:
        blue = 1
    if lista[v][0] == 1:
        yellow = 1
    if tl == tr:
        return yellow*blue
    tm = (tl + tr)//2
    return check(v*2, tl, tm, yellow, blue) + check(v*2 + 1, tm + 1, tr, yellow, blue)


for i in range(m):
    l, r, k = map(int, input().split())
    update(1, 1, n, l, r, k)

print(check(1, 1, n, 0, 0))
