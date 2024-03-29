# urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path("",views.index,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('adduser/', views.add_view, name='adduser'),
    path('updateuser/<int:pk>', views.update_view, name='updateuser'),
    path('courses/', views.view_courses, name='view-courses'),
    path('buy/<int:course_id>/', views.buy_course, name='buy-course'),
    path('my-courses/', views.my_courses, name='my-courses'),
    path('add-course/', views.add_course, name='add-course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit-course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete-course'),
    path('course-stats/', views.user_course_stats, name='user-course-stats'),
]
