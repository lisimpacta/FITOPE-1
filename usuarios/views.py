from django.shortcuts import render


def vendas(request):
    return render(request, 'vendas.html')


def marketing(request):
    return render(request, 'marketing.html')


def financeiro(request):
    return render(request, 'financeiro.html')


def outros(request):
    return render(request, 'outros.html')
