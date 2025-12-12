from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import json

app = Flask(__name__)
# Permitir CORS para que el frontend (Live Server) pueda conectar
CORS(app) 

# -------------------------
# Conexión a MySQL
# -------------------------
def conectar():
    # Asegúrate de que MySQL esté corriendo en XAMPP/WAMP
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",     # Usuario por defecto de XAMPP
            password="",     # Vacío por defecto
            # ¡IMPORTANTE! Nombre de la base de datos de tu proyecto
            database="petconnect_db" 
        )
    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}") 
        return None

# ----------------------------------------------------
# 1. RUTA: /api/data (GET) - Cargar todas las mascotas y usuarios
# ----------------------------------------------------
@app.route("/api/data", methods=["GET"])
def get_all_data():
    conn = conectar()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener la lista de mascotas
        cursor.execute("SELECT * FROM mascotas")
        mascotas = cursor.fetchall()
        
        # Obtener la lista de usuarios (datos de contacto sin contraseña)
        cursor.execute("SELECT id_usuario, nombre, correo, telefono, edad FROM usuarios")
        usuarios = cursor.fetchall()

        # Retornar ambos conjuntos de datos
        return jsonify({
            "mascotas": mascotas,
            "users": usuarios  # El frontend espera 'users'
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error al ejecutar consulta SQL: {err}"}), 500
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------
# 2. RUTA: /api/auth/register (POST) - Registro de nuevo usuario
# ----------------------------------------------------
@app.route("/api/auth/register", methods=["POST"])
def register_user():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    edad = data.get('edad')
    contrasena = data.get('contrasena') # NOTA: En producción, aquí se usaría un hash (bcrypt)

    if not all([nombre, correo, contrasena]):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    conn = conectar()
    if conn is None:
        return jsonify({"message": "Error de servidor al conectar a DB"}), 500
    
    cursor = conn.cursor()
    
    try:
        # Verificar si el correo ya existe
        cursor.execute("SELECT correo FROM usuarios WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return jsonify({"message": "El correo ya está registrado."}), 409 # Conflict

        # Insertar nuevo usuario
        sql = """
            INSERT INTO usuarios (nombre, correo, telefono, edad, contrasena)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, correo, telefono, edad, contrasena)
        cursor.execute(sql, valores)
        conn.commit()
        
        # Devolver el usuario recién creado (sin contraseña)
        new_user_id = cursor.lastrowid
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": {
                "id_usuario": new_user_id,
                "nombre": nombre,
                "correo": correo,
                "telefono": telefono,
                "edad": edad
            }
        }), 201

    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"message": f"Error SQL al registrar: {err}"}), 500
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------
# 3. RUTA: /api/auth/login (POST) - Inicio de sesión
# ----------------------------------------------------
@app.route("/api/auth/login", methods=["POST"])
def login_user():
    data = request.get_json()
    correo = data.get('correo')
    password_input = data.get('contrasena')
    
    conn = conectar()
    if conn is None:
        return jsonify({"message": "Error de servidor al conectar a DB"}), 500
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener el usuario por correo
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()

        if user and user['contrasena'] == password_input: # Validación simple (sin hash)
            # Login exitoso. Creamos un objeto sin la contraseña para enviar al frontend
            logged_user = {
                "id_usuario": user['id_usuario'],
                "nombre": user['nombre'],
                "correo": user['correo'],
                "telefono": user['telefono'],
                "edad": user['edad']
            }
            return jsonify({"message": "Login exitoso", "user": logged_user}), 200
        else:
            return jsonify({"message": "Credenciales incorrectas o usuario no encontrado."}), 401 # Unauthorized

    except mysql.connector.Error as err:
        return jsonify({"message": f"Error SQL al loguearse: {err}"}), 500
    finally:
        if conn:
            conn.close()

# ----------------------------------------------------
# 4. RUTA: /api/mascotas/registrar (POST) - Registrar una mascota
# ----------------------------------------------------
@app.route("/api/mascotas/registrar", methods=["POST"])
def register_pet():
    data = request.get_json()
    
    conn = conectar()
    if conn is None:
        return jsonify({"message": "Error de servidor al conectar a DB"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Simulación de URL de foto, ya que no estamos manejando la subida real
    foto_url = data.get('foto', "default_pet.jpg") 

    try:
        sql = """
            INSERT INTO mascotas (id_usuario, nombre, especie, raza, color, tamano, ciudad, estado, descripcion, foto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data.get('id_usuario'),
            data.get('nombre'),
            data.get('especie'),
            data.get('raza'),
            data.get('color'),
            data.get('tamano'),
            data.get('ciudad'),
            data.get('estado'),
            data.get('descripcion'),
            foto_url
        )
        cursor.execute(sql, valores)
        conn.commit()
        
        # Devolver el objeto de la nueva mascota
        new_pet_id = cursor.lastrowid
        cursor.execute("SELECT * FROM mascotas WHERE id_mascota = %s", (new_pet_id,))
        new_pet = cursor.fetchone()

        return jsonify({"message": "Mascota registrada exitosamente", "newPet": new_pet}), 201

    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"message": f"Error SQL al registrar mascota: {err}"}), 500
    finally:
        if conn:
            conn.close()

# Arrancar el servidor
if __name__ == "__main__":
    app.run(debug=True, port=5000)