from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    autor = models.ForeignKey(get_user_model(), verbose_name='Autor', on_delete=models.CASCADE)
    titulo = models.CharField('Titulo', max_length=100)
    texto = models.TextField('Texto', max_length=400)

    def __str__(self):
        return self.titulo


class Produto(models.Model):
    SKU = models.CharField('SKU', max_length=50)
    nome_produto = models.CharField('Nome do Produto', max_length=50, primary_key=True)
    cor = models.CharField('Cor', max_length=20)
    tamanho = models.CharField('Tamanho', max_length=2)
    categoria = models.CharField('Categoria', max_length=20)
    preco = models.DecimalField('Preço', max_digits=19, decimal_places=2)


class ProdutoPedido(models.Model):
    pedido_id = models.IntegerField('Id do Pedido', primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)
    quantidade = models.IntegerField('Quantidade')
    preco_unitario = models.DecimalField('Preço Unitátio', max_digits=19, decimal_places=2)


class Cliente(models.Model):
    cliente_id = models.IntegerField('Id do Cliente', primary_key=True)
    nome = models.CharField('Nome', max_length=255)
    sobrenome = models.CharField('Sobrenome', max_length=255)
    telefone = models.CharField('Telefone', max_length=255)
    endereco = models.CharField('Endereco', max_length=255)
    numero = models.CharField('Numero', max_length=10)
    cidade = models.CharField('Cidade', max_length=50)
    estado = models.CharField('Estado', max_length=2)
    cep = models.IntegerField('CEP')
    sexo = models.CharField('Sexo', max_length=255)


class Pedido(models.Model):
    pedido_id = models.IntegerField('Id do Pedido', primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)
    data_pedido = models.DateTimeField('Data do Pedido')
    data_pagamento = models.DateTimeField('Data do Pagamento')
    data_envio = models.DateTimeField('Data do Envio')
    status = models.CharField('Status', max_length=20)
    fonte_mkt = models.CharField('Fonte de Marketing', max_length=20)
    comentarios = models.CharField('Comentários', max_length=255)


class Pagamentos(models.Model):
    NF = models.CharField('Nota Fiscal', max_length=255)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, default=1)
    data_pagamento = models.DateTimeField('Data do Pagamento')
    meio_pagamento = models.CharField('Meio de Pagamento', max_length=20)
    valor = models.DecimalField('Valor do Pagamento', max_digits=19, decimal_places=2)


class ClienteOrigem(models.Model):
    cliente_id = models.IntegerField('Id do Cliente', primary_key=True)
    nome = models.CharField('Nome', max_length=255)
    sobrenome = models.CharField('Sobrenome', max_length=255)
    telefone = models.CharField('Telefone', max_length=255)
    cpf = models.CharField('CPF', max_length=12)
    endereco = models.CharField('Endereco', max_length=255)
    numero = models.CharField('Numero', max_length=10)
    bairro = models.CharField('Bairro', max_length=255, null=True)
    cidade = models.CharField('Cidade', max_length=50)
    estado = models.CharField('Estado', max_length=2)
    cep = models.IntegerField('CEP')
    sexo = models.CharField('Sexo', max_length=255)
    email = models.EmailField('E-mail', null=True)


class PedidoOrigem(models.Model):
    pedido_id = models.IntegerField('Id do Cliente', primary_key=True)
    cliente_id = models.ForeignKey(ClienteOrigem, on_delete=models.CASCADE, default=1)
    data_pedido = models.DateTimeField('Data do Pedido')
    data_pagamento = models.DateTimeField('Data do Pagamento')
    data_envio = models.DateTimeField('Data do Envio')
    status = models.CharField('Status', max_length=20)
    fonte_mkt = models.CharField('Fonte de Marketing', max_length=20)
    comentarios = models.CharField('Comentários', max_length=255)
    NF = models.CharField('Nota Fiscal', max_length=255)
    meio_pagamento = models.CharField('Meio de Pagamento', max_length=20)
    valor = models.DecimalField('Valor', max_digits=19, decimal_places=2)
    SKU_origem = models.CharField('SKU', max_length=50, null=True)
    quantidade = models.IntegerField('Quantidade')
    preco_unitario = models.DecimalField('Preço Unitario', max_digits=19, decimal_places=2)
    nome_produto = models.CharField('Nome do Produto', max_length=50)
    cor = models.CharField('Cor', max_length=20)
    tamanho = models.CharField('Tamanho', max_length=2)
    categoria = models.CharField('Categoria', max_length=20)
