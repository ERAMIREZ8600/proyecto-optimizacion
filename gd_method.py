import numpy as np

def step_descenso_gradiente(x, grad_num, backtracking_wolfe, f_num, beta_val, sigma_val):
    g = grad_num(*x)
    d = -g 
    alpha = backtracking_wolfe(f_num, grad_num, x, d, beta=beta_val, sigma=sigma_val)
    x_next = x + alpha * d
    return x_next, g