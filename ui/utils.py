from django import urls


def reverse(*args, query_params: dict = None, **kwargs):
    """Get URI by path name and inject query parameters."""
    query_str = (
        '&'.join([f'{key}={value}' for key, value in query_params.items()])
        if query_params
        else ''
    )
    return f'{urls.reverse(*args, **kwargs)}?{query_str}'
