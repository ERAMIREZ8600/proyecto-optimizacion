import numpy as np
import sympy as sp

# Importación de los métodos modulares
from gd_method import step_descenso_gradiente
from newton_method import step_newton
from cg_method import step_gradiente_conjugado

def preparar_herramientas(func_texto, num_variables):
    """
    Genera funciones numéricas analíticas robustas traduciendo expresiones
    de SymPy a funciones evaluables puras de NumPy sin residuos simbólicos.
    """
    try:
        if num_variables == 1:
            vars_sym = [sp.symbols('x')]
        elif num_variables == 2:
            vars_sym = list(sp.symbols('x y'))
        else:
            vars_sym = list(sp.symbols(f'x0:{num_variables}'))
            
        f_simbolica = sp.parse_expr(func_texto.replace("^", "**"))
        
        # Derivadas analíticas explícitas
        grad_f = [sp.diff(f_simbolica, var) for var in vars_sym]
        hess_f = [[sp.diff(g, var) for var in vars_sym] for g in grad_f]
        
        # Lambdify estructurado pasándole la lista de símbolos exacta
        raw_f = sp.lambdify(vars_sym, f_simbolica, 'numpy')
        raw_grad = sp.lambdify(vars_sym, grad_f, 'numpy')
        raw_hess = sp.lambdify(vars_sym, hess_f, 'numpy')
        
        # Envolturas definitivas que aíslan el comportamiento matricial de una dimensión
        f_num = lambda *args: float(raw_f(*args))
        grad_num = lambda *args: np.array(raw_grad(*args), dtype=float).flatten()
        hess_num = lambda *args: np.array(raw_hess(*args), dtype=float).reshape(num_variables, num_variables)
        
        return f_num, grad_num, hess_num
    except Exception:
        return None, None, None

def backtracking_wolfe(f, grad, x, d, alpha=1.0, beta=1e-4, sigma=0.9, rho=0.5):
    """
    Búsqueda de línea inexacta bajo condiciones fuertes de Wolfe (Armijo + Curvatura).
    """
    f_actual = f(*x)
    g_actual = grad(*x)
    deriv_direccional = np.dot(g_actual, d)
    
    while alpha > 1e-10:
        x_next = x + alpha * d
        # Wolfe I: Condición de Armijo
        if f(*x_next) <= f_actual + beta * alpha * deriv_direccional:
            g_next = grad(*x_next)
            # Wolfe II: Condición de Curvatura Fuerte
            if abs(np.dot(g_next, d)) <= sigma * abs(deriv_direccional):
                return alpha
        alpha *= rho
    return alpha if alpha > 1e-10 else 1e-4

def ejecutar_optimizacion(metodo, f, grad, hess, x0, tol, max_iter, beta, sigma):
    x = np.array(x0, dtype=float)
    log_error = []
    trayectoria = [x.copy()]
    
    d_prev = None
    g_prev = None
    criterio_parada = "Máximo de iteraciones alcanzado"
    
    for i in range(max_iter):
        g_check = grad(*x)
        norma_g = np.linalg.norm(g_check)
        log_error.append(norma_g)
        
        if norma_g < tol:
            criterio_parada = f"Convergencia Exitosa (||grad f|| = {norma_g:.2e} < {tol})"
            break
            
        if metodo == "Descenso de Gradiente":
            x, g = step_descenso_gradiente(x, grad, backtracking_wolfe, f, beta, sigma)
        elif metodo == "Método de Newton":
            x, g = step_newton(x, grad, hess, backtracking_wolfe, f, beta, sigma)
        elif metodo == "Gradiente Conjugado (FR)":
            x, g, d_prev = step_gradiente_conjugado(x, grad, backtracking_wolfe, f, beta, sigma, i, d_prev, g_prev)
            g_prev = g.copy()
            
        trayectoria.append(x.copy())
        
    return x, log_error, np.array(trayectoria), criterio_parada