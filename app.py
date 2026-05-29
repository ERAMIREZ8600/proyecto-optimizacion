import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import base64
from engine import preparar_herramientas, ejecutar_optimizacion

# 1. Configuración de la página estilo Dashboard de Alta Fidelidad (Light)
st.set_page_config(page_title="Optimization Lab", layout="wide", initial_sidebar_state="expanded")

# FUNCIÓN AUXILIAR: Transforma imágenes locales a formato base64 para que el HTML de Streamlit las lea sin bloqueos
def obtener_imagen_base64(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return ""

# Cargar los bytes de los iconos limpios desde tu carpeta assets
cube_b64 = obtener_imagen_base64("assets/cube_icon.png")
panel_b64 = obtener_imagen_base64("assets/panel_icon.png")

# 2. Inyección CSS para Diseño Light Tech Premium (Clean Minimalist)
st.markdown("""
    <style>
    /* Fondo general de la aplicación en tono gris muy claro y limpio */
    .stApp {
        background-color: #F4F6F9 !important;
        color: #1E293B !important;
    }
    
    /* Panel lateral de configuración en un tono blanco-azulado tenue */
    section[data-testid="stSidebar"] {
        background-color: #EBF0F5 !important;
        border-right: 1px solid #D2DCE5 !important;
    }
    
    /* Textos generales de la barra lateral */
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: #334155 !important;
    }
    
    /* Tarjetas de Métricas y Estado (Blancas con bordes suaves y sombra sutil) */
    div[data-testid="stMetric"], div.stAlert {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        padding: 22px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* Ajustes de color dentro de las métricas */
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0F172A !important;
    }
    
    /* Contenedores de los gráficos integrados al entorno claro */
    .stPlotlyChart {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }
    
    /* Botón de Ejecución Azul Eléctrico Corporativo */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #1E6091 0%, #1A73E8 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        height: 3.8em !important;
        box-shadow: 0 4px 10px rgba(26, 115, 232, 0.2) !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1A73E8 0%, #1557B0 100%) !important;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.4) !important;
        transform: translateY(-1px);
    }
    
    /* Inputs de texto, selectores y números estilizados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 10px !important;
    }
    
    /* Estilización de tablas de datos e historial */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    /* Contenedores Flexbox para alinear los encabezados con sus respectivos íconos */
    .main-header-container, .sidebar-header-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO PRINCIPAL AJUSTADO: Cubo Azul + PANEL DE CONTROL ---
if cube_b64:
    st.markdown(f"""
        <div class='main-header-container'>
            <img src='data:image/png;base64,{cube_b64}' width='45' height='45'>
            <h1 style='color: #1A73E8; font-family: sans-serif; font-weight: 700; margin: 0; padding: 0;'>PANEL DE CONTROL</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h1 style='color: #1A73E8; font-family: sans-serif; font-weight: 700;'>🎛️ PANEL DE CONTROL</h1>", unsafe_allow_html=True)

st.markdown("<p style='color: #64748B; font-size: 0.95em; margin-top: -10px;'>📡 Estación Analítica • Métodos de Optimización • Grupo Punto Crítico • Universidad Mayor</p>", unsafe_allow_html=True)

# 3. Barra lateral (Panel de Configuración de Datos de Entrada)
with st.sidebar:
    # --- BARRA LATERAL AJUSTADA: Barras Negras + OPTIMIZATION LAB ---
    if panel_b64:
        st.markdown(f"""
            <div class='sidebar-header-container'>
                <img src='data:image/png;base64,{panel_b64}' width='32' height='32'>
                <h2 style='color: #1E6091; font-size: 1.5em; font-weight: 600; margin: 0; padding: 0;'> METODOS DE OPTIMIZATION </h2>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color: #1E6091; font-size: 1.5em; font-weight: 600;'>🧪 OPTIMIZMETODOS DE OPTIMIZATIONTION </h2>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    n_vars = st.number_input("Número de variables", min_value=1, max_value=10, value=2)
    
    if n_vars == 1:
        default_func = "x**2 - 4*x + 3"
        st.caption("Variable aceptada: x")
    elif n_vars == 2:
        default_func = "x**2 + y**2 + x*y"
        st.caption("Variables aceptadas de manera estándar: x, y")
    else:
        default_func = " + ".join([f"x{i}**2" for i in range(n_vars)])
        st.caption(f"Variables en formato indexado: " + ", ".join([f"x{i}" for i in range(n_vars)]))

    func_txt = st.text_input("Función objetivo f", value=default_func)
    
    with st.expander("📖 Guía de Escritura Matemática"):
        st.markdown("""
        | Operación | Sintaxis | Ejemplo |
        | :--- | :--- | :--- |
        | **Multiplicación** | Usar siempre `*` | `4*x` |
        | **Potencias** | Usar `**` o `^` | `x**2` o `x^2` |
        | **Raíz Cuadrada** | `sqrt(x)` | `sqrt(x**2 + y**2)` |
        | **Euler ($e^x$)** | `exp(x)` | `exp(-x)` |
        | **Logaritmo** | `log(x)` | `log(x) + y` |
        """)
    st.markdown("---")
    
    metodo_sel = st.selectbox("Algoritmo", ["Descenso de Gradiente", "Método de Newton", "Gradiente Conjugado (FR)"])
    
    st.markdown("<b style='color: #1E6091;'>📍 Coordenadas Iniciales (x₀)</b>", unsafe_allow_html=True)
    x_init = []
    
    # Renderizado dinámico de los cuadros independientes para las coordenadas
    columnas_puntos = st.columns(min(n_vars, 3))
    for i in range(n_vars):
        label_coor = "Coord. X" if n_vars == 1 else (f"Coord. {['X', 'Y'][i]}" if n_vars == 2 else f"Coord. x{i}")
        with columnas_puntos[i % 3]:
            val_coor = st.number_input(label_coor, value=4.0, key=f"init_val_{i}", step=0.5, format="%.2f")
            x_init.append(val_coor)
            
    st.markdown("---")
    
    st.markdown("<b style='color: #1E6091;'>⚙️ Parámetros de Wolfe</b>", unsafe_allow_html=True)
    beta_val = st.slider("Beta (Wolfe I - Armijo)", 1e-4, 0.3, 1e-4, format="%.4f")
    sigma_val = st.slider("Sigma (Wolfe II - Curvatura)", 0.1, 0.9, 0.9, format="%.2f")
    
    st.markdown("---")
    st.markdown("<b style='color: #1E6091;'>🛑 Criterios de Parada</b>", unsafe_allow_html=True)
    tol_val = st.number_input("Tolerancia de convergencia", value=1e-6, format="%.1e")
    max_it = st.number_input("Número máximo de iteraciones", value=100, min_value=1, max_value=1000)
    
    st.markdown("<br>", unsafe_allow_html=True)
    btn = st.button("⚡ INICIAR SIMULACIÓN ANALÍTICA")

# Compilación analítica de herramientas matemáticas desde el motor
f_n, g_n, h_n = preparar_herramientas(func_txt, n_vars)

# 4. Bloque de Despliegue de Resultados e Interfaces Gráficas
if btn and f_n:
    if len(x_init) != n_vars:
        st.error(f"Error dimensional: El punto inicial debe contener exactamente {n_vars} coordenadas.")
    else:
        # --- Fundamento Analítico Dinámico ---
        st.markdown(f"## 📖 Fundamento Analítico: {metodo_sel}")
        
        if metodo_sel == "Descenso de Gradiente":
            st.info("**¿En qué consiste?** Es un algoritmo de optimización de primer orden. Busca el mínimo local de la función realizando pasos proporcionales al negativo del gradiente en el punto actual, ya que esta dirección representa el máximo descenso local.")
            st.latex(r"d_k = -\nabla f(x_k)")
            st.info("**Fórmula de actualización:** El algoritmo calcula secuencialmente la siguiente posición combinando el punto previo con la dirección y el tamaño de paso sintonizado dinámicamente:")
            st.latex(r"x_{k+1} = x_k + \alpha_k d_k")
            
        elif metodo_sel == "Método de Newton":
            st.info("**¿En qué consiste?** Es un algoritmo de segundo orden. A diferencia del gradiente, utiliza tanto la pendiente como la curvatura local de la función mediante las segundas derivadas parciales organizadas en la Matriz Hessiana.")
            st.latex(r"H f(x_k)")
            st.info("**Fórmula de actualización:** Al mapear la curvatura, el método aproxima la función como una parábola cuadrática, permitiendo una convergencia rápida hacia el mínimo real:")
            st.latex(r"x_{k+1} = x_k - [H f(x_k)]^{-1} \nabla f(x_k)")
            
        elif metodo_sel == "Gradiente Conjugado (FR)":
            st.info("**¿En qué consiste?** Es un método intermedio de optimización que utiliza la variante de Fletcher-Reeves (FR). Genera direcciones de búsqueda conjugadas (ortogonales respecto a la matriz del sistema), eliminando el avance en zigzag clásico en valles estrechos sin el costo de calcular la Hessiana.")
            st.latex(r"d_k = -\nabla f(x_k) + \beta_k^{FR} d_{k-1}")
            st.info("**Fórmula de actualización:** Mantiene la estructura de avance lineal calculando el paso con las condiciones de curvatura fuertes de Wolfe:")
            st.latex(r"x_{k+1} = x_k + \alpha_k d_k")
            
        st.markdown("---")

        # Ejecución del orquestador matemático
        x_opt, errores, camino, motivo = ejecutar_optimizacion(
            metodo_sel, f_n, g_n, h_n, x_init, tol_val, int(max_it), beta_val, sigma_val
        )
        
        try:
            res_raw = f_n(*x_opt)
            valor_optimo_puro = float(res_raw.evalf()) if hasattr(res_raw, 'evalf') else float(res_raw)
        except Exception:
            valor_optimo_puro = float(f_n(*camino[-1]))

        # Sección superior de paneles informativos
        st.markdown("<h3 style='color: #1E293B;'>🖥️ TELEMETRÍA Y ESTADO DEL MODELO</h3>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Valor Mínimo f(x*)", f"{valor_optimo_puro:.4f}")
        m2.metric("Iteraciones Procesadas", f"{len(errores)}")
        
        with m3:
            st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
            st.success(f"🏁 {motivo}")

        st.markdown("<h3 style='color: #1E293B;'>🎯 MATRIZ DE MÍNIMOS LOCALES</h3>", unsafe_allow_html=True)
        columnas_pt = [f"Variable x{i}" if n_vars > 2 else (['Variable X', 'Variable Y'][i] if n_vars == 2 else ['Variable X'][i]) for i in range(n_vars)]
        df_pt = pd.DataFrame([x_opt], columns=columnas_pt)
        st.dataframe(df_pt, use_container_width=True)

        st.markdown("<h3 style='color: #1E293B;'>📈 MONITOREO GRÁFICO DEL RENDIMIENTO</h3>", unsafe_allow_html=True)
        col_left, col_right = st.columns([1.2, 1])
        
        with col_left:
            fig_err = go.Figure(go.Scatter(y=errores, mode='lines', fill='tozeroy', 
                                         line=dict(color='#1A73E8', width=3),
                                         fillcolor='rgba(26, 115, 232, 0.06)'))
            fig_err.update_layout(title="Métrica: Magnitud del Error (||grad f||) por Iteración", 
                                template="simple_white", height=400,
                                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                xaxis_title="Iteración", yaxis_title="Magnitud del Gradiente (Escala Log)",
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
                    go.Contour(z=Z_grid, x=x_m, y=y_m, colorscale='Blues', opacity=0.25, showscale=False),
                    go.Scatter(x=camino[:,0], y=camino[:,1], mode='lines+markers', 
                               line=dict(color='#1A73E8', width=2.5),
                               marker=dict(size=7, symbol='circle', color='#1E6091', 
                                           line=dict(color='#FFFFFF', width=1)))
                ])
                fig_path.update_layout(title="Mapa Espacial: Trayectoria de Descenso 2D", 
                                     template="simple_white", height=400,
                                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_path, use_container_width=True)
                
            elif n_vars == 1:
                x_vals = np.linspace(camino.min() - 2, camino.max() + 2, 100)
                y_vals = [f_n(xv) for xv in x_vals]
                camino_plano = camino.flatten()
                y_camino = [f_n(pt) for pt in camino_plano]
                
                fig_1d = go.Figure([
                    go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)', line=dict(color='#1A73E8', width=2)),
                    go.Scatter(x=camino_plano, y=y_camino, mode='markers+lines', name='Pasos', 
                               line=dict(color='#1E6091', width=1.5), 
                               marker=dict(size=8, color='#1E6091', symbol='circle'))
                ])
                fig_1d.update_layout(title="Curva f(x): Comportamiento de Pasos en 1D", 
                                    template="simple_white", height=400,
                                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                    xaxis_title="Variable X", yaxis_title="f(x)")
                st.plotly_chart(fig_1d, use_container_width=True)
            else:
                st.warning("⚠️ Monitoreo dimensional espacial (2D/1D) inhabilitado para optimizaciones de alta complejidad (> 2 variables).")

        # Historial analítico de pasos
        st.markdown("<h3 style='color: #1E293B;'>📋 REGISTRO CRONOLÓGICO DE ITERACIONES</h3>", unsafe_allow_html=True)
        columnas_hist = [f"Coordenada x{i}" if n_vars > 2 else (['Coordenada X', 'Coordenada Y'][i] if n_vars == 2 else ['Coordenada X'][i]) for i in range(n_vars)]
        df_steps = pd.DataFrame(camino, columns=columnas_hist)
        df_steps.insert(0, "Iteración", range(len(camino)))
        df_steps["Valor f(x)"] = [f_n(*p) for p in camino]
        st.dataframe(df_steps.style.format({"Valor f(x)": "{:.6f}"}), use_container_width=True)
else:
    st.markdown("<div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 12px; color: #475569; box-shadow: 0 4px 12px rgba(0,0,0,0.02);'>🧬 <b>Estación de control remota lista.</b> Configure las propiedades analíticas del modelo en el panel lateral y presione '⚡ INICIAR SIMULACIÓN'.</div>", unsafe_allow_html=True)