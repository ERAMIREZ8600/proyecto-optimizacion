import numpy as np

def step_newton(x, grad_num, hess_num, backtracking_wolfe, f_num, beta_val, sigma_val):
    g = grad_num(*x)
    h = hess_num(*x)
    
    try:
        if x.shape[0] == 1:
            # Caso univariable directo escalar
            d = np.array([-g[0] / h[0, 0]]) if abs(h[0, 0]) > 1e-12 else -g
        else:
            d = np.linalg.solve(h, -g)
    except np.linalg.LinAlgError:
        d = -g
        
    alpha = backtracking_wolfe(f_num, grad_num, x, d, beta=beta_val, sigma=sigma_val)
    x_next = x + alpha * d
    return x_next, g