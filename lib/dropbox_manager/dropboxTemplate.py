from Framework.lib.ext_lib.dropbox import file_properties

class DropboxTemplate(object):

    def __init__(self, template):

        if not isinstance(template, file_properties.GetTemplateResult):
            raise TypeError("Template must be a list of 'file_properties.PropertyFieldTemplate', not {}".format(type(template)))

        self._template = template

    def __str__(self):
        return str(self.template)

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

    @property
    def fieldsNames(self):
        return [propertyFieldTemplate.name for propertyFieldTemplate in self.fields]

    @property
    def fields(self):
        return self.template.fields

    # def getField(self, fieldKey):
    #     if not fieldKey in self.fieldsNames:
    #         raise RuntimeError("{} not in {}".format(fieldKey, str(self.fieldsNames)))
    #
    #     field = self._getKeyedField(fieldKey)
    #     if field:
    #         return getattr(field, fieldKey)
    #     return None
    #
    # def _getKeyedField(self, key):
    #     for field in self.fields:
    #         if key == field.name:
    #             return field
    #     return None
