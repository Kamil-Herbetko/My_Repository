

n, m = map(int, input().split())
lista = [[0, 0, 0] for i in range(2*n)]
answear = 0



def update(v, tl, tr, l, r, new_val):
    if l > r:
        return
    if l == tl and tr == r:
        lista[v][new_val - 1] = new_val
    else:
        tm = (tl + tr)//2
        update(v*2, tl, tm, l, min(r, tm), new_val)
        update(v*2 + 1, tm + 1, tr, max(l, tm + 1), r, new_val)

def check(v, yellow, blue):
    if lista[v][2] == 3:
        return 0
    if ((yellow or lista[v][0] == 1) and (blue or lista[v][1])):
        return 1
    else:
        if v == 0:
            return 0
        else:
            return check(v//2, yellow or lista[v][0] == 1, blue or lista[v][1] == 2)

for i in range(m):
    l, r, k = map(int, input().split())
    update(1, 1, n, l, r, k)
for node in range(n, 2*n):
    answear += check(node, False, False)

print(answear)
