#!/usr/bin/env python3
import os
import requests
import time
import concurrent.futures
import random
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class Color:
    BLUE = '\033[94m'
    GREEN = '\033[1;92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class BSQLI:
    # Menambahkan lebih banyak user-agent pada daftar
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.70",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15"
    ]

    def __init__(self):
        self.vulnerabilities_found = 0
        self.total_tests = 0
        self.verbose = False  # Default non-verbose
        self.vulnerable_urls = []  # Menyimpan URL yang rentan

    def get_random_user_agent(self):
        """Mengembalikan user-agent secara acak."""
        return random.choice(self.USER_AGENTS)

    def inject_payload_into_url(self, url, payload):
        """
        Memasukkan payload ke setiap value parameter dalam URL.
        Jika URL memiliki query string, payload akan ditambahkan di setiap value.
        Jika tidak, payload akan ditambahkan sebagai query string.
        """
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            # Tambahkan payload ke setiap value parameter
            for key in params:
                params[key] = [v + payload for v in params[key]]
            new_query = urlencode(params, doseq=True)
            new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, 
                                  parsed.params, new_query, parsed.fragment))
            return new_url
        else:
            # Jika tidak ada query, tambahkan payload sebagai query string
            if '?' in url:
                return url + '&' + payload
            else:
                return url + '?' + payload

    def perform_request(self, url, payload, cookie):
        """
        Melakukan GET request setelah menyisipkan payload ke seluruh parameter.
        Mengembalikan tuple:
          (success, url_with_payload, response_time, status_code, error_message)
        """
        url_with_payload = self.inject_payload_into_url(url, payload)
        start_time = time.time()

        headers = {
            'User-Agent': self.get_random_user_agent()
        }

        try:
            response = requests.get(url_with_payload, headers=headers, cookies={'cookie': cookie} if cookie else None)
            response.raise_for_status()
            response_time = time.time() - start_time
            success = True
            error_message = None
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            success = False
            error_message = str(e)

        return success, url_with_payload, response_time, response.status_code if success else None, error_message

    def read_file(self, path):
        """Membaca file dan mengembalikan daftar baris yang tidak kosong."""
        try:
            with open(path) as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"{Color.RED}Error reading file {path}: {e}{Color.RESET}")
            return []

    def save_vulnerable_urls(self, filename):
        """Menyimpan URL yang rentan ke file."""
        try:
            with open(filename, 'w') as file:
                for url in self.vulnerable_urls:
                    file.write(f"{url}\n")
            print(f"{Color.GREEN}Vulnerable URLs saved to {filename}{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}Error saving vulnerable URLs to file: {e}{Color.RESET}")

    def main(self):
        # Parsing argumen command-line
        parser = argparse.ArgumentParser(description="BSQLi Scanner Tool")
        parser.add_argument("-f", "--file", required=True,
                            help="Input file dengan URL (satu per baris), satu URL, atau folder yang berisi file")
        parser.add_argument("-mode", "--mode", choices=["V", "N", "v", "n"], default="N",
                            help="Mode verbose: V untuk verbose, N untuk non-verbose")
        parser.add_argument("-threads", "--threads", type=int, default=0,
                            help="Jumlah thread (0-10)")
        parser.add_argument("-o", "--output",
                            help="Nama file output atau folder untuk menyimpan URL yang rentan (opsional)")
        args = parser.parse_args()

        # Tampilan banner
        print(Color.CYAN + r"""
    _____               __ __
    |   __ \.-----.-----.|  |__
    |   __ <|__ --|  _  ||  |  |
    |______/|_____|__   ||__|__|
                    |__|
    
    made by Coffinxp & hexsh1dow
    YOUTUBE: Lostsec
        """ + Color.RESET)

        # Set mode verbose
        self.verbose = args.mode.upper() == "V"

        # Ambil URL dari file, URL langsung, atau folder
        if os.path.isdir(args.file):
            urls = []
            for filename in os.listdir(args.file):
                full_path = os.path.join(args.file, filename)
                if os.path.isfile(full_path):
                    urls.extend(self.read_file(full_path))
        elif os.path.isfile(args.file):
            urls = self.read_file(args.file)
        else:
            urls = [args.file]
        if not urls:
            print(f"{Color.RED}No valid URLs provided.{Color.RESET}")
            return

        # Input file payload (dibiarkan interaktif karena tidak didefinisikan di argumen)
        payload_path = input(Color.CYAN + "Enter the full path to the payload file (e.g., payloads/xor.txt): " + Color.RESET).strip()
        payloads = self.read_file(payload_path)
        if not payloads:
            print(f"{Color.RED}No valid payloads found in file: {payload_path}{Color.RESET}")
            return

        # Cookie (jika diperlukan)
        cookie = input(Color.CYAN + "Enter the cookie to include in the GET request (leave empty if none): " + Color.RESET).strip()

        threads = args.threads
        if threads < 0 or threads > 10:
            print(f"{Color.RED}Invalid number of threads. Must be between 0 and 10.{Color.RESET}")
            return

        print(f"\n{Color.PURPLE}Starting scan...{Color.RESET}")

        try:
            if threads == 0:
                for url in urls:
                    for payload in payloads:
                        self.total_tests += 1
                        success, url_with_payload, response_time, status_code, error_message = self.perform_request(url, payload, cookie)
                        # Deteksi delay lebih dari atau sama dengan 30 detik
                        if success and status_code and response_time >= 10:
                            self.vulnerabilities_found += 1
                            self.vulnerable_urls.append(url_with_payload)
                            if self.verbose:
                                print(f"{Color.GREEN}✓ SQLi Found! URL: {url_with_payload} - Response Time: {response_time:.2f}s - Status Code: {status_code}{Color.RESET}")
                            else:
                                print(f"{Color.GREEN}✓ Vulnerable URL: {url_with_payload}{Color.RESET}")
                        else:
                            if self.verbose:
                                print(f"{Color.RED}✗ Not Vulnerable: {url_with_payload} - Response Time: {response_time:.2f}s - Status Code: {status_code}{Color.RESET}")
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = [executor.submit(self.perform_request, url, payload, cookie) for url in urls for payload in payloads]
                    for future in concurrent.futures.as_completed(futures):
                        self.total_tests += 1
                        success, url_with_payload, response_time, status_code, error_message = future.result()
                        if success and status_code and response_time >= 10:
                            self.vulnerabilities_found += 1
                            self.vulnerable_urls.append(url_with_payload)
                            if self.verbose:
                                print(f"{Color.GREEN}✓ SQLi Found! URL: {url_with_payload} - Response Time: {response_time:.2f}s - Status Code: {status_code}{Color.RESET}")
                            else:
                                print(f"{Color.GREEN}✓ Vulnerable URL: {url_with_payload}{Color.RESET}")
                        else:
                            if self.verbose:
                                print(f"{Color.RED}✗ Not Vulnerable: {url_with_payload} - Response Time: {response_time:.2f}s - Status Code: {status_code}{Color.RESET}")
        except KeyboardInterrupt:
            print(f"{Color.YELLOW}Scan interrupted by user.{Color.RESET}")

        print(f"\n{Color.BLUE}Scan Complete.{Color.RESET}")
        print(f"{Color.YELLOW}Total Tests: {self.total_tests}{Color.RESET}")
        print(f"{Color.GREEN}BSQLi Found: {self.vulnerabilities_found}{Color.RESET}")
        if self.vulnerabilities_found > 0:
            print(f"{Color.GREEN}✓ Your scan has found {self.vulnerabilities_found} vulnerabilities!{Color.RESET}")
        else:
            print(f"{Color.RED}✗ No vulnerabilities found. Better luck next time!{Color.RESET}")

        # Simpan URL yang rentan jika argumen output disediakan.
        if args.output:
            output_path = args.output
            # Jika output adalah folder, simpan ke file 'vulnerable_urls.txt' di folder tersebut.
            if os.path.isdir(args.output):
                output_path = os.path.join(args.output, "vulnerable_urls.txt")
            self.save_vulnerable_urls(output_path)

        print(f"{Color.CYAN}Thank you for using BSQLi tool!{Color.RESET}")

if __name__ == "__main__":
    scanner = BSQLI()
    scanner.main()
