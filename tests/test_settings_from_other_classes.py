from cashew import Plugin, PluginMeta

class Report(Plugin):
    __metaclass__ = PluginMeta
    _settings = {}
    _other_class_settings = {
            'doc' : {
                'bar' : ("Bar setting.", None)
                }
            }

class Filter(Plugin):
    __metaclass__ = PluginMeta
    _settings = {}
    _other_class_settings = {
            'doc' : {
                'foo' : ("Foo setting", None)
                }
            }

class Document(Plugin):
    __metaclass__ = PluginMeta
    aliases = ['doc']

class SomeKindOfDocument(Document):
    """
    Some kind.
    """
    aliases = ['somekind']

def test_other_class_settings():
    assert sorted(PluginMeta._store_other_class_settings['doc']) == ['bar', 'foo']
    x = Document.create_instance('somekind')
    assert sorted(x.setting_values()) ==  ['aliases', 'bar', 'foo', 'help']
