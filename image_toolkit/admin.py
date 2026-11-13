class ImageGridAdminMixin:
    change_list_template = 'image_toolkit/admin/image_grid.html'

    grid_image_field = 'file'
    grid_title_field = 'name'

    grid_list_edit = True
    grid_enable_copy = True
    grid_enable_delete = True
    grid_edit_page = False

    def get_list_display(self, request):
        display = list(super().get_list_display(request))
        if self.grid_image_field and self.grid_image_field not in display:
            display.append(self.grid_image_field)
        if self.grid_title_field and self.grid_title_field not in display:
            display.append(self.grid_title_field)
        return tuple(display)

    def get_list_display_links(self, request, list_display):
        if self.grid_list_edit and self.grid_image_field:
            return (self.grid_image_field,)

        return super().get_list_display_links(request, list_display)

    def changelist_view(self, request, extra_context=None):
        if self.grid_list_edit and self.grid_title_field:
            if not getattr(self, 'list_editable', None):
                self.list_editable = []

            editable = list(self.list_editable)
            if self.grid_title_field not in editable:
                editable.append(self.grid_title_field)
                self.list_editable = tuple(editable)

        response = super().changelist_view(request, extra_context=extra_context)

        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            cl = response.context_data['cl']

            form_iter = iter(cl.formset.forms) if cl.formset else None

            for obj in cl.result_list:
                file_attr = getattr(obj, self.grid_image_field, None)

                obj.grid_image = file_attr
                obj.grid_title = getattr(obj, self.grid_title_field, '') if self.grid_title_field else ''
                obj.grid_tile_field = self.grid_title_field

                if file_attr and hasattr(file_attr, 'url'):
                    obj.grid_abs_url = request.build_absolute_uri(file_attr.url)
                else:
                    obj.grid_abs_url = ''

                if form_iter:
                    form = next(form_iter)
                    obj.grid_form = form
                    if self.grid_title_field and self.grid_title_field in form.fields:
                        form.fields[self.grid_title_field].widget.attrs['class'] = 'image-card__input'
                        obj.grid_title_input = form[self.grid_title_field]

        return response

    class Media:
        css = {'all': ('image_toolkit/css/admin_image_grid.css',)}
        js = ('image_toolkit/js/admin_image_grid.js',)
