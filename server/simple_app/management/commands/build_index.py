from django.core.management.base import BaseCommand
from pathlib import Path
from system.settings import DEBUG, HOME_DIR

class Command(BaseCommand): 
    help = 'Create Super User'

    def handle(self, *args, **options):
        ENV = "prod" if not DEBUG else "dev"
        template_path = Path(HOME_DIR / "client/html/desktop/index.template.html")
        output_path = Path(HOME_DIR / "client/html/desktop/index.html")

        critical_css = ""
        full_css = ""
        scripts = ""

        if ENV == "prod":
            critical_css = '<link rel="stylesheet" href="/cache/users/static/css/{{css_version}}/main_min_critical.css">'
            full_css = '<link rel="stylesheet" href="/cache/users/static/css/{{css_version}}/main_min.css">'
            scripts = '<script type="module" scr="/cache/users/static/js/{{js_version}}/main_min.js"></script>'
        else:
            critical_css = '' 
            full_css = "\n".join([
                '<link rel="stylesheet" href="/static/css/main.css">',
                '<link rel="stylesheet" href="/static/css/user/form.css">',
                '<link rel="stylesheet" href="/static/css/user/login.css">',
                '<link rel="stylesheet" href="/static/css/user/logup.css">'
            ])
            scripts = "\n".join([
                '<script src="/static/js/dom.js" defer></script>',
                '<script src="/static/js/menu.js" defer></script>',
                '<script type="module" src="/static/js/vanilla/prototype/index.js"></script>',
                '<script type="module" src="/static/js/vanilla/dom.js"></script>',
                '<script type="module" src="/static/js/main.js"></script>',
                '''<script type="module">
                    import { Dom } from "/static/js/vanilla/dom.js";
                    import { Main } from "/static/js/main.js";

                    window.Main = new Main();
                    window.Dom = Dom;
                </script>''',
            ])

        # Read template
        template = template_path.read_text()

        # Replace tags
        rendered = (
            template.replace("{{critical_css}}", critical_css)
                    .replace("{{full_css}}", full_css)
                    .replace("{{scripts}}", scripts)
        )

        # Write result
        output_path.write_text(rendered)

        print(f"[✓] index.html generated for {ENV}")