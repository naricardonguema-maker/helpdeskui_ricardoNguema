# DataDesk Helpdesk System

<div align="center">
  
  ![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Tkinter](https://img.shields.io/badge/Tkinter-GUI-008CBA?style=for-the-badge&logo=python&logoColor=white)
  ![JSON](https://img.shields.io/badge/JSON-Persistence-000000?style=for-the-badge&logo=json&logoColor=white)
  ![MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
  ![Status](https://img.shields.io/badge/Status-Production-00C853?style=for-the-badge)
  
  <p align="center">
    <b>Aplicación de escritorio profesional para la gestión de tickets de soporte técnico</b>
  </p>
  
  <p align="center">
    <a href="#-características">Características</a> •
    <a href="#-tecnologías">Tecnologías</a> •
    <a href="#-instalación">Instalación</a> •
    <a href="#-uso">Uso</a> •
    <a href="#-arquitectura">Arquitectura</a> •
    <a href="#-capturas">Capturas</a>
  </p>
</div>

---

## 📋 Descripción del Proyecto

**DataDesk** es una aplicación de escritorio completa y profesional diseñada para la gestión eficiente de tickets de soporte técnico en entornos empresariales. Desarrollada siguiendo el patrón de diseño **Separación de Responsabilidades (SoC)**, esta herramienta ofrece una interfaz gráfica intuitiva y un almacenamiento persistente robusto, superando las limitaciones de los scripts tradicionales por consola.

### 🎯 Objetivo del Proyecto

El objetivo principal de DataDesk es proporcionar a las empresas una herramienta ágil y confiable para gestionar las incidencias internas de sus clientes y empleados, mejorando la productividad y la trazabilidad de los tickets de soporte.

---

## ✨ Características Principales

### 🔧 Gestión de Tickets (CRUD)
- **Crear**: Registro de nuevas incidencias con validación de campos
- **Leer**: Visualización completa de todos los tickets en una tabla interactiva
- **Actualizar**: Cambio de estado de tickets (Pendiente ↔ Resuelto)
- **Eliminar**: Borrado seguro de tickets con confirmación previa

### 🔍 Funcionalidades Avanzadas
- **Filtrado en Tiempo Real**: Búsqueda dinámica que filtra tickets mientras escribes
- **Panel de Métricas**: Estadísticas automáticas de total, pendientes y resueltos
- **Validación de Datos**: Control de campos obligatorios y formato de entrada
- **Persistencia Automática**: Guardado inmediato en archivo JSON

### 🎨 Experiencia de Usuario
- **Interfaz Profesional**: Diseño limpio y organizado con Tkinter/TTK
- **Feedback Visual**: Mensajes informativos para acciones del usuario
- **Código de Colores**: Diferenciación visual entre estados (verde/resuelto, rojo/pendiente)
- **Manejo de Errores**: Mensajes descriptivos para validaciones y errores

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.8+ | Lenguaje de programación principal |
| **Tkinter** | Estándar | Framework de interfaz gráfica |
| **TTK** | Estándar | Widgets modernos para Tkinter |
| **JSON** | Estándar | Formato de almacenamiento persistente |
| **Type Hints** | 3.8+ | Tipado estático para mejor mantenibilidad |
| **POO** | - | Programación Orientada a Objetos |

### 📦 Dependencias
```bash
# DataDesk solo utiliza módulos estándar de Python
# No requiere instalación de dependencias externas