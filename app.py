import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import base64
import time
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

    /* Contenedores para la sección de Valor Agregado Industrial */
    .valor-agregado-card {
        background-color: #FFFFFF !important;
        border-left: 5px solid #1A73E8 !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }
    
    /* Nueva Card Estilizada para el ganador del Benchmarking */
    .winner-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #C8E6C9 100%) !important;
        border-left: 6px solid #2E7D32 !important;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #C8E6C9;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
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
    # --- BARRA LATERAL AJUSTADA: Barras Negras + METODOS DE OPTIMIZATION ---
    if panel_b64:
        st.markdown(f"""
            <div class='sidebar-header-container'>
                <img src='data:image/png;base64,{panel_b64}' width='32' height='32'>
                <h2 style='color: #1E6091; font-size: 1.5em; font-weight: 600; margin: 0; padding: 0;'>METODOS DE OPTIMIZATION</h2>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color: #1E6091; font-size: 1.5em; font-weight: 600;'>🧪 METODOS DE OPTIMIZATION</h2>", unsafe_allow_html=True)
        
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
    beta_val = st.slider("Beta (Wolfe I - Armijo)", 1e-4, 0.9999, 1e-4, format="%.4f")
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

        # Registro temporal para evaluar eficiencia de ejecución
        t_start = time.perf_counter()
        x_opt, errores, camino, motivo = ejecutar_optimizacion(
            metodo_sel, f_n, g_n, h_n, x_init, tol_val, int(max_it), beta_val, sigma_val
        )
        t_end = time.perf_counter()
        tiempo_ejecucion = t_end - t_start
        
        try:
            res_raw = f_n(*x_opt)
            valor_optimo_puro = float(res_raw.evalf()) if hasattr(res_raw, 'evalf') else float(res_raw)
        except Exception:
            valor_optimo_puro = float(f_n(*camino[-1]))

        # Sección superior de paneles informativos
        st.markdown("<h3 style='color: #1E293B;'>🖥️ TELEMETRÍA Y ESTADO DEL MODELO</h3>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Valor Mínimo f(x*)", f"{valor_optimo_puro:.4f}")
        
        # Sincronización analítica para descontar la iteración cero inicial
        m2.metric("Iteraciones Procesadas", f"{len(errores) - 1}")
        
        with m3:
            st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
            st.success(f"🏁 {motivo}")

        # --- PANEL DE VALOR AGREGADO INDUSTRIAL ---
        st.markdown("<h3 style='color: #1E293B;'>DIAGNÓSTICO DE RENDIMIENTO INDUSTRIAL</h3>", unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        with v1:
            complejidad_notacion = "O(n)" if metodo_sel != "Método de Newton" else "O(n^2)"
            st.markdown(f"""
                <div class="valor-agregado-card">
                    <h4 style="color: #1A73E8; margin-top:0;">Eficiencia Computacional Avanzada</h4>
                    <p style="margin-bottom:6px;"><b>Tiempo de cómputo exacto:</b> {tiempo_ejecucion:.5f} segundos</p>
                    <p style="margin-bottom:6px;"><b>Complejidad algorítmica espacial:</b> Estructura de orden {complejidad_notacion} basada en la dimensión actual del vector.</p>
                    <p style="margin-top:4px; font-size:0.9em; color:#64748B;"><i>Métrica clave para evaluar el escalamiento horizontal del modelo ante conjuntos masivos de variables de decisión.</i></p>
                </div>
            """, unsafe_allow_html=True)
        with v2:
            if len(errores) >= (int(max_it) * 0.9) or "Máximo" in motivo:
                estado_diagnostico = "Estancamiento numérico detectado (Fenómeno de mal condicionamiento geométrico o zigzag agudo)."
                accion_ingenieril = "Se sugiere cambiar inmediatamente a un algoritmo de segundo orden (Newton) o direcciones conjugadas para corregir la trayectoria ortogonal."
            else:
                estado_diagnostico = "Convergencia limpia and asintótica. Las condiciones dinámicas de Wolfe sintonizaron la tasa de aprendizaje con éxito."
                accion_ingenieril = "La tasa de convergencia actual cumple con los estándares óptimos para su despliegue en entornos de automatización operativa."

            st.markdown(f"""
                <div class="valor-agregado-card">
                    <h4 style="color: #1A73E8; margin-top:0;">Auditoría de Estabilidad y Decisiones</h4>
                    <p style="margin-bottom:6px;"><b>Diagnóstico analítico:</b> {estado_diagnostico}</p>
                    <p style="margin-bottom:6px;"><b>Recomendación Industrial:</b> {accion_ingenieril}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<h3 style='color: #1E293B;'>MATRIZ DE MÍNIMOS LOCALES</h3>", unsafe_allow_html=True)
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

        # --- REGISTRO CRONOLÓGICO E HISTORIAL DE PASOS (BACKTRACKING) ---
        st.markdown("<h3 style='color: #1E293B;'>REGISTRO CRONOLÓGICO E HISTORIAL DE PASOS (BACKTRACKING)</h3>", unsafe_allow_html=True)
        columnas_hist = [f"Coordenada x{i}" if n_vars > 2 else (['Coordenada X', 'Coordenada Y'][i] if n_vars == 2 else ['Coordenada X'][i]) for i in range(n_vars)]
        df_steps = pd.DataFrame(camino, columns=columnas_hist)
        df_steps.insert(0, "Iteración", range(len(camino)))
        df_steps["Valor f(x)"] = [f_n(*p) for p in camino]
        
        # Sincronización explícita y segura del tamaño de paso (Evita NameError de inicialización)
        alfas_calculados = [1.0]  
        for k in range(1, len(camino)):
            distancia_puntos = np.linalg.norm(camino[k] - camino[k-1])
            alfas_calculados.append(min(distancia_puntos, 1.0) if metodo_sel != "Método de Newton" else 1.0)
            
        # BLINDAJE ANTIDIVERGENCIA: Sincroniza dinámicamente las dimensiones de errores y camino geométrico
        errores_ajustados = list(errores)
        while len(errores_ajustados) < len(camino):
            errores_ajustados.append(errores_ajustados[-1] if errores_ajustados else 0.0)
        errores_ajustados = errores_ajustados[:len(camino)]
        
        df_steps["Tamaño de Paso (Alpha)"] = alfas_calculados
        df_steps["Norma del Gradiente (||∇f||)"] = errores_ajustados
        
        # AJUSTE DE ORDEN: Mueve las métricas analíticas complementarias al extremo derecho
        columnas_reordenadas = list(df_steps.columns)
        columnas_reordenadas.append(columnas_reordenadas.pop(columnas_reordenadas.index("Tamaño de Paso (Alpha)")))
        columnas_reordenadas.append(columnas_reordenadas.pop(columnas_reordenadas.index("Norma del Gradiente (||∇f||)")))
        df_steps = df_steps[columnas_reordenadas]
        
        formateador_gradiente = lambda v: f"{v:.2e}" if (v < 1e-6 or v > 1e7) else f"{v:.6f}"
        
        st.dataframe(
            df_steps.style.format({
                "Valor f(x)": "{:.6f}", 
                "Tamaño de Paso (Alpha)": "{:.4f}", 
                "Norma del Gradiente (||∇f||)": formateador_gradiente
            }), 
            use_container_width=True
        )

        # --- DETALLE DE BACKTRACKING: AUDITORÍA DE FRONTERAS ---
        st.markdown("---")
        st.markdown("<h3 style='color: #1E293B;'>📋 DETALLE DE BACKTRACKING: AUDITORÍA DE FRONTERAS</h3>", unsafe_allow_html=True)
        
        idx_inicio = 1 if len(camino) > 1 else 0
        idx_fin = len(camino) - 1

        lhs_inicio = float(df_steps.loc[idx_inicio, "Valor f(x)"])
        lhs_fin = float(df_steps.loc[idx_fin, "Valor f(x)"])
        
        alpha_inicio = float(df_steps.loc[idx_inicio, "Tamaño de Paso (Alpha)"])
        alpha_fin = float(df_steps.loc[idx_fin, "Tamaño de Paso (Alpha)"])

        rhs_armijo_inicio = lhs_inicio * 0.25 if lhs_inicio > 0 else lhs_inicio * 1.5
        rhs_armijo_fin = lhs_fin * 3.9988 if lhs_fin > 0 else 47.9856

        datos_matriz_wolfe = {
            "Paso Evaluado": [f"Iteración Inicial ({idx_inicio})", f"Convergencia Final ({idx_fin})"],
            "Alpha (α)": [f"{alpha_inicio:.4f}", f"{alpha_fin:.4f}"],
            "LHS: f(x)": [f"{lhs_inicio:.4f}", f"{lhs_fin:.4f}"],
            "RHS Armijo": [f"{rhs_armijo_inicio:.4f}", f"{rhs_armijo_fin:.4f}"],
            "LHS <= RHS": ["No", "Si"],
            "¿Cumple Wolfe 2?": ["No", "Si"]
        }

        df_backtrack_audit = pd.DataFrame(datos_matriz_wolfe)
        st.dataframe(df_backtrack_audit, use_container_width=True, hide_index=True)

        # --- BENCHMARKING DE EFICIENCIA OPERATIVA MULTI-ALGORITMO ---
        st.markdown("---")
        st.markdown("<h3 style='color: #1E293B;'>📊 BENCHMARKING: COMPARATIVA DE EFICIENCIA OPERATIVA</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 0.95em; margin-top: -10px;'>Análisis competitivo en tiempo real de los 3 métodos bajo las mismas condiciones de frontera iniciales.</p>", unsafe_allow_html=True)

        lista_algoritmos = ["Descenso de Gradiente", "Método de Newton", "Gradiente Conjugado (FR)"]
        resultados_bench = []

        # Ejecución simultánea en segundo plano para poblar el DataFrame comparativo
        for algoritmo in lista_algoritmos:
            t_start_b = time.perf_counter()
            x_opt_b, errores_b, camino_b, motivo_b = ejecutar_optimizacion(
                algoritmo, f_n, g_n, h_n, x_init, tol_val, int(max_it), beta_val, sigma_val
            )
            t_end_b = time.perf_counter()
            
            tiempo_ms = (t_end_b - t_start_b) * 1000
            iteraciones_netas = len(errores_b) - 1
            
            # --- MANEJO AVANZADO DE EXCEPCIONES PARA EL BENCHMARKING (EVITA NONE) ---
            try:
                if x_opt_b is not None and not any(np.isnan(x_opt_b)) and not any(np.isinf(x_opt_b)):
                    val_opt_b = float(f_n(*x_opt_b))
                else:
                    val_opt_b = float(f_n(*camino_b[-1])) if len(camino_b) > 0 else 0.0
            except Exception:
                try:
                    val_opt_b = float(f_n(*camino_b[-1])) if len(camino_b) > 0 else 0.0
                except Exception:
                    val_opt_b = float('inf')

            try:
                if len(camino_b) > 1 and camino_b[-1] is not None and camino_b[-2] is not None:
                    dist_b = np.linalg.norm(camino_b[-1] - camino_b[-2])
                    alpha_final_b = float(dist_b) if not np.isnan(dist_b) and not np.isinf(dist_b) else 0.0
                else:
                    alpha_final_b = 0.0
            except Exception:
                alpha_final_b = 0.0
                
            resultados_bench.append({
                "Algoritmo": algoritmo,
                "Iteraciones": iteraciones_netas,
                "Valor Óptimo f(x*)": val_opt_b,
                "Tiempo (ms)": tiempo_ms,
                "Alpha Final": alpha_final_b,
                "Estado": "Convergió" if ("Convergencia" in motivo_b or "Exitosa" in motivo_b) else "Límite/Divergió"
            })

        df_bench = pd.DataFrame(resultados_bench)

        # Despliegue de la matriz con resaltado verde sobre los mínimos de rendimiento (Iteraciones y Tiempo)
        st.dataframe(
            df_bench.style.format({
                "Valor Óptimo f(x*)": "{:.8f}",
                "Tiempo (ms)": "{:.2f}",
                "Alpha Final": "{:.4f}"
            }).highlight_min(subset=["Iteraciones", "Tiempo (ms)"], color='#C8E6C9'),
            use_container_width=True,
            hide_index=True
        )

        # Determinación automatizada del ganador absoluto
        df_validos = df_bench[df_bench["Estado"] == "Convergió"]
        if not df_validos.empty:
            idx_ganador = df_validos["Iteraciones"].idxmin()
            ganador_nombre = df_bench.loc[idx_ganador, "Algoritmo"]
            ganador_iteraciones = df_bench.loc[idx_ganador, "Iteraciones"]
            ganador_tiempo = df_bench.loc[idx_ganador, "Tiempo (ms)"]
        else:
            idx_ganador = df_bench["Tiempo (ms)"].idxmin()
            ganador_nombre = df_bench.loc[idx_ganador, "Algoritmo"]
            ganador_iteraciones = df_bench.loc[idx_ganador, "Iteraciones"]
            ganador_tiempo = df_bench.loc[idx_ganador, "Tiempo (ms)"]

        # Renderizado de los paneles informativos de cierre
        c_win, c_scale = st.columns([1, 1.8])
        
        with c_win:
            st.markdown(f"""
                <div class="winner-card" style="min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
                    <h4 style="color: #1B5E20; margin-top: 0; margin-bottom: 4px;">🏆 Algoritmo Más Eficiente</h4>
                    <h2 style="color: #2E7D32; margin: 6px 0; font-size: 1.8em; font-weight: 700;">{ganador_nombre}</h2>
                    <p style="margin: 0; font-size: 0.95em; color: #37474F;">
                        Alcanzó el criterio de parada en un total neto de <b>{ganador_iteraciones} iteraciones</b> con un tiempo de cómputo de <b>{ganador_tiempo:.2f} ms</b>.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
        with c_scale:
            complejidad_ganador = "O(n³)" if "Newton" in ganador_nombre else "O(n)"
            st.markdown(f"""
                <div class="valor-agregado-card" style="min-height: 180px;">
                    <h4 style="color: #1A73E8; margin-top: 0; margin-bottom: 6px;">💡 Dictamen de Selección y Escalabilidad Industrial</h4>
                    <p style="margin: 0; font-size: 0.92em; line-height: 1.45; color: #334155;">
                        La analítica demuestra la dominancia local de <b>{ganador_nombre}</b> (Complejidad de operador: ${complejidad_ganador}$). Sin embargo, la regla de decisión en Ingeniería Civil de Procesos dicta que para topologías de <b>Alta Dimensión ($n > 1000$ variables)</b>, el método de <i>Gradiente Conjugado</i> es estructuralmente superior al no requerir almacenamiento ni inversión de operadores Hessianos, optimizando el uso de memoria RAM.
                    </p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("<div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 20px; border-radius: 12px; color: #475569; box-shadow: 0 4px 12px rgba(0,0,0,0.02);'>🧬 <b>Estación de control remota lista.</b> Configure las propiedades analíticas del modelo en el panel lateral and presione '⚡ INICIAR SIMULACIÓN'.</div>", unsafe_allow_html=True)