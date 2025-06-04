import torch 

x = torch.tensor(0.0, requires_grad=True)
y = torch.tensor(0.0, requires_grad=True)
z = torch.tensor(0.0, requires_grad=True)

lr = 0.0012

for i in range(10000):
    loss = x**2+y**2+z**2-2*x-4*y-6*z+8
    loss.backward()
    x.data-=x.grad*lr
    y.data-=y.grad*lr
    z.data-=z.grad*lr
    x.grad.zero_()
    y.grad.zero_()
    z.grad.zero_()

print(f'x={x.data:.4f},y={y.data:.4f},z={z.data:.4f}')