# Tasarım 3 — El feneri (Flashlight)

**Durum:** Yok. Kontrol Merkezi’nde uçak modu, bildirim, ses, parlaklık, karanlık mod var; fener yok.
**Hedef:** Telefonda tek dokunuşla açılan fener — gece madencilik/rol yapma için.
**İş yükü:** çok küçük (1 toggle + 1 efekt yardımcısı + 1 ikon). Diğer iki tasarımdan önce yapılabilir.

---

## 1. Üç uygulama seçeneği

| Seçenek | Nasıl | Artı | Eksi |
|---|---|---|---|
| **A. Gece görüşü efekti (önerilen, bağımlılıksız)** | Oyuncuya `MobEffects.NIGHT_VISION` (sonsuz, parçacıklar kapalı) ver / kaldır | Hiç bağımlılık yok, her sunucuda çalışır, 30 satır kod | Gerçek ışık değil, blok ışık seviyesi değişmez |
| **B. Dinamik ışık entegrasyonu** | LambDynamicLights / DynamicLights varsa API üzerinden ışık kaynağı kaydet | Gerçek ışık, çok daha “doğru” | Opsiyonel bağımlılık, sürüm/API kırılganlığı |
| **C. Işık bloğu yerleştirme (gölge ışık)** | Oyuncunun bulunduğu yere görünmez `light` bloğu | Gerçek ışık | Sunucu tarafı dünya değişikliği, chunk güncellemesi, geride iz kalabilir |

**Öneri:** A şimdi, B opsiyonel olarak `PhoneCommonCompat`/`PhoneClientCompat` kalıbıyla (Kuronomy köprüsünde olduğu gibi “varsa kullan, yoksa sessizce geç”).

## 2. Veri & ayar

`PhoneSettingsStore` zaten `notificationsEnabled`, `soundEnabled`, `doNotDisturbEnabled`, `airplaneModeEnabled`, `darkModeEnabled`, `brightnessPercent`, `lockPinCode` tutuyor. Aynı kalıpla:

```java
private static boolean flashlightEnabled = false;
public static boolean isFlashlightEnabled();
public static void toggleFlashlight();   // efekti uygular + save()
```

Toggle davranışı:
- **Telefon elde değilse** → açılmasın (veya açıksa otomatik kapanıp efekt kaldırılsın).
- **Uçak modu** feneri etkilemesin (fener çevrimdışı çalışır).
- Oyuncu ölürse / boyut değiştirirse efekt yeniden uygulanmalı (`PhoneHealthEvents` benzeri bir olay dinleyicisi veya client tick’te 1 sn’de bir doğrulama — Saat tasarımındaki yöntem).

## 3. Efekt yardımcısı

```java
public final class PhoneFlashlight {
    public static void apply(Player player) {
        player.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION,
                MobEffectInstance.INFINITE_DURATION, 0, false, false, false));
    }
    public static void clear(Player player) {
        player.removeEffect(MobEffects.NIGHT_VISION);
    }
    public static void syncFromSettings(Player player) {
        if (PhoneSettingsStore.isFlashlightEnabled()) apply(player); else clear(player);
    }
}
```

Not: gece görüşü, başka bir kaynaktan (ör. fener/beacon/sıvı) gelen efektle çakışabilir; kaldırmadan önce “bu efekti modun kendisi mi verdi” bilgisi tutulabilir (ör. NBT etiketi veya basit bir `Set<UUID>`), aksi halde oyuncunun mevcut gece görüşü yanlışlıkla silinir.

## 4. UI

1. **Kontrol Merkezi** (`PhoneControlCenterScreen`): mevcut 2×2/3×2 kutu ızgarasına “Fener” kutusu. Açıkken kutu `getAccentColor()` ile dolar, ikon dolar.
2. **Durum çubuğu**: açıkken Dynamic Island’da küçük fener ikonu (`PhoneDynamicIslandHelper$IconType`’a yeni bir tip eklenir) — kullanıcıya “açık unutuldu” uyarısı.
3. **Kilit ekranı**: kilitliyken de alt köşede fener kısayolu (gerçek telefonlarda olduğu gibi) — opsiyonel, çok sevilen detay.
4. **İkon:** `assets/mattupolis_phone/textures/gui/icons/flashlight.png` (16×16, mevcut ikon stiliyle).
5. **Ses:** `PhoneSoundManager.playClick()` ile geri bildirim.

## 5. Opsiyonel: gerçek ışık (B seçeneği)

`PhoneCommonCompat` içine Kuronomy köprüsündeki gibi güvenli bir kontrol:

```java
public static final boolean DYNAMIC_LIGHTS = ModList.get() != null && ModList.get().isLoaded("lambdynamiclights");
```

Dinamik ışık modülü yüklüyse, oyuncu konumuna hafif bir ışık kaynağı ekle; değilse A seçeneğine düş. Bu, “mod uyumluluğu” başlığında sunucu sahiplerinin en çok isteyeceği özelliklerden biri.

## 6. Metinler (5 dil)

| Anahtar | EN | TR |
|---|---|---|
| flashlight | Flashlight | El feneri |
| flashlight.on | Flashlight on | El feneri açık |
| flashlight.off | Flashlight off | El feneri kapalı |
| flashlight.need_phone | You need to hold your phone | Telefonunu tutman gerekiyor |

## 7. Kabul kriterleri

- [ ] Kontrol Merkezi’nden tek tıkla açılıp kapanıyor.
- [ ] Açıkken efekt uygulanıyor, kapanınca kaldırılıyor; durum kaydediliyor.
- [ ] Telefon elden bırakıldığında/ölümde efekt temizleniyor (hayalet gece görüşü kalmıyor).
- [ ] Ölüm/boyut değişimi sonrası durum yeniden uygulanıyor.
- [ ] Dynamic Island’da açık olduğu görülüyor.
- [ ] Sunucuda (dedicated) da çalışıyor, console’da hata yok.
