from django import forms
from .models import Comment
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget
import bleach
from django.conf import settings

widget = CKEditorWidget(config_name='default')
class CommentForm(forms.ModelForm):
    #content = forms.CharField(widget=CKEditorWidget(config_name='default'))
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        print ('hello')
        content = self.cleaned_data.get('content')
        print (content)
        cleaned_text = bleach.clean(content, settings.BLEACH_VALID_TAGS, settings.BLEACH_VALID_ATTRS, settings.BLEACH_VALID_STYLES)
        return cleaned_text #sanitize html
