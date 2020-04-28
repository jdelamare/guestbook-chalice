from chalice import Chalice, Response
from chalicelib import gbmodel
import jinja2
import os
import urllib

app = Chalice(app_name='guestbook')
app.debug = True

# Model exists here
model = gbmodel.model()

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./"))
    try:
        return env.get_template(filename).render(context)
    except jinja2.TemplateError as e:
        print(e)

@app.route('/', methods=['GET'])
def index():
    template = render("chalicelib/templates/index.html", get_context())
    return Response(template, status_code=200, headers={"Content-Type": "text/html"})
    
@app.route('/sign', methods=['POST'], content_types=["application/x-www-form-urlencoded"])
def sign():
    post_json = urllib.parse.parse_qs(app.current_request.__dict__.get("_body")) # source below
    email = post_json[b'email'][0]
    name = post_json[b'name'][0]
    msg = post_json[b'message'][0]
    model.insert(name, email, msg)
    template = render("chalicelib/templates/index.html", get_context())
    return Response(template, status_code=303, headers={"Content-Type": "text/html", "Location": "/"})

def get_context():
    context = {
        "entries": [dict(name=row[0], email=row[1], signed_on=row[2], message=row[3] ) for row in model.select()]
    }
    return context

# Resources
# https://medium.com/richcontext-engineering/creating-a-serverless-blog-with-chalice-bdc39b835f75