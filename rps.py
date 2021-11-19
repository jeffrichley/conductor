from cvxopt import matrix, solvers
from cvxopt.modeling import op
from cvxopt.modeling import variable
from cvxopt.solvers import options
glpksolver = 'cvxopt_glpk'
options['show_progress'] = False

# Minimize: U + R + P + S
c = matrix([-1., 0., 0., 0.])
# 1. U – P + S <= 0 => [1, 0,-1, 1]
# 2. U + R – S <= 0 => [1, 1, 0,-1]
# 3. U – R + P <= 0 => [1,-1, 1, 0]
# 4. -R <= 0 => [0,-1, 0, 0]
# 5. -P <= 0 => [0, 0,-1, 0]
# 6. -S <= 0 => [0, 0, 0,-1]
# 7. R + P + S <= 1 => [0, 1, 1, 1]
# 8. -R – P – S <=-1 => [0,-1,-1,-1]
G = matrix([[1., 1., 1., 0., 0., 0., 0., 0.],
            [0., 1., -1., -1., 0., 0., 1., -1],
            [-1., 0., 1., 0., -1., 0., 1., -1.],
            [1., -1., 0., 0., 0., -1., 1., -1.]])
h = matrix([0., 0., 0., 0., 0., 0., 1., -1.])
sol = solvers.lp(c, G, h, solver=glpksolver)
print(sol['status'])
print(sol['x'])
# print(sol)

# print('------------------------------')
# Duff Bear DPV 7.4
# A = matrix([[-1., 1.], [2., 1.]])
# b = matrix([0., 3000.])
# c = matrix([-1., -1.5])
# sol = solvers.lp(c, A, b)
# print(sol['status'])
# print(sol['x'])



c = matrix([0., 0., 0.])
# 1. U – P + S <= 0 => [1, 0,-1, 1]
# 2. U + R – S <= 0 => [1, 1, 0,-1]
# 3. U – R + P <= 0 => [1,-1, 1, 0]
# 4. -R <= 0 => [0,-1, 0, 0]
# 5. -P <= 0 => [0, 0,-1, 0]
# 6. -S <= 0 => [0, 0, 0,-1]
# 7. R + P + S <= 1 => [0, 1, 1, 1]
# 8. -R – P – S <=-1 => [0,-1,-1,-1]
G = matrix([[0., 1., -1., -1., 0., 0., 1., -1],
            [-1., 0., 1., 0., -1., 0., 1., -1.],
            [1., -1., 0., 0., 0., -1., 1., -1.]])
h = matrix([0., 0., 0., 0., 0., 0., 1., -1.])
sol = solvers.lp(c, G, h, solver=glpksolver)
print(sol['status'])
print(sol['x'])