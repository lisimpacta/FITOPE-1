from django.contrib import admin

from .models import Post, Produto, ProdutoPedido, Cliente, Pedido, Pagamentos, ClienteOrigem, PedidoOrigem

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', '_autor')
    exclude = ['autor',]

    def _autor(self, instance):
        return f'{instance.autor.get_full_name()}'

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(autor=request.user)

    def save_model(self, request, obj, form, change):
        obj.autor = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Produto)
admin.site.register(ProdutoPedido)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Pagamentos)
admin.site.register(ClienteOrigem)
admin.site.register(PedidoOrigem)
