# EEL CIBERSEGURIDAD

# Laboratorio SQL Injection desde cero

Laboratorio educativo para comprender de forma práctica cómo se produce una vulnerabilidad **SQL Injection**, qué ocurre cuando una aplicación incorpora de manera insegura datos controlados por el usuario dentro de una consulta SQL y cómo corregirla mediante consultas parametrizadas.

La aplicación utiliza **Python, Flask y SQLite** y escucha únicamente en `127.0.0.1:5000`.

> ⚠️ **ADVERTENCIA**  
> Proyecto creado exclusivamente con fines educativos y de capacitación en ciberseguridad. Utilizar únicamente en sistemas propios, laboratorios controlados o entornos expresamente autorizados. Los datos son ficticios. No exponer esta aplicación a Internet.

## Que es la SQLI?

SQLi (SQL Injection) es una vulnerabilidad que permite alterar una consulta a una base de datos mediante datos introducidos por el usuario, pudiendo provocar acceso no autorizado a información o manipulación de datos.

## Objetivo

Recorrido del laboratorio:

`Aplicación → consulta normal → detección → alteración lógica → UNION → estructura de la base → corrección`

Se estudiará:

- funcionamiento normal de una consulta SQL;
- detección de una posible SQL Injection;
- alteración de condiciones SQL;
- acceso a otros registros ficticios;
- uso educativo de `UNION SELECT`;
- identificación de SQLite;
- enumeración de tablas y estructura;
- causa de la vulnerabilidad;
- corrección mediante consultas parametrizadas.

## 1. Requisitos

Comprobar Python:

```bash
python3 --version
```

En Kali Linux instalar Flask:

```bash
sudo apt update
sudo apt install python3-flask -y
```

También puede utilizarse:

```bash
python3 -m pip install -r requirements.txt
```

## 2. Descargar el laboratorio

```bash
git clone https://github.com/eelciberseguridad/Lab-SQLInject.git
cd Lab-SQLInject
```

## 3. Ejecutar

```bash
python3 app.py
```

Abrir:

```text
http://127.0.0.1:5000
```

La base `laboratorio.db` se crea automáticamente con tres usuarios ficticios.

## 4. Funcionamiento normal

Introducir:

```text
1
```

La aplicación devuelve a Ana y muestra la consulta ejecutada:

```sql
SELECT id, nombre, email, rol FROM usuarios WHERE id = '1'
```

Probar también `2` y `3`.

## 5. Dónde está la vulnerabilidad

La versión de laboratorio concatena directamente la entrada del usuario:

```python
consulta = (
    "SELECT id, nombre, email, rol "
    "FROM usuarios WHERE id = '" + user_id + "'"
)
```

Esto mezcla datos controlados por el usuario con la estructura SQL.

## 6. Detectar SQL Injection

Introducir solamente:

```text
'
```

La entrada altera la sintaxis de la consulta y puede provocar un error SQL. Esto constituye un indicio de inyección.

## 7. Alterar la condición

Introducir:

```text
1' OR '1'='1
```

La consulta pasa a contener una condición siempre verdadera y puede devolver los tres usuarios ficticios.

## 8. Verdadero contra falso

Condición verdadera:

```text
1' AND '1'='1
```

Condición falsa:

```text
1' AND '1'='2
```

Comparar las respuestas permite observar que la entrada controla parte de la lógica evaluada por SQL.

## 9. UNION SELECT

Introducir:

```text
1' UNION SELECT 99,'PRUEBA','SQL INJECTION','CONTROLADO' -- 
```

El resultado puede incluir un registro construido por la segunda consulta, demostrando que `UNION` permite combinar resultados compatibles.

## 10. Identificar SQLite

```text
1' UNION SELECT 99,sqlite_version(),'Motor SQLite','LAB' -- 
```

La respuesta mostrará la versión del motor SQLite del laboratorio.

## 11. Enumerar tablas

```text
1' UNION SELECT 99,name,type,'TABLA' FROM sqlite_master WHERE type='table' -- 
```

Entre los resultados aparecerá la tabla `usuarios`.

## 12. Observar la estructura

```text
1' UNION SELECT 99,name,sql,'ESTRUCTURA' FROM sqlite_master WHERE name='usuarios' -- 
```

Esto permite visualizar la definición de la tabla ficticia y sus columnas.

## 13. Corregir la vulnerabilidad

Detener Flask con `Ctrl+C` y editar `app.py`.

Reemplazar la construcción vulnerable por una consulta parametrizada:

```python
consulta = """
SELECT id, nombre, email, rol
FROM usuarios
WHERE id = ?
"""

cursor.execute(consulta, (user_id,))
```

La diferencia fundamental es que la estructura SQL y el valor proporcionado por el usuario pasan a tratarse separadamente.

## 14. Repetir las pruebas

Ejecutar nuevamente:

```bash
python3 app.py
```

Comprobar que `1` continúa funcionando y repetir las entradas de inyección anteriores. Una vez parametrizada correctamente la consulta, esas cadenas deben tratarse como datos y no como sintaxis SQL.

## Lección final

SQL Injection no es simplemente escribir `' OR '1'='1`. Esa cadena es una demostración del problema. La vulnerabilidad aparece cuando una aplicación permite que **datos controlados por el usuario sean interpretados como parte de una instrucción SQL**.

La defensa fundamental consiste en mantener separados los datos y el código SQL mediante consultas parametrizadas, complementadas con mínimo privilegio, controles de acceso y manejo seguro de errores.

## Autor

**EEL CIBERSEGURIDAD**  
GitHub: `eelciberseguridad`
