from flask import Flask, render_template, request, redirect, url_for
import itertools
import mysql.connector

app = Flask(__name__)

SECRET_KEY = b"kunci_rahasia_untuk_tugas_kriptografi_123456789" 

def stream_xor_encrypt_decrypt(data_bytes: bytes, key: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data_bytes, itertools.cycle(key)))

def encrypt_data(plaintext: str) -> bytes:
    plaintext_bytes = plaintext.encode('utf-8')
    return stream_xor_encrypt_decrypt(plaintext_bytes, SECRET_KEY)

def decrypt_data(ciphertext_bytes: bytes) -> str:
    decrypted_bytes = stream_xor_encrypt_decrypt(ciphertext_bytes, SECRET_KEY)
    return decrypted_bytes.decode('utf-8')


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'kripto_db'
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None


def get_all_users(view_mode):
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, data_rahasia FROM users")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    users = []
    for uid, uname, cipher in results:
        display_data = ""
        data_style = ""
        

        if view_mode == 'plaintext':
            display_data = decrypt_data(cipher)
            data_style = "plaintext-style" 
        else: 
            display_data = cipher.hex()
            data_style = "ciphertext-style" 

        users.append({
            'id': uid,
            'username': uname,
            'data_display': display_data,
            'data_style': data_style,
            'original_plaintext': decrypt_data(cipher) 
        })
    return users


@app.route('/', methods=['GET', 'POST'])
def index():
    
    view_mode = request.args.get('view', 'plaintext')

    if request.method == 'POST':
        action = request.form.get('action')
        
        username = request.form.get('username')
        rahasia = request.form.get('rahasia')
        user_id = request.form.get('id')

        conn = get_db_connection()
        if not conn:
            return "Koneksi database gagal!", 500
        cursor = conn.cursor()

        try:
            if action == 'create':
                data_terenkripsi = encrypt_data(rahasia)
                sql = "INSERT INTO users (username, data_rahasia) VALUES (%s, %s)"
                cursor.execute(sql, (username, data_terenkripsi))
            
            elif action == 'update':
                data_terenkripsi = encrypt_data(rahasia)
                sql = "UPDATE users SET data_rahasia = %s WHERE id = %s"
                cursor.execute(sql, (data_terenkripsi, user_id))
            
            elif action == 'delete':
                sql = "DELETE FROM users WHERE id = %s"
                cursor.execute(sql, (user_id,))
            
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return f"Error saat operasi {action}: {err}", 500
        finally:
            cursor.close()
            conn.close()
        
       
        return redirect(url_for('index', view=view_mode))

    
    users = get_all_users(view_mode)
    return render_template('index.html', users=users, view_mode=view_mode)


if __name__ == '__main__':
    app.run(debug=True)
