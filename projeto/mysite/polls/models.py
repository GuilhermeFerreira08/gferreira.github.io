from django.db import models
from django import forms
from django.core.validators import EmailValidator,ValidationError,RegexValidator
from django.urls import reverse
from django.contrib import auth
from regex import compile,match
# Create your models here.
class Endereco(forms.Form):
    rua = forms.CharField(required=True)
    compl = forms.CharField(required=True)
    cep = forms.IntegerField(label='xxxxx-xxx',required=True,validators = [RegexValidator(regex = compile(r'[^\D{5}-\D{3}$]'),message="somente caracteres numéricos")])
    prcl = forms.BooleanField(widget=forms.widgets.CheckboxInput(attrs={'class': 'checkbox-inline'}))
    default_data = {'rua': 'Rua', 'compl': 'nº'}
    
    class Meta():
        total_ordering_name=['rua','compl','cep','prcl']
        verbose_name_plural = "enderecos"
        
    def __str__(self):
        return f'{self.rua},{self.compl}-{self.cep}'

class Usuario(forms.ModelForm):
    nome = forms.CharField(label="nome",max_length=20,help_text="Insira nome de identificacao",error_messages={'blank': 'Utilize nome de cadastro'})
    email = forms.EmailField(label="email",max_length=50,empty_value=None,required=True,validators=[EmailValidator("entre com email válido")])
    cpf = forms.IntegerField(label="cpf",required=True)
    senha = forms.CharField(widget=forms.PasswordInput())
    cosenha = forms.CharField(widget=forms.PasswordInput())
    constraints = [models.CheckConstraint(check=models.Q(senha=cosenha), name='senha')]
        
    class Meta():        
        field = ['data_cadastro','status','end_cliente']
        exclude = ['id_cliente']
        unique_together = [['senha', 'cosenha']]
        indexes = [models.Index(fields=['nome','email','cpf'])]
    
    def clean_nome(self):
        return self.cleaned_data['nome']

class Cliente(models.Model):
    STATUS=[('Pad','padrão'),('Esp','especial'),('Prm','premium')]
    id_cliente = models.OneToOneField('Usuario',primary_key=True,on_delete=models.CASCADE)
    nome_cliente = models.CharField(max_length=35)
    data_cadastro = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=3,choices=STATUS,default='Pad')
    #end_cliente = models.ForeignKey('Endereco',on_delete=models.RESTRICT)
    
    class Meta():
        db_table = 'ecommerce_cliente'
            
    def __str__(self):
        return f'{self.id_cliente} - {self.nome_cliente}'

    def validate_cpf(self):
        pass


class Categoria(models.Model):
    produtos = models.ForeignKey('Produto',on_delete=models.CASCADE,blank=True,parent_link=True,related_name="categoria")
    nome = models.CharField(max_length=30,blank=False,primary_key=True)

    def __str__(self):
        return f'{self.nome}'

    def get_absolute_url(self):
        return reverse('categoria',args=[str(self.nome)])    

    def display_view_cat(self):
        return ',\n'.join(self.nome) 
    #display_view.short_description = 'ViewCategory'

class Produto(models.Model):
    id_produto = models.ForeignKey(Categoria,on_delete=models.RESTRICT,related_name='pk')
    nome_produto = models.CharField(max_length=100,primary_key=True)
    descricao = models.TextField(max_length=300)
    img_prdt = models.ImageField(upload_to='mysite',default='noimage.png')
    class Class(models.IntegerChoices):
        PESSIMO = 1
        BOM = 2
        REGULAR = 3
        OTIMO = 4      
    clsf = models.IntegerField(choices=Class.choices)

    class Meta():
        managed = True
        
    def __str__(self):
        return f'{self.id_produto}-{self.nome_produto}'

    def get_absolute_url(self):
        return reverse('detalhe_produto',args=[str(self.id_produto)])

    def display_view(self):
        return ' \n'.join('{p.nome_produto}-{p.descricao}')
    display_view.short_description = 'ViewProduct'


class Item(models.Model):
    item_produto = models.OnetoOneField(Produto,primary_key = True,on_delete=models.CASCADE) 
    preco = models.DecimalField(max_digits=5,decimal_places=2)
    quant_total = models.IntegerField(max_length=50)
    cond = models.CharField(choices=[('U','usado'),('N','novo')],default = None,blank = False)      
    
    class Meta(Meta.Produto):
        fields = __all__

    def get_absolute_url(self):
        return reverse('detalhe_produto',kwargs={'pk':self.id_produto})

class Cliente_compras(models.Model):
    id_cliente = model.OnetoOneField(Cliente, on_delete=models.CASCADE) #id do cliente
    cliente_compras = models.ForeignKey(ItemPedido,on_delete=models.CASCADE)#varios pedidos por cliente
    
       
import uuid
class ItemPedido(models.Model):
     ped_id = models.UUIDField(primary_key=True, default=uuid.uuid4)#id do item  
     comprado = models.BooleanField() 
        

        
#
