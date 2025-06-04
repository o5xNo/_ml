from micrograd.engine import Value

x = Value(0.0)
y = Value(0.0)
z = Value(0.0)

lr = 0.0006

for i in range(10000):
    loss = x**2+y**2+z**2-2*x-4*y-6*z+8
    x.grad=0
    y.grad=0
    z.grad=0
    loss.backward()
    x.data-=x.grad*lr
    y.data-=y.grad*lr
    z.data-=z.grad*lr


print(f'x={x.data:.4f},y={y.data:.4f},z={z.data:.4f}')