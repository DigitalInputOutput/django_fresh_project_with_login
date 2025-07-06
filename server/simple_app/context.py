from simple_app.services.minify.minify import MinifyService

def index_context(request):
    return {
        "css_version": MinifyService.get_version("css"),
        "js_version": MinifyService.get_version("js")
    }