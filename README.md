# BSQLI Scanner Tool

A multi-threaded SQL Injection vulnerability scanner that injects payloads into URL parameters to detect potential vulnerabilities based on response time delays. This tool is written in Python and uses the `requests` library to perform HTTP GET requests.

> **Disclaimer:**  
> This tool is for educational and authorized testing purposes only. **Do not use it on systems without explicit permission.** Unauthorized scanning is illegal and unethical.

## Features

- **Multi-threaded scanning:** Gunakan hingga 10 thread untuk mempercepat proses scanning.
- **Payload Injection:** Menyisipkan payload ke setiap parameter URL untuk menguji kerentanan.
- **Flexible Input:** Mendukung input berupa file, URL tunggal, atau folder yang berisi file dengan URL.
- **Output yang Dapat Disesuaikan:**  
  - Simpan seluruh hasil ke satu file output (menggunakan opsi `-o`/`--output`).  
  - Atau, simpan hasil per domain dengan format `{domain}.vulnsqli.<ekstensi>` (menggunakan opsi `-of`/`--output-folder`).
- **Verbose Mode:** Pilihan mode verbose untuk menampilkan detail tiap permintaan.
- **Custom Cookie:** Opsi untuk menambahkan cookie pada setiap request.

## Requirements

- **Python 3.6+**
- **Dependencies:**  
  Install module [requests](https://pypi.org/project/requests/):

  ```bash
  pip install requests
  ```

## Installation

1. Clone repository ini:

   ```bash
   git clone https://github.com/marz-hunter/bsqli-scanner.git
   cd bsqli-scanner
   ```

2. Pastikan dependencies telah terinstall (lihat bagian Requirements).

## Usage

Jalankan tool dengan memberikan argumen yang diperlukan. Tool ini mendukung:
- Input berupa file (URL per baris) atau folder yang berisi file dengan URL.
- Mode verbose atau non-verbose.
- Pengaturan jumlah thread.
- Output berupa satu file atau per domain.

### Contoh Perintah

- **Scan dari file dan simpan seluruh hasil ke satu file:**

  ```bash
  python3 bsqli_scanner.py -f input_urls.txt -o /root/vuln/vuln_urls.txt
  ```

- **Scan dari folder dan simpan hasil per domain:**

  ```bash
  python3 bsqli_scanner.py -f /path/to/url_folder -of /root/vuln
  ```

- **Scan dengan mode verbose dan 5 thread:**

  ```bash
  python3 bsqli_scanner.py -f input_urls.txt -mode V -threads 5 -o /root/vuln/vuln_urls.txt
  ```

### Selama Eksekusi

1. **Payload File:**  
   Tool akan meminta Anda memasukkan *full path* ke file payload (misal: `payloads/xor.txt`). File ini harus berisi payload yang akan disisipkan ke parameter URL, satu payload per baris.

2. **Cookie (Opsional):**  
   Anda juga dapat memasukkan cookie jika diperlukan untuk request. Jika tidak, biarkan kosong.

## Credits

- **Original Authors:**  
  Konsep dan beberapa bagian kode awal diambil dari karya [Coffinxp](https://github.com/Coffinxp) & [hexsh1dow](https://github.com/hexsh1dow).
  
- **Maintained by:**  
  [marz-hunter](https://github.com/marz-hunter)
