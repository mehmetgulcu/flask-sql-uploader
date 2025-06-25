# Flask SQL Uploader

Web tarayıcısı üzerinden `.sql`, `.dump` ve `.backup` uzantılı PostgreSQL yedek dosyalarını yükleyebileceğiniz basit ve pratik bir Flask uygulamasıdır.

## 🚀 Özellikler

- `.sql`, `.dump`, `.backup` uzantılı dosyaları destekler
- Dosyanın türünü otomatik tespit eder (`pg_restore` veya `psql`)
- Flask tabanlı sade bir web arayüzü sunar
- Yerel veya uzak PostgreSQL veritabanlarına veri yüklemeyi kolaylaştırır

## 🎯 Kullanım Senaryosu

Bu uygulama; geliştirici makinelerinden, staging veya test ortamlarına veri aktarımını kolaylaştırmak amacıyla geliştirilmiştir. Özellikle AWS RDS, Azure Database gibi platformlara yüklemeyi hızlandırır.

## 🛠 Kurulum

1. Projeyi klonlayın:

```bash
git clone https://github.com/kullaniciadi/flask-sql-uploader.git
cd flask-sql-uploader
