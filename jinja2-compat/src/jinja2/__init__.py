def _export_jinja(name, ns):
    import warnings
    from importlib import import_module

    mod_name = "jinja" if not name else ("jinja." + name)
    warnings.warn(
        "'jinja2' has been renamed to 'jinja'. Import from %r instead." % mod_name,
        DeprecationWarning,
        stacklevel=3,
    )

    try:
        mod = import_module(mod_name)
    except ImportError:
        warnings.warn(
            "%r no longer exists. Either fully migrate to Jinja >= 3.0"
            " or downgrade to an earlier version." % mod_name,
            stacklevel=3,
        )
        return

    for key, value in vars(mod).items():
        if not key.startswith("__") or key == "__version__":
            ns[key] = value

    if name:
        ns.pop("_export_jinja")


_export_jinja(None, globals())
