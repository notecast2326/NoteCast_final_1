import re

from django import forms
from .models import Notice
from django import forms
from .models import CustomUser



# ================= NOTICE FORM =================

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['notice_subject', 'display_category', 'message', 'file_upload', 'thumbnail']
        labels = {
            'notice_subject': 'Notice Title',
            'display_category': 'Notice Type',
            'message': 'Description',
            'file_upload': 'Attachment (Optional)',
            'thumbnail': 'Thumbnail Image (Optional)'
        }


# ================= COMMON VALIDATIONS =================

def validate_username(username):
    if not re.match(r'^[A-Za-z ]+$', username):
        raise ValidationError("Username can contain only letters and spaces.")


def validate_password(password):
    if len(password) < 5:
        raise ValidationError("Password must be at least 5 characters.")

    if not re.search(r'[A-Za-z]', password):
        raise ValidationError("Password must contain at least one letter.")

    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one number.")

    if not re.search(r'[@$!%*#?&]', password):
        raise ValidationError("Password must contain at least one special character.")


# ================= STUDENT REGISTER =================

class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'admission_no', 'department']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)
        return username

    def clean_admission_no(self):
        admission_no = self.cleaned_data.get('admission_no')

        if not admission_no.isdigit():
            raise ValidationError("Admission number must contain only digits.")

        if len(admission_no) != 4:
            raise ValidationError("Admission number must be exactly 4 digits.")

        return admission_no

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user


# ================= HOD REGISTER =================

class HodRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'department']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'hod'
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user


# ================= STAFF REGISTER =================

class StaffRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'staff'
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


# ================= LOGIN FORM =================

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



# ================= PROFILE UPDATE =================

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo', 'address', 'phone', 'university_reg_no', 'employee_id']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user and user.user_type != 'student':
            self.fields.pop('university_reg_no')

        if user and user.user_type != 'hod':
            self.fields.pop('employee_id')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            if not phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")

            if len(phone) != 10:
                raise ValidationError("Phone number must be exactly 10 digits.")

        return phone

    def clean_university_reg_no(self):
        reg = self.cleaned_data.get('university_reg_no')

        if reg and not reg.replace(" ", "").isalnum():
            raise ValidationError("University register number cannot contain special characters.")

        return reg

    def clean_employee_id(self):
        emp = self.cleaned_data.get('employee_id')

        if emp:
            if not re.match(r'^[A-Za-z0-9]+$', emp):
                raise ValidationError("Employee ID can contain only letters and numbers.")

            if len(emp) > 8:
                raise ValidationError("Employee ID cannot be more than 8 characters.")

        return emp