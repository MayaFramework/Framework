from Framework.lib.ext_lib import dropbox
from Framework.lib.ext_lib.dropbox import files
from Framework.lib.ext_lib.dropbox import file_properties
from dropboxTemplate import DropboxTemplate


class DropboxMetadata(object):

    TOKENID = "JRK_a6mrxaAAAAAAAAAFAVrk1F0DewHl7V_eQrtBo7d6671VCUMaA3ylJ915VkTv"
    TEMPLATEID = "ptid:JRK_a6mrxaAAAAAAAAAFAw"

    def __init__(self, metadata):

        if not isinstance(metadata, files.Metadata):
            raise TypeError("Metadata must be 'files.Metadata', not {}".format(type(metadata)))

        self._metadata = metadata

    def __str__(self):
        return str(self.metadata)

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @property
    def name(self):
        return getattr(self.metadata, "name")

    @property
    def customProperties(self):
        property_groups = getattr(self.metadata, "property_groups", list())
        return property_groups[0] if property_groups else None

    def getValue(self, key):
        if not hasattr(self.metadata, key):
            raise ValueError("{} not in Metadata".format(key))
        return getattr(self.metadata, key)

    def getTemplate(self):
        if not self.customProperties:
            templateID = DropboxMetadata.TEMPLATEID
        else:
            templateID = self.customProperties.template_id
        dbx = dropbox.Dropbox(DropboxMetadata.TOKENID)
        try:
            return DropboxTemplate(dbx.file_properties_templates_get_for_team(templateID))
        except:
            return DropboxTemplate(dbx.file_properties_templates_get_for_user(templateID))

    def getTemplateFields(self, getNames=False):
        template = self.getTemplate()
        if getNames:
            return template.fieldsNames
        return template.fields

    def addCustomProperties(self):
        template = self.getTemplate()
        print template
        propertyFields = list()
        for name in template.fieldsNames:
            propertyFields.append(file_properties.PropertyField(name, "null"))
        return [file_properties.PropertyGroup(DropboxMetadata.TEMPLATEID, propertyFields)]

    def updateCustomProperties(self, **properties):
        fieldsNames = self.getTemplateFields(getNames=True)
        propertyFields = list()
        for key, value in properties.iteritems():
            if key not in fieldsNames:
                continue
            propertyFields.append(file_properties.PropertyField(key, value))
        return [file_properties.PropertyGroupUpdate(self.customProperties.template_id, propertyFields)]



