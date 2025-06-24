from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

prompt = """
Eres una IA educativa entrenada para analizar perfiles estudiantiles y generar recomendaciones pedagógicas personalizadas. A continuación, se te proporcionará la información de un alumno. Evalúa su perfil considerando los enfoques de la psicología educativa, incluyendo la teoría de las inteligencias múltiples, la teoría de la autodeterminación, el coeficiente intelectual (CI), y estilos de aprendizaje. Luego, ofrece sugerencias prácticas al docente para mejorar el desempeño y el bienestar emocional del alumno.

Perfil del alumno:
- Nombre: Diego Ramírez
- Edad: 12 años
- Nivel: Primer año de secundaria
- Notas académicas:
  - Matemática: 11/20
  - Comunicación: 13/20
  - Ciencia y Tecnología: 10/20
  - Arte: 17/20
  - Educación Física: 18/20
  - Inglés: 12/20
- Tipo de inteligencia predominante: Corporal-Kinestésica, Musical (según test de Gardner)
- Estilo de aprendizaje: Kinestésico
- CI (según WISC): 95 (inteligencia promedio)
- Observaciones psicológicas:
  - Tiene buena autoestima, pero se distrae fácilmente en clases teóricas.
  - Alta motivación en actividades prácticas y grupales.
  - Muestra frustración ante tareas repetitivas o puramente escritas.

Tareas para ti, IA:
1. Interpreta este perfil combinando todos los factores.
2. Detecta posibles causas de bajo rendimiento en algunas materias.
3. Sugiere mínimo 3 recomendaciones pedagógicas prácticas para el docente (con base científica).
4. Propón una forma de visualización útil para el docente en Power BI, que resuma las áreas fuertes y débiles del alumno.
5. Advierte sobre posibles errores o prejuicios al clasificar al alumno solo por sus notas o CI.

Genera tu respuesta en un lenguaje claro, orientado a docentes.
"""

chat = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=2048,
    temperature=0.7,
)

print(chat.choices[0].message.content)
