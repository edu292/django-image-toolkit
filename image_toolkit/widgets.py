from typing import Any

from django import forms


class PreviewImageInput(forms.FileInput):
    template_name = 'image_toolkit/preview_image_input.html'

    def __init__(self, attrs=None, placeholder=None):
        self.placeholder = placeholder
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['placeholder'] = self.placeholder
        return context

    def format_value(self, value: Any) -> str | None:
        return value


class CamImageInput(forms.FileInput):
    template_name = 'image_toolkit/cam_image_input.html'

    def __init__(self, capture_width=1920, capture_height=1080, attrs=None):
        self.capture_width = capture_width
        self.capture_height = capture_height
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['capture_width'] = self.capture_width
        context['widget']['capture_height'] = self.capture_height
        exclude = {'name', 'class', 'id'}

        extra_attrs = {k: v for k, v in context['widget']['attrs'].items() if k not in exclude}

        context['widget']['extra_attrs'] = extra_attrs

        return context

    def format_value(self, value):
        return value


class ResizableImageWidget(forms.MultiWidget):
    def __init__(self, allow_resize=True, allow_quality=True, default_quality=80, attrs=None):
        self.default_quality = default_quality

        DimWidget = forms.NumberInput if allow_resize else forms.HiddenInput
        QualWidget = forms.NumberInput if allow_quality else forms.HiddenInput

        widgets = (
            forms.FileInput(attrs={'accept': 'image/*'}),
            DimWidget(attrs={'placeholder': 'Max Width (px)', 'min': 1}),
            DimWidget(attrs={'placeholder': 'Max Height (px)', 'min': 1}),
            QualWidget(attrs={'placeholder': 'Quality (1-100)', 'min': 1, 'max': 100}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        return [value, None, None, self.default_quality] if value else [None, None, None, self.default_quality]
