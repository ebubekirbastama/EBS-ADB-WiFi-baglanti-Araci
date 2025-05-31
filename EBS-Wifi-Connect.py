import sys
import subprocess
import re

# Otomatik kütüphane yükleyici
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

# PyQt6 yüklü değilse yükle
install_and_import("PyQt6")

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QIcon

class AdbWifiConnector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADB WiFi Aracı 📶")
        self.setGeometry(300, 300, 600, 400)
        
        self.layout = QVBoxLayout()
        
        self.connection_emoji = QLabel("🔴 Bağlı değil")
        self.connection_emoji.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.connection_emoji)
        
        self.status_label = QLabel("Durum: Bekleniyor ⏳")
        self.layout.addWidget(self.status_label)
        
        self.ip_label = QLabel("Telefon IP adresi:")
        self.layout.addWidget(self.ip_label)
        
        self.ip_line_edit = QLineEdit()
        self.layout.addWidget(self.ip_line_edit)
        
        self.get_ip_button = QPushButton("📡 IP Adresini Al")
        self.get_ip_button.clicked.connect(self.get_device_ip)
        self.layout.addWidget(self.get_ip_button)
        
        self.connect_button = QPushButton("🔌 Bağlan (WiFi üzerinden)")
        self.connect_button.clicked.connect(self.connect_device)
        self.layout.addWidget(self.connect_button)
        
        self.console_label = QLabel("🔧 ADB Komut Konsolu:")
        self.layout.addWidget(self.console_label)
        
        self.command_input = QLineEdit()
        self.layout.addWidget(self.command_input)
        
        self.run_command_button = QPushButton("▶ Komutu Çalıştır")
        self.run_command_button.clicked.connect(self.run_adb_command)
        self.layout.addWidget(self.run_command_button)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)
        
        self.setLayout(self.layout)
    
    def run_subprocess(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
            return result.stdout.strip(), result.stderr.strip()
        except Exception as e:
            return "", str(e)
    
    def get_device_ip(self):
        self.status_label.setText("Durum: IP adresi alınıyor... 📡")
        self.connection_emoji.setText("🟡 Alınıyor...")
        stdout, stderr = self.run_subprocess("adb shell ip addr show wlan0")
        if stderr:
            self.status_label.setText("Hata: ADB cihazına bağlanılamadı ❌")
            self.connection_emoji.setText("🔴 Bağlı değil")
            QMessageBox.critical(self, "Hata", f"ADB hata mesajı:\n{stderr}")
            return
        
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/\d+', stdout)
        if match:
            ip = match.group(1)
            self.ip_line_edit.setText(ip)
            self.status_label.setText(f"IP adresi bulundu: {ip} ✅")
            self.connection_emoji.setText("🟡 Hazır")
        else:
            self.status_label.setText("Durum: IP adresi bulunamadı ⚠️")
            self.connection_emoji.setText("🔴 Bağlı değil")
            QMessageBox.warning(self, "Uyarı", "Telefon IP adresi alınamadı.")
    
    def connect_device(self):
        ip = self.ip_line_edit.text().strip()
        if not ip:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce IP adresini alınız veya manuel giriniz.")
            return

        self.status_label.setText("TCP/IP moduna geçiliyor... ⏳")
        self.connection_emoji.setText("🟡 Bağlantı deneniyor...")
        stdout, stderr = self.run_subprocess("adb tcpip 5555")

        if "more than one device" in stderr.lower():
            self.status_label.setText("⚠️ Çoklu cihaz algılandı. Tüm bağlantılar kesiliyor...")
            self.connection_emoji.setText("🟡 Sıfırlanıyor...")
            self.output_text.append("⚠️ Uyarı: Aynı anda birden fazla cihaz bağlıydı. 'adb disconnect' çalıştırılıyor...\n")
            subprocess.run("adb disconnect", shell=True)
            stdout, stderr = self.run_subprocess("adb tcpip 5555")

        if stderr and "error" in stderr.lower():
            self.status_label.setText(f"Hata (tcpip): {stderr} ❌")
            self.connection_emoji.setText("🔴 Bağlı değil")
            QMessageBox.critical(self, "Hata", f"tcpip komutu hata verdi:\n{stderr}")
            return

        self.status_label.setText(f"{ip}:5555 bağlantısı deneniyor...")
        self.connection_emoji.setText("🟡 Bağlantı kuruluyor...")
        stdout, stderr = self.run_subprocess(f"adb connect {ip}:5555")

        if "connected to" in stdout.lower():
            self.status_label.setText(f"Bağlandı: {ip}:5555 ✅")
            self.connection_emoji.setText("🟢 Bağlantı başarılı")
            self.output_text.append(f"✅ Bağlantı kuruldu: {ip}:5555\n")
        else:
            self.status_label.setText(f"Bağlantı başarısız ❌")
            self.connection_emoji.setText("🔴 Bağlantı yok")
            QMessageBox.critical(self, "Hata", f"Bağlantı başarısız:\n{stdout}\n{stderr}")
    
    def run_adb_command(self):
        cmd_text = self.command_input.text().strip()
        if not cmd_text:
            QMessageBox.warning(self, "Uyarı", "Çalıştırılacak ADB komutunu giriniz.")
            return

        full_cmd = f"adb.exe {cmd_text}"
        self.status_label.setText(f"Komut çalışıyor: {full_cmd} 🛠️")
        stdout, stderr = self.run_subprocess(full_cmd)

        if stderr:
            self.output_text.append(f"⚠️ Hata: {stderr}\n")
        if stdout:
            self.output_text.append(f"> {full_cmd}\n{stdout}\n")
        else:
            self.output_text.append(f"> {full_cmd}\n(Çıktı yok)\n")

        self.status_label.setText("Komut tamamlandı ✅")

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon.fromTheme("network-wireless"))
    window = AdbWifiConnector()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
