# Mevcut Durum Envanteri — MikasRevs Phone 1.3.3

JAR içeriği analiz edilerek çıkarıldı (`com/mattupolis/phone/...`, 334 sınıf, 80 ekran sınıfı).

## 1. Kimlik

| Alan | Değer |
|---|---|
| modId | `mikasrevs_phone` |
| Sürüm | 1.3.3 (build 2026-06-20) |
| Loader | Forge `javafml` ≥ 47 |
| Minecraft | 1.20.1 – 1.21 (1.20.1 hedef) |
| Lisans | All Rights Reserved |
| Zorunlu bağımlılık | forge, minecraft |
| Opsiyonel | **Simple Voice Chat** (kod içinde, `de.maxhenkel.voicechat.api`), **Kuronomy** ≥ 3.2.6 (banka köprüsü, `ordering = AFTER`) |
| Eşya namespace'i | `mikasrevs_phone:*` (modId) |
| Asset namespace'leri | `mikasrevs_phone` **ve** `mattupolis_phone` (ikonlar/sesler eski namespace'ten okunuyor) |
| JAR boyutu | 1.5 MB |

## 2. Item'lar (`ModItems`)

- `phone` — tarif: 4 demir + 3 redstone + 2 cam bölme (şekilli)
- 12 kılıf: `midnight_black`, `silver`, `white_frost`, `navy_blue`, `forest_green`, `wine_red`, `transparent`, `gold_luxury`, `pink_blossom`, `creeper`, `police_blue`, `mattupolis_city`
- Kılıf tarifi (hepsi aynı kalıp): 4 deri + merkezde özel madde (boya / demir külçesi / altın külçesi / barut / cam bölme)
- Kılıflar prosedürel çiziliyor; `creeper`, `mattupolis_city`, `police_blue`, `transparent` için özel çizim rutinleri var.

## 3. Uygulama kataloğu (`PhoneHomeAppCatalog`, 23 kayıt)

| id | Ad | Not |
|---|---|---|
| `gram` | Gram | Instagram klonu: gönderi, story, DM, yorum, beğeni, takip istekleri, keşfet, bildirimler, engellenenler, ayarlar, story izleyenler |
| `twitter` | Mattu | Tweet, anket (poll), trend, yorum, bildirim, profil |
| `settings` | Ayarlar | Uçak modu, bildirimler, ses, parlaklık, tema, karanlık mod, dil |
| `gps` | GPS | Hedef işaretleme, yüzey haritası, kompakt overlay (`PhoneGpsCompactOverlay`) |
| `bank` | Banka | Hesap, PIN, transfer, geçmiş, admin paneli, denetim logu + Kuronomy köprüsü |
| `camera` | Kamera | Canlı kamera oturumu (`PhoneLiveCameraSession`), deklanşör sesi, galeriye kayıt |
| `store` | Mine Store | “Uygulama indir” — Jump ve ColorTap oyunları satın/alın (`isJumpInstalled`, `isColorTapInstalled`) |
| `notes` | Notlar | Kalıcı not listesi |
| `calendar` | Takvim | Hatırlatıcılar, bugün sayacı |
| `marketplace` | Pazar | İlan oluşturma/inceleme, yorumlar, satış, sunucu tarafı store |
| `tasks` | Görevler | ⚠️ **“SOON / YAKINDA” placeholder — uygulanmamış** |
| `calculator` | Hesap | Temel hesap makinesi |
| `health` | Sağlık | Can/açlık/biyom bilgisi, olay dinleyici |
| `cases` | Kılıflar | Kılıf seçici |
| `music` | Müzik | Çalar, ses seviyesi, tekrar/karıştır, ilerleme çubuğu (parça listesi hardcoded) |
| `weather` | Hava durumu | Hava durumu durum makinesi |
| `mail` | Mail | Gelen kutusu, oluşturma, detay |
| `library` | Uygulama Kitaplığı | Tüm uygulamaların listesi + arama |
| `wallpaper` | Duvar kağıdı | Kilit/ana ekran duvar kağıdı (prosedürel: city, forest, gold vb.) |
| `gallery` | Galeri | Fotoğraf ızgarası + büyük görüntüleyici |
| `admin` | Admin | Sosyal medya moderasyon paneli (op) |
| `jump` | Mattu Jump | Engel oyunu (yüksek skor) |
| `color_tap` | ColorTap | Refleks oyunu |

Dock/ayrı akışlar: **Telefon/Arama** (`PhoneCallScreen`, `PhoneCallingScreen`, `PhoneIncomingCallScreen`, `PhoneActiveCallScreen`), **Mesajlar** (`PhoneMessagesScreen`, sohbet, fotoğraf, konum, kamera, bilgi), **Kişiler** (`PhoneContactsScreen`, kişi istekleri), **Arama geçmişi** (`PhoneCallHistoryStore`), **Video görüşme** (`PhoneVideoCallLiveSession`, kare akışı), **NPC mesajları** (`PhoneNpcMessageStore`).

## 4. UI/UX sistemleri

- `PhoneScreenBase` — ortak telefon gövdesi: durum çubuğu (saat, 5G/uçak modu), üst bar, parlaklık katmanı, ev göstergesi
- **Kilit ekranı + PIN akışı** (`PhoneLockScreen$PinFlow`), **Kontrol Merkezi** (`PhoneControlCenterScreen`)
- **Dynamic Island** bildirim sistemi (`PhoneDynamicIslandHelper`: durum, ikon tipi, tıklama hedefi)
- **Bildirim paneli** + overlay (`PhoneNotificationStore`, `PhoneNotificationPanelOverlay`)
- **Ana ekran düzeni kaydetme** (`PhoneHomeLayoutStore` — ikonlar taşınabiliyor), uygulama kitaplığı ve arama
- **Tema motoru** (`PhoneTheme`: Blue / Purple / Green / Classic / Night, tam renk paleti, karanlık mod)
- **Duvar kağıdı motoru** (`PhoneWallpaperStore`, prosedürel silüet çizimleri)
- **Dil motoru** (`PhoneLanguageStore`: EN / TR / RU / ES / PL — **metinler Java içinde hardcoded**)
- **Ses yöneticisi** (`PhoneSoundManager`) + 8 `.ogg` (deklanşör, mesaj gönder/al, tıklama, hata, toast, kilit açma)
- Kılıf çerçevesi overlay'i, GUI ölçek koruması, skin uyumluluğu, sessiz yazı kutusu (klavye kısayollarını yutma)

## 5. Ağ katmanı (`PhoneNetwork`)

- **46 clientbound + 49 serverbound** paket sınıfı; kanal namespace'i `mikasrevs_phone`
- Medya (fotoğraf, video karesi) için boyut limitleri: `PhoneMediaPacketLimits`
- Sunucu tarafı store'lar: `PhoneBankServerStore`, `PhoneMarketplaceServerStore`, `PhoneSocialServerStore`, `PhoneNumberServerStore` (numara rehberi + lookup)
- İstemci tarafı (dosyaya yazan) store'lar: mesajlar, notlar, takvim, galeri, gram, twitter, kılıf, duvar kağıdı, ayarlar, tema, müzik…

## 6. Komutlar

- `/phonecall <oyuncu>` — Simple Voice Chat üzerinden arama başlat
- `/phonehangup` — aktif aramayı kapat

## 7. Tespit edilen zayıf noktalar / fırsatlar

1. **Tasks uygulaması boş** — ekranda sadece “SOON / YAKINDA” yazıyor.
2. **Türkçe karakter regresyonu** — aktif `mikasrevs_phone` lang dosyası ASCII'ye kaçırılmış (“Gumus”, “Seffaf”, “Altin Luxury”), eski `mattupolis_phone` dosyası doğru yazılmış. *(Düzeltmesi: `resourcepacks/mikasrevs_phone_turkish_fix`)*
3. **Ölü asset'ler** — `assets/mattupolis_phone/{models,textures/item,lang}` + `data/mattupolis_phone/recipes` ≈ **226 KB** gereksiz (kayıtlı olmayan namespace). İkon ve sesler o namespace'te **olduğu için silinmemeli**.
4. **Metinler koda gömülü** — yeni dil/çeviri için 5 yeri güncellemek gerekiyor; topluluk çevirisi imkânsız.
5. **İçerik hardcoded** — kılıflar, duvar kağıtları, müzik listesi, uygulama kataloğu Java'da → addon/resource pack ile içerik eklenemiyor.
6. **İstemci tarafı kalıcılık** — banka/market/sosyal hariç çoğu veri istemci dosyasında; senkronizasyon/istismar ve veri kaybı riski.
7. **Config/izin yok** — sunucu sahipleri uygulamaları/limitleri kapatamıyor, admin op'a bağlı.
8. **Başarım (advancement) yok** — datapack ile eklendi (`datapacks/mikasrevs_phone_extras`).
9. **Repo'da kaynak kod yok** — sadece derlenmiş JAR; CI/build/issue şablonu yok.
