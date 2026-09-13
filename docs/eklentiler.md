# JAR'a dokunmadan eklenebilen içerikler

Bu klasörlerdeki paketler **kod derlemeden, JAR'ı değiştirmeden** çalışır. Modun 1.3.3 sürümüyle uyumlu (Minecraft 1.20.1, `pack_format: 15`).

## 1. Datapack — `datapacks/mikasrevs_phone_extras/`

**Kurulum (tek oyunculu):** `mikasrevs_phone_extras` klasörünü `.minecraft/saves/<DÜNYA>/datapacks/` içine kopyala, dünyayı aç, `/reload`.
**Kurulum (sunucu):** `world/datapacks/` içine kopyala, `/reload`. (Global datapack için sunucuya özel `datapacks` klasörü de kullanılabilir.)

İçindekiler:

| Dosya | Ne yapar |
|---|---|
| `data/mikasrevs_phone/tags/items/phone_cases.json` | 12 kılıfı tek etikette toplar |
| `data/mikasrevs_phone/recipes/recolor_*.json` (12) | **Kılıf boyama:** herhangi bir kılıf + ilgili boya/madde → istediğin kılıf. (Örn. kılıf + kırmızı boya → Şarap Kırmızısı). 4 deriyi yeniden harcamak gerekmez. |
| `data/mikasrevs_phone/recipes/case_recycle_leather.json` | İstenmeyen kılıf → 2 deri |
| `data/mikasrevs_phone/advancements/root.json` | “MikasRevs Phone” başarım sekmesi (telefonu edinince) |
| `.../stylish.json` | 5 farklı kılıf → “Stil Sahibi” (+50 xp) |
| `.../case_collector.json` | 12 kılıfın tamamı → “Kılıf Koleksiyoncusu” (+250 xp) |

Boyama eşleşmeleri, modun kendi kılıf tarifleriyle birebir aynı: siyah boya, demir külçesi, beyaz boya, mavi boya, yeşil boya, kırmızı boya, cam bölme, altın külçesi, pembe boya, barut, açık mavi boya, camgöbeği boya.

> Not: Başarım koşulları 1.20.1 biçimiyle (`"item": "..."` tekil alan) yazılmıştır. 1.20.5+ sürümlere taşınırsa `"items": ["..."]` olarak güncellenmeli.

## 2. Resource pack — `resourcepacks/mikasrevs_phone_turkish_fix/`

**Kurulum:** klasörü `.minecraft/resourcepacks/` içine kopyala, oyunda *Seçenekler → Kaynak Paketleri*'nden **en üste** taşı (mod asset'lerini geçersiz kılması gerekir).

Ne düzeltiyor: modun aktif `tr_tr.json` dosyasında Türkçe karakterler kaybolmuş — “Gumus”, “Seffaf”, “Yesil”, “Sarap Kirmizisi”, “Altin Luxury Telefon Kilifi”. Eski (artık kullanılmayan) `mattupolis_phone` dosyasında yazımlar doğruydu; bu paket doğru yazımları aktif namespace'e geri getiriyor:

> Gümüş · Şeffaf · Orman Yeşili · Şarap Kırmızısı · Buz Beyazı · Gece Siyahı · Altın Lüks · Pembe Çiçek · Mattupolis Şehir

Aynı düzeltmeyi kalıcı yapmak istersen: bu dosyayı JAR'daki `assets/mikasrevs_phone/lang/tr_tr.json` ile değiştirmen yeterli (kaynak projede `src/main/resources/assets/mikasrevs_phone/lang/tr_tr.json`).

## 3. Doğrulama

Repo'ya eklenen tüm JSON'lar `json.tool` ile doğrulanmıştır (geçerli JSON, UTF-8). Datapack'i yükledikten sonra oyun logunda “Selected new data pack” ve hata uyarısı olmamasını kontrol et.
