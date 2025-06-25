import os
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"sql", "dump", "backup"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Veritabanı bilgileri
db_host = "localhost"
db_port = "5432"
db_name = "AvrupaSarjDb"
db_user = "postgres"
db_password = "avrupasarj"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_file_type(filepath):
    # Dosya türünü belirlemek için "file" komutunu kullan
    result = subprocess.run(["file", filepath], capture_output=True, text=True)
    if "PostgreSQL custom database dump" in result.stdout:
        return "custom"
    return "sql"

def run_sql_import(filepath):
    os.environ['PGPASSWORD'] = db_password

    file_type = detect_file_type(filepath)

    if file_type == "custom":
        command = [
            "pg_restore",
            "-h", db_host,
            "-p", db_port,
            "-U", db_user,
            "-d", db_name,
            "--verbose",
            filepath
        ]
    else:
        command = [
            "psql",
            "-h", db_host,
            "-p", db_port,
            "-U", db_user,
            "-d", db_name,
            "-f", filepath
        ]

    try:
        subprocess.run(command, check=True)
        return True, f"✅ {file_type.upper()} formatındaki SQL başarıyla yüklendi."
    except subprocess.CalledProcessError as e:
        return False, f"❌ Yükleme hatası:\n{e}"

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "Dosya bulunamadı.", 400
        file = request.files["file"]
        if file.filename == "":
            return "Dosya seçilmedi.", 400
        if file and allowed_file(file.filename):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            success, message = run_sql_import(filepath)
            return render_template_string(PAGE_TEMPLATE, message=message)
        else:
            return "Sadece .sql, .dump, .backup dosyaları yüklenebilir.", 400

    return render_template_string(PAGE_TEMPLATE, message=None)

PAGE_TEMPLATE = """
<!doctype html>
<title>SQL Yükleyici</title>
<h2>SQL Dosyası Yükle (.sql, .dump)</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=file accept=".sql,.dump,.backup">
  <input type=submit value=Yükle>
</form>
{% if message %}
    <p><strong>{{ message }}</strong></p>
{% endif %}
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
