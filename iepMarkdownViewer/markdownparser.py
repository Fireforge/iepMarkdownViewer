import markdown
from mdx_linkify.mdx_linkify import LinkifyExtension


def dont_linkify_python(attrs, new=False):
    if not new:  # This is an existing <a> tag, leave it be.
        return attrs

    # If the TLD is '.py', make sure it starts with http: or https:
    text = attrs['_text']
    if text.endswith('.py') and \
       not text.startswith(('www.', 'http:', 'https:')):
        # This looks like a Python file, not a URL. Don't make a link.
        return None

    # Everything checks out, keep going to the next callback.
    return attrs


def getparser():
    # Return a correctly configured markdown parser
    linkify_configs = {'linkifycallbacks': [[dont_linkify_python], '']}
    linkify = LinkifyExtension(configs=linkify_configs)

    markdown_extensions = ['extra', 'codehilite', 'sane_lists', linkify]
    return markdown.Markdown(extensions=markdown_extensions)
