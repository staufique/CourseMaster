from functools import wraps
from django.shortcuts import render

# Create your views here.

# views.py
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.decorators import permission_required,login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .models import Course
from django.shortcuts import render, redirect



def index(request):
    return render(request,'index.html')


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        city = request.POST.get('city')
        password = request.POST.get('password')

        user = User.objects.create_user(name=name, email=email, phone=phone, dob=dob, city=city, password=password)
        if user:
            return redirect('login')
        else:
            return HttpResponse('Failed to create user', status=400)

    return render(request, 'signup.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            access_token = generate_access_token(user)
            response = redirect('dashboard')
            response.set_cookie('access_token', access_token)
            return response
        else:
            return HttpResponse('Invalid credentials', status=401)
    return render(request, 'login.html')

def logout_view(request):
    response = redirect('login')
    response.delete_cookie('access_token')
    return response

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return HttpResponse('Session expired. Please login again.', status=401)
            except jwt.InvalidTokenError:
                return HttpResponse('Invalid token. Please login again.', status=401)
        else:
            return redirect('login')
    return wrapper


@custom_login_required
def dashboard(request):
    # This code block will only be executed if the user is authenticated
    user = request.user
    return render(request, 'dashboard.html', {'user': user})





@custom_login_required
@permission_required('app.add_user', raise_exception=True)
def add_view(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        city = request.POST.get('city')
        password = request.POST.get('password')
        # Create new instance of User
        user = User.objects.create_user(email=email, password=password, name=name, phone=phone, dob=dob, city=city)
        return redirect('adduser')  # Replace 'success_url' with the URL you want to redirect after successful addition
    return render(request, 'adduser.html')



@custom_login_required
@permission_required('app.change_user', raise_exception=True)
def update_view(request, pk):
    instance = get_object_or_404(User, pk=pk)  # Assuming pk is the primary key of your model
    if request.method == 'POST':
        # Handle form submission
        instance.name = request.POST.get('name')
        instance.email = request.POST.get('email')
        instance.phone = request.POST.get('phone')
        instance.dob = request.POST.get('dob')
        instance.city = request.POST.get('city')
        instance.set_password(request.POST.get('password'))  # Set new password
        instance.save()
        return redirect('updateuser')  # Replace 'success_url' with the URL you want to redirect after successful update
    return render(request, 'updateuser.html', {'instance': instance})




@custom_login_required
def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

@custom_login_required
def buy_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        user.courses.add(course)
        return redirect('view-courses')
    else:
        return HttpResponse('Method not allowed', status=405)

@custom_login_required
def my_courses(request):
    user = request.user
    courses = user.courses.all()
    return render(request, 'my_course.html', {'courses': courses, 'user': user})

@custom_login_required
@permission_required('app.add_course', raise_exception=True)
def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        Course.objects.create(name=name, price=price)
        return redirect('my-courses')
    return render(request, 'add_course.html')

@custom_login_required
@permission_required('app.change_course', raise_exception=True)
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.name = request.POST.get('name')
        course.price = request.POST.get('price')
        course.save()
        return redirect('view-courses')
    return render(request, 'edit_course.html', {'course': course})

@custom_login_required
@permission_required('app.delete_course', raise_exception=True)
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('view-courses')
    return render(request, 'delete_course.html', {'course': course})

@custom_login_required
@permission_required('app.view_course', raise_exception=True)
def user_course_stats(request):
    courses = Course.objects.all()
    user_course_count = {}
    for course in courses:
        user_count = User.objects.filter(courses=course).count()
        user_course_count[course] = user_count
    return render(request, 'user_course_stats.html', {'user_course_count': user_course_count})
