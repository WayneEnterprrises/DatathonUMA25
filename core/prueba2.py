import json
import re
from .chatbots import generar_info_adicional, enriquecer_respuesta_con_pubmed
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

enlaces = generar_info_adicional(prompt)

print(enriquecer_respuesta_con_pubmed(prompt, enlaces))