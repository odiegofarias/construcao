from django.http import HttpResponse
from django.shortcuts import render
from .models import Categoria, Imagem, Produto
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


def add_produto(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        produtos = Produto.objects.all()

        context = {
            'categorias': categorias,
            'produtos': produtos
        }

        return render(request, 'estoque/add_produto.html', context)

    elif request.method == "POST":
        data = request.POST

        nome = data.get('nome')
        categoria = data.get('categoria')
        quantidade = data.get('quantidade')
        preco_compra = data.get('preco_compra')
        preco_venda = data.get('preco_venda')

        produto = Produto(
            nome=nome,
            # Mandando ID no template
            categoria_id=categoria,
            quantidade=quantidade,
            preco_compra=preco_compra,
            preco_venda=preco_venda,
        ) 
        produto.save()
        for imagem in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg'
            img = Image.open(imagem)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img)
            draw.text((20, 280), f"Construct {date.today()}", (255, 255, 255))
            output = BytesIO()
            img.save(output, format="JPEG", quality=80)
            output.seek(0)
            img_final = InMemoryUploadedFile(
                output,
                'ImageField',
                name,
                'Imagem/jpeg',
                sys.getsizeof(output),
                None,
            )

            img_padrao = Imagem(imagem = img_final, produto=produto)
            img_padrao.save()

        messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso.')
        return redirect(reverse('add_produto'))