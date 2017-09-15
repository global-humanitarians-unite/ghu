from django import forms

class RichTextWidget(forms.Textarea):
    """
    A CKEditor version of forms.Textarea designed for the Django admin.
    Must be used with RichTextField below for good results.
    """

    class Media:
        js = ('ghu_global/bower/ckeditor/ckeditor.js',)
        # Hide the <label> for CKEditor (WYSIWYG) fields. Otherwise in
        # the Admin, CKEditor gets all screwed up: the controls (bold,
        # italic, etc.) are to the right of the label, but the field is
        # below and it looks awful.
        css = {
            'all': ('ghu_global/css/hide-empty-labels.css',),
        }

    def __init__(self, **kwargs):
        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}
        # When ckeditor.js starts up, it looks for <textarea>s with the
        # ckeditor class and replaces them, so give our <textarea> the
        # ckeditor class
        kwargs['attrs']['class'] = kwargs['attrs'].get('class', '') + ' ckeditor'

        super().__init__(**kwargs)

class RichTextField(forms.CharField):
    """
    A form field which has no label (allowing the WYSIWYG to fill the
    width of the screen) and uses RichTextField to activate CKEditor.
    """

    def __init__(self, **kwargs):
        # Make the <label> element empty so hide-empty-labels.css
        # (pulled in by RichTextWidget above) will hide it. This class
        # basically exists to do this in a clean way; in a perfect world
        # you'd just use CharField with RichTextWidget
        kwargs['label'] = ''
        if 'widget' not in kwargs:
            kwargs['widget'] = RichTextWidget()

        super().__init__(**kwargs)

class CheckboxBlanker(forms.BooleanField):
    """

    """
    class Media:
        js = ('checkboxBlanker.js')
