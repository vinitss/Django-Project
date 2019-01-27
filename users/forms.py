from django import forms
from .models import Profile,Student_Profile,Faculty_Profile,Community_Profile
from django.contrib.auth.forms import User,UserCreationForm
import datetime


class UserForm(UserCreationForm):
    email = forms.EmailField()
    #first_name = forms.CharField(max_length=30)
    #last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = [ 'username','email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    '''
    def clean_username(self):
            username = self.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Such username exists")
            else:
                return username
    '''
    class Meta:
        model = User
        #exclude = ['username']
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class StudentRegisterForm(forms.ModelForm):
    location = forms.CharField()
    now = datetime.datetime.now()
    start_year=now.year-4
    end_year=now.year+1 # end_year in range is exclusive
    # hence in for loop
    # [start_year,end_year)
    # we have printed 5 years because current month is not taken into consideration
    BRANCH_CHOICES =(('Computer','Computer Engineering'),
                    ('Electrical','Electrical Engineering'),
                    ('Civil','Civil Engineering'),
                    ('I.T','I.T Engineering'),
                    ('Mechanical','Mechanical Engineering'),
                        )

    year_of_admission = forms.ChoiceField(choices=[(x,x) for x in range(start_year,end_year)])
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES
    )
    roll_number = forms.IntegerField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = Student_Profile
        fields = ['first_name','last_name','year_of_admission','branch','roll_number','location']


class FacultyRegisterForm(forms.ModelForm):
    location = forms.CharField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = Faculty_Profile
        fields = [ 'first_name','last_name','location']



class CommunityRegisterForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    admin_username = forms.CharField(max_length=50)
    def clean_admin_username(self):
            admin_username = self.cleaned_data['admin_username']
            if User.objects.filter(username=admin_username).exists():
                return admin_username
            else:
                raise forms.ValidationError("No such username exists")

    class Meta:
        model = Community_Profile
        fields = ['name','admin_username']





'''
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = [ 'username','email','company', 'password1', 'password2']
'''
