from django.urls import path
from . import views
from apps.comentarios.views import ComentarioUpdateView, ComentarioDeleteView

app_name = "posts"

urlpatterns = [
    path("", views.feed_principal, name="feed"),
    path("categorias/", views.categorias_index, name="categorias"),          # <-- NUEVA
    path("categoria/<int:pk>/", views.feed_por_categoria, name="feed_categoria"),

    path("post/<int:pk>/", views.post_detalle, name="post_detalle"),
    path("post/nuevo/", views.PostCrearView.as_view(), name="post_crear"),
    path("post/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post_editar"),
    path("post/<int:pk>/eliminar/", views.PostDeleteView.as_view(), name="post_eliminar"),

    # Comentarios
    path("comentario/<int:pk>/editar/", ComentarioUpdateView.as_view(), name="comentario_editar"),
    path("comentario/<int:pk>/eliminar/", ComentarioDeleteView.as_view(), name="comentario_eliminar"),

    # Estáticas mínimas
    path("acerca/", views.acerca, name="acerca"),
    path("contacto/", views.contacto, name="contacto"),
]
