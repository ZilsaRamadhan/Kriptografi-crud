# 🔐 IMPLEMENTASI KRIPTOGRAFI SIMETRIS (STREAM XOR) PADA OPERASI CRUD MYSQL DENGAN FLASK

Proyek ini adalah simulasi aplikasi web yang dibangun menggunakan **Python Flask** yang menerapkan kriptografi simetris **Stream XOR** untuk melindungi data rahasia yang tersimpan di database MySQL.

---

## I. Konsep Kriptografi (Stream XOR)

1.  **Mekanisme Enkripsi/Dekripsi:** Stream XOR bekerja dengan meng-XOR-kan (*Exclusive OR*) Plaintext dengan Kunci Rahasia yang diulang (*cycled*). Operasi yang sama digunakan untuk enkripsi dan dekripsi.
    $$Ciphertext = Plaintext \oplus Key$$

2.  **Penyimpanan Data:** Data terenkripsi disimpan dalam kolom **`VARBINARY(255)`** pada database MySQL, yang merupakan tipe data yang tepat untuk data biner/ciphertext.

---

## II. Implementasi pada Operasi CRUD

Kriptografi diimplementasikan sepenuhnya pada sisi aplikasi (Python/Flask).

| Operasi | Kriptografi | Keterangan |
| :--- | :--- | :--- |
| **CREATE & UPDATE** | Data **dienkripsi** | Data dienkripsi menggunakan `encrypt_data()` sebelum disimpan ke DB. |
| **READ** | Data **didekripsi** | Data terenkripsi diambil dari DB, lalu didekripsi menggunakan `decrypt_data()` sebelum ditampilkan ke web. |
| **DELETE** | N/A | Operasi penghapusan data baris. |

---

## III. Panduan Menjalankan Aplikasi

### A. Persyaratan

1.  **Python 3.x**
2.  **MySQL Server** (Harus berjalan).

### B. Langkah-Langkah

#### 1. Instalasi Dependensi Python

```bash
pip install -r requirements.txt
