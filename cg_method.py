import numpy as np

def step_gradiente_conjugado(x, grad_num, backtracking_wolfe, f_num, beta_val, sigma_val, idx, d_prev, g_prev):
    g = grad_num(*x)
    
    if idx == 0 or d_prev is None or g_prev is None:
        d = -g
    else:
        num = np.dot(g, g)
        den = np.dot(g_prev, g_prev)
        beta_fr = num / den if den > 1e-12 else 0.0
        d = -g + beta_fr * d_prev
        
    alpha = backtracking_wolfe(f_num, grad_num, x, d, beta=beta_val, sigma=sigma_val)
    x_next = x + alpha * d
    return x_next, g, d