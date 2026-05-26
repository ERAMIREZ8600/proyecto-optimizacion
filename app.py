import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from engine import preparar_herramientas, ejecutar_optimizacion

# 1. Configuración de la página estilo Dashboard Premium
st.set_page_config(page_title="Optimization Dashboard", layout="wide")

# 2. CSS para fijar el aspecto visual moderno (Look Skillset)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FB; }
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E6E9EF;
    }
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        border: 1px solid #F0F2F6;
    }
    .stPlotlyChart {
        background-color: #FFFFFF;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        padding: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #1A1C1E;
        color: white;
        font-weight: 600;
        border: none;
        height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #404040;
        color: #FFFFFF;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.write("# Dashboard de Optimización")
st.caption("Proyecto Métodos de Optimización • Emilio Ramirez • Universidad Mayor")

# 3. Barra lateral (Panel de Configuración de Datos de Entrada)
with st.sidebar:
    st.title("Skillset Config")
    st.markdown("---")
    
    n_vars = st.number_input("Número de variables", min_value=1, max_value=10, value=2)
    
    if n_vars == 1:
        default_func = "x**2 - 4*x + 3"
        default_init = "10.0"
        st.caption("Variable aceptada: x")
    elif n_vars == 2:
        default_func = "x**2 + y**2 + x*y"
        default_init = "4.0, 4.0"
        st.caption("Variables aceptadas de manera estándar: x, y")
    else:
        default_func = " + ".join([f"x{i}**2" for i in range(n_vars)])
        default_init = ", ".join(["4.0"] * n_vars)
        st.caption(f"Variables en formato indexado: " + ", ".join([f"x{i}" for i in range(n_vars)]))

    func_txt = st.text_input("Función objetivo f", value=default_func)
    
    # --- NUEVO APARTADO: Instructivo desplegable de sintaxis matemática ---
    with st.expander("📖 Guía de Escritura Matemática"):
        st.markdown("""
        Para que el motor analítico procese correctamente tu función, utiliza la siguiente estructura estándar:
        
        | Operación / Función | Entrada en Texto | Ejemplo Práctico |
        | :--- | :--- | :--- |
        | **Multiplicación** | Siempre usa `*` | `4*x` *(en vez de 4x)* |
        | **Potencias / Exponentes** | Usa `**` (o `^`) | `x**2` o `x^2` |
        | **Raíz Cuadrada** | `sqrt(x)` | `sqrt(x**2 + y**2)` |
        | **Número de Euler ($e^x$)** | `exp(x)` | `exp(-x)` |
        | **Logaritmo Natural** | `log(x)` | `log(x) + y` |
        | **Trigonométricas** | `sin(x)`, `cos(x)`, `tan(x)` | `sin(x) * cos(y)` |
        
        *⚠️ **Nota Importante:** Recuerda marcar explícitamente las multiplicaciones. Escribir `2x` arrojará un error; la forma correcta es `2*x`.*
        """)
    st.markdown("---")
    
    metodo_sel = st.selectbox("Algoritmo", ["Descenso de Gradiente", "Método de Newton", "Gradiente Conjugado (FR)"])
    init_txt = st.text_input("Punto de partida (separado por comas)", value=default_init)
    
    st.subheader("Condiciones de Wolfe")
    beta_val = st.slider("Beta (Wolfe I - Armijo)", 1e-4, 0.3, 1e-4, format="%.4f")
    sigma_val = st.slider("Sigma (Wolfe II - Curvatura)", 0.1, 0.9, 0.9, format="%.2f")
    
    st.subheader("Criterios de Parada")
    tol_val = st.number_input("Tolerancia de convergencia", value=1e-6, format="%.1e")
    max_it = st.number_input("Número máximo de iteraciones", value=100, min_value=1, max_value=1000)
    
    btn = st.button("🚀 Ejecutar Análisis")

# Parsear el punto de partida ingresado como texto a una lista de flotantes
try:
    x_init = [float(i.strip()) for i in init_txt.split(",")]
except Exception:
    x_init = [4.0] * n_vars

# Compilación y preparación analítica de las herramientas simbólicas
f_n, g_n, h_n = preparar_herramientas(func_txt, n_vars)

# 4. Bloque de Despliegue de Resultados Esperados
if btn and f_n:
    if len(x_init) != n_vars:
        st.error(f"Error dimensional: El punto inicial debe contener exactamente {n_vars} coordenadas.")
    else:
        # Ejecución del orquestador matemático
        x_opt, errores, camino, motivo = ejecutar_optimizacion(
            metodo_sel, f_n, g_n, h_n, x_init, tol_val, int(max_it), beta_val, sigma_val
        )
        
        # Forzamos la evaluación numérica real extrayendo los componentes nativos
        try:
            res_raw = f_n(*x_opt)
            if hasattr(res_raw, 'evalf'):
                valor_optimo_puro = float(res_raw.evalf())
            elif isinstance(res_raw, (np.ndarray, list)):
                valor_optimo_puro = float(np.array(res_raw).flatten()[0])
            else:
                valor_optimo_puro = float(res_raw)
        except Exception:
            valor_optimo_puro = float(f_n(*camino[-1]))

        # Despliegue de métricas principales exigidas por el enunciado
        m1, m2, m3 = st.columns(3)
        m1.metric("Valor Óptimo f(x*)", f"{valor_optimo_puro:.4f}")
        m2.metric("Iteraciones Realizadas", f"{len(errores)}")
        st.info(f"🏁 **Criterio de parada alcanzado:** {motivo}")

        # Mostrar el punto mínimo encontrado
        st.markdown("### 📍 Punto Mínimo Encontrado")
        columnas_pt = [f"Variable x{i}" if n_vars > 2 else (['Variable X', 'Variable Y'][i] if n_vars == 2 else ['Variable X'][i]) for i in range(n_vars)]
        df_pt = pd.DataFrame([x_opt], columns=columnas_pt)
        st.dataframe(df_pt, use_container_width=True)

        st.markdown("### Análisis de Rendimiento")
        col_left, col_right = st.columns([1.2, 1])
        
        with col_left:
            fig_err = go.Figure(go.Scatter(y=errores, mode='lines', fill='tozeroy', 
                                         line=dict(color='#1A1C1E', width=3),
                                         fillcolor='rgba(26, 28, 30, 0.1)'))
            fig_err.update_layout(title="Gráfico de convergencia: Error (||grad f||) versus Iteraciones", 
                                template="simple_white", height=380,
                                xaxis_title="Número de Iteración", yaxis_title="Magnitud del Error",
                                yaxis_type="log")
            st.plotly_chart(fig_err, use_container_width=True)

        with col_right:
            if n_vars == 2:
                margin_x = max(abs(camino[:,0].max() - camino[:,0].min()) * 0.5, 1.0)
                margin_y = max(abs(camino[:,1].max() - camino[:,1].min()) * 0.5, 1.0)
                
                x_m = np.linspace(camino[:,0].min() - margin_x, camino[:,0].max() + margin_x, 50)
                y_m = np.linspace(camino[:,1].min() - margin_y, camino[:,1].max() + margin_y, 50)
                X_grid, Y_grid = np.meshgrid(x_m, y_m)
                
                Z_grid = np.zeros_like(X_grid)
                for r in range(X_grid.shape[0]):
                    for c in range(X_grid.shape[1]):
                        Z_grid[r,c] = f_n(X_grid[r,c], Y_grid[r,c])

                fig_path = go.Figure(data=[
                    go.Contour(z=Z_grid, x=x_m, y=y_m, colorscale='Greys', opacity=0.15, showscale=False),
                    go.Scatter(x=camino[:,0], y=camino[:,1], mode='lines+markers', 
                               line=dict(color='#FF4B4B', width=2),
                               marker=dict(size=6, symbol='circle', color='#1A1C1E'))
                ])
                fig_path.update_layout(title="Valor Agregado: Mapa de Trayectoria del Algoritmo (2D)", 
                                     template="simple_white", height=380)
                st.plotly_chart(fig_path, use_container_width=True)
                
            elif n_vars == 1:
                x_vals = np.linspace(camino.min() - 2, camino.max() + 2, 100)
                y_vals = [f_n(xv) for xv in x_vals]
                
                camino_plano = camino.flatten()
                y_camino = [f_n(pt) for pt in camino_plano]
                
                fig_1d = go.Figure([
                    go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)', line=dict(color='#1A1C1E', width=2)),
                    go.Scatter(x=camino_plano, y=y_camino, mode='markers+lines', name='Pasos', 
                               line=dict(color='#FF4B4B', width=1.5), 
                               marker=dict(size=8, color='#FF4B4B', symbol='circle'))
                ])
                fig_1d.update_layout(title="Valor Agregado: Trayectoria del Algoritmo sobre la Curva (1D)", 
                                    template="simple_white", height=380,
                                    xaxis_title="Variable X", yaxis_title="f(x)")
                st.plotly_chart(fig_1d, use_container_width=True)
            else:
                st.warning("⚠️ El mapa espacial de curvas de nivel (trayectoria 2D) está inhabilitado para optimizaciones con más de 2 variables.")

        # Historial de Pasos
        st.markdown("### Historial de Pasos")
        columnas_hist = [f"Coordenada x{i}" if n_vars > 2 else (['Coordenada X', 'Coordenada Y'][i] if n_vars == 2 else ['Coordenada X'][i]) for i in range(n_vars)]
        df_steps = pd.DataFrame(camino, columns=columnas_hist)
        df_steps.insert(0, "Iteración", range(len(camino)))
        
        df_steps["Valor f(x)"] = [f_n(*p) for p in camino]
        st.dataframe(df_steps.style.format({"Valor f(x)": "{:.6f}"}), use_container_width=True)
else:
    st.info("👋 Bienvenido. Configure los parámetros solicitados en el panel lateral y presione 'Ejecutar Análisis' para procesar el modelo local.")