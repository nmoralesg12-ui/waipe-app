import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("waipe.db")

def crear_tablas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS materia_prima (
        fecha TEXT,
        blanco REAL,
        color REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trabajadores (
        nombre TEXT PRIMARY KEY,
        aldea TEXT,
        pendiente REAL,
        tipo TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS empaque (
        tipo TEXT,
        waipe TEXT,
        cantidad REAL
    )
    """)

    con.commit()
    con.close()

# -------------------------
# MATERIA PRIMA
# -------------------------
def limpiar_materia_prima():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM materia_prima")
    con.commit()
    con.close()

def guardar_materia_prima(blanco, color):
    con = conectar()
    cur = con.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")

    cur.execute("INSERT INTO materia_prima VALUES (?, ?, ?)", (fecha, blanco, color))

    con.commit()
    con.close()

def obtener_materia_total():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT blanco, color FROM materia_prima")
    r = cur.fetchone()

    con.close()
    return r if r else (0, 0)

# -------------------------
# TRABAJADORES
# -------------------------
def guardar_trabajador(nombre, aldea, pendiente, tipo):
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO trabajadores VALUES (?, ?, ?, ?)
    ON CONFLICT(nombre) DO UPDATE SET
    pendiente=excluded.pendiente,
    tipo=excluded.tipo
    """, (nombre, aldea, pendiente, tipo))

    con.commit()
    con.close()

def obtener_trabajadores_por_aldea(aldea):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT nombre, pendiente FROM trabajadores WHERE aldea=?", (aldea,))
    datos = cur.fetchall()

    con.close()
    return datos

def obtener_pendiente(nombre):
    if not nombre:
        return 0

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT pendiente FROM trabajadores WHERE nombre=?", (nombre,))
    r = cur.fetchone()

    con.close()
    return r[0] if r else 0

def obtener_tipo(nombre):
    if not nombre:
        return "color"

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT tipo FROM trabajadores WHERE nombre=?", (nombre,))
    r = cur.fetchone()

    con.close()
    return r[0] if r else "color"

def eliminar_trabajador(nombre):
    con = conectar()
    cur = con.cursor()

    cur.execute("DELETE FROM trabajadores WHERE nombre=?", (nombre,))

    con.commit()
    con.close()

# -------------------------
# EMPAQUE
# -------------------------
def guardar_empaque(tipo, waipe, cantidad):
    con = conectar()
    cur = con.cursor()

    cur.execute("INSERT INTO empaque VALUES (?, ?, ?)", (tipo, waipe, cantidad))

    con.commit()
    con.close()

def obtener_empaque(tipo, waipe):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT SUM(cantidad) FROM empaque WHERE tipo=? AND waipe=?", (tipo, waipe))
    r = cur.fetchone()[0]

    con.close()
    return r if r else 0

def reducir_empaque(tipo, waipe, cantidad):
    guardar_empaque(tipo, waipe, -cantidad)

# -------------------------
if __name__ == "__main__":
    crear_tablas()
    print("✅ BASE LISTA")
