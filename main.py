import time
import urllib.request

def measure_download_speed(url, file_size_mb):
    start_time = time.time()
    urllib.request.urlretrieve(url, 'test_file')
    end_time = time.time()
    elapsed_time = end_time - start_time
    download_speed_mbps = (file_size_mb * 8) / elapsed_time  # Megabit/s
    return download_speed_mbps


import http.client
import os

def measure_upload_speed(file_path, server_url):
    conn = http.client.HTTPConnection(server_url)
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as file:
        start_time = time.time()
        conn.request("POST", "/upload", body=file, headers={'Content-Type': 'application/octet-stream'})
        response = conn.getresponse()
        end_time = time.time()
    elapsed_time = end_time - start_time
    upload_speed_mbps = (file_size * 8) / elapsed_time / 1_000_000  # Megabit/s
    conn.close()
    return upload_speed_mbps

import platform
import subprocess

def measure_ping(host):
    # İşletim sistemi türünü belirle
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Ping komutunu oluştur
    command = ['ping', param, '4', host]
    
    try:
        # Komutu çalıştır ve çıktıyı al
        output = subprocess.run(command, capture_output=True, text=True)
        output_lines = output.stdout.split('\n')
        
        # Ping sürelerini listeye ekle
        ping_times = []
        for line in output_lines:
            if 'time=' in line:
                time_str = line.split('time=')[1]
                if 'ms' in time_str:
                    time_ms = float(time_str.split('ms')[0])
                else:
                    time_ms = float(time_str)
                ping_times.append(time_ms)
        
        # Ping sürelerinin ortalamasını hesapla
        if ping_times:
            avg_ping = sum(ping_times) / len(ping_times)
            return avg_ping
        else:
            return None
    except Exception as e:
        print(f"Ping komutu çalıştırılırken bir hata oluştu: {e}")
        return None




# download speed call
url = 'http://speedtest.tele2.net/10MB.zip' 
file_size_mb = 10
download_speed = measure_download_speed(url, file_size_mb)
print(f"Download Speed: {download_speed:.2f} Mbit/s")

# upload speed call 
file_path = 'test_file'
server_url = 'example.com'  # Kendi sunucunuzu kullanın
upload_speed = measure_upload_speed(file_path, server_url)
print(f"Upload Speed: {upload_speed:.2f} Mbit/s")

#ping process
host = 'google.com'
ping = measure_ping(host)
if ping is not None:
    print(f"Ping: {ping:.2f} ms")
else:
    print("Ping ölçülemedi.")
