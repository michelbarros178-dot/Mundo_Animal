# 🐾 Mundo Animal - Sistema de Gestión

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-black?style=for-the-badge&logo=render&logoColor=white)

**Mundo Animal** es una aplicación web completa para la gestión de una tienda y veterinaria. Permite administrar clientes, registrar mascotas, controlar el inventario de productos y agendar citas para servicios de baño y peluquería.

🌐 **Aplicación desplegada en vivo:** [https://mundo-animal-ilvs.onrender.com/](https://mundo-animal-ilvs.onrender.com/)

---

## 📋 Características

- **Gestión de Clientes:** Registro, edición y eliminación de clientes.
- **Gestión de Mascotas:** Asociación de mascotas a sus respectivos dueños (clientes).
- **Control de Inventario:** Administración de productos, precios y niveles de stock.
- **Agendamiento de Citas:** Programación de servicios, control de estados (Pendiente, Confirmada, Cancelada).
- **Panel de Administración:** Interfaz de Django Admin personalizada para la gestión interna.

---

## 🏗️ Arquitectura del Proyecto

El proyecto fue refactorizado desde un enfoque de Programación Orientada a Objetos (POO) monolítico hacia el patrón de arquitectura **MVC (Modelo-Vista-Controlador)** adaptado a Django:

- **Modelo (Models):** Clases de base de datos (`Cliente`, `Mascota`, `Producto`, `Cita`).
- **Vista (Templates):** Interfaz de usuario construida con HTML5, CSS3 y Bootstrap 5.
- **Controlador (Views):** Lógica de negocio en Django, manejando peticiones HTTP y validaciones.
- **Base de Datos:** PostgreSQL en producción y SQLite en desarrollo local.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.12, Django 5.0
- **Frontend:** HTML5, Bootstrap 5, Bootstrap Icons, Google Fonts (Inter)
- **Base de Datos:** PostgreSQL (Producción), SQLite (Desarrollo)
- **Servidor Web:** Gunicorn + WhiteNoise (Estáticos)
- **Contenedores:** Docker & Docker Compose
- **Despliegue:** Render (PaaS)


git clone https://github.com/tu-usuario/tu-repositorio.git
cd mundo_animal_web
