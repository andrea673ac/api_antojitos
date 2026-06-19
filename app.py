from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route('/guardar_pedido', methods=['POST'])
def guardar_pedido():
    data = request.json

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO pedidos
        (producto, carne, bebida, ingredientes, cantidad, total)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        data["producto"],
        data["carne"],
        data["bebida"],
        data["ingredientes"],
        data["cantidad"],
        data["total"]
    ))

    db.commit()

    return jsonify({"ok": True})

# 🔗 CONEXIÓN A MYSQL
# 🔗 CONEXIÓN A MYSQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="antojitos",
    autocommit=True
)

def reconectar():
    global db

    try:
        if not db.is_connected():
            db.reconnect(
                attempts=3,
                delay=2
            )
    except:
       import os
import mysql.connector

db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT")),
    autocommit=True
)
# =========================
# 🔐 LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE correo=%s AND password=%s",
        (data['correo'], data['password'])
    )

    user = cursor.fetchone()
    return jsonify(user)

# =========================
# 📝 REGISTRO
# =========================
@app.route('/registro', methods=['POST'])
def registro():
    data = request.json
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO usuarios (correo, password, rol) VALUES (%s,%s,'user')",
        (data['correo'], data['password'])
    )

    db.commit()
    return jsonify({"ok": True})

# =========================
# 🍔 MENÚ USUARIO (solo disponibles)
# =========================

@app.route('/menu', methods=['GET'])
def menu():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE disponible=1")
    return jsonify(cursor.fetchall())

@app.route('/ingredientes_all', methods=['GET'])
def ingredientes_all():

    reconectar()

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ingredientes")

    return jsonify(cursor.fetchall())

@app.route('/carnes', methods=['GET'])
def carnes():

    reconectar()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM carnes WHERE disponible=1"
    )

    return jsonify(cursor.fetchall())

@app.route('/ingredientes', methods=['GET'])
def ingredientes():

    reconectar()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM ingredientes WHERE disponible=1"
    )

    return jsonify(cursor.fetchall())
# =========================
# 👩‍💼 ADMIN (ver TODO)
# =========================
@app.route('/menu_all', methods=['GET'])
def menu_all():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    return jsonify(cursor.fetchall())



@app.route('/carnes_all', methods=['GET'])
def carnes_all():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carnes")
    return jsonify(cursor.fetchall())

# =========================
# 🔁 TOGGLE DISPONIBLE
# =========================
@app.route('/toggle/<tabla>/<int:id>', methods=['PUT'])
def toggle(tabla, id):
    cursor = db.cursor()

    query = f"UPDATE {tabla} SET disponible = NOT disponible WHERE id=%s"
    cursor.execute(query, (id,))
    db.commit()

    return jsonify({"ok": True})

# =========================
# 🚀 INICIO SERVIDOR
# =========================

@app.route('/estadisticas', methods=['GET'])
def estadisticas():

    reconectar()

    cursor = db.cursor(dictionary=True)

    # Dinero total vendido
    cursor.execute("""
        SELECT IFNULL(SUM(total),0) AS total_vendido
        FROM pedidos
    """)
    total = cursor.fetchone()

    # Productos vendidos
    cursor.execute("""
        SELECT IFNULL(SUM(cantidad),0) AS productos_vendidos
        FROM pedidos
    """)
    productos = cursor.fetchone()

    # Producto más vendido
    cursor.execute("""
        SELECT producto,
               SUM(cantidad) AS vendidos
        FROM pedidos
        GROUP BY producto
        ORDER BY vendidos DESC
        LIMIT 1
    """)

    top = cursor.fetchone()

    return jsonify({
        "total_vendido": total["total_vendido"],
        "productos_vendidos": productos["productos_vendidos"],
        "producto_top":
            top["producto"] if top else "Sin ventas",
        "cantidad_top":
            top["vendidos"] if top else 0
    })
@app.route('/bebidas', methods=['GET'])
def bebidas():

    reconectar()

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM bebidas WHERE disponible=1"
    )

    return jsonify(cursor.fetchall())

@app.route('/bebidas_all', methods=['GET'])
def bebidas_all():
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM bebidas"
    )
    return jsonify(cursor.fetchall())
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))

    app.run(
        host='0.0.0.0',
        port=port
    )