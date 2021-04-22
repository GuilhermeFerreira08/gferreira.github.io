from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,render,reverse,Http404
from polls.models import Usuario, Cliente,Endereco
#from polls.models import Produto, Item,Endereco,Categoria,Pedido
from django.core.exceptions import ValidationError
from django.views.generic import DetailView, CreateView, DeleteView, ListView,UpdateView,FormView

##revela o formulario do cliente
class ClienteView(FormView):
    template_name = "registration.html"
    form_class = Cliente
    success_url = '/registered'

    def cadastro(self,form):
        return super().form_valid(form)
    
# listar produtos 
class ProdutosListView(ListView):
    model = Produto
    context_object_name = 'produtos'
    template_name = 'mysite/index.html'

    def listar_produtos(request,words):
        try:
            itens_produtos = Item.objects.filter(nome_produto__icontains = words)[10] #filtrar os mais recentes no BD
        except Item.DoesNotExist:
            raise Http404("Não há item catalogado")
        return render(request,'mysite/index.html',context={'id':itens_produtos.id_produto,'nome':itens_produtos.nome_produto,'foto':itens_produtos.img_prdt,'class':itens.produtos.clsf})

    def listar_itens_usuario(self,usr):
        item = Item.objects.filter(usr)
        return item

    def listar_itens_cat(self,cat):
        item = Item.objects.filter(nome = cat)

    def get_nome_produto(self,request,keyword):
        it_p = Produto.objects.filter(nome_produto__icontains=keyword)
        num = it_p.count()
        return render(request,'mysite/exibicao.html',context={it_p.nome_produto,num}) 
    
    def get_classif(self,request,cl): 
        it_cl = Produto.objects.filter(clsf__exact=cl)
        num = it_cl.count()
        return redirect(exibe_produtos,context={it_cl.clsf}) 
    
    def get_countprdt(self,request):
        tudo = Produto.objects.all().count
        return tudo

class CategoriaListView(ListView):
    model = Categoria
    context_object_name = 'categoria'
    template_name = 'mysite/categoria.html'
    c = count_cat()
    
    def list_cat(self,c):
        lst_cat = Categoria.objects.all()[c]
        return lst_cat

    def count_cat(self):
        return Categoria.objects.all().count()

    def get_cat(self,n):
        return Categoria.objects.filter(categoria_nome=n) 

class DeleteCategoria(DeleteView):
    model = Categoria
    #template_name =
    def deleta_cat(self,n):
        return Categoria.objects.get(nome=n).delete()

class DeleteItem(DeleteView):
    model = Item
    def delete_all_item(self):
        return Item.objects.all().delete()
    def delete_item(self,t):
        return Item.objects.get(item_produto=t).delete()
    def delete_pedido(self,pd):
        pass
 
# listagem na pagina principal

class DetailItem(DetailView):
    model = Item
    template_name='mysite/exibicao.html'
#exibir produto
    def get_detail_item(self,request,item_produto):
        it = get_object_or_404(Item, pk=item_produto)
        return render(request, 'mysite/exibicao.html', context={'id': it.item_produto,'nome':it.nome_produto,'preco':it.preco,'condicao':it.cond})   

class DetailProduto(DetailView):
    model= Produto
    template_name='mysite/exibicao.html'

    def get_descr_produto(self,request,it):
        it_p = get_object_or_404(Produto, pk=it)
        return render(request, 'mysite/exibicao.html', context={'detalhes':it_p.descricao})

class ItemCreate(CreateView):
    model = Item
    fields = ['item_produto','preco','quant_total','cond']
    template_name_suffix = '_item'
    
    def create_item(self,*fields):
        pd = Item.objects.create(item_produto='item_produto',preco='preco',quant_total='quant_total',cond='cond')
        pd.save()

class ItemList(ListView):
    model = Item
    context_object_name = 'item'
    template_name='mysite/exibicao.html'

    def get_cond_itens(self,request,att):
        itens_cond = Item.objects.all().filter(cond__icontains=att)
        cn = get_list_or_404(itens_cond)
        return redirect('exibe-produtos',cn) 

    def get_preco_items(self,request,*pc): #retorna itens com faixa de preco
        itens_pr = Item.objects.all().filter(preco__in=pc)
        pr = get_list_or_404(itens_pr)
        return redirect('exibe-produtos',pr)

class PedidoCreate(CreateView):
    model = Pedido
    field = ['d_produto','nome_produto','descricao','img_prdt']
    p = Pedido.objects.create('d_produto','nome_produto','descricao','img_prdt')
    p.save()

class EnderecoCreate(CreateView):
    model = Endereco
    field = ['rua','compl','cep','prcl']
    
    def cadastro_endereco(self,request):
        if(request.method=='POST'):
            form_end = Endereco(request.POST)
        if(form_end.is_valid()):
            r=self.cleaned_data['rua']
            c=self.cleaned_data['compl']
            ce=self.cleaned_data['cep']
            p=self.cleaned_data['prcl']
            return HttpResponse(request,conte)
# listagem na pagina principal

class DetailItem(DetailView):
    model = Item
    template_name='mysite/exibicao.html'
#exibir produto
    def get_detail_item(self,request,item_produto):
        it = get_object_or_404(Item, pk=item_produto)
        return render(request, 'mysite/exibicao.html', context={'id': it.item_produto,'nome':it.nome_produto,'preco':it.preco,'condicao':it.cond})   

class DetailProduto(DetailView):
    model= Produto
    template_name='mysite/exibicao.html'

    def get_descr_produto(self,request,it):
        it_p = get_object_or_404(Produto, pk=it)
        return render(request, 'mysite/exibicao.html', context={'detalhes':it_p.descricao})

class ItemCreate(CreateView):
    model = Item
    fields = ['item_produto','preco','quant_total','cond']
    template_name_suffix = '_item'
    
    def create_item(self,*fields):
        pd = Item.objects.create(item_produto='item_produto',preco='preco',quant_total='quant_total',cond='cond')
        pd.save()

class ItemList(ListView):
    model = Item
    context_object_name = 'item'
    template_name='mysite/exibicao.html'

    def get_cond_itens(self,request,att):
        itens_cond = Item.objects.all().filter(cond__icontains=att)
        cn = get_list_or_404(itens_cond)
        return redirect('exibe-produtos',cn) 

    def get_preco_items(self,request,*pc): #retorna itens com faixa de preco
        itens_pr = Item.objects.all().filter(preco__in=pc)
        pr = get_list_or_404(itens_pr)
        return redirect('exibe-produtos',pr)

class PedidoCreate(CreateView):
    model = Pedido
    field = ['d_produto','nome_produto','descricao','img_prdt']
    p = Pedido.objects.create('d_produto','nome_produto','descricao','img_prdt')
    p.save()

class EnderecoCreate(CreateView):
    model = Endereco
    field = ['rua','compl','cep','prcl']
    
 
    def cadastro_endereco(self,request):
        if(request.method=='POST'):
            form_end = Endereco(request.POST)
        if(form_end.is_valid()):
            r=self.cleaned_data['rua']
            c=self.cleaned_data['compl']
            ce=self.cleaned_data['cep']
            p=self.cleaned_data['prcl']
            return HttpResponse(request,conte)
# listagem na pagina principal

class DetailItem(DetailView):
    model = Item
    template_name='mysite/exibicao.html'
#exibir produto
    def get_detail_item(self,request,item_produto):
        it = get_object_or_404(Item, pk=item_produto)
        return render(request, 'mysite/exibicao.html', context={'id': it.item_produto,'nome':it.nome_produto,'preco':it.preco,'condicao':it.cond})   

class DetailProduto(DetailView):
    model= Produto
    template_name='mysite/exibicao.html'

    def get_descr_produto(self,request,it):
        it_p = get_object_or_404(Produto, pk=it)
        return render(request, 'mysite/exibicao.html', context={'detalhes':it_p.descricao})

class ItemCreate(CreateView):
    model = Item
    fields = ['item_produto','preco','quant_total','cond']
    template_name_suffix = '_item'
    
    def create_item(self,*fields):
        pd = Item.objects.create(item_produto='item_produto',preco='preco',quant_total='quant_total',cond='cond')
        pd.save()

class ItemList(ListView):
    model = Item
    context_object_name = 'item'
    template_name='mysite/exibicao.html'

    def get_cond_itens(self,request,att):
        itens_cond = Item.objects.all().filter(cond__icontains=att)
        cn = get_list_or_404(itens_cond)
        return redirect('exibe-produtos',cn) 

    def get_preco_items(self,request,*pc): #retorna itens com faixa de preco
        itens_pr = Item.objects.all().filter(preco__in=pc)
        pr = get_list_or_404(itens_pr)
        return redirect('exibe-produtos',pr)

class PedidoCreate(CreateView):
    model = Pedido
    field = ['d_produto','nome_produto','descricao','img_prdt']
    p = Pedido.objects.create('d_produto','nome_produto','descricao','img_prdt')
    p.save()

class EnderecoCreate(CreateView):
    model = Endereco
    field = ['rua','compl','cep','prcl']
    
 
    def cadastro_endereco(self,request):
        if(request.method=='POST'):
            form_end = Endereco(request.POST)
        if(form_end.is_valid()):
            r=self.cleaned_data['rua']
            c=self.cleaned_data['compl']
            ce=self.cleaned_data['cep']
            p=self.cleaned_data['prcl']
            return HttpResponse(request,conte)

class EnderecoUpdateView(UpdateView):
    template_name = 'mysite/atualiza_endereco.html'
    model = Cliente
    field = 'end_cliente'
    context_object_name = 'endereco'
    success_url = 'mysite/index.html'
    template_name_suffix = '_endereco'
    
    def get_absolute_url(self):
        return reverse("atualiza_endereco",args=[field])
    
 
