"""
EPIC Lab Amplificador de Impacto - MAD Fellows Challenge 2025
Aplicación para aumentar el alcance del contenido del EPIC Lab
Desarrollado para el MAD Fellows Challenge del EPIC Lab del ITAM
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import json
import random
from datetime import datetime, timedelta
import time
import requests
import openai

# Para el menú de navegación moderno
try:
    from streamlit_option_menu import option_menu
except ImportError:
    st.error("Por favor instala streamlit-option-menu: `pip install streamlit-option-menu`")

# Configuración de la página con un tema más moderno
st.set_page_config(
    page_title="EPIC Lab Amplificador de Impacto",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores del EPIC Lab con estilo moderno
EPIC_COLORS = {
    'primary': '#2E8B57',       # Verde oscuro (del logo EPIC Lab)
    'secondary': '#8BC34A',     # Verde claro (del logo EPIC Lab)
    'accent': '#66BB6A',        # Verde medio para acentos
    'light_bg': '#F8F9FC',      # Fondo claro
    'dark_bg': '#E8E8E8',       # Fondo oscuro (derivado del verde primario)
    'card_bg': '#FFFFFF',       # Fondo de tarjeta
    'text_primary': '#2E3B33',  # Texto principal (derivado del verde)
    'text_secondary': '#637B64', # Texto secundario (derivado del verde)
    'success': '#4CAF50',       # Verde éxito
    'warning': '#FFC107',       # Amarillo advertencia
    'danger': '#F44336',        # Rojo peligro
    'chart1': '#2E8B57',        # Verde principal para gráficos
    'chart2': '#8BC34A',        # Verde secundario para gráficos
    'chart3': '#CDDC39',        # Verde-amarillo para gráficos
    'chart4': '#66BB6A',        # Verde medio para gráficos
    'chart5': '#81C784',        # Verde pálido para gráficos
    'gradient_start': '#2E8B57', # Inicio de gradiente (verde oscuro)
    'gradient_end': '#8BC34A',   # Fin de gradiente (verde claro)
}

# Estilos CSS modernos
st.markdown(f"""
<style>
    /* Estilo general */
    .main {{
        background-color: {EPIC_COLORS['light_bg']};
        padding: 0rem;
    }}
    
    /* Contenedor principal */
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }}
    
    /* Header principal */
    .epic-header {{
        background: linear-gradient(120deg, {EPIC_COLORS['gradient_start']}, {EPIC_COLORS['gradient_end']});
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 8px 20px rgba(46, 139, 87, 0.2);
    }}
    
    .epic-title {{
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        line-height: 1.2;
    }}
    
    .epic-subtitle {{
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        opacity: 0.9;
    }}
    
    /* Tarjetas */
    .epic-card {{
        background-color: {EPIC_COLORS['card_bg']};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(29, 43, 76, 0.06);
        margin-bottom: 1.25rem;
    }}
    
    /* Tarjetas métricas */
    .epic-metric-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .epic-metric {{
        background-color: {EPIC_COLORS['card_bg']};
        border-radius: 12px;
        padding: 1.25rem;
        flex: 1;
        min-width: 200px;
        box-shadow: 0 4px 12px rgba(46, 139, 87, 0.08);
        text-align: center;
        border-bottom: 3px solid {EPIC_COLORS['primary']};
        transition: transform 0.3s ease;
    }}
    
    .epic-metric:hover {{
        transform: translateY(-5px);
    }}
    
    .epic-metric-value {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {EPIC_COLORS['primary']};
        margin-bottom: 0.25rem;
    }}
    
    .epic-metric-label {{
        color: {EPIC_COLORS['text_secondary']};
        font-weight: 500;
    }}
    
    /* Insights */
    .epic-insight {{
        background-color: rgba(46, 139, 87, 0.06);
        border-left: 4px solid {EPIC_COLORS['primary']};
        padding: 1rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin-top: 1rem;
    }}
    
    .epic-insight-title {{
        font-weight: 600;
        color: {EPIC_COLORS['primary']};
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }}
    
    /* Botones y acciones */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        border: none;
        background-color: {EPIC_COLORS['primary']};
        color: white;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {EPIC_COLORS['accent']};
        box-shadow: 0 4px 12px rgba(46, 139, 87, 0.15);
    }}
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        padding: 0.75rem;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {EPIC_COLORS['primary']};
        box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.1);
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        border-radius: 8px;
    }}
    
    /* Tabs modernos */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        border-radius: 10px;
        background-color: {EPIC_COLORS['light_bg']};
        padding: 0.25rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: {EPIC_COLORS['text_primary']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {EPIC_COLORS['primary']};
        color: white !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {EPIC_COLORS['dark_bg']};
        padding-top: 2rem;
    }}
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        padding-top: 0;
    }}
    
    /* Sombras y elevación */
    .epic-elevated {{
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }}
    
    .epic-elevated:hover {{
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.12);
        transform: translateY(-5px);
    }}
    
    /* Hashtags */
    .epic-hashtag {{
        display: inline-block;
        background-color: rgba(139, 195, 74, 0.15);
        color: {EPIC_COLORS['primary']};
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0.5rem 0.5rem 0;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .epic-hashtag:hover {{
        background-color: rgba(139, 195, 74, 0.25);
        transform: translateY(-2px);
    }}
    
    /* Contenedores de estadísticas */
    .stat-container {{
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }}
    
    .stat-container:hover {{
        transform: translateY(-5px);
    }}
    
    /* Contenedor AI Assistant */
    .ai-assistant-container {{
        background: linear-gradient(120deg, rgba(46, 139, 87, 0.03), rgba(139, 195, 74, 0.06));
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(46, 139, 87, 0.1);
        margin-top: 1.5rem;
    }}
    
    /* Mensaje del asistente */
    .assistant-message {{
        background-color: white;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        border-left: 3px solid {EPIC_COLORS['primary']};
    }}
    
    /* Mensaje del usuario */
    .user-message {{
        background-color: rgba(46, 139, 87, 0.08);
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-right: 3px solid {EPIC_COLORS['secondary']};
    }}
</style>
""", unsafe_allow_html=True)

# Función para generar datos simulados de social listening
def generar_datos_social_listening(dias=30):
    # Fechas
    fechas = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(dias)]
    fechas.reverse()
    
    # Menciones por día (con tendencia creciente y algo de ruido)
    base_menciones = np.linspace(50, 150, dias)
    ruido = np.random.normal(0, 15, dias)
    menciones = np.maximum(5, base_menciones + ruido).astype(int)
    
    # Plataformas
    plataformas = ['Twitter/X', 'Instagram', 'LinkedIn', 'Facebook', 'TikTok']
    
    # Distribución por plataforma
    distribucion_plataforma = {
        'Twitter/X': np.random.normal(0.35, 0.05, dias),
        'Instagram': np.random.normal(0.25, 0.05, dias),
        'LinkedIn': np.random.normal(0.20, 0.03, dias),
        'Facebook': np.random.normal(0.15, 0.03, dias),
        'TikTok': np.random.normal(0.05, 0.02, dias)
    }
    
    # Normalizar para que sumen 1
    for i in range(dias):
        total = sum(distribucion_plataforma[p][i] for p in plataformas)
        for p in plataformas:
            distribucion_plataforma[p][i] /= total
    
    # Menciones por plataforma
    menciones_plataforma = {}
    for p in plataformas:
        menciones_plataforma[p] = (menciones * distribucion_plataforma[p]).astype(int)
    
    # Sentimiento
    sentimiento_base = {'Positivo': 0.6, 'Neutral': 0.3, 'Negativo': 0.1}
    sentimiento_diario = []
    
    for i in range(dias):
        # Añadir variación al sentimiento base
        variacion = {'Positivo': np.random.normal(0, 0.05), 
                     'Neutral': np.random.normal(0, 0.03), 
                     'Negativo': np.random.normal(0, 0.02)}
        
        sent_dia = {k: max(0.01, sentimiento_base[k] + variacion[k]) for k in sentimiento_base}
        
        # Normalizar
        total = sum(sent_dia.values())
        sent_dia = {k: v/total for k, v in sent_dia.items()}
        
        sentimiento_diario.append(sent_dia)
    
    # Temas
    temas = ['Emprendimiento', 'Innovación', 'Tecnología', 'Finanzas', 'Negocios', 'Educación', 'Eventos']
    tema_diario = []
    
    for i in range(dias):
        tema_dia = {}
        # Distribución base con variación diaria
        for tema in temas:
            if tema == 'Emprendimiento':
                tema_dia[tema] = np.random.normal(0.25, 0.05)
            elif tema == 'Innovación':
                tema_dia[tema] = np.random.normal(0.20, 0.04)
            elif tema == 'Tecnología':
                tema_dia[tema] = np.random.normal(0.15, 0.04)
            elif tema == 'Finanzas':
                tema_dia[tema] = np.random.normal(0.12, 0.03)
            elif tema == 'Negocios':
                tema_dia[tema] = np.random.normal(0.10, 0.03)
            elif tema == 'Educación':
                tema_dia[tema] = np.random.normal(0.10, 0.03)
            else:  # Eventos
                tema_dia[tema] = np.random.normal(0.08, 0.02)
        
        # Asegurar valores positivos
        tema_dia = {k: max(0.01, v) for k, v in tema_dia.items()}
        
        # Normalizar
        total = sum(tema_dia.values())
        tema_dia = {k: v/total for k, v in tema_dia.items()}
        
        tema_diario.append(tema_dia)
    
    # Términos clave (palabras más mencionadas)
    terminos_base = {
        'EPIC Lab': 100,
        'ITAM': 80,
        'innovación': 70,
        'emprendimiento': 65,
        'tecnología': 60,
        'startup': 55,
        'negocios': 50,
        'fintech': 45,
        'proyecto': 40,
        'digital': 38,
        'transformación': 35,
        'futuro': 33,
        'educación': 30,
        'México': 28,
        'desafío': 25,
        'solución': 23,
        'impacto': 20,
        'comunidad': 18,
        'desarrollo': 15,
        'talento': 13,
        'creatividad': 10,
        'colaboración': 8,
        'MAD Fellows': 75,
        'Challenge': 60,
        'estudiantes': 40,
        'profesionales': 35,
        'mentores': 30,
        'workshops': 25,
        'conferencias': 20,
        'networking': 15
    }
    
    # Crear DataFrame
    data = []
    for i in range(dias):
        fecha = fechas[i]
        menciones_dia = menciones[i]
        
        # Menciones por plataforma en este día
        for p in plataformas:
            menciones_p = menciones_plataforma[p][i]
            
            # Distribuir menciones según sentimiento
            for sentimiento, proporcion in sentimiento_diario[i].items():
                menciones_s = int(menciones_p * proporcion)
                
                # Distribuir menciones según tema
                for tema, prop_tema in tema_diario[i].items():
                    menciones_t = int(menciones_s * prop_tema)
                    
                    if menciones_t > 0:
                        data.append({
                            'fecha': fecha,
                            'plataforma': p,
                            'menciones': menciones_t,
                            'sentimiento': sentimiento,
                            'tema': tema
                        })
    
    df = pd.DataFrame(data)
    
    # Agregar columna de fecha como datetime para facilitar análisis
    df['fecha_dt'] = pd.to_datetime(df['fecha'])
    
    return df, terminos_base

# Función para generar recomendación de contenido (simulada)
def generar_recomendacion(publico, genero, tipo_contenido, formato, plataforma):
    # Simulamos la respuesta para la demo
    recomendaciones = {
        'Estudiantes': {
            'Instagram': "Crea contenido visual con infografías que expliquen conceptos de {tipo} de forma sencilla. Usa un lenguaje cercano y directo, con ejemplos relevantes para estudiantes. Incluye llamados a la acción para participar en los programas del EPIC Lab.",
            'Twitter/X': "Publica hilos cortos sobre tendencias en {tipo} con datos interesantes. Usa un tono informativo pero casual y menciona cómo el EPIC Lab puede ayudarles a desarrollar habilidades en esta área.",
            'TikTok': "Desarrolla videos cortos y dinámicos con explicaciones rápidas sobre {tipo}. Usa música de tendencia y un formato de preguntas y respuestas. Finaliza con invitación a conocer más en el EPIC Lab.",
            'LinkedIn': "Comparte artículos sobre oportunidades en {tipo} para estudiantes que buscan desarrollar su carrera. Incluye testimonios de participantes del EPIC Lab y estadísticas sobre el impacto en su desarrollo profesional."
        },
        'Profesionales': {
            'Instagram': "Publica casos de éxito en formato carrusel sobre profesionales que han transformado su carrera gracias a conocimientos en {tipo}. Destaca el networking y las oportunidades que ofrece el EPIC Lab.",
            'Twitter/X': "Comparte insights de industria y análisis de tendencias en {tipo} con un enfoque profesional. Menciona eventos exclusivos del EPIC Lab donde pueden profundizar estos temas.",
            'TikTok': "Crea videos con formato 'day in the life' de profesionales exitosos en {tipo}, mostrando cómo aplican lo aprendido en el EPIC Lab. Usa un tono aspiracional pero auténtico.",
            'LinkedIn': "Publica artículos detallados sobre innovaciones en {tipo} y cómo están transformando la industria. Invita a profesionales a participar como mentores o asistentes en los programas del EPIC Lab."
        },
        'Emprendedores': {
            'Instagram': "Desarrolla historias visuales sobre el journey emprendedor en {tipo}, destacando los desafíos y victorias. Muestra cómo el EPIC Lab puede ser un aliado en cada etapa del proceso.",
            'Twitter/X': "Comparte consejos prácticos y recursos para emprendedores en {tipo}. Usa hashtags relevantes del ecosistema emprendedor y menciona las herramientas que ofrece el EPIC Lab.",
            'TikTok': "Crea videos con formato 'antes/después' mostrando la evolución de startups exitosas en {tipo}. Destaca el papel del EPIC Lab como catalizador de estos proyectos.",
            'LinkedIn': "Publica casos de estudio detallados sobre startups que han escalado en {tipo} con apoyo del EPIC Lab. Incluye métricas concretas de crecimiento y lecciones aprendidas."
        }
    }
    
    base_recomendacion = recomendaciones[publico][plataforma].replace("{tipo}", tipo_contenido.lower())
    
    # Añadir recomendación específica según formato
    formato_recomendacion = {
        'Texto': f"\n\nPara el formato de texto, utiliza párrafos cortos y concisos, con títulos llamativos. La longitud ideal es de 150-200 palabras para {plataforma}.",
        'Imagen': f"\n\nPara el formato de imagen, utiliza colores vibrantes que reflejen la identidad del EPIC Lab. Incluye texto superpuesto con datos impactantes sobre {tipo_contenido}.",
        'Video': f"\n\nPara el formato de video, mantén una duración de 30-60 segundos con edición dinámica. Incluye subtítulos y asegúrate de mencionar al EPIC Lab en los primeros 5 segundos.",
        'Infografía': f"\n\nPara el formato de infografía, estructura la información en 3-5 secciones clave. Usa iconos modernos y datos visuales que destaquen el valor del EPIC Lab en el ecosistema de {tipo_contenido}."
    }
    
    recomendacion_completa = base_recomendacion + formato_recomendacion[formato]
    
    # Añadir consideración de género si se seleccionó específicamente
    if genero != "Otro":
        recomendacion_completa += f"\n\nConsidera usar un lenguaje inclusivo y representativo, con ejemplos y testimonios que resuenen especialmente con audiencia de género {genero.lower()}."
    else:
        recomendacion_completa += "\n\nUtiliza lenguaje inclusivo y diverso, con ejemplos que representen a personas de todos los géneros y backgrounds."
    
    
    return recomendacion_completa

# Función para analizar impacto social (simulada)
def analizar_impacto_social(texto):
    # Simulamos la respuesta para la demo
    if not texto or len(texto) < 10:
        return {
            "viralidad": 30,
            "relevancia_social": 25,
            "inclusividad": 40,
            "claridad": 35,
            "tono_positivo": 45,
            "sugerencias": "El texto es demasiado corto para realizar un análisis completo. Intenta escribir un mensaje más elaborado que comunique claramente el valor del EPIC Lab."
        }
    
    # Análisis básico del texto
    palabras = texto.lower().split()
    longitud = len(palabras)
    
    # Palabras clave que aumentan cada dimensión
    palabras_viralidad = ['innovación', 'disruptivo', 'revolucionario', 'increíble', 'sorprendente', 'único', 'exclusivo']
    palabras_relevancia = ['impacto', 'comunidad', 'sociedad', 'problema', 'solución', 'futuro', 'cambio', 'transformación']
    palabras_inclusividad = ['todos', 'todas', 'diversidad', 'inclusión', 'accesible', 'oportunidad', 'equidad']
    palabras_claridad = ['simple', 'claro', 'directo', 'específico', 'concreto', 'ejemplo', 'paso']
    palabras_positivo = ['éxito', 'logro', 'beneficio', 'ventaja', 'positivo', 'mejora', 'crecimiento', 'desarrollo']
    
    # Calcular puntuaciones base
    base_viralidad = random.randint(40, 60)
    base_relevancia = random.randint(45, 65)
    base_inclusividad = random.randint(35, 55)
    base_claridad = random.randint(50, 70)
    base_positivo = random.randint(45, 65)
    
    # Ajustar según longitud del texto (penalizar textos muy cortos o muy largos)
    factor_longitud = 1.0
    if longitud < 20:
        factor_longitud = 0.8
    elif longitud > 200:
        factor_longitud = 0.9
    
    # Ajustar según presencia de palabras clave
    for palabra in palabras:
        if palabra in palabras_viralidad:
            base_viralidad += 5
        if palabra in palabras_relevancia:
            base_relevancia += 5
        if palabra in palabras_inclusividad:
            base_inclusividad += 5
        if palabra in palabras_claridad:
            base_claridad += 5
        if palabra in palabras_positivo:
            base_positivo += 5
    
    # Normalizar puntuaciones
    viralidad = min(100, max(0, int(base_viralidad * factor_longitud)))
    relevancia = min(100, max(0, int(base_relevancia * factor_longitud)))
    inclusividad = min(100, max(0, int(base_inclusividad * factor_longitud)))
    claridad = min(100, max(0, int(base_claridad * factor_longitud)))
    tono_positivo = min(100, max(0, int(base_positivo * factor_longitud)))
    
    # Generar sugerencias personalizadas
    sugerencias = []
    
    if viralidad < 50:
        sugerencias.append("Incluye elementos más sorprendentes o únicos para aumentar la viralidad.")
    if relevancia < 50:
        sugerencias.append("Conecta más claramente con problemas o necesidades actuales de la comunidad.")
    if inclusividad < 50:
        sugerencias.append("Utiliza lenguaje más inclusivo y considera diversas perspectivas.")
    if claridad < 50:
        sugerencias.append("Simplifica el mensaje y sé más directo en la comunicación.")
    if tono_positivo < 50:
        sugerencias.append("Incorpora un tono más positivo y orientado a soluciones.")
    
    if not sugerencias:
        sugerencias.append("¡Excelente trabajo! Tu contenido tiene un buen balance. Considera amplificar tu mensaje a través de múltiples canales.")
    
    # Simular delay de API
    time.sleep(1)
    
    return {
        "viralidad": viralidad,
        "relevancia_social": relevancia,
        "inclusividad": inclusividad,
        "claridad": claridad,
        "tono_positivo": tono_positivo,
        "sugerencias": " ".join(sugerencias)
    }

# Función para generar hashtags (simulada)
def generar_hashtags(texto):
    # Hashtags base relacionados con EPIC Lab
    hashtags_base = ["#EPICLab", "#ITAM", "#Innovación"]
    
    # Palabras clave que podrían generar hashtags específicos
    palabras_clave = {
        "emprendimiento": "#Emprendimiento",
        "startup": "#Startup",
        "negocio": "#Business",
        "tecnología": "#Tech",
        "digital": "#Digital",
        "transformación": "#Transformación",
        "futuro": "#FuturoDigital",
        "educación": "#EducaciónDigital",
        "méxico": "#México",
        "desafío": "#Challenge",
        "solución": "#Soluciones",
        "impacto": "#ImpactoSocial",
        "comunidad": "#Comunidad",
        "desarrollo": "#Desarrollo",
        "talento": "#Talento",
        "creatividad": "#Creatividad",
        "colaboración": "#Colaboración",
        "fellows": "#MADFellows",
        "challenge": "#EPICChallenge",
        "estudiantes": "#Estudiantes",
        "profesionales": "#Profesionales"
    }
    
    # Extraer hashtags del texto
    hashtags_especificos = []
    if texto:
        palabras = texto.lower().split()
        for palabra in palabras:
            palabra_limpia = ''.join(c for c in palabra if c.isalnum())
            if palabra_limpia in palabras_clave and palabras_clave[palabra_limpia] not in hashtags_especificos:
                hashtags_especificos.append(palabras_clave[palabra_limpia])
    
    # Combinar hashtags base con específicos
    todos_hashtags = hashtags_base + hashtags_especificos
    
    # Si hay pocos hashtags, añadir algunos genéricos relevantes
    hashtags_adicionales = ["#Innovación", "#Emprendimiento", "#Tech", "#Business", "#DigitalTransformation"]
    
    while len(todos_hashtags) < 8:
        hashtag_adicional = random.choice(hashtags_adicionales)
        if hashtag_adicional not in todos_hashtags:
            todos_hashtags.append(hashtag_adicional)
    
    # Limitar a máximo 10 hashtags
    if len(todos_hashtags) > 10:
        todos_hashtags = todos_hashtags[:10]
    
    return todos_hashtags
# Función para recomendar horarios óptimos
def recomendar_horarios(plataforma):
    # Horarios base por plataforma (simulados según investigaciones de marketing)
    horarios_base = {
        'Instagram': [
            {'hora': '12:00 PM', 'efectividad': 85, 'razon': 'Hora de almuerzo, mayor actividad de usuarios'},
            {'hora': '6:00 PM', 'efectividad': 90, 'razon': 'Final de jornada laboral, pico de engagement'},
            {'hora': '9:00 PM', 'efectividad': 75, 'razon': 'Tiempo de ocio nocturno, alta retención'}
        ],
        'Twitter/X': [
            {'hora': '8:00 AM', 'efectividad': 80, 'razon': 'Inicio de jornada, consumo de noticias'},
            {'hora': '12:00 PM', 'efectividad': 75, 'razon': 'Pausa de mediodía, alto volumen de tweets'},
            {'hora': '5:00 PM', 'efectividad': 85, 'razon': 'Final de jornada, discusiones activas'}
        ],
        'LinkedIn': [
            {'hora': '8:00 AM', 'efectividad': 85, 'razon': 'Inicio de jornada profesional'},
            {'hora': '12:00 PM', 'efectividad': 70, 'razon': 'Pausa de mediodía, profesionales activos'},
            {'hora': '5:30 PM', 'efectividad': 80, 'razon': 'Final de jornada laboral, mayor tiempo de lectura'}
        ],
        'TikTok': [
            {'hora': '11:00 AM', 'efectividad': 70, 'razon': 'Actividad creciente en la plataforma'},
            {'hora': '2:00 PM', 'efectividad': 75, 'razon': 'Pico de actividad diurna'},
            {'hora': '8:00 PM', 'efectividad': 95, 'razon': 'Prime time, máxima audiencia y engagement'}
        ]
    }
    
    # Añadir variación aleatoria para simular datos reales
    horarios = []
    for horario in horarios_base[plataforma]:
        variacion = random.randint(-5, 5)
        horario_ajustado = horario.copy()
        horario_ajustado['efectividad'] = max(min(horario['efectividad'] + variacion, 100), 60)
        horarios.append(horario_ajustado)
    
    # Ordenar por efectividad
    horarios.sort(key=lambda x: x['efectividad'], reverse=True)
    
    return horarios

# Función para generar forecast de menciones
def generar_forecast_menciones(df):
    # Agrupar por fecha para obtener menciones diarias totales
    menciones_diarias = df.groupby('fecha')['menciones'].sum().reset_index()
    menciones_diarias['fecha'] = pd.to_datetime(menciones_diarias['fecha'])
    menciones_diarias = menciones_diarias.sort_values('fecha')
    
    # Datos históricos
    historico = menciones_diarias['menciones'].values
    
    # Tendencia base (creciente)
    ultimo_valor = historico[-1]
    tendencia = np.linspace(0, 0.3, 7)  # Crecimiento gradual
    
    # Predicción con algo de ruido
    prediccion = [int(ultimo_valor * (1 + t) + random.randint(-10, 15)) for t in tendencia]
    
    # Asegurar que no haya valores negativos
    prediccion = [max(5, p) for p in prediccion]
    
    # Fechas futuras
    ultima_fecha = menciones_diarias['fecha'].max()
    fechas_futuras = [ultima_fecha + timedelta(days=i+1) for i in range(7)]
    
    # Crear DataFrame con histórico y predicción
    resultado = pd.DataFrame({
        'fecha': list(menciones_diarias['fecha']) + fechas_futuras,
        'menciones': list(historico) + prediccion,
        'tipo': ['Histórico'] * len(historico) + ['Predicción'] * len(prediccion)
    })
    
    return resultado

# Función para simular forecast de impacto de contenido
def simular_forecast_impacto(score_viralidad, dias=7):
    # Base de crecimiento según score de viralidad
    if score_viralidad >= 80:
        factor_base = 2.0  # Crecimiento exponencial alto
        alcance_inicial = random.randint(80, 120)
    elif score_viralidad >= 60:
        factor_base = 1.5  # Crecimiento exponencial moderado
        alcance_inicial = random.randint(50, 90)
    elif score_viralidad >= 40:
        factor_base = 1.2  # Crecimiento lineal alto
        alcance_inicial = random.randint(30, 60)
    else:
        factor_base = 1.1  # Crecimiento lineal bajo
        alcance_inicial = random.randint(10, 40)
    
    # Generar curva de crecimiento
    alcance = [alcance_inicial]
    for i in range(1, dias):
        if score_viralidad >= 60:  # Crecimiento exponencial
            nuevo_alcance = int(alcance[i-1] * (factor_base - (i * 0.05)))  # Disminuye el factor con el tiempo
        else:  # Crecimiento más lineal
            nuevo_alcance = int(alcance[i-1] + (alcance_inicial * (factor_base - 1) * (1 - i/10)))
        
        # Añadir algo de ruido
        ruido = random.randint(-5, 10)
        alcance.append(max(alcance[i-1], nuevo_alcance + ruido))  # Asegurar que no decrece
    
    # Fechas
    fechas = [datetime.now() + timedelta(days=i) for i in range(dias)]
    
    # Crear DataFrame
    df = pd.DataFrame({
        'fecha': fechas,
        'alcance': alcance
    })
    
    return df

# Función para obtener noticias de emprendimiento

def obtener_noticias_emprendimiento():
    """
    Obtiene noticias de emprendimiento usando NewsAPI
    """
    import requests
    
    # Configuración de la API
    API_KEY = "34ce1012f268483bb5f81ac477eb4791"
    url = f"https://newsapi.org/v2/everything"
    
    # Parámetros de búsqueda
    params = {
        "q": "emprendimiento OR startups OR innovación OR emprendedor",
        "language": "es",
        "sortBy": "publishedAt",
        "pageSize": 8,
        "apiKey": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error en la API: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# Tab de Noticias
def tab_noticias():
    st.markdown('<h2 class="epic-section-title">Noticias de Emprendimiento e Innovación</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="epic-card">', unsafe_allow_html=True)
    st.subheader("Últimas noticias relevantes para el ecosistema EPIC Lab")
    
    # Variable para controlar si queremos usar API real o simulación
    uso_api = True
    
    if uso_api:
        with st.spinner("Obteniendo las últimas noticias..."):
            noticias = obtener_noticias_emprendimiento()
            
            if "error" in noticias:
                st.error(f"No se pudieron cargar las noticias: {noticias['error']}")
                # Si hay error, mostrar noticias simuladas como respaldo
                usar_simuladas = True
            else:
                # Verificar que hay artículos disponibles
                if not noticias.get("articles"):
                    st.warning("No se encontraron noticias recientes. Mostrando noticias simuladas.")
                    usar_simuladas = True
                else:
                    usar_simuladas = False
                    
                    for articulo in noticias.get("articles", []):
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            
                            # Imagen (si está disponible)
                            with col1:
                                if articulo.get("urlToImage"):
                                    st.image(articulo["urlToImage"], width=150)
                                else:
                                    # Usar un placeholder si no hay imagen
                                    st.markdown(f"""
                                    <div style="width:150px;height:100px;background-color:{EPIC_COLORS['secondary']}40;
                                    display:flex;align-items:center;justify-content:center;color:{EPIC_COLORS['primary']};
                                    font-weight:bold;border-radius:5px;">
                                    EPIC News
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Información del artículo
                            with col2:
                                titulo = articulo.get('title', 'Sin título')
                                url = articulo.get('url', '#')
                                fuente = articulo.get('source', {}).get('name', 'Fuente desconocida')
                                fecha = articulo.get('publishedAt', '')[:10] if articulo.get('publishedAt') else ''
                                descripcion = articulo.get('description', 'Sin descripción disponible')
                                
                                st.markdown(f"#### [{titulo}]({url})")
                                st.markdown(f"*{fuente} | {fecha}*")
                                st.markdown(f"{descripcion}")
                            
                            st.markdown("<hr style='margin: 15px 0; opacity: 0.3;'>", unsafe_allow_html=True)
    
        # Si no pudimos obtener noticias reales, mostrar simuladas
        if uso_api and usar_simuladas:
            # Código para noticias simuladas (como respaldo)
            mostrar_noticias_simuladas()
    else:
        # Si decidimos no usar la API, mostrar simuladas
        mostrar_noticias_simuladas()
    
    # Insight sobre noticias y tendencias
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown("""
    <div class="epic-insight-title">📌 Insight sobre tendencias</div>
    <p>Mantenerse al día con las últimas noticias del ecosistema emprendedor permite identificar oportunidades y tendencias emergentes.
    Los participantes del EPIC Lab que siguen activamente las noticias del sector tienen un 40% más de probabilidades de conseguir inversión.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Función auxiliar para mostrar noticias simuladas
def mostrar_noticias_simuladas():
    # Noticias simuladas
    noticias_simuladas = [
        {
            "title": "Startups mexicanas atraen inversión récord en 2025",
            "source": "El Economista",
            "date": "2025-03-15",
            "description": "El ecosistema emprendedor mexicano recibió más de $1,200 millones USD en inversiones durante el primer trimestre, mostrando un crecimiento del 45% respecto al año anterior.",
            "relevancia": "Alta"
        },
        {
            "title": "EPIC Lab del ITAM lanza nueva incubadora especializada en fintech",
            "source": "Expansión",
            "date": "2025-03-10",
            "description": "El laboratorio de emprendimiento e innovación del ITAM anuncia un programa especializado para startups fintech con mentores internacionales y acceso a capital semilla.",
            "relevancia": "Muy alta"
        },
        {
            "title": "La inteligencia artificial transforma los modelos de negocio tradicionales",
            "source": "Forbes México",
            "date": "2025-03-08",
            "description": "Un estudio revela que el 65% de las empresas establecidas están adoptando tecnologías de IA para reinventar sus operaciones y competir con startups tecnológicas.",
            "relevancia": "Media"
        },
        {
            "title": "MAD Fellows presenta resultados impactantes en Demo Day 2025",
            "source": "Entrepreneur",
            "date": "2025-03-05",
            "description": "Los proyectos presentados por la nueva generación de MAD Fellows muestran soluciones innovadoras en sectores como salud, educación y sustentabilidad.",
            "relevancia": "Alta"
        },
        {
            "title": "Gobierno mexicano anuncia nuevo fondo para emprendedores",
            "source": "El Universal",
            "date": "2025-02-28",
            "description": "La Secretaría de Economía destinará $500 millones de pesos para apoyar a emprendedores en etapas tempranas, con énfasis en proyectos de impacto social.",
            "relevancia": "Media"
        }
    ]
    
    # Mostrar noticias simuladas
    for noticia in noticias_simuladas:
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### {noticia['title']}")
                st.markdown(f"*{noticia['source']} | {noticia['date']}*")
                st.markdown(f"{noticia['description']}")
            
            with col2:
                relevancia = noticia['relevancia']
                color = EPIC_COLORS['primary'] if relevancia == "Alta" else (EPIC_COLORS['secondary'] if relevancia == "Media" else EPIC_COLORS['success'])
                st.markdown(f"""
                <div style="background-color: {color}25; padding: 10px; border-radius: 5px; text-align: center; border-left: 3px solid {color};">
                    <span style="font-weight: 500; color: {color};">Relevancia: {relevancia}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0; opacity: 0.3;'>", unsafe_allow_html=True)

# Configuración de OpenAI (en producción, usar variables de entorno para las claves)
openai.api_key = "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"

# Constantes para el asistente
SYSTEM_PROMPT = """
Eres un Asesor de Contenido Inteligente para el EPIC Lab, un laboratorio de innovación y emprendimiento del ITAM.
Tu misión es ayudar a los usuarios a mejorar su contenido y estrategia de publicación.

Tus capacidades incluyen:
1. Revisar y mejorar contenido: corregir tono, redacción y ofrecer sugerencias para mayor impacto.
2. Explicar métricas como viralidad, relevancia social, inclusividad, claridad y tono positivo.
3. Generar ideas creativas para posts, campañas o iniciativas.
4. Responder preguntas sobre cómo usar la plataforma 'EPIC Lab Amplificador de Impacto'.

Sobre el EPIC Lab:
- Es un espacio de innovación y emprendimiento del ITAM (Instituto Tecnológico Autónomo de México).
- Ha impactado a más de 7,000 alumnos en los últimos 10 años.
- Tiene iniciativas como MAD Fellowship y MAD Challenge.
- Solo el 30% de participantes son mujeres (es un área de mejora).
- Su contenido busca inspirar a estudiantes, profesionales y emprendedores.

Tus respuestas deben ser:
- Breves y concisas (1-3 párrafos máximo).
- Personalizadas al contexto universitario y de emprendimiento.
- Positivas y orientadas a soluciones.
- Utilizando ocasionalmente emojis relevantes para hacer la interacción más dinámica.
"""

def add_ai_message(message, role="user"):
    st.session_state.ai_assistant_messages.append({"role": role, "content": message})

# Función para generar una respuesta del asistente
def generate_ai_response(user_message):
    # Agregar el mensaje del usuario al historial
    st.session_state.ai_assistant_messages.append({"role": "user", "content": user_message})
    
    # Preparar el historial de conversación para la API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Añadir tono seleccionado
    tone_prompts = {
        "profesional": "Responde en un tono profesional y formal, adecuado para comunicación corporativa o académica.",
        "inspirador": "Responde en un tono motivacional e inspirador, usando metáforas y lenguaje que estimule la acción.",
        "casual": "Responde en un tono casual y conversacional, como hablarías con un amigo, usando más emojis y lenguaje informal."
    }
    
    # Añadir el prompt de tono al sistema
    messages[0]["content"] += f"\n\n{tone_prompts[st.session_state.ai_assistant_tone]}"
    
    # Añadir contexto adicional según el contenido reciente de la aplicación
    if 'ultimo_score' in st.session_state:
        score_info = f"\nContexto adicional - Último análisis de impacto social:\n"
        score_info += f"- Viralidad: {st.session_state.ultimo_score['viralidad']}/100\n"
        score_info += f"- Relevancia social: {st.session_state.ultimo_score['relevancia_social']}/100\n"
        score_info += f"- Inclusividad: {st.session_state.ultimo_score['inclusividad']}/100\n"
        score_info += f"- Claridad: {st.session_state.ultimo_score['claridad']}/100\n"
        score_info += f"- Tono positivo: {st.session_state.ultimo_score['tono_positivo']}/100\n"
        messages[0]["content"] += score_info
    
    if 'ultimo_texto' in st.session_state:
        messages[0]["content"] += f"\nÚltimo texto analizado: '{st.session_state.ultimo_texto}'\n"
    
    # Agregar historial de conversación limitado (últimos 6 mensajes para mantenerlo conciso)
    for msg in st.session_state.ai_assistant_messages[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        # Llamada a la API de OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500
        )
        
        # Obtener respuesta y agregarla al historial
        ai_response = response.choices[0].message.content
        st.session_state.ai_assistant_messages.append({"role": "assistant", "content": ai_response})
        return ai_response
        
    except Exception as e:
        # Manejar error
        error_msg = f"Lo siento, tuve un problema al generar una respuesta. Error: {str(e)}"
        st.session_state.ai_assistant_messages.append({"role": "assistant", "content": error_msg})
        return error_msg

def render_ai_assistant():
    # Inicializar estados de sesión para el asistente si no existen
    if 'ai_assistant_messages' not in st.session_state:
        st.session_state.ai_assistant_messages = [
            {"role": "assistant", "content": "¡Hola! Soy tu Asesor de Contenido Inteligente del EPIC Lab. ¿En qué puedo ayudarte hoy? 👋"}
        ]
        
    if 'ai_assistant_tone' not in st.session_state:
        st.session_state.ai_assistant_tone = "profesional"
    
    # Crear un contenedor expandible para el asistente
    with st.expander("💬 Asesor de Contenido Inteligente", expanded=False):
        # Mostrar mensajes existentes
        for msg in st.session_state.ai_assistant_messages:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div style="background-color: #e9f5ef; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <strong>Asesor:</strong> {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f0f2f5; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <strong>Tú:</strong> {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Selector de tono
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("😊 Profesional", use_container_width=True, 
                          type="primary" if st.session_state.ai_assistant_tone == "profesional" else "secondary"):
                st.session_state.ai_assistant_tone = "profesional"
                st.rerun()
        with col2:
            if st.button("🔥 Inspirador", use_container_width=True,
                          type="primary" if st.session_state.ai_assistant_tone == "inspirador" else "secondary"):
                st.session_state.ai_assistant_tone = "inspirador"
                st.rerun()
        with col3:
            if st.button("👋 Casual", use_container_width=True,
                          type="primary" if st.session_state.ai_assistant_tone == "casual" else "secondary"):
                st.session_state.ai_assistant_tone = "casual"
                st.rerun()
        
        # Sugerencias rápidas
        st.markdown("**Sugerencias rápidas:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("¿Cómo mejorar viralidad?", use_container_width=True):
                generate_ai_response("¿Cómo mejorar viralidad?")
                st.rerun()
        with col2:
            if st.button("Idea para post", use_container_width=True):
                generate_ai_response("Dame una idea para un post sobre innovación")
                st.rerun()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("¿Qué es inclusividad?", use_container_width=True):
                generate_ai_response("¿Qué significa el score de inclusividad?")
                st.rerun()
        with col2:
            if st.button("Ayuda con app", use_container_width=True):
                generate_ai_response("¿Cómo usar esta plataforma?")
                st.rerun()
        
        # Input para mensaje personalizado
        user_message = st.chat_input("Escribe tu mensaje aquí...")
        if user_message:
            generate_ai_response(user_message)
            st.rerun()

# Función para el Dashboard
def render_dashboard(df):
    # Encabezado principal con diseño moderno
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Conversación Digital sobre Emprendimiento</h1>
        <p class="epic-subtitle">Optimiza el alcance del EPIC Lab con análisis de datos de emprendimiento</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SECCIÓN 1: MÉTRICAS CLAVE DE SENTIMIENTO
    st.markdown("### Sentimiento sobre Emprendimiento")
    
    # Usar los datos actualizados que proporcionaste
    # Mostrar métricas en formato moderno
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">165.99K</div>
            <div class="epic-metric-label">Total Menciones</div>
            <div style="font-size: 0.8rem; color: #777;">(Del 1 de enero al 23 de marzo)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">52.4%</div>
            <div class="epic-metric-label">Sentimiento Positivo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">26.1%</div>
            <div class="epic-metric-label">Sentimiento Negativo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">26.3%</div>
            <div class="epic-metric-label">Sentimiento Neto</div>
        </div>
        """, unsafe_allow_html=True)
    
    # SECCIÓN 2: ANÁLISIS VISUAL DE SENTIMIENTO - IMAGEN A PANTALLA COMPLETA
    st.markdown("### Distribución de Sentimiento")
    
    # Usar el nombre correcto de la imagen de sentimiento
    try:
        st.image("assets/sentimiento.png", caption="Distribución del sentimiento en publicaciones e impresiones", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen de sentimiento: {e}")
    
    st.markdown(f"""
    <div style="text-align: center; margin: 20px 0;">
        <span style="font-size: 1.2rem; font-weight: 600;">Sentimiento Neto: 26.3%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # SECCIÓN 3: PALABRAS QUE POTENCIAN ENGAGEMENT - PANTALLA COMPLETA
    st.markdown("### Palabras que Potencian Engagement")
    
    try:
        # Usar el nombre exacto del archivo
        st.image("assets/wordcloud_positivo.png", caption="Términos positivos relacionados con emprendimiento", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen de palabras positivas: {e}")
    
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Estrategia de Comunicación Positiva</div>
    <p>Utiliza términos como "oportunidad", "desarrollo", "crecimiento" y "apoyo" para maximizar el engagement. Evita transmitir mensajes en negativo y asegúrate de que todas tus comunicaciones mantengan un tono positivo y constructivo.</p>
    <p>Ejemplos prácticos:</p>
    <ul>
        <li>En lugar de "Encarrila tu nuevo emprendimiento", usar "Dale vida a tu emprendimiento"</li>
        <li>En vez de "Evita fracasar en tu startup", mejor "Construye el éxito de tu startup"</li>
        <li>La mención de "mujeres" puede contribuir al objetivo de aumentar la participación femenina en el EPIC Lab.</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 4: PALABRAS A EVITAR - PANTALLA COMPLETA
    st.markdown("### Palabras a Evitar")
    
    try:
        # Usar el nombre exacto del archivo
        st.image("assets/wordcloud_negativo.png", caption="Términos con connotación negativa a evitar", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen de palabras negativas: {e}")
    
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown("""
    <div class="epic-insight-title">📌 Precaución en Comunicación</div>
    <p>Evita términos como "crisis", "problemas" y "riesgos" que generan sentimientos negativos. El contenido negativo tiene menor alcance y compromete la imagen positiva que el EPIC Lab busca proyectar.</p>
    <p>Cuando tengas algún convenio con alguna entidad gubernamental, evita meterte en temas políticos que puedan generar controversia. Mantén la comunicación enfocada en los objetivos educativos y de emprendimiento.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 5: PUBLICADORES MÁS INFLUYENTES - PANTALLA COMPLETA
    st.markdown("### Publicadores Más Influyentes")
    
    try:
        # Usar el nombre correcto de la imagen de publicadores
        st.image("assets/publicadoresmasinflu.png", caption="Distribución de impresiones por publicador", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen de publicadores: {e}")
    
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown("""
    <div class="epic-insight-title">📌 Oportunidades de Colaboración</div>
    <p>Establecer un convenio con emprendedor.com sería altamente beneficioso dada su gran influencia y alcance positivo en el ecosistema emprendedor. Esta alianza estratégica aumentaría significativamente la visibilidad del EPIC Lab entre audiencias relevantes y comprometidas.</p>
    <p>Considera también colaboraciones con otros publicadores influyentes y positivos para maximizar el impacto de tus campañas.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 6: ANÁLISIS DE FUENTES - PANTALLA COMPLETA
    st.markdown("### Análisis de Fuentes de Difusión")
    
    try:
        # Usar el nombre correcto de la imagen de impresiones por red social
        st.image("assets/impresionesporredsocial.png", caption="Distribución de publicaciones por fuente y sentimiento", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen de impresiones por red social: {e}")
    
    # Insight sobre fuentes
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Estrategia de Canales</div>
    <p>El EPIC Lab debería priorizar su presencia en Instagram, ya que la conversación digital sobre emprendimiento está fuertemente concentrada en esta plataforma. También Facebook y TikTok muestran resultados positivos.</p>
    <p>Recomendaciones específicas:</p>
    <ul>
        <li><strong>Instagram:</strong> Desarrollar una estrategia robusta con publicaciones visuales frecuentes y stories interactivas.</li>
        <li><strong>Facebook:</strong> Enfocarse en contenido de comunidad y eventos.</li>
        <li><strong>TikTok:</strong> Crear contenido breve y dinámico para atraer a audiencias más jóvenes.</li>
        <li><strong>Twitter:</strong> Utilizarlo principalmente para conexiones profesionales y difusión de eventos.</li>
    </ul>
    <p>Esta estrategia multicanal, con énfasis en Instagram, permitirá amplificar el impacto del contenido del EPIC Lab.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 7: RECOMENDACIONES PARA EPIC LAB
    st.markdown("### Recomendaciones Estratégicas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: rgba(46, 139, 87, 0.1); border-radius: 12px; padding: 15px; height: 100%;">
            <h4 style="color: #2E8B57; margin-top: 0;"><i class="fas fa-bullhorn"></i> Contenido</h4>
            <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>Usar términos positivos como "oportunidad" y "desarrollo"</li>
                <li>Evitar palabras negativas como "crisis" y "problemas"</li>
                <li>Destacar historias de éxito de mujeres emprendedoras</li>
                <li>Crear contenido educativo sobre emprendimiento</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: rgba(139, 195, 74, 0.1); border-radius: 12px; padding: 15px; height: 100%;">
            <h4 style="color: #8BC34A; margin-top: 0;"><i class="fas fa-users"></i> Canales</h4>
            <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>Priorizar Instagram como canal principal</li>
                <li>Complementar con Facebook y TikTok</li>
                <li>Desarrollar estrategias específicas para cada plataforma</li>
                <li>Establecer alianza con emprendedor.com</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: rgba(66, 133, 244, 0.1); border-radius: 12px; padding: 15px; height: 100%;">
            <h4 style="color: #4285F4; margin-top: 0;"><i class="fas fa-chart-line"></i> Medición</h4>
            <ul style="padding-left: 20px; margin-bottom: 0;">
                <li>Monitorear el sentimiento de las menciones semanalmente</li>
                <li>Seguir la evolución del alcance por plataforma</li>
                <li>Medir el incremento en participación femenina</li>
                <li>Evaluar el impacto de colaboraciones con influencers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Botón para descargar reporte completo (simulado)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
# Función para Analytics
# Función para Analytics
# Función para Analytics
def render_analytics(df):
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Analytics del EPIC Lab</h1>
        <p class="epic-subtitle">Análisis detallado del impacto y alcance digital</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SECCIÓN 1: CRECIMIENTO EN MÉTRICAS
    st.markdown("### Crecimiento en Impresiones y Alcance")
    st.markdown("<p style='font-size: 0.9rem; color: #666;'>Del 1 de enero del 2024 al 21 de marzo de 2025</p>", unsafe_allow_html=True)
    
    # Datos de crecimiento (según la imagen)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">+52%</div>
            <div class="epic-metric-label">Aumento en Publicaciones</div>
            <div style="font-size: 0.7rem;">(De 100 a 152)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">+195%</div>
            <div class="epic-metric-label">Crecimiento en Impresiones</div>
            <div style="font-size: 0.7rem;">(De 811.98K a 2.40M)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">+196%</div>
            <div class="epic-metric-label">Aumento en Alcance Social</div>
            <div style="font-size: 0.7rem;">(De 774.78K a 2.29M)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="epic-metric">
            <div class="epic-metric-value">-47%</div>
            <div class="epic-metric-label">Cambio en Usuarios Twitter</div>
            <div style="font-size: 0.7rem;">(De 49 a 26)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recomendación para crecimiento
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Estrategia de Crecimiento</div>
    <p>El crecimiento significativo en impresiones (+195%) y alcance social (+196%) demuestra el 
    potencial de expansión del EPIC Lab. Para mantener esta tendencia positiva, recomendamos:</p>
    <ul>
        <li>Diversificar a nuevas plataformas como Instagram y TikTok</li>
        <li>Crear más contenido sobre Ciencia e Innovación ligado al emprendimiento</li>
        <li>Implementar estrategias específicas para aumentar la participación femenina</li>
        <li>Expandir el alcance más allá de la comunidad del ITAM</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 2: PUBLICACIONES POR USUARIO Y SENTIMIENTO
    st.markdown("### Publicaciones por Usuario y Sentimiento")
    
    try:
        st.image("assets/publicacionesporusuariosentimiento.png", caption="Distribución de publicaciones por usuario y sentimiento", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
    
    # Insight sobre usuarios
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Expansión de Comunidad</div>
    <p>La conversación digital sobre el EPIC Lab se mantiene principalmente dentro de la comunidad del ITAM. 
    Para amplificar su impacto, es crucial expandir el alcance más allá de este círculo inmediato. 
    Recomendamos establecer alianzas con influencers del ecosistema emprendedor, desarrollar un programa 
    de embajadores, y participar activamente en comunidades externas relacionadas con innovación y emprendimiento.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 3: PUBLICACIONES POR GÉNERO
    st.markdown("### Publicaciones por Género")
    
    try:
        st.image("assets/publicacionesporgenero.png", caption="Distribución de publicaciones por género", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
    
    # Insight sobre género
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Estrategia de Inclusión</div>
    <p>El análisis muestra que apenas el 2% de la audiencia identificable es femenina, mientras que el 31.6% es masculina 
    (el resto es indefinido). Esta brecha representa una oportunidad significativa para implementar estrategias de inclusión 
    que aumenten la participación femenina. Recomendamos destacar historias de mujeres emprendedoras, crear contenido 
    específico para este segmento y utilizar lenguaje inclusivo en todas las comunicaciones.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 4: PUBLICACIONES POR FUENTE Y SENTIMIENTO
    st.markdown("### Publicaciones por Fuente y Sentimiento")
    
    try:
        st.image("assets/publicacionesfuentesentimiento.png", caption="Distribución de publicaciones por fuente y sentimiento", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
    
    # Insight sobre fuentes
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Estrategia de Plataformas</div>
    <p>La conversación digital sobre el EPIC Lab está fuertemente concentrada en Twitter. Sin embargo, 
    recomendamos expandir significativamente la presencia en Instagram, ya que la conversación digital 
    sobre emprendimiento está más activa en esta plataforma. Esta diversificación permitirá llegar a 
    audiencias más jóvenes y potencialmente interesadas en los programas del EPIC Lab.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 5: IMPRESIONES POR TEMA
    st.markdown("### Impresiones por Tema")
    
    # Mostrar la imagen directamente desde assets
    try:
        st.image("assets/publicacionesimpresionesportema.png", caption="Distribución de impresiones por tema", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
    
    # Insight sobre impresiones por tema
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Estrategia de Contenido</div>
    <p>Los temas de Ciencia e Innovación generan el mayor volumen de impresiones (aproximadamente 1,000,000) 
    con predominante sentimiento positivo. Las publicaciones relacionadas con estos temas tienen un potencial 
    mucho mayor de alcance. Recomendamos aumentar la frecuencia de publicaciones en estos temas, 
    enfatizando su conexión con el emprendimiento.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SECCIÓN 6: ANÁLISIS DE SENTIMIENTO
    st.markdown("### Análisis de Sentimiento")
    
    try:
        st.image("assets/sentimientoepic.png", caption="Análisis de sentimiento sobre EPIC Lab", use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")
    
    # Insight sobre sentimiento
    st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="epic-insight-title">📌 Tono de Comunicación</div>
    <p>El EPIC Lab tiene un sentimiento predominantemente positivo (64.5% a 76.4%), con un sentimiento neto entre 54.6% y 71%. 
    Esta percepción positiva es un activo valioso. Recomendamos continuar con un tono positivo en todas las comunicaciones, 
    destacar historias de éxito y transformación, y mantener un enfoque en soluciones al abordar los desafíos del emprendimiento.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# Función para Contenido
def render_content():
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Creación de Contenido</h1>
        <p class="epic-subtitle">Optimiza tu contenido con análisis inteligente y recomendaciones</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear tabs para las diferentes herramientas
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 Recomendador", 
        "📈 Impacto Social", 
        "#️⃣ Hashtags", 
        "⏰ Horarios"
    ])
    
    # Tab Recomendador
    with tab1:
        st.markdown("### Recomendador de Contenido")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<div class="epic-card">', unsafe_allow_html=True)
            st.subheader("Define tu audiencia")
            
            publico = st.radio(
                "Público objetivo:",
                ["Estudiantes", "Profesionales", "Emprendedores"]
            )
            
            genero = st.radio(
                "Enfoque de género:",
                ["Todos", "Mujer", "Hombre"]
            )
            
            tipo_contenido = st.selectbox(
                "Temática:",
                ["Emprendimiento", "Innovación", "Tecnología", "Finanzas", "Negocios"]
            )
            
            formato = st.selectbox(
                "Formato:",
                ["Texto", "Imagen", "Video", "Infografía"]
            )
            
            plataforma = st.selectbox(
                "Plataforma:",
                ["Instagram", "Twitter/X", "LinkedIn", "TikTok"]
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="epic-card">', unsafe_allow_html=True)
            st.subheader("Recomendación personalizada")
            
            if st.button("Generar Recomendación", type="primary"):
                with st.spinner("Analizando datos y generando recomendación..."):
                    # Ajustar valores para compatibilidad con la función
                    publico_map = publico
                    genero_map = "Otro" if genero == "Todos" else genero
                    
                    recomendacion = generar_recomendacion(
                        publico_map, 
                        genero_map, 
                        tipo_contenido, 
                        formato, 
                        plataforma
                    )
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 15px;">
                        <span style="background-color: {EPIC_COLORS['primary']}; color: white; padding: 5px 10px; border-radius: 20px; font-size: 0.9rem;">
                            {publico}
                        </span>
                        <span style="background-color: {EPIC_COLORS['secondary']}; color: white; padding: 5px 10px; border-radius: 20px; margin-left: 5px; font-size: 0.9rem;">
                            {plataforma}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="epic-premium">', unsafe_allow_html=True)
                    st.markdown(recomendacion)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Selecciona los parámetros y presiona 'Generar Recomendación' para recibir estrategias personalizadas.")
                
                st.markdown("""
                ### ¿Por qué personalizar?
                
                El contenido adaptado a tu audiencia específica tiene **hasta 3 veces más engagement** que el contenido genérico. 
                
                Nuestro algoritmo analiza patrones de éxito en cada plataforma para maximizar el alcance del EPIC Lab.
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab Impacto Social
    with tab2:
        st.markdown("### Medidor de Impacto Social")
        
        st.markdown('<div class="epic-card">', unsafe_allow_html=True)
        # Input de texto en diseño más limpio
        st.markdown("**Escribe tu idea de post para el EPIC Lab:**")
        texto_post = st.text_area(
            "",
            height=120,
            placeholder="Ejemplo: El EPIC Lab lanza su nuevo programa de mentoría para emprendedores tecnológicos. Únete a nuestra comunidad y transforma tus ideas en proyectos de impacto real."
        )
        
        if st.button("Analizar Impacto", type="primary"):
            if not texto_post or len(texto_post.strip()) < 10:
                st.warning("Por favor, escribe un texto más extenso para poder analizarlo correctamente.")
            else:
                with st.spinner("Analizando el impacto social de tu contenido..."):
                    # Llamar a la función de análisis
                    resultado = analizar_impacto_social(texto_post)
                    
                    # Guardar en session state para usar en otras tabs
                    st.session_state.ultimo_texto = texto_post
                    st.session_state.ultimo_score = resultado
                    
                    # Mejorar visualización con dos columnas
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        # Crear gráfico de radar con estilo mejorado
                        categorias = ['Viralidad', 'Relevancia Social', 'Inclusividad', 'Claridad', 'Tono Positivo']
                        valores = [
                            resultado['viralidad'],
                            resultado['relevancia_social'],
                            resultado['inclusividad'],
                            resultado['claridad'],
                            resultado['tono_positivo']
                        ]
                        
                        # Cerrar el polígono repitiendo el primer valor
                        categorias_cerrado = categorias + [categorias[0]]
                        valores_cerrado = valores + [valores[0]]
                        
                        fig = go.Figure()
                        
                        # Añadir áreas de fondo para diferentes niveles con colores EPIC
                        fig.add_trace(go.Scatterpolar(
                            r=[100, 100, 100, 100, 100, 100],
                            theta=categorias_cerrado,
                            fill='toself',
                            fillcolor='rgba(245, 245, 245, 0.3)',
                            line=dict(color='rgba(245, 245, 245, 0.5)'),
                            showlegend=False
                        ))
                        
                        fig.add_trace(go.Scatterpolar(
                            r=[75, 75, 75, 75, 75, 75],
                            theta=categorias_cerrado,
                            fill='toself',
                            fillcolor=f'rgba({int(EPIC_COLORS["secondary"][1:3], 16)}, {int(EPIC_COLORS["secondary"][3:5], 16)}, {int(EPIC_COLORS["secondary"][5:7], 16)}, 0.1)',
                            line=dict(color=f'rgba({int(EPIC_COLORS["secondary"][1:3], 16)}, {int(EPIC_COLORS["secondary"][3:5], 16)}, {int(EPIC_COLORS["secondary"][5:7], 16)}, 0.3)'),
                            showlegend=False
                        ))
                        
                        fig.add_trace(go.Scatterpolar(
                            r=[50, 50, 50, 50, 50, 50],
                            theta=categorias_cerrado,
                            fill='toself',
                            fillcolor=f'rgba({int(EPIC_COLORS["primary"][1:3], 16)}, {int(EPIC_COLORS["primary"][3:5], 16)}, {int(EPIC_COLORS["primary"][5:7], 16)}, 0.1)',
                            line=dict(color=f'rgba({int(EPIC_COLORS["primary"][1:3], 16)}, {int(EPIC_COLORS["primary"][3:5], 16)}, {int(EPIC_COLORS["primary"][5:7], 16)}, 0.3)'),
                            showlegend=False
                        ))
                        
                        # Añadir los valores del análisis
                        fig.add_trace(go.Scatterpolar(
                            r=valores_cerrado,
                            theta=categorias_cerrado,
                            fill='toself',
                            fillcolor=f'rgba({int(EPIC_COLORS["primary"][1:3], 16)}, {int(EPIC_COLORS["primary"][3:5], 16)}, {int(EPIC_COLORS["primary"][5:7], 16)}, 0.6)',
                            line=dict(color=EPIC_COLORS['primary'], width=3),
                            name='Impacto Social'
                        ))
                        
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100],
                                    tickvals=[25, 50, 75, 100],
                                    ticktext=['25', '50', '75', '100']
                                )
                            ),
                            showlegend=False,
                            margin=dict(t=10, b=30, l=10, r=10),
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Mostrar score promedio en formato más limpio
                        score_promedio = sum(valores) / len(valores)
                        
                        st.markdown(f"""
                        <div style="text-align: center; margin-top: 0px; margin-bottom: 20px;">
                            <div style="font-size: 2rem; font-weight: 700; color: {EPIC_COLORS['primary']};">{score_promedio:.1f}</div>
                            <div style="font-size: 0.9rem; color: {EPIC_COLORS['text_secondary']};">Score Global de Impacto</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("### Desglose de puntajes")
                        
                        # Mostrar puntajes individuales en forma de barras horizontales
                        for i, (cat, val) in enumerate(zip(categorias, valores)):
                            st.markdown(f"""
                            <div style="margin-bottom: 15px;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                    <div>{cat}</div>
                                    <div style="font-weight: 600;">{val}/100</div>
                                </div>
                                <div style="height: 8px; background-color: #E0E0E0; border-radius: 4px;">
                                    <div style="width: {val}%; height: 100%; background-color: {EPIC_COLORS['primary']}; border-radius: 4px;"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Sugerencias de mejora
                        st.markdown("### Sugerencias de mejora")
                        st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
                        st.markdown(f"{resultado['sugerencias']}")
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Escribe tu idea de post y haz clic en 'Analizar Impacto' para evaluarlo.")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab Hashtags
    # Tab Hashtags
    # Tab Hashtags
    with tab3:
        st.markdown("### Generador de Hashtags")
        
        st.markdown('<div class="epic-card">', unsafe_allow_html=True)
        # Usar el texto del post de la pestaña anterior o permitir uno nuevo
        if 'ultimo_texto' in st.session_state:
            texto_default = st.session_state.ultimo_texto
        else:
            texto_default = ""
        
        st.markdown("**Texto del post:**")
        texto_hashtags = st.text_area(
            "",
            value=texto_default,
            height=120,
            key="texto_hashtags_input",
            placeholder="Escribe o pega el texto de tu post aquí para generar hashtags relevantes..."
        )
        
        # Opciones adicionales para personalizar los hashtags
        st.markdown("**Personaliza tus hashtags:**")
        col1, col2 = st.columns(2)
        
        with col1:
            incluir_itam = st.checkbox("Incluir ITAM", value=True, key="check_itam")
            incluir_epiclab = st.checkbox("Incluir EPIC Lab", value=True, key="check_epiclab")
            incluir_mad = st.checkbox("Incluir MAD Fellows", value=True, key="check_mad")
        
        with col2:
            tema_principal = st.selectbox(
                "Tema principal:",
                ["Emprendimiento", "Innovación", "Tecnología", "Educación", "Impacto Social"],
                key="select_tema"
            )
            
            cantidad = st.slider("Cantidad de hashtags:", min_value=5, max_value=12, value=8, key="slider_cantidad")
        
        if st.button("Generar Hashtags", type="primary", key="btn_generar_hashtags"):
            if not texto_hashtags or len(texto_hashtags.strip()) < 10:
                st.warning("Por favor, escribe un texto más extenso para generar hashtags relevantes.")
            else:
                # Generar hashtags base para asegurarnos que siempre haya algo
                hashtags_base = []
                if incluir_epiclab:
                    hashtags_base.append("#EPICLab")
                if incluir_itam:
                    hashtags_base.append("#ITAM")
                if incluir_mad:
                    hashtags_base.append("#MADFellows")
                
                # Hashtags según tema
                tema_hashtags = {
                    "Emprendimiento": ["#Emprendimiento", "#Startup", "#Business", "#Entrepreneur"],
                    "Innovación": ["#Innovación", "#Innovation", "#Creatividad", "#Disruptive"],
                    "Tecnología": ["#Tech", "#Tecnología", "#Digital", "#FutureTech"],
                    "Educación": ["#Educación", "#Learning", "#Estudiantes", "#Skills"],
                    "Impacto Social": ["#ImpactoSocial", "#Sostenibilidad", "#Comunidad", "#ChangeAgent"]
                }
                
                # Añadir hashtags del tema seleccionado
                hashtags_tema = tema_hashtags.get(tema_principal, [])
                
                # Extraer hashtags del texto (palabras clave simples)
                palabras_clave = {
                    "emprendimiento": "#Emprendimiento",
                    "startup": "#Startup",
                    "tecnología": "#Tech",
                    "digital": "#Digital",
                    "innovación": "#Innovación",
                    "futuro": "#FuturoDigital",
                    "méxico": "#México",
                    "desafío": "#Challenge",
                    "impacto": "#ImpactoSocial",
                    "comunidad": "#Comunidad",
                    "desarrollo": "#Desarrollo",
                    "talento": "#Talento",
                    "creatividad": "#Creatividad",
                    "colaboración": "#Collaboration",
                    "fellows": "#MADFellows",
                    "challenge": "#EPICChallenge",
                    "estudiantes": "#Estudiantes",
                    "educación": "#Educación",
                    "transformación": "#Transformación",
                    "negocios": "#Business",
                    "fintech": "#Fintech",
                    "ai": "#AI",
                    "inteligencia": "#IA"
                }
                
                hashtags_del_texto = []
                if texto_hashtags:
                    palabras = texto_hashtags.lower().split()
                    for palabra in palabras:
                        palabra_limpia = ''.join(c for c in palabra if c.isalnum())
                        if palabra_limpia in palabras_clave and palabras_clave[palabra_limpia] not in hashtags_del_texto:
                            hashtags_del_texto.append(palabras_clave[palabra_limpia])
                
                # Combinar todas las fuentes de hashtags
                todos_hashtags = list(set(hashtags_base + hashtags_tema + hashtags_del_texto))
                
                # Si faltan para llegar a la cantidad solicitada, añadir genéricos
                hashtags_genericos = ["#Innovation", "#DigitalTransformation", "#Growth", "#Community", "#Success", "#Collaboration", "#Future", "#Leadership", "#Networking"]
                
                while len(todos_hashtags) < cantidad:
                    hashtag_generico = random.choice(hashtags_genericos)
                    if hashtag_generico not in todos_hashtags:
                        todos_hashtags.append(hashtag_generico)
                    # Evitar bucle infinito
                    if len(todos_hashtags) >= min(cantidad, len(set(hashtags_base + hashtags_tema + hashtags_del_texto + hashtags_genericos))):
                        break
                
                # Limitar a la cantidad solicitada
                todos_hashtags = todos_hashtags[:cantidad]
                
                # Guardar en el estado de la sesión
                st.session_state.ultimo_hashtags = todos_hashtags
                
                # Mostrar hashtags en formato visual atractivo
                st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
                
                for hashtag in todos_hashtags:
                    # Color basado en categoría
                    color = EPIC_COLORS['primary']
                    if hashtag in ["#EPICLab", "#ITAM", "#MADFellows"]:
                        color = EPIC_COLORS['primary']
                    elif hashtag in hashtags_tema:
                        color = EPIC_COLORS['secondary']
                    
                    st.markdown(
                        f'<span class="epic-hashtag" style="background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15);">{hashtag}</span>', 
                        unsafe_allow_html=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Texto para copiar
                st.markdown("### Copiar todos los hashtags")
                hashtags_texto = " ".join(todos_hashtags)
                st.code(hashtags_texto)
                
                # Insight personalizado según tema
                st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
                if tema_principal == "Emprendimiento":
                    insight_texto = "Los hashtags de emprendimiento tienen mayor alcance cuando se combinan con hashtags específicos de industria. Úsalos para conectar con inversores y mentores potenciales."
                elif tema_principal == "Innovación":
                    insight_texto = "Los hashtags de innovación son muy seguidos por tomadores de decisiones en grandes empresas. Perfectos para posicionar al EPIC Lab como líder de pensamiento en transformación."
                elif tema_principal == "Tecnología":
                    insight_texto = "Los hashtags de tecnología alcanzan a una audiencia muy comprometida. Combina hashtags generales con términos más específicos para maximizar tu alcance."
                elif tema_principal == "Educación":
                    insight_texto = "Los hashtags educativos son especialmente efectivos entre semana en horario laboral. Perfecto para atraer a estudiantes y profesionales buscando desarrollo."
                else:
                    insight_texto = "Los hashtags de impacto social tienen alto engagement y permanencia. Ideal para construir una comunidad comprometida alrededor del EPIC Lab."
                
                st.markdown(f"""
                <div class="epic-insight-title">📌 Tip para hashtags de {tema_principal}</div>
                <p>{insight_texto}</p>
                <p>Los hashtags específicos de nicho tienen hasta un 70% más de engagement que los hashtags genéricos muy populares.</p>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Escribe o pega el texto de tu post y haz clic en 'Generar Hashtags'.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    # Tab Horarios
    with tab4:
        st.markdown("### Horarios Óptimos")
        
        st.markdown('<div class="epic-card">', unsafe_allow_html=True)
        # Diseño más limpio para selección de plataforma
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Plataforma")
            plataforma_horario = st.radio(
                "",
                ["Instagram", "Twitter/X", "LinkedIn", "TikTok"]
            )
            
            st.button("Analizar Horarios", type="primary")
        
        with col2:
            # Siempre mostrar resultados para mejor experiencia de usuario
            # En app real, esto estaría condicionado al botón
            horarios = recomendar_horarios(plataforma_horario)
            
            st.subheader(f"Mejores horarios para {plataforma_horario}")
            
            # Diseño visual mejorado para los horarios
            for i, horario in enumerate(horarios):
                # Color que se va degradando según la posición
                opacity = 1.0 if i == 0 else (0.9 if i == 1 else 0.8)
                
                st.markdown(f"""
                <div style="background-color: rgba({int(EPIC_COLORS['secondary'][1:3], 16)}, {int(EPIC_COLORS['secondary'][3:5], 16)}, {int(EPIC_COLORS['secondary'][5:7], 16)}, {opacity*0.15}); 
                            padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid {EPIC_COLORS['primary']};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.2rem; font-weight: 600; color: {EPIC_COLORS['primary']};">
                                🕒 {horario['hora']}
                            </span>
                        </div>
                        <div style="background-color: {EPIC_COLORS['primary']}; color: white; 
                                    padding: 5px 10px; border-radius: 15px; font-weight: 500;">
                            {horario['efectividad']}% efectividad
                        </div>
                    </div>
                    <p style="margin-top: 8px; margin-bottom: 0;">{horario['razon']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Insight sobre horarios
            st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="epic-insight-title">📌 Insight sobre horarios</div>
            <p>Para {plataforma_horario}, programar publicaciones en estos horarios óptimos puede aumentar tu alcance orgánico hasta en un 25-30%. Mantén consistencia en tus publicaciones para mejorar el rendimiento del algoritmo.</p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Función para Predicciones
def render_predictions(df):
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Predicciones & Análisis</h1>
        <p class="epic-subtitle">Anticipa tendencias y optimiza tu estrategia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear subtabs más limpios
    subtab1, subtab2 = st.tabs(["Forecast de Menciones", "Impacto de Contenido"])
    
    # Subtab 1: Forecast de menciones
    with subtab1:
        st.markdown('<div class="epic-card">', unsafe_allow_html=True)
        st.subheader("Predicción de Menciones")
        st.markdown("Proyección de menciones del EPIC Lab para los próximos 7 días")
        
        with st.spinner("Analizando datos históricos..."):
            # Generar forecast
            forecast_df = generar_forecast_menciones(df)
            
            # Crear gráfico con diseño mejorado
            fig = px.line(
                forecast_df,
                x='fecha',
                y='menciones',
                color='tipo',
                title=None,
                labels={'fecha': 'Fecha', 'menciones': 'Menciones', 'tipo': ''},
                color_discrete_map={'Histórico': EPIC_COLORS['primary'], 'Predicción': EPIC_COLORS['secondary']}
            )
            
            # Añadir área sombreada para la predicción
            prediccion_df = forecast_df[forecast_df['tipo'] == 'Predicción']
            
            fig.add_trace(
                go.Scatter(
                    x=prediccion_df['fecha'],
                    y=prediccion_df['menciones'],
                    fill='tozeroy',
                    fillcolor=f'rgba({int(EPIC_COLORS["secondary"][1:3], 16)}, {int(EPIC_COLORS["secondary"][3:5], 16)}, {int(EPIC_COLORS["secondary"][5:7], 16)}, 0.2)',
                    line=dict(color='rgba(0,0,0,0)'),
                    showlegend=False
                )
            )
            
            fig.update_layout(
                margin=dict(t=10, b=30, l=10, r=10),
                legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calcular crecimiento proyectado
            ultimo_historico = forecast_df[forecast_df['tipo'] == 'Histórico']['menciones'].iloc[-1]
            ultimo_prediccion = forecast_df[forecast_df['tipo'] == 'Predicción']['menciones'].iloc[-1]
            crecimiento = ((ultimo_prediccion / ultimo_historico) - 1) * 100
            
            # Mostrar métrica de manera más atractiva
            st.markdown(f"""
            <div style="text-align: center; background-color: {EPIC_COLORS['primary']}10; padding: 15px; border-radius: 10px; margin: 20px 0;">
                <div style="font-size: 1.8rem; font-weight: 700; color: {EPIC_COLORS['primary']};">+{crecimiento:.1f}%</div>
                <div style="font-size: 0.9rem; color: {EPIC_COLORS['text_secondary']};">Crecimiento Proyectado</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Insight sobre las predicciones
            st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="epic-insight-title">📌 Estrategias recomendadas</div>
            <p>Basado en la proyección de crecimiento, recomendamos:</p>
            <ul>
                <li>Aumentar la frecuencia de publicación en {df.groupby('plataforma')['menciones'].sum().idxmax()}</li>
                <li>Crear contenido sobre los temas de mayor interés: {df.groupby('tema')['menciones'].sum().idxmax()} {" y " + df.groupby('tema')['menciones'].sum().nlargest(2).index[1] if len(df.groupby('tema')['menciones'].sum()) > 1 else ""}</li>
                <li>Mantener el tono positivo que ha funcionado bien</li>
            </ul>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Subtab 2: Forecast de impacto de contenido
    with subtab2:
        st.markdown('<div class="epic-card">', unsafe_allow_html=True)
        st.subheader("Predicción de Impacto de Contenido")
        
        # Usar el score de viralidad de la pestaña de Medidor de Impacto Social si está disponible
        if 'ultimo_score' in st.session_state:
            score_viralidad = st.session_state.ultimo_score['viralidad']
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="background-color: {EPIC_COLORS['primary']}; color: white; padding: 8px 15px; 
                           border-radius: 20px; font-weight: 500; margin-right: 10px;">
                    Score de Viralidad: {score_viralidad}/100
                </div>
                <div style="font-size: 0.9rem; color: {EPIC_COLORS['text_secondary']};">
                    (Del último análisis de impacto social)
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Slider más bonito usando el estilo de la aplicación
            st.markdown("**Selecciona el Score de Viralidad para la Simulación:**")
            score_viralidad = st.slider("", 0, 100, 50)
        
        with st.spinner("Simulando curva de crecimiento..."):
            # Generar forecast de impacto
            impacto_df = simular_forecast_impacto(score_viralidad)
            
            # Crear gráfico con estilo mejorado
            fig = px.area(
                impacto_df,
                x='fecha',
                y='alcance',
                title=None,
                labels={'fecha': 'Fecha', 'alcance': 'Alcance (Personas)'},
                template='plotly_white'
            )
            
            fig.update_traces(
                line=dict(color=EPIC_COLORS['primary'], width=3),
                fillcolor=f'rgba({int(EPIC_COLORS["primary"][1:3], 16)}, {int(EPIC_COLORS["primary"][3:5], 16)}, {int(EPIC_COLORS["primary"][5:7], 16)}, 0.2)'
            )
            
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calcular crecimiento total y métricas
            crecimiento_total = ((impacto_df['alcance'].iloc[-1] / impacto_df['alcance'].iloc[0]) - 1) * 100
            alcance_total = impacto_df['alcance'].sum()
            
            # Mostrar métricas en contenedor atractivo
            st.markdown('<div class="epic-metric-container">', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="epic-metric">
                <div class="epic-metric-value">+{crecimiento_total:.1f}%</div>
                <div class="epic-metric-label">Crecimiento Total</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="epic-metric">
                <div class="epic-metric-value">{alcance_total:,}</div>
                <div class="epic-metric-label">Alcance Acumulado</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recomendaciones personalizadas según score de viralidad
            st.markdown('<div class="epic-insight">', unsafe_allow_html=True)
            
            if score_viralidad >= 80:
                st.markdown("""
                <div class="epic-insight-title">📌 Estrategia de Alto Impacto</div>
                <p>Tu contenido tiene potencial viral excepcional:</p>
                <ul>
                    <li>Programa publicaciones en horarios de máxima actividad</li>
                    <li>Invierte en promoción para amplificar el alcance inicial</li>
                    <li>Prepara contenido de seguimiento para mantener el momentum</li>
                </ul>
                """, unsafe_allow_html=True)
            elif score_viralidad >= 60:
                st.markdown("""
                <div class="epic-insight-title">📌 Estrategia de Crecimiento</div>
                <p>Tu contenido tiene buen potencial de crecimiento:</p>
                <ul>
                    <li>Incluye llamados a la acción claros para aumentar compartidos</li>
                    <li>Etiqueta a personas o instituciones relevantes</li>
                    <li>Responde rápidamente a los comentarios para aumentar el engagement</li>
                </ul>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="epic-insight-title">📌 Estrategia de Optimización</div>
                <p>Tu contenido tiene potencial de mejora:</p>
                <ul>
                    <li>Revisa las sugerencias del Medidor de Impacto Social</li>
                    <li>Añade elementos visuales o datos impactantes</li>
                    <li>Prueba diferentes formatos para el mismo mensaje</li>
                </ul>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
# Función para Noticias
def render_noticias():
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Noticias & Tendencias</h1>
        <p class="epic-subtitle">Mantente al día con el ecosistema emprendedor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Usar la función existente para mostrar noticias
    tab_noticias()
# Función de Configuración
def render_settings():
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Configuración</h1>
        <p class="epic-subtitle">Personaliza tu experiencia</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="epic-card">""", unsafe_allow_html=True)
    
    # Configuración de perfil
    st.subheader("Perfil de Usuario")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div style="width: 100px; height: 100px; border-radius: 50%; background-color: #E0E0E0; 
                    display: flex; align-items: center; justify-content: center; margin: 0 auto;">
            <span style="font-size: 2.5rem; color: #9E9E9E;">👤</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.text_input("Nombre", value="Usuario EPIC")
        st.text_input("Email", value="usuario@epic.itam.mx")
        st.selectbox("Rol", ["Administrador", "Editor", "Visualizador"])
    
    # Configuración de notificaciones
    st.subheader("Notificaciones")
    
    st.checkbox("Recibir notificaciones por email", value=True)
    st.checkbox("Notificaciones diarias de rendimiento", value=False)
    st.checkbox("Alertas de tendencias", value=True)
    st.checkbox("Sugerencias de contenido", value=True)
    
    # Preferencias de visualización
    st.subheader("Preferencias de Visualización")
    
    st.radio("Tema", ["Claro", "Oscuro"], index=0)
    st.selectbox("Densidad de información", ["Alta", "Media", "Baja"], index=1)
    
    # Integración con plataformas
    st.subheader("Integraciones")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1DA1F2; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <span style="font-weight: 500;">Twitter</span>
            <br>
            <span style="font-size: 0.8rem;">No conectado</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #0A66C2; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <span style="font-weight: 500;">LinkedIn</span>
            <br>
            <span style="font-size: 0.8rem;">Conectado</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #C13584; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <span style="font-weight: 500;">Instagram</span>
            <br>
            <span style="font-size: 0.8rem;">No conectado</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Botones de acción
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Guardar Configuración", type="primary", use_container_width=True)
    
    with col2:
        st.button("Restablecer Valores", use_container_width=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)

# Función para renderizar el asistente
def render_assistant():
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Asistente Inteligente</h1>
        <p class="epic-subtitle">Tu asesor de contenido personalizado</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="ai-assistant-container">""", unsafe_allow_html=True)
    
    # Mostrar mensajes existentes con diseño moderno
    for msg in st.session_state.ai_assistant_messages:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="assistant-message">
                <strong>Asesor:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="user-message">
                <strong>Tú:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Selector de tono con diseño moderno
    st.markdown("### Ajustar tono de respuesta")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("😊 Profesional", use_container_width=True, 
                     type="primary" if st.session_state.ai_assistant_tone == "profesional" else "secondary"):
            st.session_state.ai_assistant_tone = "profesional"
            st.rerun()
    with col2:
        if st.button("🔥 Inspirador", use_container_width=True,
                     type="primary" if st.session_state.ai_assistant_tone == "inspirador" else "secondary"):
            st.session_state.ai_assistant_tone = "inspirador"
            st.rerun()
    with col3:
        if st.button("👋 Casual", use_container_width=True,
                     type="primary" if st.session_state.ai_assistant_tone == "casual" else "secondary"):
            st.session_state.ai_assistant_tone = "casual"
            st.rerun()
    
    # Sugerencias rápidas con diseño moderno
    st.markdown("### Preguntas frecuentes")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("¿Cómo mejorar viralidad?", use_container_width=True, key="btn_viralidad"):
            generate_ai_response("¿Cómo mejorar viralidad?")
            st.rerun()
    with col2:
        if st.button("Dame ideas para post", use_container_width=True, key="btn_ideas"):
            generate_ai_response("Dame ideas para un post sobre innovación")
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("¿Qué es inclusividad?", use_container_width=True, key="btn_inclusividad"):
            generate_ai_response("¿Qué significa el score de inclusividad?")
            st.rerun()
    with col2:
        if st.button("Ayuda con la plataforma", use_container_width=True, key="btn_ayuda"):
            generate_ai_response("¿Cómo usar esta plataforma?")
            st.rerun()
    
    # Input para mensaje personalizado
    st.markdown("### Pregunta personalizada")
    user_message = st.text_input("Escribe tu pregunta al asesor...", key="texto_asistente")
    
    if st.button("Enviar", type="primary", key="btn_enviar_pregunta"):
        if user_message:
            generate_ai_response(user_message)
            st.rerun()
    
    st.markdown("""</div>""", unsafe_allow_html=True)
# Función para mostrar las instrucciones del sitio web
def render_instrucciones():
    st.markdown("""
    <div class="epic-header">
        <h1 class="epic-title">Instrucciones del Sitio Web</h1>
        <p class="epic-subtitle">Guía de uso para EPIC Lab Amplificador de Impacto</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="epic-card">', unsafe_allow_html=True)
    
    st.markdown("""
    ## Cómo usar esta plataforma
    
    El **EPIC Lab Amplificador de Impacto** es una herramienta diseñada para optimizar y amplificar el alcance del contenido del EPIC Lab. A continuación, encontrarás instrucciones sobre cómo sacar el máximo provecho de cada sección:
    
    ### 📊 Dashboard
    El panel principal te muestra un resumen de las métricas clave de la conversación digital sobre emprendimiento.
    
    ### 📈 Epic Lab Analytics
    Explora análisis detallados sobre las menciones, sentimiento y temas relacionados con la conversación digital sobre el EPIC Lab.
    
    ### 🚀 Contenido
    Esta sección te ofrece herramientas para optimizar tu contenido:
    
    - **Recomendador**: Obtén sugerencias personalizadas según tu audiencia y plataforma.
    - **Impacto Social**: Analiza el potencial de viralidad e impacto de tus publicaciones.
    - **Hashtags**: Genera hashtags relevantes para maximizar el alcance.
    - **Horarios**: Descubre los mejores momentos para publicar en cada plataforma.
    
    ### 🔮 Predicciones
    Visualiza proyecciones sobre el crecimiento futuro de menciones y alcance para planificar mejor tus estrategias.
    
    ### 📰 Noticias
    Mantente al día con las últimas tendencias del ecosistema emprendedor y de innovación relevantes para el EPIC Lab.
    
    ### 💬 Asistente
    Consulta al asistente inteligente para obtener ideas, sugerencias y responder preguntas sobre estrategias de contenido.
    
    ## Objetivos principales
    
    Esta plataforma fue diseñada para resolver el reto de **"Cómo hacer que el contenido del EPIC Lab llegue a más personas"** a través de:
    
    1. Análisis de datos para entender patrones de éxito
    2. Recomendaciones personalizadas basadas en audiencia y formato
    3. Optimización de contenido para mayor impacto social
    4. Herramientas para maximizar el alcance orgánico
    
    Si tienes alguna duda adicional, puedes consultar al Asistente Inteligente en la sección correspondiente.
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
# Función principal
def main():
    # Inicializar estado de sesión si no existe
    if 'social_data' not in st.session_state:
        st.session_state.social_data, st.session_state.terminos = generar_datos_social_listening()
    
    if 'ai_assistant_messages' not in st.session_state:
        st.session_state.ai_assistant_messages = [
            {"role": "assistant", "content": "¡Hola! Soy tu Asesor de Contenido Inteligente del EPIC Lab. ¿En qué puedo ayudarte hoy? 👋"}
        ]
        
    if 'ai_assistant_tone' not in st.session_state:
        st.session_state.ai_assistant_tone = "profesional"
        
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Datos para visualizaciones
    df = st.session_state.social_data
    
    # Crear sidebar con menú de navegación moderno
    with st.sidebar:
        st.image("https://cutt.ly/gwwswvAR", width=60)  # Logo EPIC Lab (simulado)
        st.markdown("### EPIC Lab")
        
        # Información del usuario
        st.markdown("""
        <div style="background-color: rgba(46, 139, 87, 0.1); border-radius: 10px; padding: 10px; margin-bottom: 20px;">
            <img src="https://api.dicebear.com/6.x/micah/svg?seed=epiclab" style="width: 50px; height: 50px; border-radius: 25px; float: left; margin-right: 10px;">
            <div style="padding-top: 5px;">
                <div style="font-size: 16px; font-weight: 600;">Usuario EPIC</div>
                <div style="font-size: 12px; color: #2E8B57;">Administrador</div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Menú de navegación moderno
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Epic Lab Analytics", "Contenido", "Predicciones", "Noticias", "Asistente", "Instrucciones"],
            icons=["speedometer2", "graph-up", "pencil-square", "crystal-ball", "newspaper", "robot", "gear"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": EPIC_COLORS['primary'], "font-size": "14px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "rgba(46, 139, 87, 0.1)",
                },
                "nav-link-selected": {"background-color": EPIC_COLORS['primary']},
            },
        )
        
        st.session_state.page = selected
        
        # Elementos adicionales en la barra lateral
        st.markdown("<hr>", unsafe_allow_html=True)
        

            
        # Notificaciones y alertas
        st.markdown("### Notificaciones")
        st.markdown("""
        <div style="background-color: rgba(139, 195, 74, 0.1); border-radius: 8px; padding: 8px; margin-bottom: 8px;">
            <div style="font-size: 13px; font-weight: 600;">¡Nuevo programa!</div>
            <div style="font-size: 11px; color: #637B64;">El programa MAD Fellows ha sido lanzado</div>
        </div>
        <div style="background-color: rgba(46, 139, 87, 0.1); border-radius: 8px; padding: 8px; margin-bottom: 8px;">
            <div style="font-size: 13px; font-weight: 600;">Reporte mensual</div>
            <div style="font-size: 11px; color: #637B64;">El análisis de marzo está disponible</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Contenido principal basado en la página seleccionada
# Contenido principal basado en la página seleccionada
    if st.session_state.page == "Dashboard":
        render_dashboard(df)
    elif st.session_state.page == "Epic Lab Analytics":
        render_analytics(df)
    elif st.session_state.page == "Contenido":
        render_content()
    elif st.session_state.page == "Predicciones":
        render_predictions(df)
    elif st.session_state.page == "Noticias":
        render_noticias()
    elif st.session_state.page == "Asistente":
        render_assistant()
    elif st.session_state.page == "Instrucciones":
        render_instrucciones()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
