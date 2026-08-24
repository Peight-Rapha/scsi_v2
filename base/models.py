from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import get_object_or_404


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        abstract = True


class BrokerageQuerySet(models.QuerySet):
    def for_brokerage(self, brokerage):
        if brokerage is None:
            return self.none()
        return self.filter(brokerage=brokerage)


class BrokerageManager(models.Manager.from_queryset(BrokerageQuerySet)):
    pass


class BrokerageModel(TimeStampedModel):
    brokerage = models.ForeignKey(
        'brokerages.Brokerage',
        verbose_name='corretora',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_set',
        db_index=True,
    )

    objects = BrokerageManager()

    class Meta:
        abstract = True


class TenantQuerySetMixin:
    def get_brokerage(self):
        return getattr(self.request, 'brokerage', None)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.for_brokerage(self.get_brokerage())


class TenantObjectMixin(TenantQuerySetMixin):
    def form_valid(self, form):
        if hasattr(form.instance, 'brokerage_id') and not form.instance.brokerage_id:
            form.instance.brokerage = self.get_brokerage()
        return super().form_valid(form)


class BrokerageScopedFormMixin:
    brokerage_scoped_fields = ()

    def __init__(self, *args, brokerage=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.brokerage = brokerage
        if brokerage and hasattr(self.instance, 'brokerage_id') and not self.instance.brokerage_id:
            self.instance.brokerage = brokerage
        if not brokerage:
            return
        for field_name in self.brokerage_scoped_fields:
            if field_name in self.fields:
                self.fields[field_name].queryset = self.fields[field_name].queryset.for_brokerage(brokerage)


class BrokerageScopedFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['brokerage'] = self.get_brokerage()
        return kwargs


class CurrentBrokerageRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, 'is_authenticated', False):
            return super().dispatch(request, *args, **kwargs)
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not getattr(request, 'brokerage', None):
            raise PermissionDenied('Usuário sem corretora ativa.')
        return super().dispatch(request, *args, **kwargs)


class TenantAdminMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.for_brokerage(getattr(request.user, 'brokerage', None))

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'brokerage_id') and not obj.brokerage_id and not request.user.is_superuser:
            obj.brokerage = request.user.brokerage
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if request.user.is_superuser:
            return formfield
        queryset = getattr(formfield, 'queryset', None)
        if queryset is not None and hasattr(queryset, 'for_brokerage'):
            formfield.queryset = queryset.for_brokerage(getattr(request.user, 'brokerage', None))
        return formfield


def get_tenant_object_or_404(model, brokerage, **kwargs):
    return get_object_or_404(model.objects.for_brokerage(brokerage), **kwargs)


def user_can_access_brokerage(user, brokerage):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return getattr(user, 'brokerage_id', None) == getattr(brokerage, 'id', None)
