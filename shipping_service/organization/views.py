from django.views.generic import ListView
from organization.models import NewManager
from shop_app.utils import DataMixin


class ContactsHome(DataMixin, ListView):
    """
    Представление для отображения контактной информации магазина.
    """
    model = NewManager
    template_name = 'shop_app/contacts.html'
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        """
        Набор данных для отображения контактной информации магазина.
        """
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Контактная информация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """
        Возвращает queryset с данными о руководителях организаций и связанными адресами.
        """
        return NewManager.objects.prefetch_related('addresses')
