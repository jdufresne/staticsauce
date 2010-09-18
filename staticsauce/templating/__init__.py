from staticsauce.templating.jinja2templaterenderer import Jinja2TemplateRenderer


render_jinja2 = None

def init():
    global render_jinja2
    renderer = Jinja2TemplateRenderer()
    render_jinja2 = renderer.render

