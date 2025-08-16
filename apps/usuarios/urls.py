from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
from . import views

app_name = "usuarios"

urlpatterns = [
    # Autenticación
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=reverse_lazy("usuarios:login")),
        name="logout",
    ),

    # Registro y perfil
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/editar/", views.profile_edit, name="profile_edit"),

    # Mis comentarios
    path("mis-comentarios/", views.mis_comentarios, name="mis_comentarios"),

    # Cambio de contraseña
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form_public.html",
            success_url=reverse_lazy("usuarios:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done_public.html"
        ),
        name="password_change_done",
    ),

    # Recuperación de contraseña
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form_public.html",
            email_template_name="registration/password_reset_email.txt",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("usuarios:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done_public.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm_public.html",
            success_url=reverse_lazy("usuarios:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete_public.html"
        ),
        name="password_reset_complete",
    ),
]
