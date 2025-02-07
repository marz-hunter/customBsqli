import os
import requests
import time
import concurrent.futures
import random

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
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/133.0.6943.33 Mobile/15E148 Safari/604.1"
    ]

    def __init__(self):
        self.vulnerabilities_found = 0
        self.total_tests = 0
        self.verbose = False  # Default tidak verbose
        self.vulnerable_urls = []  # Menyimpan URL yang rentan

    def get_random_user_agent(self):
        """
        Mengembalikan string user-agent secara acak dari daftar.
        """
        return random.choice(self.USER_AGENTS)

    def perform_request(self, url, payload, cookie):
        """
        Melakukan GET request dengan URL, payload, dan cookie yang diberikan.
        Mengembalikan tuple yang berisi:
            - success (bool): True jika request berhasil, False jika tidak.
            - url_with_payload (str): URL yang telah ditambahkan payload.
            - response_time (float): Waktu yang diperlukan untuk menyelesaikan request.
            - status_code (int): HTTP status code.
            - error_message (str): Pesan error jika terjadi kegagalan.
        """
        url_with_payload = f"{url}{payload}"
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
        """
        Membaca file dan mengembalikan daftar baris yang tidak kosong.
        """
        try:
            with open(path) as file:
                return [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"{Color.RED}Error reading file {path}: {e}{Color.RESET}")
            return []

    def save_vulnerable_urls(self, filename):
        """
        Menyimpan daftar URL yang rentan ke file.
        """
        try:
            with open(filename, 'w') as file:
                for url in self.vulnerable_urls:
                    file.write(f"{url}\n")
            print(f"{Color.GREEN}Vulnerable URLs saved to {filename}{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}Error saving vulnerable URLs to file: {e}{Color.RESET}")

    def main(self):
        print(Color.CYAN + r"""
    _____               __ __
    |   __ \.-----.-----.|  |__
    |   __ <|__ --|  _  ||  |  |
    |______/|_____|__   ||__|__|
                    |__|
    
    made by Coffinxp & hexsh1dow
    YOUTUBE: Lostsec
        """ + Color.RESET)

        # Mode verbose
        verbose_input = input(Color.PURPLE + "Enable verbose mode? (y/n): " + Color.RESET).strip().lower()
        if verbose_input in ['y', 'yes']:
            self.verbose = True

        # Input URL atau file daftar URL
        input_url_or_file = input(Color.PURPLE + "Enter the URL or path to the URL list file: " + Color.RESET).strip()
        if not input_url_or_file:
            print(f"{Color.RED}No URL or URL list file provided.{Color.RESET}")
            return

        urls = [input_url_or_file] if not os.path.isfile(input_url_or_file) else self.read_file(input_url_or_file)
        if not urls:
            print(f"{Color.RED}No valid URLs provided.{Color.RESET}")
            return

        # Input file payload
        payload_path = input(Color.CYAN + "Enter the full path to the payload file (e.g., payloads/xor.txt): " + Color.RESET).strip()
        payloads = self.read_file(payload_path)
        if not payloads:
            print(f"{Color.RED}No valid payloads found in file: {payload_path}{Color.RESET}")
            return

        # Input cookie
        cookie = input(Color.CYAN + "Enter the cookie to include in the GET request (leave empty if none): " + Color.RESET).strip()

        # Input jumlah thread
        threads_input = input(Color.CYAN + "Enter the number of concurrent threads (0-10, leave empty for default 0): " + Color.RESET).strip()
        try:
            threads = int(threads_input) if threads_input else 0
            if threads < 0 or threads > 10:
                raise ValueError("Number of threads must be between 0 and 10.")
        except ValueError as e:
            print(f"{Color.RED}Invalid number of threads: {e}{Color.RESET}")
            return

        print(f"\n{Color.PURPLE}Starting scan...{Color.RESET}")

        try:
            if threads == 0:
                for url in urls:
                    for payload in payloads:
                        self.total_tests += 1
                        success, url_with_payload, response_time, status_code, error_message = self.perform_request(url, payload, cookie)
                        # Ubah threshold deteksi delay menjadi 30 detik
                        if success and status_code and response_time >= 30:
                            self.vulnerabilities_found += 1
                            self.vulnerable_urls.append(url_with_payload)
                            if self.verbose:
                                print(f"{Color.GREEN}✓ SQLi Found! URL: {url_with_payload} - Response Time: {response_time:.2f} seconds - Status Code: {status_code}{Color.RESET}")
                            else:
                                print(f"{Color.GREEN}✓ Vulnerable URL: {url_with_payload}{Color.RESET}")
                        else:
                            if self.verbose:
                                print(f"{Color.RED}✗ Not Vulnerable: {url_with_payload} - Response Time: {response_time:.2f} seconds - Status Code: {status_code}{Color.RESET}")
            else:
                with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = [executor.submit(self.perform_request, url, payload, cookie) for url in urls for payload in payloads]
                    for future in concurrent.futures.as_completed(futures):
                        self.total_tests += 1
                        success, url_with_payload, response_time, status_code, error_message = future.result()
                        # Ubah threshold deteksi delay menjadi 30 detik
                        if success and status_code and response_time >= 30:
                            self.vulnerabilities_found += 1
                            self.vulnerable_urls.append(url_with_payload)
                            if self.verbose:
                                print(f"{Color.GREEN}✓ SQLi Found! URL: {url_with_payload} - Response Time: {response_time:.2f} seconds - Status Code: {status_code}{Color.RESET}")
                            else:
                                print(f"{Color.GREEN}✓ Vulnerable URL: {url_with_payload}{Color.RESET}")
                        else:
                            if self.verbose:
                                print(f"{Color.RED}✗ Not Vulnerable: {url_with_payload} - Response Time: {response_time:.2f} seconds - Status Code: {status_code}{Color.RESET}")
        except KeyboardInterrupt:
            print(f"{Color.YELLOW}Scan interrupted by user.{Color.RESET}")

        print(f"\n{Color.BLUE}Scan Complete.{Color.RESET}")
        print(f"{Color.YELLOW}Total Tests: {self.total_tests}{Color.RESET}")
        print(f"{Color.GREEN}BSQLi Found: {self.vulnerabilities_found}{Color.RESET}")
        if self.vulnerabilities_found > 0:
            print(f"{Color.GREEN}✓ Your scan has found {self.vulnerabilities_found} vulnerabilities!{Color.RESET}")
        else:
            print(f"{Color.RED}✗ No vulnerabilities found. Better luck next time!{Color.RESET}")

        # Menyimpan URL yang rentan ke file jika diinginkan
        save_file = input(Color.PURPLE + "Enter the filename to save the list of vulnerable URLs (leave empty to skip): " + Color.RESET).strip()
        if save_file:
            self.save_vulnerable_urls(save_file)

        print(f"{Color.CYAN}Thank you for using BSQLi tool!{Color.RESET}")

if __name__ == "__main__":
    scanner = BSQLI()
    scanner.main()
