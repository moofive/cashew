from cashew.plugin import Plugin, PluginMeta

import example.classes
from example.classes1 import Csv

class Data(example.classes.Data):
    """
    Docstring goes here.
    """
    @classmethod
    def load_class_from_locals(cls, class_name):
        from example.classes1 import *
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

