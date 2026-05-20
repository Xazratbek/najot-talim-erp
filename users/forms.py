from django import forms
from .models import User
from .models import User, Roles
from django.core.exceptions import ValidationError
import re

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone',
            'avatar',
            'role',
            'balance',
            'branch',
            'gender',
            'is_active',
        ]



class TeacherCreateForm(UserForm):
    def __init__(self, *args, **kwargs):
        self.role = Roles.TEACHER
        return super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get("username")

        username = username.lower()

        if not username:
            raise ValidationError("Username kiritish majburiy")

        if len(username) != 5:
            raise ValidationError("Username 5-ta elementdan iborat bolsin")

        if username.isalpha():
            raise ValidationError("Username faqat harfdan iborat bo'lishi mumkin emas")

        if username.isdigit():
            raise ValidationError("Username faqat sondan iborat bo'lishi mumkin emas")

        forbidden_usernames = ['admin', 'superuser', 'root', 'moderator', 'support']
        if username in forbidden_usernames:
            raise ValidationError("Bu username tizim tomonidan band qilingan, boshqa nom tanlang")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu username allaqachon band qilingan")

        return username


    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if not first_name:
            raise ValidationError("Ism kiritish majburiy")

        if not first_name.isalpha():
            raise ValidationError("Ism faqat harfdan iborat bo'lsin")

        if len(first_name) < 2:
            raise ValidationError("Ism kamida 2-ta harfdan iborat bo'lsin")

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if not last_name:
            raise ValidationError("Familiya kiritish majburiy")

        if not last_name.isalpha():
            raise ValidationError("Familiya faqat harfdan iborat bo'lsin")

        if len(last_name) < 2:
            raise ValidationError("Familiya kamida 2-ta harfdan iborat bo'lsin")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise ValidationError("Telefon raqamini kiritish majburiy")

        # 2. Faqat raqamlar va '+' belgisini qoldirib, qolgan hamma narsani (bo'shliq, qavs, chiziqcha) o'chirish
        # Masalan: "+998 (90) 123-45-67" -> "+998901234567"
        cleaned_phone = re.sub(r'[^\d+]', '', phone)

        # 3. Agar foydalanuvchi raqamni 901234567 shaklida (kodsiz) kiritgan bo'lsa, boshigari "+998" ni qo'shish
        if len(cleaned_phone) == 9 and cleaned_phone.isdigit():
            cleaned_phone = f"+998{cleaned_phone}"

        # 4. Agar foydalanuvchi boshibagi '+' ni unutib "998901234567" yozgan bo'lsa, '+' ni qo'shib qo'yamiz
        if len(cleaned_phone) == 12 and cleaned_phone.isdigit():
            cleaned_phone = f"+{cleaned_phone}"

        # 5. Yakuniy tekshiruv (Regex): Raqam albatta +998 bilan boshlanishi va undan keyin rosa 9 ta raqam bo'lishi shart
        # Jami uzunlik: 13 ta belgi bo'ladi (+ va 12 ta raqam)
        phone_regex = r'^\+998\d{9}$'
        if not re.match(phone_regex, cleaned_phone):
            raise ValidationError("Telefon raqami formati noto'g'ri. Namuna: +998901234567")

        if User.objects.filter(phone=cleaned_phone).exists():
            raise ValidationError("Bu raqam bilan allaqachon ro'yxatdan o'tilgan ")

        #bir xil formatda saqlaymiz: +998901234567
        return cleaned_phone

class AdminStudentCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'role',
            'gender'
        ]


class LoginForm(forms.Form):
    login = forms.CharField(max_length=15,required=True)
    password = forms.CharField(max_length=15,required=False)