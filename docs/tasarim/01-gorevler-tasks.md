# Tasarım 1 — Görevler (Tasks) uygulaması

**Durum:** `PhoneTasksScreen` şu an sadece “SOON / YAKINDA” yazan bir placeholder (`drawSoon()`).
**Hedef:** Notlar (`PhoneNotesStore`) ve Takvim (`PhoneCalendarStore`) kalıbını kullanarak çalışan bir yapılacaklar listesi.
**İş yükü:** küçük–orta (1–2 dosya yeni + 1 ekran düzenlemesi + katalog entegrasyonu).

---

## 1. Veri modeli

```java
public class PhoneTasksStore {
    public static class TaskItem {
        public final String id;          // UUID
        public String title;             // zorunlu
        public String note;              // opsiyonel açıklama
        public long dueAt;               // epoch millis, 0 = tarih yok
        public Priority priority;        // LOW | NORMAL | HIGH
        public boolean done;
        public long createdAt;
        public long completedAt;
        public Repeat repeat;            // NONE | DAILY | WEEKLY
        public String listName;          // "Genel", "İş", "Alışveriş"…
    }
    public enum Priority { LOW, NORMAL, HIGH }
    public enum Repeat   { NONE, DAILY, WEEKLY }

    private static final List<TaskItem> TASKS = new ArrayList<>();
    private static boolean loaded;
}
```

Not: `PhoneNotesStore$NoteItem` ve `PhoneCalendarStore$ReminderItem` bu yapıya çok benziyor; alan adlarını onlarla tutarlı tut ( `title`, `createdAt`, `done` zaten kullanılıyor).

## 2. Kalıcılık

Modun mevcut kalıbı: statik liste + `loadIfNeeded()` + `save()` + `getStoreFile()` (istemci tarafı dosya).
Görevler için satır formatı önerisi (mevcut store'lardaki `Encoder`/`Decoder` yaklaşımıyla, Base64 kaçışlı tek satır):

```
id|createdAt|dueAt|priority|repeat|done|listName|title|note
```

- `loadIfNeeded()` ilk erişimde dosyayı okur, bozuksa satırı atlar.
- `save()` her mutasyondan sonra çağrılır (notlar/takvim ile aynı davranış).
- **İyileştirme önerisi:** uzun vadede görevler sunucu tarafına taşınmalı (bkz. `ROADMAP.md` §5.6). İlk sürümde istemci tarafı yeterli.

## 3. API (ekran ve katalog bunları kullanır)

```java
static List<TaskItem> getTasks();              // sıralı kopya: önce done=false, sonra dueAt, sonra priority
static int  getOpenCount();                    // ana ekran rozeti / bugün sayacı
static int  getTodayCount();                   // dueAt bugün ve done=false
static void addTask(String title, long dueAt, Priority p, Repeat r, String listName);
static void toggleDone(String id);
static void deleteTask(String id);
static void editTask(String id, String title, String note, long dueAt, Priority p, Repeat r);
static void sanitize(String s);                // satır sonu / ayırıcı temizliği, uzunluk sınırı (örn. 120)
```

## 4. Ekran akışı (`PhoneTasksScreen`)

1. `drawSoon()` çağrısını kaldır → liste çizimi:
   - Üstte filtre sekmeleri: **Tümü / Bugün / Planlandı / Tamamlandı**
   - Satır: solda yuvarlak kutu (tık → `toggleDone`), başlık (tamamlanmışsa üstü çizili + `getMutedTextColor()`), sağda tarih/saat (`HH:mm` / `dd.MM`), yüksek öncelikte `getAccentColor()` ile nokta.
   - Boş durum: “Görev yok. + ile ekle.”
2. Alt bar: **+ Yeni görev** → `PhoneTaskEditScreen` (yeni, küçük ekran: başlık, not, tarih/saat, öncelik, tekrar, liste).
3. Satıra sağ tık / uzun basma → sil; satıra tık → düzenle.
4. `PhoneScreenBase.drawTopBar()` kalıbı korunur; geri butonu ana ekrana döner.

Yeni ekran dosyası: `client/gui/PhoneTaskEditScreen.java` (yaklaşık 150–200 satır; `PhoneNotesScreen` kopyalanıp uyarlanabilir — sessiz yazı kutusu için `PhoneSilentEditBox`, metin çizimi için `PhoneEditBoxTextRenderer` hazır).

## 5. Entegrasyon noktaları

| Yer | Değişiklik |
|---|---|
| `PhoneHomeAppCatalog` | `tasks` kaydının badge metodu `getOpenCount()`/`getTodayCount()`’a bağlanır (gram/notes/calendar örnekleri var). |
| `PhoneAppLibraryScreen` | Arama anahtarlarına “görev, task, todo, yapılacak” ekle. |
| `PhoneNotificationStore` | `dueAt` yaklaşınca bildirim (takvim hatırlatıcılarıyla aynı mekanizma). |
| `PhoneDynamicIslandHelper` | Görev tamamlandığında kısa “tamamlandı” balonu (opsiyonel). |
| `PhoneLanguageStore` | 5 dil için metinler (aşağıda). |

## 6. Metinler (`PhoneLanguageStore` kalıbı — Ingilizce/Türkçe/Rusça/İspanyolca/Lehçe)

| Anahtar | EN | TR |
|---|---|---|
| tasks.empty | No tasks yet | Henüz görev yok |
| tasks.add | New task | Yeni görev |
| tasks.today | Today | Bugün |
| tasks.scheduled | Scheduled | Planlandı |
| tasks.done | Completed | Tamamlandı |
| tasks.all | All | Tümü |
| tasks.priority | Priority | Öncelik |
| tasks.repeat | Repeat | Tekrarla |
| tasks.due | Due | Son tarih |
| tasks.delete | Delete task? | Görev silinsin mi? |
| tasks.daily / weekly | Daily / Weekly | Günlük / Haftalık |

## 7. Kabul kriterleri

- [ ] Görev eklenebiliyor, düzenlenebiliyor, tamamlandı olarak işaretlenebiliyor, silinebiliyor.
- [ ] Oyun kapatılıp açıldığında görevler korunuyor.
- [ ] Ana ekranda `Görevler` ikonunda açık görev sayısı rozeti görünüyor.
- [ ] “SOON / YAKINDA” yazısı tamamen kalktı.
- [ ] 5 dilde metinler mevcut; uzun başlıklarda taşma yok (kırpma/“...”).
- [ ] Türkçe karakterler (ş, ğ, ı, İ, ç, ö, ü) doğru yazılıyor.
