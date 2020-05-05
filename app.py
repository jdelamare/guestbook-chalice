from chalice import Chalice, Response
from chalice import BadRequestError, ChaliceViewError
from chalicelib import gbmodel
import boto3
import jinja2
import os
import urllib

app = Chalice(app_name='guestbook')
app.debug = True

_GUESTBOOK_DB = None

def get_guestbook_db():
    """ This function provides the model, a DynamoDB instance.
    Args: None

    Returns: A `model` class, which has acts as a handle on the only table.
    """
    global _GUESTBOOK_DB

    # if the guestbook database and table does not exist one is created
    if _GUESTBOOK_DB is None:
        _GUESTBOOK_DB = gbmodel.model(
            boto3.resource('dynamodb').Table(

                # recordresources.py must have been run by here <---- IMPORTANT
                os.environ['GUESTBOOK_TABLE_NAME'])) 

    return _GUESTBOOK_DB

def get_context():
    """ Retrieve all entries from model.
    Args: 
        None

    Returns: 
        A list of entries
    """
    model = get_guestbook_db()
    entries = model.select()

    return entries

def render(tpl_path, context):
    """ Serializes the webpage to return.
    Args: 
        tpl_path: Path to the template
        context: A `dict` of items to be included in the serialized template. May be empty.

    Returns:
        String: A serialized Template which is likely an HTML file, optionally with some `context`.

    Raises:
        TemplateError: An error may occur when attempting to serialize the template and context.
                       Error message will only be printed to the backend.
    """
    path, filename = os.path.split(tpl_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or "./"))
    try:
        return env.get_template(filename).render(entries=context)
    except jinja2.TemplateError as e:
        print(e)

@app.route('/', methods=['GET'])
def index():
    """ The main page, which has a form for insertion and a list of all entries.
    Args: 
        None

    Returns:
        A Chalice `Response` object, which allows for control of the header fields. 

    Raises: 
        ChaliceViewError: If `render(..)` fails, this error is returned to the user.
    """
    try:
        template = render("chalicelib/templates/index.html", get_context())
    except:
        raise ChaliceViewError("Error rendering the template")

    return Response(template, status_code=200, headers={"Content-Type": "text/html"})
    
@app.route('/sign', methods=['POST'], content_types=["application/x-www-form-urlencoded"])
def sign():
    """ The route taken when the form is submitted, it adds an entry.
    Args:
        None

    Returns:
        A Chalice `Response` object, redirecting back to the main page.
       
    Raises:
        BadRequestError: If the user doesn't submit all form fields this error is raised.
        ChaliceViewError: Server side error, perhaps missing credentials.
        ChaliceViewError: The `render` function failed.
    """
    # Grab the passed form parameters from the `_body`. code snippet source below
    post_json = urllib.parse.parse_qs(app.current_request.__dict__.get("_body")) 
    try:
        email = post_json['email'][0]
        name = post_json['name'][0]
        msg = post_json['message'][0]
    except BadRequestError as e:
        raise BadRequestError("Missing parameters here", e)

    # `insert` returns None if successful, json HTTP headers if not
    insert_status = get_guestbook_db().insert(name, email, msg) 
    if insert_status:
        raise ChaliceViewError("Database insertion was unsuccessful")

    try:
        template = render("chalicelib/templates/index.html", get_context())
    except:
        raise ChaliceViewError("Error rendering the template")

    return Response(template,
                    status_code=302, 
                    headers={"Content-Type": "text/html",
                             "Location": "/ddb"})


@app.route("/test")
def test():
    template = render("chalicelib/templates/test.html", {})
    return Response(template, status_code=200, headers={"Content-Type": "text/html"})
