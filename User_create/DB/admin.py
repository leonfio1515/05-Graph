from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Client
from django.conf import settings
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export import fields
from import_export.widgets import ForeignKeyWidget
##########################################################################


class UsersAdmin(UserAdmin):
    list_display = (
        "username",
        "is_active",
        "is_staff",
        "id",
        "dni",
        "phone_number",
        "country"
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'dni', 'email',
         'country', 'city', 'address', 'number_address', 'phone_number', 'image_user')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    list_per_page = 25


class ClientResource(resources.ModelResource):
    id = fields.Field(column_name='id', attribute='id')
    user_create = fields.Field(column_name='usuario', attribute='usuario',widget=ForeignKeyWidget(settings.AUTH_USER_MODEL, field='username'))
    user_update = fields.Field(column_name='Usuario edicion', attribute='user_update',widget=ForeignKeyWidget(settings.AUTH_USER_MODEL, field='username'))
    date_create = fields.Field(column_name='Date create', attribute='date_create')
    date_update = fields.Field(column_name='Date update', attribute='date_update')

    name = fields.Field(column_name='name', attribute='name')
    dni = fields.Field(column_name='dni',attribute='dni')
    gender = fields.Field(column_name='gender',attribute='gender')
    country = fields.Field(column_name='country', attribute='country')
    sales = fields.Field(column_name='sales',attribute='sales')
    payment_type = fields.Field(column_name='payment_type',attribute='payment_type')


    class Meta:
        model = Client


class ClientAdmin(ImportExportActionModelAdmin):
    resource_class = ClientResource
    list_display = (
        "user_create",
        "date_create",

        "name",
        "dni",
        "gender",
        "country",
        "sales",
        "payment_type",
    )
    search_fields = (
        "user_create",
        "date_create",

        "name",
        "dni",
        "gender",
        "country",
        "sales",
        "payment_type",
    )
    list_per_page = 25
    exclude = ("user_update", "user_create",)


##########################################################################


admin.site.register(Users, UsersAdmin)

admin.site.register(Client, ClientAdmin)
