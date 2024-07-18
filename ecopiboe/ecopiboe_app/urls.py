from django.urls import path
from . import views
from . import blog_view
from django.conf.urls.static import static
from django.conf import settings
from .views import visualize_ai_results
from django.urls import path
from .user_settings import user_settings

from .footer_pages import (
    about_us, careers, contact_us, blog, whitepapers, case_studies,
    help_center, faqs, support_services, feature_1, feature_2, feature_3
)


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='user_login'), 
    path('signup/', views.signup, name='signup'),
    path('login_success/', views.login_success, name='login_success'), 
    path('user_logout/', views.user_logout, name='user_logout'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('accounts/profile/', views.login_success, name='login_success'),
    
    path('felix_about/', views.felix_about, name='felix_about'),
    path('test_db_connection/', views.testing, name='test_db_connection/'),
    
    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('password_reset_success/', views.password_reset_success, name='password_reset_success'),
    path('reset_link_sent/', views.reset_link_sent, name='reset_link_sent'),
    path('videos/', views.video_page, name='video_page'),
    
    path('chatbot/', views.chatbot, name='chatbot'),
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
    
    
    path('improve_email/', views.improve_email, name='improve_email'),
    path('send-email/', views.send_email, name='send_email'),
    path('google-reauthorize/', views.google_reauthorize, name='google_reauthorize'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'), 
    
    #slugs
    path('blog/', blog_view.blog_list, name='blog_list'),
    path('blog/<int:pk>/', blog_view.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/', blog_view.blog_detail, name='blog_detail'),
    
    # path('test404/', views.test404, name='test404'),
    
    #User Settings
    path('settings/', user_settings.user_settings, name='user_settings'),
        
    #footer pages
    path('about/', about_us, name='about_us'),
    path('careers/', careers, name='careers'),
    path('contact/', contact_us, name='contact_us'),
    path('blog/', blog, name='blog'),
    path('whitepapers/', whitepapers, name='whitepapers'),
    path('case-studies/', case_studies, name='case_studies'),
    path('help-center/', help_center, name='help_center'),
    path('faqs/', faqs, name='faqs'),
    path('support-services/', support_services, name='support_services'),
    path('feature-1/', feature_1, name='feature_1'),
    path('feature-2/', feature_2, name='feature_2'),
    path('feature-3/', feature_3, name='feature_3'),

]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

