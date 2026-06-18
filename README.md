# Mapas Electorales · Valparaíso

Visualización interactiva del territorio electoral de Valparaíso, cruzando datos del Censo 2024 con resultados de elecciones noviembre 2025.

## 📊 Características

- **210 Unidades Vecinales** con perfil completo
- **50 Áreas Electorales** por local de votación
- **Datos integrados**: Censo 2024 (INE) + Elecciones Nov 2025 (Servel)
- **Mapas interactivos** con Leaflet.js
- **Filtros por capas**: Electoral, Social, Candidatos

## 🗂️ Estructura del Proyecto

```
/workspace
├── index.html                    # Landing page
├── valparaiso_perfil_completo.html   # Mapa UV completo
├── valparaiso_areas_perfil.html      # Mapa áreas electorales
├── css/
│   └── styles.css                # Estilos refactorizados
├── js/
│   └── map.js                    # Lógica del mapa (pendiente)
├── data/
│   ├── censo_2024.json           # Datos censales
│   ├── elecciones_nov2025.json   # Resultados electorales
│   └── datos_completos.json      # Dataset fusionado
├── scripts/
│   └── process_data.py           # Pipeline de procesamiento
└── README.md                     # Este archivo
```

## 🚀 Uso

### Visualizar Mapas

Abre los archivos HTML directamente en tu navegador:

```bash
# Opción 1: Abrir directamente
open index.html

# Opción 2: Servidor local (recomendado)
python -m http.server 8000
# Visita: http://localhost:8000
```

### Procesar Datos

El pipeline convierte datos CSV crudos en JSON optimizado:

```bash
# Generar datos de ejemplo
python scripts/process_data.py --generate-sample

# Procesar datos reales
python scripts/process_data.py \
  --censo data/raw/censo_2024.csv \
  --elecciones data/raw/elecciones_nov2025.csv \
  --output data/
```

## 📁 Formato de Datos

### Censo (`censo_2024.json`)
```json
{
  "28": {
    "uv": 28,
    "nombre": "Cerro Concepción",
    "poblacion": 1250,
    "viviendas": 480,
    "edad_promedio": 42.5
  }
}
```

### Elecciones (`elecciones_nov2025.json`)
```json
{
  "28": {
    "uv": 28,
    "inscritos": 890,
    "votos_totales": 623,
    "participacion": 70.0,
    "d_uxch": 180,
    "d_chgu": 120
  }
}
```

## 🔧 Refactorización Realizada

### CSS Separado
- **Antes**: 170 líneas de CSS inline en cada HTML
- **Ahora**: `css/styles.css` centralizado y reutilizable

### Próximos Pasos de Refactorización
1. Extraer JavaScript a `js/map.js`
2. Crear módulos para:
   - Configuración de capas
   - Renderizado de perfiles
   - Manejo de eventos
3. Implementar sistema de build (opcional)

## 📈 Mejoras Futuras

### Datos
- [ ] Automatizar descarga desde INE/Servel
- [ ] Validación de consistencia de datos
- [ ] Histórico electoral (2021, 2024, 2025)

### Funcionalidades
- [ ] Exportar reportes PDF por UV
- [ ] Comparar períodos electorales
- [ ] Filtrado avanzado por rango de valores
- [ ] Modo presentación

### Performance
- [ ] Lazy loading de geometrías
- [ ] Web Workers para cálculos pesados
- [ ] Tile server propio

## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Mapas**: Leaflet.js 1.9.4
- **Fuentes**: Syne, IBM Plex Mono (Google Fonts)
- **Datos**: JSON, CSV
- **Pipeline**: Python 3 + Pandas

## 📝 Licencia

Proyecto de uso interno · 
---

**Datos**: INE Censo 2024 · Servel Elecciones Nov 2025  
**Geometrías**: Unidades Vecinales Valparaíso  
**Desarrollo**: UNCO · VPO
