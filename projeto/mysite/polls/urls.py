# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('',views.index,name='index'),
    path('polls/usuario',views.ClienteCreate.as_view(),name='usuario'),
    path('polls/usuario/endereco',views.EnderecoDetailView.as_view(),name='endereco'),
    path('projeto/mysite/index/',views.IndexProdutos.as_view(),name='index'),
    path('projeto/mysite/index/sessao/<id>',views.DetailCliente.as_view(),name='sessao_cliente'),
    path('projeto/mysite/categoria/',view.CategoriaListView,name = 'categorias'),
    path('projeto/mysite/categoria/<nome>/',views.CategoriaDetailView, name = 'categoria'),
    path('projeto/mysite/categoria/<nome>/produto/',views.IndexProdutos.asview(), name='exibe_produtos'),
    path('projeto/mysite/categoria/<nome>/produto/<id>',views.DetailView.as_view(), name='detalhe_produto'),
    path('projeto/mysite/cliente/<id>/',views.ClienteCreate.cadastro().as_view(), name='cadastro'),
    path('projeto/mysite/cliente/<id>/atualiza',views.EnderecoUpdate.as_view(),name = 'atualiza_endereco'),
    path('projeto/mysite/cliente/<id>/',views.EnderecoDelete.as_view(),name = 'deleta_endereco'),
    path('projeto/mysite/cliente/<id>/compras/',views,name = 'carrinho'),
    path('projeto/mysite/categoria/<nome>/produto/<id>', views.DeleteItem.as_view()),name='deleta_compra'),
    ]
