from flask import render_template


def htmx_template_selector(request, partial_html, full_html, context=None):
    if request.headers.get('Hx-Request') != None:
        return render_template(partial_html, **context)
    return render_template(full_html, **context)
