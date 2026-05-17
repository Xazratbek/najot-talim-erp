# Najot Ta'lim ERP loyihasi uchun TZ (Junior Developer formatida)

## 1) Loyiha maqsadi
Najot Ta'lim o'quv markazi uchun ERP tizimi ishlab chiqiladi. Tizimda 3 asosiy rol bo'ladi:
- Admin / Staff
- O'qituvchi
- O'quvchi

Asosiy talab: **o'qituvchi va o'quvchi self-registration qilmaydi**. Ularni faqat:
- `admin`
- yoki `is_staff=True` bo'lgan foydalanuvchi
qo'sha oladi.

---

## 2) Auth va Role qoidalari

### 2.1 Login
- Faqat login (username + password) orqali kiriladi.
- Register endpoint/page bo'lmaydi (teacher/student uchun).

### 2.2 User yaratish huquqlari
- Teacher yaratish: faqat admin yoki staff.
- Student yaratish: faqat admin yoki staff.

### 2.3 Role asosida ruxsatlar
- **Teacher**: faqat quyidagi funksiyalar:
  - vazifa berish
  - davomat qilish
  - yangi dars qo'shish
  - imtihon yaratish/berish
  - dars va imtihonni tekshirish
  - o'z guruhlarini ko'rish
  - yig'ilayotgan guruhlarni ko'rish
- **Student**:
  - login
  - dashboard
  - to'lovlarim
  - guruhlarim va lesson/homework submission
  - ko'rsatgichlarim (XP/reyting)
  - do'kon
  - sozlamalar

---

## 3) Modullar bo'yicha funksional talablar

## 3.1 Admin/Staff boshqaruvi

### View: `AdminTeacherCreateView`
**Mas'ul:** Nozimjon  
**Vazifa:** Teacher yaratish formi va saqlash.

**Logika:**
1. Request user admin yoki `is_staff=True` bo'lmasa `403`.
2. Form validate.
3. Role avtomatik `teacher` ga qo'yiladi.
4. Username/phone unique tekshiriladi.
5. Parol hash qilinib user yaratiladi.

### View: `AdminStudentCreateView`
**Mas'ul:** Xazratbek  
**Vazifa:** Student yaratish formi va saqlash.

**Logika:**
1. Request user admin yoki `is_staff=True` bo'lmasa `403`.
2. Form validate.
3. Role avtomatik `student` ga qo'yiladi.
4. Username/phone unique tekshiriladi.
5. Parol hash bilan saqlanadi.

---

## 3.2 Teacher panel

### View: `TeacherGroupListView`
**Mas'ul:** Nozimjon  
**Vazifa:** O'qituvchining o'z guruhlari ro'yxati.

**Logika:**
1. User role `teacher` bo'lmasa `403`.
2. Faqat current teacherga biriktirilgan guruhlar chiqadi.
3. Filter: active / archived.

### View: `TeacherCollectingGroupListView`
**Mas'ul:** Xazratbek  
**Vazifa:** Yig'ilayotgan (start qilmagan) guruhlar ro'yxati.

**Logika:**
1. Role check (`teacher`).
2. `status=collecting` guruhlar.
3. Teacher branchiga mos guruhlar.

### View: `TeacherGroupDetailView`
**Mas'ul:** Nozimjon  
**Vazifa:** Group detail: group info + darsliklar bo'limi.

**Logika:**
1. Teacher faqat o'ziga tegishli guruh detailini ko'radi.
2. Sahifada 2 yirik blok:
   - Guruh ma'lumotlari
   - Guruh darsliklari
3. Darsliklar ichida sub bo'limlar:
   - Uyga vazifalar
   - Videolar
   - Imtihonlar

### View: `TeacherLessonCreateView`
**Mas'ul:** Xazratbek  
**Vazifa:** Yangi lesson yaratish.

**Logika:**
1. Teacher groupga tegishli ekanligi tekshiriladi.
2. Lesson sanasi, mavzu, material validatsiya.
3. Lesson yaratilgach guruh studentlariga notification queue qilinadi.

### View: `TeacherHomeworkCreateView`
**Mas'ul:** Nozimjon  
**Vazifa:** Lessonga homework biriktirish.

**Logika:**
1. Lesson teacherga tegishli bo'lishi shart.
2. Deadline > hozirgi vaqt.
3. Homework yaratilgach studentlarga notification.

### View: `TeacherAttendanceCreateView`
**Mas'ul:** Xazratbek  
**Vazifa:** Davomat belgilash.

**Logika:**
1. Faqat lesson kuni va lesson guruhi studentlari uchun attendance.
2. Har student uchun unique attendance record (lesson + student).
3. Qayta yuborilsa update rejimida ishlaydi.

### View: `TeacherExamCreateView`
**Mas'ul:** Nozimjon  
**Vazifa:** Imtihon yaratish/e'lon qilish.

**Logika:**
1. Teacher group ownership check.
2. Exam date, duration, max score validatsiya.
3. Save + "Yangi imtihon" notification yuborish.

### View: `TeacherSubmissionReviewView`
**Mas'ul:** Xazratbek  
**Vazifa:** Homework/Exam submission tekshirish.

**Logika:**
1. Teacher faqat o'z guruh submissionlarini ko'radi.
2. Ball/izoh qo'yish.
3. Status: pending -> checked.
4. Tekshirilgach studentga notification.

---

## 3.3 Student panel

### View: `StudentDashboardView`
**Mas'ul:** Nozimjon  
**Vazifa:** Bosh sahifa.

**Ko'rsatish:**
- Kumushlari
- Reyting
- Dars jadvali (yaqin darslar)

### View: `StudentPaymentsView`
**Mas'ul:** Xazratbek  
**Vazifa:** To'lovlarim sahifasi.

**Logika:**
1. Faqat current student to'lovlari.
2. Filtrlash: sana oralig'i, status, payment type.
3. Pagination bo'lishi shart.

### View: `StudentGroupsView`
**Mas'ul:** Nozimjon  
**Vazifa:** Studentning guruhlari ro'yxati.

### View: `StudentGroupDetailView`
**Mas'ul:** Xazratbek  
**Vazifa:** Guruh detail + lessons jadvali.

**Lessons ustunlari:**
- Mavzu
- Video (video soni bilan)
- Uyga vazifa holati
- Uyga vazifa tugash sanasi
- Dars sanasi

### View: `StudentLessonDetailView`
**Mas'ul:** Nozimjon  
**Vazifa:** Lesson ichida homework bo'limi.

### View: `StudentHomeworkSubmissionCreateView`
**Mas'ul:** Xazratbek  
**Vazifa:** Homework submission form.

**Logika:**
1. Deadline o'tgan bo'lsa submit bloklanadi.
2. Faqat studentning o'z submissioni yaratiladi.
3. Repeat submit qilinganda update yoki yangi versiya qoidasi aniq belgilanadi (MVPda update).

---

## 3.4 Ko'rsatgichlarim (Gamification)

### View: `StudentIndicatorsView`
**Mas'ul:** Nozimjon  
**Vazifa:** XP statistikasi.

**Ko'rsatish:**
- Dars bo'yicha XP
- Imtihon bo'yicha XP
- Boshqa eventlar bo'yicha XP

### View: `StudentRankingView`
**Mas'ul:** Xazratbek  
**Vazifa:** Reytinglar.

**Reyting kesimlari:**
- Filial bo'yicha
- Guruh bo'yicha
- Umumiy filiallar bo'yicha (global)

---

## 3.5 Do'kon

### View: `ShopProductListView`
**Mas'ul:** Nozimjon  
**Vazifa:** Productlar ro'yxati.

**Talablar:**
- Category bo'yicha filter
- Search
- Pagination

### View: `ShopProductDetailView`
**Mas'ul:** Xazratbek  
**Vazifa:** Bitta product detail.

---

## 3.6 Sozlamalar

### View: `StudentSettingsView`
**Mas'ul:** Nozimjon  
**Vazifa:** Sozlamalar bosh sahifasi.

### View: `StudentProfileEditView`
**Mas'ul:** Xazratbek  
**Vazifa:** Profile edit.

**Cheklovlar:**
- Faqat avatar o'zgartirish
- Faqat parol o'zgartirish
- Notification sozlamalari
- Boshqa maydonlar (role, balans, branch) edit qilinmaydi.

---

## 4) Notification app (kodlanadigan qism)

Ushbu task bo'yicha backendda `notifications` app yaratiladi va quyidagi fayllar bo'ladi:
- `notifications/models.py`
- `notifications/admin.py`
- `notifications/forms.py`

### Notification model talablar
- `type`: notification turi
- `receiver`: qabul qiluvchi user
- `title`: sarlavha
- `is_read`: o'qilgan/o'qilmagan

### Notification turlari
- Yangi imtihon uchun
- Imtihon e'loni uchun
- XP uchun
- Imtihon muddati yaqin qolsa
- Uyga vazifa tekshirilganda
- Guruhga qo'shilganlik haqida
- Guruhda o'qishni to'xtatilganda
- XP/Kumush berilganda

---

## 5) NFR (non-functional)
- Permissionlar har viewda server tarafda tekshirilsin.
- List endpointlar pagination bilan bo'lsin.
- Filter/search query param orqali ishlasin.
- Barcha datetime lar `Asia/Tashkent` timezonega mos bo'lsin.
- Audit uchun `created_at`, `updated_at` ishlatilsin.

---

## 6) Task taqsimoti (teng miqdorda)

### Nozimjon (11 ta view)
1. AdminTeacherCreateView
2. TeacherGroupListView
3. TeacherGroupDetailView
4. TeacherHomeworkCreateView
5. TeacherExamCreateView
6. StudentDashboardView
7. StudentGroupsView
8. StudentLessonDetailView
9. StudentIndicatorsView
10. ShopProductListView
11. StudentSettingsView

### Xazratbek (11 ta view)
1. AdminStudentCreateView
2. TeacherCollectingGroupListView
3. TeacherLessonCreateView
4. TeacherAttendanceCreateView
5. TeacherSubmissionReviewView
6. StudentPaymentsView
7. StudentGroupDetailView
8. StudentHomeworkSubmissionCreateView
9. StudentRankingView
10. ShopProductDetailView
11. StudentProfileEditView

> Eslatma: Har bir junior o'z viewiga tegishli serializer/form, service va testlarni ham o'zi yozadi.
