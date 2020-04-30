from chalice import Chalice, Response
from chalicelib import gbmodel
import boto3
import jinja2
import os
import urllib

app = Chalice(app_name='guestbook')
app.debug = True

_GUESTBOOK_DB = None

# provides model
def get_guestbook_db():
    global _GUESTBOOK_DB
    if _GUESTBOOK_DB is None:
        _GUESTBOOK_DB = gbmodel.model(
            boto3.resource('dynamodb').Table(
                os.environ['GUESTBOOK_TABLE_NAME'])) # so the resources file must be run by now...
        print("DB:", end='')
        print(_GUESTBOOK_DB.__dict__)
    return _GUESTBOOK_DB

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
    
def get_context():
    model = get_guestbook_db()
    x = model.select()
    print("I'm x:")
    print(x)

    # This doesn't work anymore because the model returns a request, remember it's an API
    context = {
        "entries": [dict(name=row[0], email=row[1], signed_on=row[2], message=row[3] ) for row in model.select()]
    }
    print("context: ", end='')
    print(context)
    return context

# TODO this is incomplete
@app.lambda_function()
def sign_guestbook(event, context):
    email = event['email'][0]
    name = event['name'][0]
    msg = event['message'][0]

    # add the message to dynamodb

#@app.route('/sign', methods=['POST'], content_types=["application/x-www-form-urlencoded"])
#def sign():
#    post_json = urllib.parse.parse_qs(app.current_request.__dict__.get("_body")) # source below
#    # TODO: parse querystrings with Requests
#    email = post_json['email'][0]
#    name = post_json[b'name'][0]
#    msg = post_json[b'message'][0]
#    model.insert(name, email, msg)
#    template = render("chalicelib/templates/index.html", get_context())
#


# Resources
# https://medium.com/richcontext-engineering/creating-a-serverless-blog-with-chalice-bdc39b835f75
# https://chalice-workshop.readthedocs.io/en/latest/media-query/03-add-db.html
