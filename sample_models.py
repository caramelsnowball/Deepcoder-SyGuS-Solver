from intexp import *
from model import *
from oracle import *
from solver import *

x = Variable("x")
y = Variable("y")
z = Variable("z")
f = Variable("f")
c1 = GTE(f, x)
c2 = GTE(f, y)
c3 = GTE(f, z)
c4 = Equals(f, x)
c5 = Equals(f, y)
c6 = Equals(f, z)
d1 = Or(And(Equals(x, y),Equals(y,z)),Or(GT(f, x), Or(GT(f, y), GT(f, z))))
d2 = Or(LTE(f, x), Or(LTE(f, y), LTE(f, z)))
d3 = Or(Equals(f, x), Or(Equals(f, y), Equals(f, z)))
e1 = ITE(GT(z, y), Equals(f, Const(2)), Equals(f, Const(1)))
e2 = ITE(LT(z, x), Equals(f, Const(0)), e1)
e3 = ITE(LT(x, y), e2, Const(True))

sample_model1 = Model([c1, c2, Or(c4, c5)], ["x", "y", "z"], "f")


sample_model2 = Model([c1, c2, c3, Or(c4, Or(c5, c6))], ["x", "y", "z"], "f")

sample_model3 = Model([Equals(f, Multiply(Add(x, x), Subtract(y, z)))], ["x", "y", "z"], "f")

sample_model4 = Model([Or(Equals(x, Const(0)), Equals(f, x)), Not(Equals(f, Const(0)))], ["x", "y", "z"], "f")

sample_model5 = Model([Equals(f, Add(x, Multiply(y, Const(2))))], ["x", "y", "z"], "f")

sample_model6 = Model([Equals(f, Add(x, Multiply(y, z)))], ["x", "y", "z"], "f")

sample_model7 = Model([Equals(f, Subtract(y, Multiply(y, z)))], ["x", "y", "z"], "f")

sample_model8 = Model([d1, d2, d3], ["x", "y", "z"], "f")

sample_model9 = Model([c3, d2, d3], ["x", "y", "z"], "f")

sample_model10 = Model([ITE(Equals(x, y), Equals(f, Const(4)),Equals(f, Const(3)))], ["x", "y", "z"], "f")


sample_models = [sample_model1, sample_model2, sample_model3, sample_model4, sample_model10, sample_model9, sample_model8, sample_model7, sample_model6, sample_model5]

sample_model11 = Model([e3], ["x", "y", "z"], "f")

test_program = synthesize(sample_model11, False, True)
programs = []
programs.append(synthesize(sample_model1, False, False))
programs.append(synthesize(sample_model2, False, False))
programs.append(synthesize(sample_model3, True, False))
programs.append(synthesize(sample_model4, True))
programs.append(synthesize(sample_model10, True))
programs.append(synthesize(sample_model9, True, False))
programs.append(synthesize(sample_model8, True, False))
programs.append(synthesize(sample_model7, True, False))
programs.append(synthesize(sample_model6, True, False))
programs.append(synthesize(sample_model5, True))


