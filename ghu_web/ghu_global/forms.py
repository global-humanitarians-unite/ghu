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

class CheckboxBlankerWidget(forms.CheckboxInput):
    """
    A checkbox which, when checked, blanks out the prepopulated field
    named target_field, re-populating it from source_field when
    necessary.
    """

    def __init__(self, target_field, source_field, **kwargs):
        if 'attrs' not in kwargs:
            kwargs['attrs'] = {}
        # XXX Don't hardcode the `id_' prefix here. Instead, use
        #     Field.auto_id somehow
        kwargs['attrs']['data-blanker-target-field'] = '#id_' + target_field
        kwargs['attrs']['data-blanker-source-field'] = '#id_' + source_field

        super().__init__(**kwargs)

    class Media:
        js = ('admin/js/checkbox_blanker.js',)

class CheckboxBlanker(forms.BooleanField):
    """
    A field which introduces a CheckboxblankerWidget with the provided
    target_field and source_field (see CheckboxBlankerWidget for
    details).
    """

    def __init__(self, target_field, source_field, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = CheckboxBlankerWidget(
                target_field=target_field,
                source_field=source_field)
        kwargs['required'] = False

        super().__init__(**kwargs)
