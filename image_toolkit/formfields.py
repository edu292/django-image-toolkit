import io
from pathlib import Path

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from .widgets import ResizableImageWidget


class ResizableImageFormField(forms.MultiValueField):
    def __init__(self, allow_resize=True, allow_quality=True, default_quality=80, **kwargs):
        self.default_quality = default_quality

        fields = (
            forms.ImageField(required=kwargs.get('required', True)),
            forms.IntegerField(required=False, min_value=1),
            forms.IntegerField(required=False, min_value=1),
            forms.IntegerField(required=False, min_value=1, max_value=100),
        )

        widget = ResizableImageWidget(
            allow_resize=allow_resize, allow_quality=allow_quality, default_quality=default_quality
        )

        super().__init__(fields, widget=widget, require_all_fields=False, **kwargs)

    def compress(self, data_list):
        if not data_list or not data_list[0]:
            return None

        img_file, max_width, max_height, quality = data_list
        quality = quality or self.default_quality

        if not hasattr(img_file, 'read'):
            return img_file

        img = Image.open(img_file)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGBA')
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        if max_width or max_height:
            target_w = max_width or img.width
            target_h = max_height or img.height
            img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)

        output = io.BytesIO()
        img.save(output, format='WEBP', quality=quality)
        output.seek(0)

        new_name = Path(img_file.name).with_suffix('.webp').name
        return SimpleUploadedFile(new_name, output.read(), content_type='image/webp')
