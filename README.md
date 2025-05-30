# Sistema de Gestión Walditos

¡Bienvenido al sistema de gestión Walditos! Esta aplicación de escritorio te permite administrar tu inventario, ventas, compras, clientes, proveedores y más, todo a través de una interfaz gráfica intuitiva desarrollada con Tkinter y una robusta base de datos MySQL.

## Contenido del Proyecto

Está organizado en los siguientes módulos principales:

- **categorias.py**: Gestiona las categorías de tus productos.
- **clientes.py**: Administra la información detallada de tus clientes.
- **compras.py**: Registra y lleva un control exhaustivo de todas tus compras de productos.
- **db.py**: El corazón de la conexión con tu base de datos MySQL.
- **detalle_compras.py**: Te permite visualizar en detalle los productos de cada compra.
- **detalle_ventas.py**: Muestra el desglose de cada venta.
- **empleados.py**: Gestiona la información de tus empleados.
- **inventario.py**: Controla el stock actual de tus productos.
- **main.py**: El archivo principal que inicia la aplicación y muestra el menú.
- **productos.py**: Realiza operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en tus productos.
- **proveedores.py**: Administra la información de tus proveedores.
- **unidades.py**: Define y gestiona las unidades de medida para tus productos.
- **ventas.py**: Procesa y registra las ventas de tus productos.
- **walditos.sql**: El script SQL fundamental para crear tu base de datos y todas las tablas.

## Requisitos Indispensables

Antes de empezar, asegúrate de tener instalado lo siguiente:

- **Python 3.x**: Puedes descargarlo directamente desde python.org.
- **MySQL Server**: Necesitas una instancia de MySQL funcionando.

## Configuración y Puesta en Marcha

Sigue estos sencillos pasos para dejar tu proyecto listo para usar:

### 1. Ubica el Proyecto
Asegúrate de tener todos los archivos del proyecto en una carpeta local en tu computadora.

### 2. Configura tu Base de Datos MySQL
Este proyecto depende de una base de datos MySQL para almacenar toda la información. ¡Es un paso crucial!

#### a. Crea la Base de Datos y las Tablas
El archivo `walditos.sql` en la carpeta de tu proyecto contiene todo lo necesario para crear la base de datos walditos y sus tablas.

1. Abre tu terminal o línea de comandos.
2. Navega hasta la carpeta donde tienes los archivos de tu proyecto.
3. Ejecuta el script SQL:
   ```
   mysql -u root -p < walditos.sql
   ```
4. Cuando te lo pida, introduce la contraseña de tu usuario root de MySQL. Esto creará automáticamente la base de datos walditos con todas sus tablas.

#### b. Ajusta la Conexión en db.py
Debes decirle a la aplicación cómo conectarse a tu base de datos MySQL. Edita el archivo `db.py` que se encuentra en la raíz de tu proyecto. Asegúrate de que `user` y `password` coincidan con tus credenciales de MySQL. El `database` debe ser `walditos`.

```python
import mysql.connector

def crear_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',         # ¡IMPORTANTE! Cambia 'root' por tu usuario MySQL
        password='david1234', # ¡IMPORTANTE! Cambia 'david1234' por tu contraseña de MySQL
        database='walditos'
    )
```

### 3. Instala las Dependencias de Python
Tu proyecto necesita algunas librerías de Python para funcionar correctamente:

- **mysql-connector-python**: Es el conector que permite a Python comunicarse con MySQL.
- **reportlab**: Una poderosa librería para generar informes en PDF, usada para tus facturas.

Para instalarlas, abre tu terminal o línea de comandos, asegúrate de estar en la carpeta raíz de tu proyecto (donde están todos los archivos .py) y ejecuta el siguiente comando:

```
pip install mysql-connector-python reportlab
```

**Nota sobre Tkinter**: ¡No te preocupes por tkinter! Es parte de la biblioteca estándar de Python y viene incluida con tu instalación, así que no necesitas instalarla con pip.

## Ejecuta la Aplicación

¡Ya casi estamos! Con la base de datos configurada y las dependencias instaladas, puedes iniciar la aplicación.

Desde la carpeta raíz de tu proyecto en la terminal o línea de comandos, ejecuta:

```
python main.py
```

Esto abrirá la ventana principal de Walditos, lista para que empieces a gestionar tu negocio.
