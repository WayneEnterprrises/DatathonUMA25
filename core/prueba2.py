import json
import re
from .chatbots import generar_info_adicional
from .config import client, client_PEDRO
from pymed import PubMed
import plotly as px
# 📌 Texto de prueba
prompt  = """El paciente Carlos García recibió los siguientes medicamentos como parte de su tratamiento para la cetoacidosis diabética:

1. Insulina regular (0.1 U/kg/h, IV perfusión):
   - Razón: Para reducir la glucemia y suprimir la cetogénesis. La administración intravenosa continua permite un control preciso de la glucemia.

2. Cloruro de potasio (20 mEq, IV c/4h):
   - Razón: Para prevenir y tratar la hipopotasemia que se produce durante el tratamiento con insulina y la corrección de la acidosis.

3. Suero fisiológico (1000 ml, IV rápido):
   - Razón: Para corregir la deshidratación severa y mejorar la perfusión tisular.

4. Bicarbonato de sodio (50 mEq, IV una dosis):
   - Razón: Para corregir la acidosis metabólica grave (pH 7.1). Se utiliza con precaución y solo en casos de acidosis severa.

5. Insulina glargina (20 U, SC nocte):
   - Razón: Como insulina basal de acción prolongada para mantener un control glucémico estable una vez superada la fase aguda.

Estos medicamentos forman parte del protocolo estándar para el manejo de la cetoacidosis diabética, abordando la hiperglucemia, la deshidratación, los desequilibrios electrolíticos y la acidosis metabólica características de esta condición."""

def generate_statistics_data(prompt):
    """
    Usa Claude para generar datos estadísticos con base en la pregunta del usuario.
    """
    
    
    stats_prompt = f"""
     Devuelve una lista de datos numéricos estructurados de la siguiente forma:
    {{ "categorias": ["Categoria1", "Categoria2"], "valores": [10, 20] }}
    Asegúrate de devolver solo un JSON válido sin explicaciones adicionales.
    Extrae la información para rellenar la lista de este texto:
    {prompt}
    
    Asegúrate de devolver solo un JSON válido sin explicaciones adicionales.
    """
    
    try:
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=[{"role": "user", "content": stats_prompt}]
        )
        
        stats_text = response.choices[0].message.content.strip()
        print("Respuesta de Claude para estadísticas:", stats_text)  # Debugging
        
        if not stats_text:
            raise ValueError("Claude no devolvió una respuesta válida para las estadísticas.")
        
        stats_data = json.loads(stats_text)
        return stats_data
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return None
    except Exception as e:
        print(f"Error en la generación de estadísticas: {e}")
        return None


px.plot_statistics(generate_statistics_data(prompt))