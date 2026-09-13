# MikasRevs Phone — repo

Minecraft **Forge 1.20.1** telefon modu (`mikasrevs_phone`, sürüm **1.3.3**).
Telefon, mesajlar, sosyal medya (Gram / Mattu), GPS, banka, pazar yeri, kamera, galeri, oyunlar ve Simple Voice Chat ile gerçek sesli/görüntülü arama içerir.

## Depo içeriği

```
mikasrevs_phone-1.3.3.jar          derlenmiş mod (modun kendisi)
ROADMAP.md                         "Başka ne ekleyebiliriz?" - öncelikli fikir listesi
docs/mevcut-durum.md               modun tam envanteri (23 uygulama, sistemler, paketler, zayıf noktalar)
docs/eklentiler.md                 JAR'a dokunmadan çalışan datapack / resource pack kurulumu
datapacks/mikasrevs_phone_extras/  kılıf boyama + geri dönüşüm + başarım sekmesi
resourcepacks/mikasrevs_phone_lang_pack/  düzeltilmiş Türkçe + 5 yeni dil (de, fr, it, pt, az)
docs/tasarim/                      Görevler / Saat-Alarm / El feneri için uygulama tasarım dokümanları
tools/                             paket doğrulama ve zip'leme betikleri
```

## Kurulum

1. `mikasrevs_phone-1.3.3.jar` dosyasını `.minecraft/mods/` (veya sunucunun `mods/`) klasörüne at.
2. İsteğe bağlı: **Simple Voice Chat** (sesli arama için), **Kuronomy** (banka bakiye köprüsü için).
3. İsteğe bağlı ekstra içerik: [`docs/eklentiler.md`](docs/eklentiler.md).

Komutlar: `/phonecall <oyuncu>` · `/phonehangup`

## Daha fazla özellik eklemek

Plan ve fikir listesi için **[ROADMAP.md](ROADMAP.md)** dosyasına bak.

Hazır tasarım dokümanları (kaynak kod gelince doğrudan uygulanabilir):
`docs/tasarim/01-gorevler-tasks.md` · `docs/tasarim/02-saat-alarm.md` · `docs/tasarim/03-el-feneri.md`

Özetle en yüksek getirili ilk beş:

1. **Görevler (Tasks) uygulamasını bitirmek** — şu an ekranda sadece “YAKINDA” yazıyor.
2. **Saat / Alarm / Kronometre** uygulaması.
3. **El feneri** (Kontrol Merkezi'ne toggle).
4. **Mesajlarda grup sohbeti + tepkiler.**
5. **Veri odaklı içerik + config/izin altyapısı** (kodsuz içerik ekleme imkânı).

⚠️ Bu depoda şu an yalnızca derlenmiş JAR var; Java kaynak kodu ve Gradle projesi yok.
Yeni uygulama/item eklemek için kaynak projenin bu depoya eklenmesi gerekir (bkz. `ROADMAP.md` → bölüm 0 ve 5.1).
