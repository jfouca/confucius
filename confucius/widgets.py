from django import forms


class ForeignKeySearchInput(forms.TextInput):
    def __init__(self, attrs=None):
        super(ForeignKeySearchInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(ForeignKeySearchInput, self).render(name, value, attrs)
        return rendered + '<script>$(function(){$("#id_languages").autocomplete("/language/");});</script>'
