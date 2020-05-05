# DynamoDB Chalice App
## Introduction
This app is a quick look at what is needed to connect a DynamoDB database to 
the guestbook app. Assuming progressive overload (you've been working up), this
will be the second of the three versions of Guestbook written with chalice. 
Only two routes are provided, so be sure to delete you DynamoDB database in the
AWS console, as that's not provided by `chalice delete`.

## Resources
Chalice does not support DynamoDB, so the database will be created based on the 
cloudformation stack specified in `resources.json`. Remember this is serverless
computing, so we'll need to pipe all of the AWS infrastructure together with the
appropriate authorization and configurations. These three files compose most of 
our infrastructure:

* `.chalice/config`
* `resources.json`
* `.chalice/policy-<stage>.json`

All of which are located with respect to the project's root directory. Note that
a stage is specified in the file `.chalice/config`, and the file 
`chalice/policy-<stage>.json` is only used if `"autogen_policy": false` exists 
below the stage in `.chalice/config`. The delination between these three files 
exists where chalice has and does not have some capability. Yes, it can be used 
to make lambda functions, API gateways, and it even supports authorization. But
in our exercise we'll be using REST APIs to populate a DynamoDB database, which 
can only be stood up using Cloudformation. Hence the need for `resources.json`.

Another thing to note is the `recordresources.py` script provided by the chalice
workshop located ![here](https://chalice-workshop.readthedocs.io/en/latest/media-query/).
This workshop, amongst other blogs, was a corner stone to the development of this
app. All of theses resources are list at the bottom of this document. Many thanks.
I digress, the python script looks complicated but it really just grabs information
provided by the AWS python SDK and records it as an environment variable in the 
lambda. This is how the lambda function knows how to get the table name. More 
specifically, this can be seen as a call out to the environment variables using
`os` in the function `get_guestbook_db()` in `app.py` (line 28).

## Deployment
First, you'll need valide AWS credentials. I'm going to assume that they're in 
the `~/.aws/credentials` file under the `[default]` profile. It could very well 
be the case that you want to develop with a specific profile, but I was initially
unable to make that work and doing so is a separate adventure. Assuming the creds
are in place, here's the steps to deploy the app:

1) `virtualenv -p python3 .venv/`
2) `source .venv/bin/activate`
3) `pip install -r requirements.txt`
4) `aws cloudformation deploy --template-file resources.json --stack-name guestbook`
5) `python3 recordresources.py --stack-name guestbook`
6) `chalice deploy`

Another expectation is that the project is whole, as in no files are missing. Here is
what my directory looks like excluding `.git, __pychache__` and other artifacts like 
previous deployments.

```
├── .chalice
│   ├── config.json
│   └── policy-dev.json
├── .gitignore
├── README.md
├── app.py
├── chalicelib
│   ├── Model.py
│   ├── gbmodel.py
│   └── templates
│       ├── index.html
│       ├── layout.html
├── recordresources.py
├── requirements.txt
└── resources.json
```

## Local Development 
Local development is weird. It's faster to deploy on `localhost`, but I've found some
strange drawbacks. Inexplicably, the `POST` parameters are ASCII on localhost and unicode
when deployed to a lambda. You'll see two separate branches in the repo acknowledging that.
Another oddity is there is a prefix specified in `.chalice/config.json` which is 
`"api_gateway_stage": "ddb"`. This will become the route prefix once it's deployed to the 
cloud, so the HTML form in `index.html` will need to be updated to `POST` to `/ddb/sign` as
opposed to `/sign` when working with `localhost`. This was a pretty solid blocker.

# Permissions
It was noted earlier that the backend will need appropriate perimssions. This can mostly be 
seen in the custom `.chalice/policy-<stage>.json`. Normally, chalice will scan your source 
code to determine the necessary permissions for things to work. Since we've ventured out of 
that ecosystem, we'll need to specify all the necessary perimssions for the DynamoDB instance
as well as a special IAM role `PassRole`. This allows us to hand off these DynamoDB permissions
to the app's lambda functions. It effectively passes the permissions from you the user to the
service, our app. Feel free to investigate the policy file further to understand more about the
capabilities. You may see that the service's DynamoDB policies are over provisioned, but that's
just been done to ease further feature development. 


## Credit Due
The folks who develop chalice and the associated workshop.
![chalice-workshop](https://chalice-workshop.readthedocs.io/)

Chalice docs
![chalice](https://chalice.readthedocs.io)

These blogs:
![Alex Pulver](https://aws.amazon.com/blogs/developer/deploying-aws-chalice-application-using-aws-cloud-development-kit/)
![Sunny Srinidhi](https://medium.com/swlh/getting-started-with-chalice-to-create-aws-lambdas-in-python-step-by-step-tutorial-3ccf01701259)
![Bas Harenslak](https://godatadriven.com/blog/ip-whitelisting-your-chalice-application/)

