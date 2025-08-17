from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, ProfileUpdateForm
from apps.comentarios.models import Comentario


# ---------- Registro ----------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Asegurar rol por defecto = lector si no viene
            user = form.save(commit=False)
            if not getattr(user, "rol", None):
                try:
                    user.rol = user.Rol.LECTOR
                except Exception:
                    user.rol = "lector"
            user.save()
            login(request, user)
            return redirect("usuarios:profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "usuarios/register.html", {"form": form})


# ---------- Perfil ----------
@login_required
def profile(request):
    # Últimos 5 comentarios del usuario (para mostrar en el perfil)
    ultimos_comentarios = (
        Comentario.objects
        .filter(usuario=request.user)
        .select_related("post")
        .order_by("-fecha_hora")[:5]
    )
    return render(request, "usuarios/profile.html", {
        "ultimos_comentarios": ultimos_comentarios
    })


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Perfil actualizado correctamente!")
            return redirect("usuarios:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "usuarios/profile_edit.html", {"form": form})


# ---------- Mis comentarios ----------
@login_required
def mis_comentarios(request):
    qs = (
        Comentario.objects
        .filter(usuario=request.user)
        .select_related("post")
        .order_by("-fecha_hora")
    )
    page_obj = Paginator(qs, 10).get_page(request.GET.get("page"))
    return render(request, "usuarios/mis_comentarios.html", {
        "page_obj": page_obj,
        "titulo_pagina": "Mis comentarios",
    })

