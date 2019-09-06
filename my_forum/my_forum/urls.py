
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_view

from  mainforum import views
from  accounts import views as accounts_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('boards/<int:pk>', views.board_topics, name="board_topics"),
    path('boards/<int:pk>/newMessage/', views.new_topics, name="new_topics"),
    path('signup/', accounts_view.signup, name="signup"),
    path('logout/', auth_view.LogoutView.as_view(), name="logout"),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name="login"),

    path('reset/', auth_view.PasswordResetView.as_view
    (template_name='password_reset.html',
     email_template_name='password_reset_email.html',
     subject_template_name='password_reset_subject.html'),
         name="password_reset"),

    path('reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name="password_reset_done"),

    re_path('^reset/(?P<puidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
            , auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
            name="password_reset_done"),

    path('reset/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name="password_reset_complete"),

    path('settings/password/', auth_view.PasswordChangeView.as_view(template_name='password_change.html'),
         name="password_change"),

    path('settings/password/done/', auth_view.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name="password_change_done"),

    path('boards/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name="topic_posts"),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_posts, name="reply_posts"),

]
