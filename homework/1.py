def f(x, y, z):
    return x*x+y*y+z*z-2*x-4*y-6*z+8

def df(x, y, z):
    return (2*x-2, 2*y-4, 2*z-6)

x=0.0
y=0.0
z=0.0
alpha=0.1
stop=0.00001
overtimes=1000

for i in range(overtimes):
    dx, dy, dz=df(x, y, z)
    x2=x-alpha*dx
    y2=y-alpha*dy
    z2=z-alpha*dz

    if abs(x2-x)<stop and abs(y2-y)<stop and abs(z2-z)<stop:
        break

    x=x2
    y=y2
    z=z2

print(f"最低點在x={x:.4f},y={y:.4f},z={z:.4f}")
print(f"最小值f= {f(x, y, z):.4f}")
x=4