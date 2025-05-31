
📶 ADB WiFi Aracı

Android cihazınıza kablosuz (WiFi) ADB bağlantısı kurmak hiç bu kadar kolay olmamıştı! Bu basit PyQt6 tabanlı araç ile cihaz IP'sini alabilir, bağlantıyı başlatabilir ve terminalden ADB komutları gönderebilirsiniz.

----------------------------------------
✨ Özellikler

- 📡 Telefon IP'sini otomatik alma
- 🔌 WiFi üzerinden ADB bağlantısı kurma
- ▶ Terminalden ADB komutları çalıştırma
- 🧠 Basit ve modern kullanıcı arayüzü
- 🟢 Bağlantı durumu emojilerle gösterim
- 🪛 Hata yönetimi ve uyarılar

----------------------------------------
🧰 Gereksinimler

- Python 3.8+
- ADB (Android Debug Bridge)
- PyQt6 (otomatik olarak yüklenir)

----------------------------------------
🚀 Kurulum

git clone https://github.com/ebubekirbastama/EBS-ADB-WiFi-baglanti-Araci.git
cd adb-wifi-araci
python adb_wifi_gui.py

Uygulama ilk çalıştığında gerekli kütüphane (PyQt6) otomatik olarak yüklenecektir.

----------------------------------------
🖥️ Kullanım

1. Android cihazınızı USB ile bilgisayara bağlayın.
2. Geliştirici Seçeneklerinden USB Hata Ayıklama (ADB) modunu etkinleştirin.
3. Uygulamayı başlatın.
4. "📡 IP Adresini Al" tuşuna basarak cihaz IP'sini alın.
5. "🔌 Bağlan" tuşuna basarak WiFi üzerinden bağlantı kurun.
6. ADB komutlarını yazın ve çalıştırın.

----------------------------------------
❓ Sık Sorulan Sorular

Cihazım listelenmiyor?
- ADB'nin düzgün kurulu olduğundan emin olun.
- adb devices komutuyla terminalden test edin.
- USB kablosu ile bağlantı kurulduğundan emin olun.

Çoklu cihaz hatası alıyorum?
- Uygulama bu durumda adb disconnect komutunu otomatik çalıştırır.

----------------------------------------
👨‍💻 Geliştirici

Ebubekir Bastama

----------------------------------------
📝 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakınız.
