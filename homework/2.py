import random
citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

def D(p1, p2):
    x1, y1=p1
    x2, y2=p2
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def allpath(p):
    dist = 0
    plen = len(p)
    for i in range(plen):
        dist += D(citys[p[i]],citys[p[(i+1)%plen]])
    return dist

def neighbor(route):
    new_route = route[:]
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

# 爬山演算法
def hillClimbing(overtime=1):
    n = len(citys)
    for i in range(3,n-1):
        overtime*=i   
    current_route = list(range(n))
    random.shuffle(current_route)  # 初始隨機路徑
    current_distance = allpath(current_route)

    for step in range(overtime):
        neighbor_route = neighbor(current_route)
        neighbor_distance = allpath(neighbor_route)

        if neighbor_distance < current_distance:
            current_route = neighbor_route
            current_distance = neighbor_distance
            print(f"Step {step}: 找到更短路徑 = {current_distance:.3f}")

    return current_route, current_distance

best_route, best_distance = hillClimbing()
print("\n最佳路徑：", best_route)
print("最短距離：", round(best_distance, 3))
