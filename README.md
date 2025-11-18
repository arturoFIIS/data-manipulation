# CRM Django Test

Prueba técnica para el puesto de Python Django Developer.

## Descripción

Aplicación Django que modela un CRM con:
- **Users:** 3 representantes de ventas
- **Companies:** 10 compañías
- **Customers:** 1000 clientes distribuidos
- **Interactions:** 500,000 interacciones (llamadas, emails, SMS, etc.)

## Cómo ejecutar
0. Crear entorno y activar
   ```
   python -m venv venv
   ```
   (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)

1. **Instalar dependencias:**
   ```
   pip install -r requirements.txt
   ```

2. **Migrar base de datos:**
   ```
   python manage.py migrate
   ```

3. **Crear superusuario:**
   ```
   python manage.py createsuperuser
   ```
   *(Ingresa usuario y contraseña de al menos 8 caracteres)*

4. **Poblar datos (Fake Data):**
   ```
   python manage.py populate_db
   ```
   Este comando genera 3 usuarios, 10 compañías, 1000 clientes y **500,000 interacciones**.
   *(Tiempo estimado: 30-60 segundos dependiendo del CPU)*

5. **Correr servidor:**
   ```
   python manage.py runserver
   ```
   - Admin: `http://127.0.0.1:8000/admin`
   - Vista CRM: `http://127.0.0.1:8000/`

## Funcionalidades

✅ **Lista de Clientes** con:
- Nombre completo
- Compañía
- Cumpleaños (formato: "February 5")
- Última interacción con tipo y fecha ("1 day ago (Phone)")

✅ **Filtros:**
- Por nombre (búsqueda en tiempo real)
- Por cumpleaños (esta semana, este mes)

✅ **Ordenamiento:**
- Por nombre, empresa, cumpleaños, última interacción

✅ **Paginación:** 25 clientes por página

## Decisiones Técnicas

- **Optimización N+1:** Se utilizó `annotate` con `Subquery` para obtener la última interacción sin consultas adicionales
- **Base de Datos:** Índices en `Interaction(customer, -date)` para acelerar búsquedas y ordenamientos
- **ORM:** `select_related()` en queries para evitar múltiples hits a BD
- **Modelos:** `User` hereda de `AbstractUser` con `related_name` personalizado
- **Frontend:** Django Templates con Bootstrap 5 para interfaz responsiva

## Estructura del Proyecto

```
data-manipulation/
├── crm_project/          # Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # App principal
│   ├── models.py         # Modelos (User, Company, Customer, Interaction)
│   ├── views.py          # Vista CRM
│   ├── admin.py          # Configuración del admin
│   ├── urls.py
│   ├── management/       # Comando populate_db
│   │   └── commands/
│   │       └── populate_db.py
│   └── templates/
│       └── core/
│           └── customer_list.html
├── templates/            # Templates globales
└── manage.py
```

## Credenciales por Defecto (Después de populate_db)

- **Usuarios generados:** `agent_0`, `agent_1`, `agent_2`
- **Contraseña:** `123456`
- **Nota:** Crear superusuario con `createsuperuser` para acceso al admin

## Rendimiento

- **500,000 interacciones** cargadas en ~30-60 segundos
- **Queries optimizadas** sin problema N+1
- **Índices de BD** para búsquedas rápidas
- **Paginación** para mejorar UX con grandes volúmenes de datos