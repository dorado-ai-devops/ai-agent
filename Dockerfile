FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instalación de dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        openssh-client \
        git \
    && rm -rf /var/lib/apt/lists/*

# Instalación de dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia del código fuente
COPY . .

# Prepara el directorio SSH (no copies claves aquí)
RUN mkdir -p /app/.ssh && chmod 700 /app/.ssh

# Copia y da permisos al entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 6001

# Utiliza el entrypoint para gestionar la clave SSH y arrancar la app
CMD ["/entrypoint.sh"]
