from django.contrib import admin


class ImageGridAdminMixin(admin.ModelAdmin):
    change_list_template = 'image_toolkit/admin/image_grid.html'
    image_field = 'file'
    name_field = 'name'
    edit_page = True

    def get_list_editable(self, request):
        editable = list(super().get_list_editable(request))
        if self.name_field and self.name_field not in editable:
            editable.append(self.name_field)
        return tuple(editable)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            cl = response.context_data['cl']
            for obj in cl.result_list:
                file_attr = getattr(obj, self.image_field, None)
                obj._image = file_attr
                obj._name = getattr(obj, self.name_field, '')
                obj._name_field = self.name_field
                obj._abs_url = request.build_absolute_uri(file_attr.url) if file_attr else ''

        return response

    class Media:
        css = {'all': ('image_toolkit/css/admin_image_grid.css',)}
        js = ('image_toolkit/js/admin_image_grid.js',)
