'''
Code adapted from http://pytorch.org/tutorials/beginner/pytorch_with_examples.html
'''
import torch
from initializer import *
from torch.autograd import Variable

def normalize(y_pred):
    # copied from https://discuss.pytorch.org/t/normalize-a-vector-to-0-1/14594
    min_v = torch.min(y_pred)
    range_v = torch.max(y_pred) - min_v
    if range_v.data[0] > 0:
        return (y_pred - min_v) / range_v.data[0]
    else:
        return torch.zeros(y_pred.size())

dtype = torch.FloatTensor
# dtype = torch.cuda.FloatTensor # Uncomment this to run on GPU

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 10, 30, 20, 11


# Create random Tensors to hold input and outputs, and wrap them in Variables.
# Setting requires_grad=False indicates that we do not need to compute gradients
# with respect to these Variables during the backward pass.
(x_python_list, y_python_list) = set_up_problem()

x = Variable(torch.FloatTensor(x_python_list), requires_grad=False)
y = Variable(torch.FloatTensor(y_python_list), requires_grad=False)

# Create random Tensors for weights, and wrap them in Variables.
# Setting requires_grad=True indicates that we want to compute gradients with
# respect to these Variables during the backward pass.
w1 = Variable(torch.randn(D_in, H).type(dtype), requires_grad=True)
w2 = Variable(torch.randn(H, D_out).type(dtype), requires_grad=True)

loss_fn = torch.nn.L1Loss()

learning_rate = 1e-6
for t in range(1000):
    # Forward pass: compute predicted y using operations on Variables; these
    # are exactly the same operations we used to compute the forward pass using
    # Tensors, but we do not need to keep references to intermediate values since
    # we are not implementing the backward pass by hand.
    y_pred = x.mm(w1).clamp(min=0).mm(w2)

    # Compute and print loss using operations on Variables.
    # Now loss is a Variable of shape (1,) and loss.data is a Tensor of shape
    # (1,); loss.data[0] is a scalar value holding the loss.
    loss = (y_pred - y).pow(2).sum()
    print(t, loss.data[0])

    # Use autograd to compute the backward pass. This call will compute the
    # gradient of loss with respect to all Variables with requires_grad=True.
    # After this call w1.grad and w2.grad will be Variables holding the gradient
    # of the loss with respect to w1 and w2 respectively.
    loss.backward()

    # Update weights using gradient descent; w1.data and w2.data are Tensors,
    # w1.grad and w2.grad are Variables and w1.grad.data and w2.grad.data are
    # Tensors.
    w1.data -= learning_rate * w1.grad.data
    w2.data -= learning_rate * w2.grad.data

    # Manually zero the gradients after updating weights
    w1.grad.data.zero_()
    w2.grad.data.zero_()



(x_test, y_test) = set_up_test_case()
x = Variable(torch.FloatTensor(x_test), requires_grad=False)
y = Variable(torch.FloatTensor(y_test), requires_grad=False)

y_pred = normalize(x.mm(w1).clamp(min=0).mm(w2))
loss = (y_pred - y).pow(2).sum()
print("LOSS", loss.data[0])
print("PREDICTION")
print(y_pred[0])
print("ACTUAL")
print(y[0])


