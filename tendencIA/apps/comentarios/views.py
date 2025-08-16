from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from .models import Comentario
from .forms import ComentarioForm

def _rol(u):
    return getattr(u, "rol", "visitante")

def puede_editar_comentario(user, comentario):
    """
    Puede editar: dueño, escritor o admin.
    (Antes: dueño o admin)
    """
    return user.is_authenticated and (
        comentario.usuario == user or _rol(user) in ("escritor", "admin")
    )

def puede_eliminar_comentario(user, comentario):
    # Propietario, escritor o admin (ya lo tenías así)
    return user.is_authenticated and (
        comentario.usuario == user or _rol(user) in ("escritor", "admin")
    )

class ComentarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = "comentarios/comentario_form.html"

    def test_func(self):
        return puede_editar_comentario(self.request.user, self.get_object())

    def form_valid(self, form):
        messages.success(self.request, "Comentario actualizado.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("posts:post_detalle", kwargs={"pk": self.object.post.pk})

class ComentarioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = "comentarios/comentario_confirm_delete.html"

    def test_func(self):
        return puede_eliminar_comentario(self.request.user, self.get_object())

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comentario eliminado.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("posts:post_detalle", kwargs={"pk": self.object.post.pk})
