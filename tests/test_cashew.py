from cashew.plugin import Plugin, PluginMeta
from cashew.exceptions import *

import example.classes
from example.classes2 import Csv

class Data(example.classes.Data):
    """
    Docstring goes here.
    """
    @classmethod
    def load_class_from_locals(cls, class_name):
        from example.classes2 import *
        return locals()[class_name]

def test_must_inherit_from_plugin_class():
    try:
        class BadPlugin(object):
            __metaclass__ = PluginMeta

        raise Exception("should not get here")

    except AssertionError as e:
        assert str(e) == "BadPlugin should inherit from class Plugin"

def test_standardize_alias_or_aliases():
    assert Data.standardize_alias_or_aliases("foo") == ['foo']
    assert Data.standardize_alias_or_aliases(["foo"]) == ['foo']

def test_get_reference_to_qualified_class():
    pygments_filter_class = Data.get_reference_to_class("dexy.filters.pyg:PygmentsFilter")
    assert pygments_filter_class.__name__ == "PygmentsFilter"

def test_get_reference_to_class():
    assert Data.get_reference_to_class(Csv) == Csv
    assert Data.get_reference_to_class("Csv") == Csv

def test_check_docstring():
    try:
        class NoDocstring(Data):
            pass
    except InternalCashewException as e:
        assert "docstring required" in str(e)

def test_register_plugins():
    plugin_info = {
            'foo|altfoo' : ("Data", { "help" : "This is the foo plugin."})
            }

    assert not 'foo' in Data.plugins
    assert not 'altfoo' in Data.plugins

    Data.register_plugins(plugin_info)

    assert 'foo' in Data.plugins
    assert 'altfoo' in Data.plugins

    foo = Data.create_instance('foo', None)
    altfoo = Data.create_instance('altfoo', None)

    assert foo.setting('help') == "This is the foo plugin."
    assert altfoo.setting('help') == "This is the foo plugin."

    assert foo.name() == "Foo"
    assert altfoo.name() == "Foo"

def test_register_plugins_from_dict():
    plugin_info = {
            'bar|altbar' : { "class" : "Data",  "help" : "This is the bar plugin."}
            }

    assert not 'bar' in Data.plugins
    assert not 'altbar' in Data.plugins

    Data.register_plugins_from_dict(plugin_info)

    assert 'bar' in Data.plugins
    assert 'altbar' in Data.plugins

    bar = Data.create_instance('bar', None)
    altbar = Data.create_instance('altbar', None)

    assert bar.setting('help') == "This is the bar plugin."
    assert altbar.setting('help') == "This is the bar plugin."


class TestSettingsBase(Plugin):
    """
    Base class for settings class used in tests.
    """
    __metaclass__ = PluginMeta
    _settings = {
            'foo' : ("Foo setting", "This is value of foo set in TestSettingsBase")
            }

class NoSettingsOfMyOwn(TestSettingsBase):
    """
    A plugin which doesn't override foo.
    """
    aliases = ['nosettingsofmyown', 'twoaliases']

def test_no_settings_of_my_own():
    nosettingsofmyown = TestSettingsBase.create_instance('nosettingsofmyown')
    assert nosettingsofmyown.setting('foo') == "This is value of foo set in TestSettingsBase"

class OverrideFooSetting(TestSettingsBase):
    """
    A plugin which sets a different value for foo and also defines a new setting bar.
    """
    aliases = ['overridefoosetting']
    _settings = {
            'foo' : "I am overriding foo.",
            'bar' : ("The bar setting.", "Default value for the bar setting.")
            }

def test_override_settings():
    override = TestSettingsBase.create_instance('overridefoosetting')
    assert override.setting('foo') == "I am overriding foo."
    assert override.setting('bar') == "Default value for the bar setting."

class UnsetFoo(TestSettingsBase):
    """
    A plugin which unsets the 'foo' setting.
    """
    _unset = ['foo']
    aliases = ['unsetfoo']

def test_unsetting_settings():
    unsetfoo = TestSettingsBase.create_instance('unsetfoo')

    try:
        unsetfoo.setting('foo')
        raise Exception("should not get here")
    except UserFeedback as e:
        assert str(e) == "No setting named 'foo'"

class Inactive(TestSettingsBase):
    """
    An inactive filter.
    """
    aliases = ['inactive']
    def is_active(self):
        return False

def test_iter():
    aliases = sorted(instance.alias for instance in TestSettingsBase)
    assert aliases == ['nosettingsofmyown', 'overridefoosetting', 'unsetfoo']

def test_safe_setting():
    data = Data.create_instance('csv', None)
    assert data.setting('write-header') == True
    assert data.safe_setting('write-header') == True
    assert data.safe_setting('right-header') == None

def test_cant_create_new_setting_without_helpstring():
    data = Data.create_instance('csv', None)
    try:
        data.update_settings({ 'foo-bar' : 123 })
    except InternalCashewException as e:
        msg = "You must specify param 'foo-bar' as a tuple of (helpstring, value)"
        assert str(e) == msg

def test_foo():
    data = Data.create_instance('csv', None)
    data.update_settings({ 'write_header' : False })
    assert data.setting('write-header') == False

def test_skip_setting_values():
    data = Data.create_instance('csv', None)

    settings = ['csv-settings', 'delimiter', 'dialect', 'lineterminator', 'write-header']
    skip_settings = ['help', 'aliases']

    assert sorted(data.setting_values()) == sorted(settings + skip_settings)
    assert sorted(data.setting_values(skip_settings)) == settings

def test_retrieve_environment_variables():
    data = Data.create_instance('csv', None)
    data.update_settings({ "working-dir" : ("The current working directory.", "$PWD")})
    assert 'cashew' in data.setting('working-dir')

def test_escaped_dollar_sign():
    data = Data.create_instance('csv', None)
    data.update_settings({ "not-a-var" : ("This is not an environmetn variable.", "\$PWD")})
    assert data.setting('not-a-var') == "$PWD"

def test_invalid_get_ref_to_class():
    try:
        Data.get_reference_to_class(123)
    except InternalCashewException as e:
        assert "Unexpected Type" in str(e)
