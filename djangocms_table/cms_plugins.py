from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from models import Table
from djangocms_table.forms import TableForm
from django.utils import simplejson
from djangocms_table.utils import static_url
from django.http import HttpResponseRedirect
from django.contrib import admin
from djangocms_table.models import CssClass

class CssClassInline(admin.TabularInline):
    model = CssClass
    extra = 0
    verbose_name_plural = "css classes"
    

class TablePlugin(CMSPluginBase):
    model = Table
    form = TableForm
    name = _("Table")
    render_template = "cms/plugins/table.html"
    text_enabled = True
    
    inlines = [CssClassInline,]

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Headers'), {

            'fields': (('headers_top', 'headers_left', 'headers_bottom'),)
        }),
        (None, {
            'fields': ('table_data', 'css_data','csv_upload')
        })
    )

    def render(self, context, instance, placeholder):
        try:
            data = simplejson.loads(instance.table_data)
            css_data = simplejson.loads(instance.css_data)
            for i in xrange(len(data)):
                data[i] = zip(data[i],css_data[i])
        except:
            data = "error"
        context.update({
            'name': instance.name,
            'data': data,
            'instance':instance,
        })
        return context

    def icon_src(self, instance):
        return static_url("img/table.png")

    def response_change(self, request, obj):
        response = super(TablePlugin, self).response_change(request, obj)
        if 'csv_upload' in request.FILES.keys():
            self.object_successfully_changed = False
        return response

plugin_pool.register_plugin(TablePlugin)
