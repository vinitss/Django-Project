from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ProfileForm,StudentRegisterForm,FacultyRegisterForm,CommunityRegisterForm, UserUpdateForm
import users.globalbaz
from .models import User

def register_profile(request):
    return redirect('register_student')


def register_student(request ) :
    print ('mG')
    users.globalbaz.Type = 'Student'
    print (users.globalbaz.Type)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_profile_form = StudentRegisterForm(request.POST)
        if user_form.is_valid() and student_profile_form.is_valid():
            user = user_form.save()
            user.profile.type = users.globalbaz.Type
            user.profile.save()
            user.student_profile.roll_number = student_profile_form.cleaned_data.get('roll_number')
            user.student_profile.location = student_profile_form.cleaned_data.get('location')
            user.student_profile.branch = student_profile_form.cleaned_data.get('branch')
            user.student_profile.year_of_admission = student_profile_form.cleaned_data.get('year_of_admission')
            user.student_profile.first_name = student_profile_form.cleaned_data.get('first_name')
            user.student_profile.last_name = student_profile_form.cleaned_data.get('last_name')
            user.student_profile.save()

            messages.success(request, f'Your profile was successfully created!')

            return redirect('login')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserForm()
        student_profile_form = StudentRegisterForm()
    return render(request, 'users/register_student.html', {
        'user_form': user_form,
        'student_profile_form': student_profile_form

    })

def register_faculty(request ) :
    print ('mG')
    users.globalbaz.Type = 'Faculty'
    print (users.globalbaz.Type)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        faculty_profile_form = FacultyRegisterForm(request.POST)
        if user_form.is_valid() and faculty_profile_form.is_valid():
            user = user_form.save()
            user.profile.type = users.globalbaz.Type
            user.profile.save()
            user.faculty_profile.location = faculty_profile_form.cleaned_data.get('location')
            user.faculty_profile.first_name = faculty_profile_form.cleaned_data.get('first_name')
            user.faculty_profile.last_name = faculty_profile_form.cleaned_data.get('last_name')

            user.faculty_profile.save()

            messages.success(request, f'Your profile was successfully created!')

            return redirect('login')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserForm()
        faculty_profile_form = FacultyRegisterForm()
    return render(request, 'users/register_faculty.html', {
        'user_form': user_form,
        'faculty_profile_form': faculty_profile_form

    })

def register_community(request ) :
    print ('mG')
    users.globalbaz.Type = 'Community'
    print (users.globalbaz.Type)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        community_profile_form = CommunityRegisterForm(request.POST)
        if user_form.is_valid() and community_profile_form.is_valid():
            user = user_form.save()
            user.profile.type = users.globalbaz.Type
            user.profile.save()

            user.community_profile.name = community_profile_form.cleaned_data.get('name')
            user.community_profile.admin_username = community_profile_form.cleaned_data.get('admin_username')

            user.community_profile.save()

            messages.success(request, f'Your profile was successfully created!')

            return redirect('login')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserForm()
        community_profile_form = CommunityRegisterForm()
    return render(request, 'users/register_community.html', {
        'user_form': user_form,
        'community_profile_form': community_profile_form

    })

def get_user_profile(request,username):

    try:
        user_p = User.objects.get(username=username)

    except (User.DoesNotExist):
        messages.warning(request,'No such username exists')
        return redirect('blog-home')
    return render(request,'users/user_profile.html',{"user_p" : user_p })


@login_required
def edit_profile(request):
    CurrentUser = request.user
    u_original_form = UserUpdateForm(instance=request.user)
    p_original_form = ProfileForm(instance=request.user.profile)
    r_original_form = None
    c_username = CurrentUser.username
    c_email = CurrentUser.email
    if (CurrentUser.profile.type == 'Student'):
        r_original_form = StudentRegisterForm(instance=request.user.student_profile)
    elif (CurrentUser.profile.type == 'Faculty'):
        r_original_form = FacultyRegisterForm( instance=request.user.faculty_profile)
    elif (CurrentUser.profile.type == 'Community'):
        r_original_form = CommunityRegisterForm( instance=request.user.community_profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        r_form = None

        #print (CurrentUser.profile.type)
        if (CurrentUser.profile.type == 'Student'):
            r_form = StudentRegisterForm(request.POST, instance=request.user.student_profile)
        elif (CurrentUser.profile.type == 'Faculty'):
            r_form = FacultyRegisterForm(request.POST, instance=request.user.faculty_profile)
        elif (CurrentUser.profile.type == 'Community'):
            r_form = CommunityRegisterForm(request.POST, instance=request.user.community_profile)
        p_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid() and r_form.is_valid():
            u_form.save()
            r_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('edit_profile')
        else:
            u_form = u_original_form
            p_form = p_original_form
            r_form = r_original_form
            messages.warning(request,'Such username exists')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
        r_form = None

        if (CurrentUser.profile.type == 'Student'):
            r_form = StudentRegisterForm(instance=request.user.student_profile)
        elif (CurrentUser.profile.type == 'Faculty'):
            r_form = FacultyRegisterForm( instance=request.user.faculty_profile)
        elif (CurrentUser.profile.type == 'Community'):
            r_form = CommunityRegisterForm( instance=request.user.community_profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'r_form' : r_form,
        'c_username' : c_username,
        'c_email' : c_email

    }

    return render(request, 'users/edit_profile.html', context)










'''
if request.method == 'POST':
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():

        global user
        user = user_form.save()

        user.profile.type = profile_form.cleaned_data.get('type')
        user.profile.save()

        messages.success(request, f'Your profile was successfully created!')

        return redirect('register_student')
    else:
        messages.error(request, f'Please correct the error below.')
else:
    user_form = UserForm()
    profile_form = ProfileForm()
return render(request, 'users/register.html', {
    'user_form': user_form,
    'profile_form': profile_form
})
'''


'''
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
'''
