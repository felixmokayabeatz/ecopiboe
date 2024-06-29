from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import visualize_ai_results
from django.views.generic import TemplateView
from django.urls import path, include


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='user_login'), 
    path('signup/', views.signup, name='signup'),
    # path('google-login/', views.google_login, name='google_login'),
    path('login_success/', views.login_success, name='login_success'), 
    path('user_logout/', views.user_logout, name='user_logout'),
    path('signup_success/', views.signup_success, name='signup_success'),
    
    path('accounts/profile/', views.signup_success, name='signup_success'),
    
    path('google/login/callback/', views.google_login_callback, name='google_login_callback'),
    
    path('felix_about/', views.felix_about, name='felix_about'),
    path('registered_users/', views.registered_users, name='registered_users'),
    path('export_users_csv/', views.export_users_csv, name='export_users_csv'),
    path('export_users_excel/', views.export_users_excel, name='export_users_excel'),
    path('testing/', views.testing, name='testing'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('password_reset_success/', views.password_reset_success, name='password_reset_success'),
    path('reset_link_sent/', views.reset_link_sent, name='reset_link_sent'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('videos/', views.video_page, name='video_page'),
    path('chat/', views.chat, name='chat'),
    path('ask_question/', views.ask_question, name='ask_question'),
    path('piano_ask/', views.piano_ask, name='piano_ask'),
    path('eco-footprint-assessment/', views.eco_footprint_assessment, name='eco_footprint_assessment'),
    path('assessment-complete/', views.assessment_complete, name='assessment_complete'),
    path('get_ai_responses/', views.get_ai_responses, name='get_ai_responses'),
    path('menu_f/', views.menu_f, name='menu_f'),
    
    path('get_ai_responses_error/', views.get_ai_responses_error, name='get_ai_responses_error'),
    path('visualize_ai_results/', visualize_ai_results, name='visualize_ai_results'),
    path('recommend_books/', views.recommend_books, name='book_recommendation'),
    path('summarize_book/', views.summarize_book, name='summarize_book'),
    path('piano/', views.piano, name='piano'),
   
    path('analyze_note/', views.analyze_note, name='analyze_note'), 
    

    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    
    path('improve_email/', views.improve_email, name='improve_email'),
    
    path('send-email/', views.send_email, name='send_email'),
    path('contact_us/', views.contact_us, name='contact_us'),
    
    #geminiAPI FILE analyser
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),
    path('delete/<int:pk>/', views.delete_file, name='delete_file'),
    

]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
