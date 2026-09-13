# Tasarım 2 — Saat / Alarm / Kronometre / Zamanlayıcı

**Durum:** Modda saat sadece **durum çubuğunda** (`HH:mm`, `DateTimeFormatter.ofPattern("HH:mm")`) ve kilit ekranında görünüyor. Bağımsız bir Saat uygulaması yok.
**Hedef:** iOS “Clock” benzeri 4 sekmeli uygulama: **Dünya saati → Alarm → Kronometre → Zamanlayıcı**.
**İş yükü:** orta (1 ekran + 1 store + tema/bildirim entegrasyonu). Sunucu tarafı paket gerekmez.

---

## 1. Zaman kaynağı

Oyun içi saat Minecraft gün döngüsünden gelir (`level.getDayTime()`), gerçek dünya saati değil.
Karar: **varsayılan = oyun saati** (rol yapma sunucuları için tutarlı), ayarlardan “gerçek saat (sistem saati)” seçeneği.

```java
long dayTime  = level.getDayTime();          // 0..24000
int  mcHour   = (int)((dayTime / 1000L + 6) % 24);   // 0 = sabah 6
int  mcMinute = (int)((dayTime % 1000L) * 60 / 1000);
```

İsteğe bağlı olarak `PhoneSettingsStore`’a `useRealClock` bayrağı (mevcut ayarlar: bildirimler, ses, rahatsız etme, uçak modu, karanlık mod, PIN, parlaklık).

## 2. Store

```java
public class PhoneClockStore {                 // istemci tarafı, PhoneSettingsStore kalıbı
    public static class Alarm {
        public final String id;                // UUID
        public int hour, minute;               // oyun saati
        public boolean enabled;
        public int snoozeMinutes = 5;          // erteleme
        public String label = "Alarm";
        public long lastFiredDay = -1;         // aynı gün iki kez çalmasın
    }
    static List<Alarm> getAlarms();
    static void addAlarm(int hour, int minute, String label);
    static void removeAlarm(String id);
    static void toggleAlarm(String id);
    static void snooze(String id);
}
```

Kronometre/zamanlayıcı **kalıcı olmak zorunda değil** (oturum içi, ekran alanında tutulabilir), ama alarm listesi kaydedilmeli.

## 3. Ekran: `PhoneClockScreen` (4 sekme)

1. **Dünya saati** — oyuncunun kaydettiği konumlar (`PhoneGpsScreen$GpsTarget` listesi yeniden kullanılabilir) için saat farkı gösterimi: “Ev (Overworld) 08:12”, “Maden (Nether) 08:12”, “Son (End) 08:12”. Basit sürüm: Overworld/Nether/End + koordinat etiketleri.
2. **Alarm** — liste + `+` ile ekleme (saat/dakika kutuları, etiket, aktif anahtarı). Çaldığında:
   - `PhoneSoundManager` üzerinden ses (yeni `alarm.ogg` veya mevcut `phone_toast.ogg`),
   - `PhoneNotificationStore`’a bildirim + **Ertele / Durdur** butonları,
   - `PhoneDynamicIslandHelper` genişleyen uyarı balonu.
3. **Kronometre** — Başlat/Duraklat/Sıfırla, tur (lap) listesi.
4. **Zamanlayıcı** — süre seç (1/5/10/30 dk), geri sayım, bitince ses + bildirim.

Çizim: `PhoneScreenBase` kalıbı (`drawPhone`, `drawStatusBar`, `drawTopBar`, `drawBrightnessOverlay`), renkler `PhoneTheme`'den (`getCardColor`, `getAccentColor`, `getTextColor`, `getSubTextColor`).
Sekme çubuğu için `PhoneSettingsScreen`/`PhoneMailScreen` içindeki sekme çizimi örnek alınabilir.

## 4. Tick / olay entegrasyonu

Alarm kontrolü her tick’te değil, saniyede bir yapılmalı (performans):

```java
@SubscribeEvent  // client tick, PhoneHealthEvents / PhoneCallMovementEvents kalıbı
public static void onClientTick(TickEvent.ClientTickEvent event) {
    if (event.phase != TickEvent.Phase.END) return;
    if (++tickCounter < 20) return;            // 20 tick = 1 sn
    tickCounter = 0;
    PhoneClockStore.checkAlarms();             // eşleşen alarm varsa bildirim + ses
}
```

- Telefon kapalıyken/kilitliyken de çalmalı (kilit ekranı üstüne “Alarm çalıyor” kartı).
- `PhoneSettingsStore.isDoNotDisturbEnabled()` → sesi kıs, bildirimi göster.
- Uçak modu alarmı etkilemesin (saat uygulaması çevrimdışı çalışır).

## 5. Katalog entegrasyonu

`PhoneHomeAppCatalog`’a yeni kayıt:

```java
add("clock", "clock saat alarm kronometre zamanlayıcı timer",
    new ResourceLocation("mattupolis_phone", "textures/gui/icons/clock.png"),
    "Clock", "Saat", "Часы", "Reloj", "Zegarek", true, false);
```

Yeni ikon gerekiyor: `assets/mattupolis_phone/textures/gui/icons/clock.png` — mevcut 22 ikonla aynı stil (16×16, düz, `calendar.png` ve `tasks.png` ile uyumlu). Katalog, ikon yolu kalıbını `"mattupolis_phone" + "textures/gui/icons/" + id + ".png"` olarak kullanıyor.

> **Uyarı:** ikonlar `mattupolis_phone` namespace'inden okunuyor (kodda `MOD_ID = "mattupolis_phone"`), item'lar ise `mikasrevs_phone`. Yeni asset'leri **doğru namespace'e** koymak gerekiyor.

## 6. Metinler (5 dil)

| Anahtar | EN | TR |
|---|---|---|
| clock.title | Clock | Saat |
| clock.world | World Clock | Dünya saati |
| clock.alarm | Alarm | Alarm |
| clock.stopwatch | Stopwatch | Kronometre |
| clock.timer | Timer | Zamanlayıcı |
| clock.add_alarm | Add alarm | Alarm ekle |
| clock.snooze | Snooze | Ertele |
| clock.stop | Stop | Durdur |
| clock.lap | Lap | Tur |
| clock.no_alarms | No alarms | Alarm yok |

## 7. Kabul kriterleri

- [ ] 4 sekme çalışıyor, saat oyun döngüsüyle senkron.
- [ ] Alarm kuruluyor, kaydediliyor, çalıyor (ses + bildirim), ertelenebiliyor.
- [ ] Kronometre tur kaydediyor; zamanlayıcı bitince uyarıyor.
- [ ] Ana ekranda yeni ikon + rozet (aktif alarm sayısı).
- [ ] Kilit ekranında da alarm görünüyor; “Rahatsız etme” sesi kısıyor.
- [ ] Durum çubuğundaki mevcut saat ile tutarlı (aynı zaman kaynağı).
