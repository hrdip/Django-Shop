from django import forms
from shop.models import ProductModel, ProductImageModel
from ckeditor.widgets import CKEditorWidget

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    brief_description = forms.CharField(widget=CKEditorWidget())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs['class'] = 'form-control'
        self.fields["title"].widget.attrs['class'] = 'form-control'
        self.fields["slug"].widget.attrs['class'] = 'form-control'
        self.fields["description"].widget.attrs['class'] = 'form-control'
        self.fields["brief_description"].widget.attrs['class'] = 'form-control'
        self.fields["status"].widget.attrs['class'] = 'form-select'
        self.fields["discount_pecent"].widget.attrs['class'] = 'form-control'
        self.fields["price"].widget.attrs['class'] = 'form-control'
        self.fields["image"].widget.attrs['class'] = 'form-control'
        self.fields["stock"].widget.attrs['class'] = 'form-control'
        self.fields["stock"].widget.attrs['type'] = 'number'

    class Meta:
        model = ProductModel
        fields = [
            "category",
            "title",
            "slug",
            "description",
            "brief_description",
            "status",
            "discount_pecent",
            "price",
            "image",
            "stock",
        ]


class ProductImageForm(forms.ModelForm):


    class Meta:
        model = ProductImageModel
        fields = [
            "file",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['accept'] = 'image/png, image/jpg, image/jpeg'