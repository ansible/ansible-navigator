"""An ansible test lookup plugin."""


# pylint: disable=invalid-name
# pylint: enable=invalid-name


DOCUMENTATION = """
    name: lookup_1
    author: test
    plugin_type: lookup
    version_added: "1.0.0"
    short_description: This is test lookup plugin
    description:
        - This is test lookup plugin
    options:
        foo:
            description:
            - Dummy option I(foo)
            type: str
            required: True
        bar:
            description:
            - Dummy option I(bar)
            default: candidate
            type: str
    notes:
    - This is a dummy lookup plugin
    """

EXAMPLES = """
    - name: Retrieve a value deep inside a using a path
      ansible.builtin.set_fact:
        value: "{{ lookup('company_name.coll_1.lookup_1', var1, var2) }}"
    """

RETURN = """
    _raw:
        description:
        - One or more zero-based indices of the matching list items.
    """
