from django.conf import settings
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation.trans_real import get_language
from djangocms_table.utils import static_url
from djangocms_table.models import CssClass


class TableWidget(Textarea):
    class Media:
        js = [static_url(path) for path in (
                'js/jquery-1.9.1.min.js',
                'js/jquery.handsontable.full.js',
                'js/jquery.ui.position.js',
                'js/json2.js',
            )]
        css = {
            'all': [static_url(path) for path in (
                'css/jquery.handsontable.full.css',
            )],
        }

    def render_textarea(self, name, value, attrs=None):
        return super(TableWidget, self).render(name, value, attrs)

    def render_additions(self, name, value, attrs=None):
        css_classes = CssClass.objects.all().filter(table=self.form_instance.instance)
        language = get_language().split('-')[0]
        context = {
            'name': name,
            'language': language,
            'data': value,
            'STATIC_URL': settings.STATIC_URL,
            'css_classes': css_classes,
        }
        return mark_safe(render_to_string(
            'cms/plugins/widgets/table.html', context))

    def render(self, name, value, attrs=None):
        return self.render_textarea(name, value, attrs) + \
            self.render_additions(name, value, attrs)
