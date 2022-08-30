from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, ThoughtPostForm, ThoughtUpdateForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth.models import auth
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Thought, User, Profile

from django.core.mail import send_mail
from django.conf import settings 



def index(request):
    thoughts = Thought.objects.all().order_by("-created")
    paginator = Paginator(thoughts, 8)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    
    
    context = {'page_obj':page_obj}
    return render(request, 'index.html', context)

def userProfile(request, pk=None):
    user = User.objects.get(id=pk)
    thoughts= user.thought_set.all()
    profile = Profile.objects.get(user=user)
    context = {'thoughts':thoughts, 'profile':profile}
    return render(request, 'profiles/userProfile.html', context)




def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():

            # saving a instance of form in current_user
            current_user = form.save(commit=False)
            form.save()

            # preparing an welcome email template
            subject="Welcome to BrickThoughts"
            msg = "Your account has been created! Start Sharing your thoughts"
            email_from = settings.DEFAULT_FORM_EMAIL
            email_to = current_user.email

            send_mail(subject, msg, email_from, [email_to])


            #  create a empty object of profile
            profile = Profile.objects.create(user=current_user)


            messages.success(request, "Account created!" )
            return redirect("userLogin")

    context = {'form':form}
    return render(request, 'register.html', context)


def userLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) 

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, f"Welcome {user.username.title()}" )
                return redirect('dashboard')

    context = {'form':form}
    return render(request, 'userlogin.html', context)

def userLogout(request):
    auth.logout(request)
    messages.success(request, "Goodbye! See you soon" )
    return redirect('index')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userLogin')
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    context = {'profile':profile}
    return render(request, 'profiles/dashboard.html',context)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userLogin')
def postThought(request):
    form = ThoughtPostForm()
    if request.method == 'POST':
        form = ThoughtPostForm(request.POST)
        if form.is_valid():
            # commit creates an instance before save 
            thought = form.save(commit=False)
            # to get the foregien-key: user
            thought.user= request.user
            thought.save()
            messages.success(request, "Great. Post is live!" )
            return redirect('myThoughts')

    context = {'form':form}
    return render(request, 'profiles/postThought.html', context)


@login_required(login_url='userLogin')
def myThoughts(request):
    current_user = request.user.id
    thoughts = Thought.objects.filter(user=current_user).order_by("-created")

    context = {'thoughts':thoughts}
    return render(request, 'profiles/mythoughts.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userLogin')
def updateThought(request, pk):
    
    thought = Thought.objects.get(id=pk)
    form = ThoughtUpdateForm(instance=thought)

    if request.method == 'POST':
        form = ThoughtUpdateForm(request.POST, instance=thought)

        if form.is_valid():
            form.save()
            messages.success(request, "Post Updated!" )
            return redirect("myThoughts")

    context = {'form':form}
    return render(request, 'profiles/updatethought.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='userLogin')
def deleteThought(request, pk):
    thought = Thought.objects.get(id=pk)
    if request.method == 'POST':
        thought.delete()
        messages.success(request, "Post Deleted!" )
        return redirect("myThoughts")
    
    return render(request, 'profiles/deleteThought.html')




@login_required(login_url='userLogin')
def manageProfile(request):
    form = UpdateUserForm(instance=request.user)

    profile = Profile.objects.get(user=request.user)

    form2 = UpdateProfileForm(instance=profile)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST,instance=request.user)
        form2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated..!" )
            return redirect("dashboard")

        if form2.is_valid():
            form2.save()
            messages.success(request, "Profile Updated..!" )
            return redirect("dashboard")

    context = {'form':form, 'form2':form2}
    return render(request, 'profiles/profile-management.html', context)


@login_required(login_url='userLogin')
def deleteAccount(request):
    if request.method == 'POST':

        deleteUser = User.objects.get(username=request.user)
        deleteUser.delete()
        return redirect('index')

    return render(request,'profiles/delete-account.html' )





    