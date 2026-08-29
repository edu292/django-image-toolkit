from django.contrib import admin


class ImageGridAdminMixin(admin.ModelAdmin):
    change_list_template = 'image_toolkit/admin/image_grid.html'

    image_field = 'file'
    name_field = 'name'

    grid_enable_edit = True
    grid_enable_copy = True
    grid_enable_delete = True

    def get_list_editable(self, request):
        editable = list(super().get_list_editable(request))
        if self.grid_enable_edit and self.name_field and self.name_field not in editable:
            editable.append(self.name_field)
        return tuple(editable)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            cl = response.context_data['cl']
            for obj in cl.result_list:
                file_attr = getattr(obj, self.image_field, None)

                obj.grid_image = file_attr
                obj.grid_title = getattr(obj, self.name_field, '') if self.name_field else ''
                obj.grid_name_field = self.name_field

                if file_attr and hasattr(file_attr, 'url'):
                    obj.grid_abs_url = request.build_absolute_uri(file_attr.url)
                else:
                    obj.grid_abs_url = ''

        return response

    class Media:
        css = {'all': ('image_toolkit/css/admin_image_grid.css',)}
        js = ('image_toolkit/js/admin_image_grid.js',)
