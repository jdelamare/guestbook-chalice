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
    return _GUESTBOOK_DB

def get_context():
    # get the DynamoDB model and select all of the entries from that model
    model = get_guestbook_db()
    entries = model.select()
    context = {
        "entries": [row for row in entries]
    }
    return entries

# serializes webpage to return
def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./"))
    try:
        return env.get_template(filename).render(entries=context)
    except jinja2.TemplateError as e:
        print(e)

@app.route('/', methods=['GET'])
def index():
    template = render("chalicelib/templates/index.html", get_context())
    return Response(template, status_code=200, headers={"Content-Type": "text/html"})
    
# TODO this is incomplete
#@app.lambda_function()
#def sign_guestbook(event, context):
#    email = event['email'][0]
#    name = event['name'][0]
#    msg = event['message'][0]
#
    # add the message to dynamodb

# is truthy, will say if insert was successful
@app.route('/sign', methods=['POST'], content_types=["application/x-www-form-urlencoded"])
def sign():
    post_json = urllib.parse.parse_qs(app.current_request.__dict__.get("_body")) # source below
    email = (post_json[b'email'][0]).decode('UTF-8')
    name = (post_json[b'name'][0]).decode('UTF-8')
    msg = (post_json[b'message'][0]).decode('UTF-8')
    get_guestbook_db().insert(name, email, msg) # TODO: if this fails, need to return 400
    template = render("chalicelib/templates/index.html", get_context())
    return Response(template, 
                    status_code=302, 
                    headers={"Content-Type": "text/html",
                             "Location": "/"})

# Resources
# https://medium.com/richcontext-engineering/creating-a-serverless-blog-with-chalice-bdc39b835f75
# https://chalice-workshop.readthedocs.io/en/latest/media-query/03-add-db.html
