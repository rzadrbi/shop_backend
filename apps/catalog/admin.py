from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from .models import Category, Attribute, CategoryAttribute, Product, ProductAttributeValue
from .forms import ProductForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # change_form_template = 'admin/catalog/product/change_form.html'
    add_form_template = 'admin/catalog/product/change_form.html'

    def add_view(self, request, form_url='', extra_context=None):
        category_id = request.GET.get('category')

        if not category_id:
            return redirect('admin:catalog_product_select_category')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            self.message_user(request, "Category not found.", level='error')
            return redirect('admin:catalog_product_select_category')


        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            attributes = category.attributes.all()
            if form.is_valid():
                product = form.save(commit=False)
                product.category = category
                product.save()
                for attr in attributes:
                    field_name = f'attr_{attr.attribute.id}'
                    raw_value = request.POST.get(field_name)

                    if raw_value:
                        value_kwargs = {
                            'product': product,
                            'attribute': attr.attribute
                        }
                        if attr.attribute.data_type == 'str':
                            value_kwargs['value_str'] = raw_value
                        elif attr.attribute.data_type == 'int':
                            try:
                                value_kwargs['value_int'] = int(raw_value)
                            except ValueError:
                                continue
                        elif attr.attribute.data_type == 'dec':
                            try:
                                value_kwargs['value_dec'] = float(raw_value)
                            except ValueError:
                                continue

                        from .models import ProductAttributeValue
                        ProductAttributeValue.objects.create(**value_kwargs)
                self.message_user(request, "Product created.")
                return redirect('admin:catalog_product_changelist')
        else:
            form = ProductForm(initial={'category': category.id})

        attributes = category.attributes.all()

        context = {
            **self.admin_site.each_context(request),
            'title': 'Add Product',
            'form': form,
            'category': category,
            'attributes': attributes,
            'is_popup': False,
            'add': True,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'change': False,
            'has_view_permission': self.has_view_permission(request),
            'has_add_permission': self.has_add_permission(request),
            'has_change_permission': self.has_change_permission(request),
            'has_delete_permission': self.has_delete_permission(request),
            'save_as': False,
            'has_editable_inline_admin_formsets': False,
        }

        return render(request, self.add_form_template, context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        product = self.get_object(request, object_id)
        attr_values = product.attr_values.select_related('attribute')

        extra_context['attributes'] = [
            {
                'attribute': attr.attribute,
                'value': attr.value_str or attr.value_int or attr.value_dec
            } for attr in attr_values
        ]
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['category'].disabled = True
        return form

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'select-category/',
                self.admin_site.admin_view(self.select_category),
                name='catalog_product_select_category'
            ),
        ]
        return custom_urls + urls

    def select_category(self, request):
        if request.method == 'POST':
            category_id = request.POST.get('category')
            add_url = reverse('admin:catalog_product_add')
            print("Selected Category ID:", category_id)
            return redirect(f'{add_url}?category={category_id}')

        categories = Category.objects.all()
        return render(
            request,
            'admin/catalog/product/select_category.html',
            {'categories': categories}
        )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        category_id = request.GET.get('category')
        if category_id:
            initial['category'] = category_id
        return initial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_type')


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute')


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute',)
