ffrom django.contrib import admin
from .models import Usuario,Cliente,Endereco,Produto,Categoria,Item
# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome','email','cpf','endereco','senha')
    #campos exibidos
    field = ['nome','email','cpf','endereco']
    #field.empty_value_display = 'None'
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nome_cliente', 'data_cadastro', 'status')
    field=[('nome_cliente','status'),'data_cadastro']
 #  inlines = [ProdutoInline,CategoriaInline]

    def display_nome(self,obj):
        return f'{obj.nome_cliente} - {obj.status}'

class EnderecoAdmin(admin.TabularInline):
    list_display=('rua','compl','cep','prcl')
    def get_min_num(self,request):
        return 2
    field = [('rua','compl','cep'),'prcl']

class ProdutoInline(admin.TabularInline):
    model = Produto
    fk_name = 'id_produto'
class CategoriaInline(admin.StackedInline):
    model = Categoria
    fk_name = 'produtos'
    
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id_produto','nome_produto','descricao','img_prdt','clsf')
    field = [('id_produto','nome_produto'),'descricao','img_prdt','clsf']
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome','produtos')
    field = ['nome']
class ItemAdmin(admin.ModelAdmin):
    list_display=('nome_produto','quant','preco','cond') 
    fieldsets = (
        (None, {
            'fields': ('id_produto', 'nome_produto')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'clsf')
        }),
        ('Disponibilidade',{
            'fields': ('quant',int('quant'*'preco'))
        }),
        (None,{
            'fields': ('img-prdt')
        }),
    )



admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Produto,ProdutoAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Item,ItemAdmin)
