from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Categoria
from .forms import PostForm
from apps.comentarios.forms import ComentarioForm
from apps.comentarios.models import Comentario

ORDENES = {
    "fecha_desc": "-fecha_hora",
    "fecha_asc": "fecha_hora",
    "titulo_asc": "titulo",
    "titulo_desc": "-titulo",
}




def _rol(u): 
    return getattr(u, "rol", "visitante")

def puede_crear(u): 
    return _rol(u) in ("escritor", "admin")

def puede_comentar(u): 
    return _rol(u) in ("lector", "escritor", "admin")

def puede_editar_post(user, post):
    r = _rol(user)
    return r in ("escritor", "admin") and (user == post.autor or r == "admin")

def feed_principal(request):
    orden = request.GET.get("orden", "fecha_desc")
    posts = (Post.objects.select_related("autor")
             .prefetch_related("categorias", "tags")
             .order_by(ORDENES.get(orden, "-fecha_hora")))
    categorias = Categoria.objects.all().order_by("nombre")
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "posts/feed.html", {
        "page_obj": page_obj, "categorias": categorias,
        "titulo_pagina": "Últimas publicaciones", "categoria_activa": None,
        "orden": orden,
    })

def feed_por_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    orden = request.GET.get("orden", "fecha_desc")
    posts = (Post.objects.filter(categorias=categoria)
             .select_related("autor").prefetch_related("categorias", "tags")
             .order_by(ORDENES.get(orden, "-fecha_hora")))
    categorias = Categoria.objects.all().order_by("nombre")
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "posts/feed.html", {
        "page_obj": page_obj, "categorias": categorias,
        "titulo_pagina": f"Categoría: {categoria.nombre}", "categoria_activa": categoria,
        "orden": orden,
    })

def post_detalle(request, pk):
    post = get_object_or_404(Post.objects.select_related("autor"), pk=pk)
    comentarios = post.comentarios.select_related("usuario").order_by("-fecha_hora")
    form = None
    if request.user.is_authenticated and puede_comentar(request.user):
        if request.method == "POST":
            form = ComentarioForm(request.POST)
            if form.is_valid():
                Comentario.objects.create(
                    post=post, usuario=request.user,
                    contenido=form.cleaned_data["contenido"]
                )
                messages.success(request, "¡Comentario publicado!")
                return redirect("posts:post_detalle", pk=post.pk)
        else:
            form = ComentarioForm()
    return render(request, "posts/post_detalle.html", {"post": post, "comentarios": comentarios, "form": form})

class PostCrearView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def test_func(self):
        return puede_crear(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "No tenés permisos para crear publicaciones.")
        return redirect("posts:feed")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, "¡Publicación creada!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("posts:post_detalle", kwargs={"pk": self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def test_func(self):
        return puede_editar_post(self.request.user, self.get_object())

    def handle_no_permission(self):
        messages.error(self.request, "No tenés permisos para editar esta publicación.")
        return redirect("posts:post_detalle", pk=self.get_object().pk)

    def form_valid(self, form):
        messages.success(self.request, "¡Publicación actualizada!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("posts:post_detalle", kwargs={"pk": self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("posts:feed")

    def test_func(self):
        return puede_editar_post(self.request.user, self.get_object())

    def handle_no_permission(self):
        messages.error(self.request, "No tenés permisos para eliminar esta publicación.")
        return redirect("posts:post_detalle", pk=self.get_object().pk)

def acerca(request):
    return render(request, "posts/acerca.html")

def contacto(request):
    return render(request, "posts/contacto.html")

def categorias_index(request):
    q = request.GET.get("q", "").strip()
    categorias = Categoria.objects.all().order_by("nombre")
    if q:
        categorias = categorias.filter(nombre__icontains=q)
    return render(request, "posts/categorias.html", {
        "categorias": categorias,
        "q": q,
        "titulo_pagina": "Categorías",
    })
