# Usar una imagen oficial de Python
FROM python:3.12-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Puerto por defecto de Render (10000)
EXPOSE 10000

# Comando para ejecutar la app (Render se encarga de las migraciones y collectstatic)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "3", "mundo_animal_web.wsgi:application"]