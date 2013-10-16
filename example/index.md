= Cashew Documentation
:toc:
:source-highlighter: pygments

== Introduction

Cashew is a plugin system for python, based on the ideas in
<http://effbot.org/zone/metaclass-plugins.htm>.

The goal of Cashew is to let you easily modify the behavior of a tool by using
configuration options, and, when you need to, by writing custom code also.

This means that you can configure a system using a data format such as YAML or
JSON, or create a nice front-end for users which exposes the available
configuration options in a user-friendly way.

You identify a subclass and/or a preconfigured bundle of settings by an alias,
and settings can further be modified at runtime to allow for multiple levels of
configuration.

== Usage Guide

=== Creating a Base Class

The first step in creating a plugin system is to create a base class, which should be a subclass of the Plugin class, and which should specify PluginMeta as its metaclass:

{{ d['classes.py|idio|asciisyn']['imports'] }}
{{ d['classes.py|idio|asciisyn']['create-plugin-base-class'] }}

There's a little about the `__metaclass__` property 
http://docs.python.org/2/reference/datamodel.html#customizing-class-creation[here in the python docs]
and several articles online if you search.

You can do anything else you normally do with a base class, like implement
instance and class methods to be shared among all subclasses.

{{ d['classes.py|idio|asciisyn']['methods'] }}

You can make as many different base classes as you want in your project, and
each will be an independent plugin system. For example, in
http://dexy.it[dexy] the https://github.com/dexy/dexy/blob/develop/dexy/filter.py[Filter class], https://github.com/dexy/dexy/blob/develop/dexy/reporter.py[Reporter class], https://github.com/dexy/dexy/blob/develop/dexy/data.py[Data class] and
several others are implemented via plugins.

=== Plugin Registration

The `__init__` method in PluginMeta handles plugin registration:

[source,python]
----
{{ d['/cashew/plugin.py|pydoc']['PluginMeta.__init__:source'] }}
----

When this method is called on the base class itself (in our example the Data
class), it creates an empty dictionary named `plugins`, and when it is
subsequently called on subclasses, it calls the `register_plugin` method which
populates the `plugins` dictionary on the base class.

The `plugins` dictionary keys are the `aliases` which are defined for each
class we want to be accessible, and the values are a tuple of class names (or
instances) and dictionaries with settings. The key to Cashew's flexibility is
that the plugins dictionary can be populated directly, as well as being
populated automagically when the base class is subclassed.

In order for the automagic to happen, you need to actually load the python
modules in which subclasses are defined.

{{ d['usage1.py|idio|pycon|asciisyn']['plugins'] }}

A nice way to do this is with a
https://github.com/dexy/dexy/blob/develop/dexy/load_plugins.py[`load_plugins`]
module which does nothing but import all the modules in which you have defined
plugin subclasses.

To actually use plugins, `PluginMeta` defines a `create_instance` factory
method which takes an alias as its argument, and optionally accepts positional
and keyword arguments to be passed to a constructor.

[source,python]
----
{{ d['/cashew/plugin.py|pydoc']['PluginMeta.create_instance:source'] }}
----

Here's an example of using the `create_instance` method for a plugin based on
the `Data` class. As we saw above, the constructor `__init__` takes a single
positional argument, and we pass a positional argument to the `create_instance`
method:

{{ d['usage1.py|idio|pycon|asciisyn']['json-example-type'] }}

=== Basic Subclassing Example

Here are two examples of simple classes which subclass `Data`, and each define
a different style of presenting the contents of the `data` attribute:

{{ d['classes1.py|idio|asciisyn']['json-subclass'] }}

{{ d['classes1.py|idio|asciisyn']['csv-subclass'] }}

Required features:

- Subclass the `Data` class (directly or indirectly).
- Define one or more aliases (unless you don't want people to be able to use that class directly).
- Provide a docstring (or a 'help' setting).

Here's the full usage example, parts of which we have seen already.

We import the `Data` class from `classes.py`:

{{ d['usage1.py|idio|pycon|asciisyn']['import'] }}

We define some `example_data`:

{{ d['usage1.py|idio|pycon|asciisyn']['example-data'] }}

We create an instance of the `json` plugin, and call its `present` method:

{{ d['usage1.py|idio|pycon|asciisyn']['json-example'] }}

And we create an instance of the `csv` plugin and also call its `present` method:

{{ d['usage1.py|idio|pycon|asciisyn']['csv-example'] }}

=== Settings

To have user-settable settings, define a dictionary named `_settings` in your subclass:

{{ d['classes2.py|idio|asciisyn']['csv-settings'] }}

The keys of this dictionary should be hyphen- or underscore-separated setting
names, which will be accessible in hyphen format later, and the values should
usually be a tuple of (docstring, default value) but may be just a default
value if the docstring has already been defined in a parent class.

This dictionary will be combined with any other `_settings` dictionaries found
in any parent class all the way up to the `Data` base class.

Individual values can be retrieved by calling the `setting` method and passing
the setting name, and all values can be retrieved by calling the
`setting_values` method.

{{ d['usage2.py|idio|pycon|asciisyn']['csv-example'] }}

Then in your code, the settings should be used to control any behavior that can
be user-customizable. In this case many of the settings are passed directly to
the `csv` library, while the `write-header` setting is used to determine if the
`writeheader()` method will be called.

{{ d['classes2.py|idio|asciisyn']['csv-present'] }}

