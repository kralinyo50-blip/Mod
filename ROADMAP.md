# MikasRevs Phone — “Başka ne ekleyebiliriz?” Yol Haritası

> Mod: **MikasRevs Phone 1.3.3** (Forge 1.20.1, `modId = mikasrevs_phone`, 334 sınıf)
> Bu belge: modun şu anki durumunu analiz edip **eklenebilecek özellikleri** öncelik + iş yükü + teknik notlarıyla listeler.
> Detaylı mevcut durum envanteri: [`docs/mevcut-durum.md`](docs/mevcut-durum.md) · Kodsuz eklentiler: [`docs/eklentiler.md`](docs/eklentiler.md)

---

## 0. Önemli not: bu depoda şu an **sadece derlenmiş JAR** var

Repo'da tek dosya var: `mikasrevs_phone-1.3.3.jar`. Java kaynak kodu, Gradle projesi ve build betiği yok.
Dolayısıyla:

| İstek | Şu an yapılabilir mi? |
|---|---|
| Yeni kılıf / item / uygulama (kod gerektirir) | ❌ Kaynak kod depoya eklenmeli |
| Tarif / başarım / etiket / dil düzeltmesi (veri odaklı) | ✅ Bu depoda hazırlandı (`datapacks/`, `resourcepacks/`) |
| Mimari öneri, plan, dokümantasyon | ✅ Bu belge |

Bu ortamda Forge/Maven'a erişim kapalı olduğu için derleme de yapılamıyor. **Kaynak projeyi bu depoya push edersen** (veya ayrı bir repo olarak verirsen) aşağıdaki maddelerin çoğunu doğrudan uygulayabilirim.

---

## 1. Hızlı kazançlar (1–2 saat, kod yok)

| # | Fikir | Açıklama | Durum |
|---|---|---|---|
| 1.1 | **Türkçe karakter hatası** | Aktif namespace'teki `tr_tr.json` ASCII'ye kaçırılmış (“Gumus”, “Seffaf”, “Yesil”, “Altin Luxury”), eski `mattupolis_phone` dosyasında ise doğru (“Gümüş”, “Şeffaf”, “Yeşil”) yazılı. Yani gerileme (regression) var. | ✅ `resourcepacks/mikasrevs_phone_turkish_fix` hazır |
| 1.2 | **Kılıf boyama (re-dye) tarifleri** | Elindeki kılıfı 1 boyayla başka bir kılıfa dönüştürme (12 tarif). Yeni kılıf üretmek için 4 deri harcamak zorunda kalmıyorsun. | ✅ `datapacks/mikasrevs_phone_extras` |
| 1.3 | **Kılıf geri dönüşümü** | Kılıf → 2 deri. | ✅ datapack içinde |
| 1.4 | **Başarım sekmesi** | “Telefon Sahibi → Stil Sahibi (5 kılıf) → Kılıf Koleksiyoncusu (12 kılıf)”. Modun kendi advancement sekmesi yoktu. | ✅ datapack içinde |
| 1.5 | **Ölü asset temizliği** | `assets/mattupolis_phone/{models,textures/item,lang}` ve `data/mattupolis_phone/recipes` kayıtlı olmayan eski namespace'e ait → **~226 KB** gereksiz (JAR'ın %15'i). Dikkat: ikonlar ve sesler `mattupolis_phone` altından okunuyor, **silinmemeli**. | ⚠️ Kaynak/JAR rebuild gerekir |
| 1.6 | **Metadata cilası** | `mods.toml`: logo (`logoFile`), `displayTest`, issue tracker URL, `updateJSONURL`, daha açıklayıcı description + Türkçe tanıtım. | ⚠️ Kaynak gerekir |
| 1.7 | **README + CHANGELOG** | Kurulum, özellik listesi, komutlar, uyumluluk, sürüm notları. | ⚠️ Bu depoda iskelet hazır |

---

## 2. Mevcut uygulamaları derinleştirme (orta iş yükü) ⭐ önerilen

| # | Uygulama | Eklenebilecekler | Teknik not |
|---|---|---|---|
| 2.1 | **Görevler (Tasks)** | Şu an ekran sadece **“SOON / YAKINDA”** yazan bir placeholder — modun en bariz boşluğu. Yapılacaklar listesi: başlık, tarih/saat, öncelik, tamamlandı işareti, tekrarlayan görev, bildirim. | `PhoneNotesStore` + `PhoneCalendarStore` kalıbı kopyalanır: `PhoneTasksStore` (JSON/properties kayıt), `PhoneTasksScreen` içindeki `drawSoon()` gerçek listeyle değişir. Badge sayacı için `PhoneHomeAppCatalog`’a `getOpenTasksCount()` gibi bir metot eklenir. |
| 2.2 | **Mesajlar** | Grup sohbeti (1→N thread), mesaj arama, sabitleme, emoji tepkileri (reactions), okundu bilgisi, yazıyor… göstergesi, sesli mesaj. | `PhoneMessagesStore$PhoneThread` tek kişilik; `participants: List<UUID>` + yeni paket (`ServerboundPhoneTextPacket`’e `groupId` alanı veya `PhoneGroupTextPacket`). Tepkiler için `Map<UUID,String>`. |
| 2.3 | **Galeri** | Albümler/klasörler, fotoğraf düzenleme (filtre, kırp, döndür), silme, PNG olarak dışa aktarma, depolama kotası. | `PhoneGalleryStore` NativeImage tutuyor; `NativeImage#writeToFile` ile `screenshots/` klasörüne export kolay. |
| 2.4 | **Müzik** | Kullanıcı kendi parçalarını eklesin (klasörden/ resource pack'ten tarama), çalma listesi, favoriler, arka planda çalma ayarı. | `PhoneMusicManager.TRACKS` şu an hardcoded. Klasör taraması (`config/mikasrevs_phone/music/*.ogg`) + dinamik `SoundEvent` kaydı yapılabilir. |
| 2.5 | **Duvar kağıdı** | Özel duvar kağıdı yükleme (URL/dosya), biyoma/gün saatine göre **dinamik** duvar kağıdı, paralaks. | `PhoneWallpaperStore` prosedürel çiziyor (`drawCitySilhouette`, `drawForestSilhouette`, `drawGoldLines`); “custom” stili eklenip dosyadan `DynamicTexture` yüklenebilir. |
| 2.6 | **Sağlık (Health)** | Adım sayısı, mesafe, aktif tick, yenilen yemek ve günlük hedef **zaten kaydediliyor** (`PhoneHealthStore`). Eksik: **geçmiş grafiği (son 7 gün)**, haftalık özet, uyku takibi, hedefe ulaşınca bildirim. | `PhoneHealthStore` alanları hazır; sadece geçmiş serisi + çizim + bildirim eklenecek. |
| 2.7 | **Banka** | IBAN/hesap no, kart (kredi/banka kartı) görünümü, faiz, kredi/taksit, otomatik ödeme, döviz kuru, para transferi makbuzu görselleştirme. | Sunucu tarafı `PhoneBankServerStore` + `KuronomyBankBridge` hazır; sadece ekran + yeni paketler. Admin denetim logu zaten var (`ClientboundBankAdminAuditPacket`). |
| 2.8 | **Marketplace** | Kategori filtresi, arama, favoriler, satıcı puanı, sipariş/kargo takibi, teslimat noktası (GPS ile). | `PhoneMarketplaceServerStore$Listing` alan eklemesi + `PhoneMarketplaceScreen` filtre UI. |
| 2.9 | **GPS** | Yer işareti (waypoint) kaydetme/atlama, çok noktalı rota, **ölüm noktası** kaydı, canlı konum paylaşımı süresi, yakındaki oyuncuları listeleme, JourneyMap/Xaero waypoint senkronizasyonu. | `PhoneGpsScreen$GpsTarget`, `PhoneGpsBridge`, `PhoneGpsCompactOverlay` var; waypoint listesi kalıcı hale getirilir. Harita modlarıyla köprü `PhoneCommonCompat`/`PhoneClientCompat` kalıbıyla yazılır (Kuronomy örneği gibi opsiyonel). |
| 2.10 | **Kamera** | Zoom, flaş (kısa süreli ışık/gece görüşü), filtreler (renk matrisi), video kaydı, selfie modu. | `PhoneLiveCameraSession` + `PhoneVideoCallLiveSession` altyapısı hazır — video kaydı neredeyse bedava. |
| 2.11 | **Gram / Mattu (sosyal)** | @bahsetme, hashtag, bildirim gruplama, DM'de grup, story'e müzik/çıkartma, taslaklar, “keşfet” algoritması. | `PhoneInstagramStore` / `PhoneTwitterStore` zaten zengin; bildirim tarafı `PhoneNotificationStore` ile birleştirilebilir. |
| 2.12 | **Mail** | Eklenti (attachment), klasörler (Gelen/Giden/Spam/Arşiv), toplu silme, okundu işareti. | `PhoneMailStore$MailItem` + `ServerboundMailPacket`. |
| 2.13 | **Takvim** | Etkinlik davetleri (başka oyuncuya davet paketi), tekrarlayan hatırlatıcı, gün/hafta/ay görünümü. | `PhoneCalendarStore$ReminderItem` + yeni paket. |
| 2.14 | **Hesap makinesi** | Bilimsel mod, geçmiş, kopyala. | `PhoneCalculatorScreen` küçük iş. |
| 2.15 | **Hava durumu** | 3 günlük tahmin, fırtına/yıldırım uyarısı, mini radar (biyom haritası üzerine yağmur overlay), sıcaklık birimi seçimi (°C/°F). | `PhoneWeatherScreen$WeatherState`; `level.isRaining()`, `getThunderLevel()` zaten kullanılıyor. |

---

## 3. Yeni uygulamalar (orta–büyük)

1. **Saat / Alarm / Kronometre / Zamanlayıcı / Dünya saati** — oyun içi gün döngüsüne bağlı alarm (ör. “saat 06:00'da uyar”), kronometre, geri sayım. *(Küçük-orta, çok istenen klasik.)*
2. **El feneri (Flashlight)** — Kontrol Merkezi'ne toggle; gece görüşü efekti + (varsa) LambDynamicLights benzeri dinamik ışık modlarıyla entegrasyon. *(Küçük.)*
3. **Sesli Notlar / Kayıt cihazı (Voice Memos)** — Simple Voice Chat zaten entegre; kayıt → mesaj olarak gönder.
4. **Dosya yöneticisi & Depolama** — telefon hafızası (fotoğraf, müzik, uygulama, mesaj) GB cinsinden; dolduğunda uyarı, “depolama alanını yönet” ekranı. Rol yapma derinliği katar, oyuncular telefonu “gerçekten” kullanır.
5. **Sesli asistan “Mattu” (Siri tarzı)** — yazılı komutlar: “X'i ara”, “Y'ye mesaj at”, “hava nasıl”, “not al: …”, “beni eve götür” (GPS yönlendirme).
6. **Yeni oyunlar** (Mine Store'dan indirilebilir, Jump/ColorTap gibi): **2048**, **Yılan (Snake)**, **Sudoku**, **Hafıza (Memory)**, **Tic-Tac-Toe (iki telefon arası çevrimiçi)**, **Flappy Mattu**, **Brick Breaker**. Çevrimiçi skor tablosu (sunucu tarafı) ayrıca eğlenceli olur.
7. **Acil durum / 112** — polis, itfaiye, sağlık çağrısı; `police_blue` kılıfı ve admin paneliyle tematik; NPC/operatör mesajları (`PhoneNpcMessageStore` zaten var) burada kullanılabilir.
8. **Taksi / Ulaşım** — GPS + banka entegrasyonu: “şuradan al”, ücret hesabı.
9. **Kurye / Yemek siparişi** — Marketplace altyapısıyla sipariş → kurye oyuncusuna görev → teslimat. Sunucu ekonomisine çok şey katar.
10. **Yatırım / Borsa** — Kuronomy entegrasyonuyla dalgalı fiyatlar, al/sat, grafik.
11. **Duyuru panosu / Haberler** — sunucu sahibi `PhoneSocialAdminStore` benzeri bir panelden tüm telefonlara bildirim/duyuru göndersin.
12. **Radyo / Podcast** — sunucu tarafı ses akışı (Voice Chat API) + müzik çalar arayüzü.
13. **Ekran Süresi (Screen Time)** — telefonda geçirilen süre istatistikleri, “Rahatsız Etme”, uygulama bazlı grafik.
14. **Kayıp / Çalıntı Telefon (Find My Phone)** — telefon başkasındaysa GPS ile bul, uzaktan kilitle/sil, polise bildir. Rol yapma sunucuları için altın değerinde.
15. **Kişi kartviziti / QR** — telefon numarasını QR ile paylaşma, kamerayla okutunca kişilere ekleme (görsel şaka + kullanışlı).

---

## 4. Yeni item & kozmetik içerik (küçük–orta)

- **Yeni kılıflar:** Ender, Netherite, Bakır, Kızıl Kum (Red Sand), Amethyst, biome temalı, bayram temalı (Noel / Cadılar Bayramı / Ramazan), klan/takım kılıfı, **oyuncu kafası baskılı kılıf** (oyuncu skin'ini kılıfa basma — çok paylaşılır).
  *Nasıl:* `ModItems#registerCase` + `PhoneCaseStore.CASES`'e kayıt + model/texture + tarif + 5 dil etiketi. Tekrarlayan ama kolay içerik.
- **Kılıfı kendin tasarla:** oyuncu renk seçiciyle kendi rengini kaydetsin (`PhoneColorTapScreen` benzeri seçici).
- **Telefon aksesuarları:** kulaklık (Voice Chat ses kalitesi/menzil bonusu), powerbank (şarj), ekran koruyucu (kırılma), tutacak/popsocket.
- **Şarj & batarya:** telefonun şarjı kullanımca azalsın (kamera/oyun/arama çok yer), şarj cihazı **bloğu**, düşük şarj uyarısı, güç tasarrufu modu. *(Uçak modu zaten var, batarya yok — en mantıklı sıradaki sistem.)*
- **Yeni cihazlar:** **Tablet** (büyük ekran, çoklu pencere), **Akıllı saat** (sağlık/bildirim aynası), **Dizüstü bilgisayar** (admin/market için masaüstü blok).
- **Masaüstü/stand bloğu:** telefon bloğa takılınca geniş ekran (sunucu lobi/ev dekorasyonu).
- **SIM kart / operatör / tarife:** hat item'ı, kota (MB), farklı operatörler — ekonomik rol yapma.
- **Zil sesi / bildirim sesi paketleri:** resource pack ile değiştirilebilir sesler (sounds.json yapısı hazır).
- **Telefon rengi/modeli:** şu an tek gövde rengi var; 3–4 gövde varyantı.

---

## 5. Teknik altyapı (büyük ama çarpan etkili)

1. **Kaynak kod + CI:** ForgeGradleworkspace, GitHub Actions ile tag → otomatik build + release JAR, `CHANGELOG`, sürüm politikası. *(Şu an manuel upload yapılıyor.)*
2. **Veri odaklı (data-driven) içerik:** kılıflar, duvar kağıtları, müzik listesi, temalar, **uygulama kataloğu** JSON'dan okunsun. Böylece içerik eklemek için kod derlemek gerekmez ve **resource pack / addon** ekosistemi doğar. *(En yüksek uzun vadeli getiri.)*
3. **Addon API:** `RegisterPhoneAppEvent` gibi bir registry event'i → başka modlar kendi uygulamasını telefon ana ekranına ekleyebilsin. Dokümantasyon + örnek addon.
4. **Forge config (client + server):** uygulama açma/kapatma, fiyatlar, mesaj/fotoğraf limitleri, GPS menzili, banka limitleri, kamera kalitesi, bildirim ayarları.
5. **İzinler (permissions):** op yerine permission node'ları; LuckPerms uyumluluğu (admin paneli, banka admini, sosyal admin için).
6. **Kalıcılık mimarisi:** birçok store **istemci tarafı dosyaya** yazıyor (`getStoreFile`). Sunucu tarafına/`SavedData`'ya taşınmalı — aksi halde veri kaybı ve istismar (banka/market hariç tutulmuş ama Gram, notlar, mesajlar, takvim istemcide). Banka/market/sosyal store'ları zaten sunucu tarafı: örnek alınabilir.
7. **Çoklu dil mimarisi:** UI metinleri **Java içinde hardcoded** (EN/TR/RU/ES/PL, `PhoneLanguageStore`). Lang dosyalarına/JSON'a taşınırsa topluluk çevirisi kolaylaşır; Almanca, Fransızca, Arapça, Azerbaycanlı, Portekizce, İtalyanca, Ukraynaca eklenebilir. *(Şu an yeni dil eklemek 5 yerde switch demek.)*
8. **Performans:** 334 sınıf, çok sayıda tam ekran yeniden çizim; fotoğrafların `NativeImage` yaşam döngüsü (sızıntı riski), ağ paketi boyutları (`PhoneMediaPacketLimits` var), delta-senkronizasyon, GUI ölçek koruması (`PhoneGuiScaleGuard` var — iyi) genişletilebilir.
9. **Güvenlik:** paket doğrulama (fotoğraf boyutu/en-boy, metin uzunluğu), rate limiting, renk kodu (`§`) enjeksiyonu temizliği, opsiyonel küfür filtresi, admin işlem logları (banka audit var, diğerlerine de).
10. **Komutlar:** mevcut `/phonecall`, `/phonehangup`. Eklenebilir: `/phone give <oyuncu>`, `/phone reload`, `/phone wipe <oyuncu>`, `/phone lookup <isim|numara>`, `/phone broadcast <mesaj>`, `/phone call <oyuncu>` için izin düğümleri.
11. **Mod uyumlulukları:** Simple Voice Chat ✅, Kuronomy ✅. Sıradaki adaylar: **JourneyMap / Xaero's Minimap** (waypoint senkronizasyonu), **LuckPerms**, **FTB Teams/Claims**, **Waystones** (ışınlanma noktaları GPS'te), **ComputerCraft** (telefon API), Discord köprüsü (sunucu botu).
12. **Sürüm/port:** 1.20.1 → 1.20.4 → 1.21 ve NeoForge/Fabric portu (büyük iş, talep varsa).
13. **Erişilebilirlik:** tuş ataması ile telefonu açma (keybind), büyük metin modu, renk körlüğü temaları, fare tekerleği ile kaydırma.

---

## 6. Önerilen sıralama

**Sprint 1 (kodsuz + küçük):** 1.1–1.4 (hazır) → 1.5 temizlik → **2.1 Tasks uygulamasını bitir** → **3.1 Saat/Alarm** → **3.2 El feneri**.
**Sprint 2:** 2.2 grup mesaj + tepkiler, 2.9 GPS waypoint, 4 yeni kılıflar (Netherite, Ender, Amethyst, oyuncu kafası).
**Sprint 3:** 5.1 kaynak+CI, 5.2 veri odaklı içerik, 5.4 config, 5.7 dil mimarisi → sonra yeni uygulamalar hızlanır.
**Rol yapma sunucuları için:** 3.7 acil durum, 3.8 taksi, 3.9 kurye, 3.14 kayıp telefon, 4 batarya/şarj, 4 SIM/operatör.

---

## 6.1 Hazır tasarım dokümanları

Kaynak kod depoya gelir gelmez uygulanabilir, sınıf/sınıf-içi detay seviyesinde yazılmış üç taslak:

- `docs/tasarim/01-gorevler-tasks.md` — Görevler (Tasks) uygulaması: veri modeli, kayıt formatı, ekran akışı, katalog/bildirim entegrasyonu, 5 dil metni, kabul kriterleri.
- `docs/tasarim/02-saat-alarm.md` — Saat / Alarm / Kronometre / Zamanlayıcı: oyun saati kaynağı, store, tick entegrasyonu, ikon yolu, kabul kriterleri.
- `docs/tasarim/03-el-feneri.md` — El feneri: 3 uygulama seçeneği (gece görüşü / dinamik ışık / ışık bloğu), ayar entegrasyonu, kontrol merkezi + Dynamic Island UI.

## 7. Bu depoda şu an hazır olanlar

- `datapacks/mikasrevs_phone_extras/` → kılıf boyama + geri dönüşüm + başarım sekmesi (JAR'a dokunmadan çalışır).
- `resourcepacks/mikasrevs_phone_lang_pack/` → düzeltilmiş Türkçe + Almanca/Fransızca/İtalyanca/Portekizce/Azerbaycanlı (eşya adları + çağrı mesajları).
- `tools/validate.py` + `tools/package_extras.py` + GitHub Actions → paket doğrulama ve dağıtım zip'i.
- `docs/tasarim/` → 3 özellik için uygulama tasarım dokümanı.
- `docs/mevcut-durum.md` → modun tam envanteri (uygulamalar, sistemler, paketler, komutlar, zayıf noktalar).
- `docs/eklentiler.md` → kurulum talimatları.

Kaynak kodu depoya eklersen bu listeden seçtiğin maddeleri doğrudan kod olarak yazabilirim.
