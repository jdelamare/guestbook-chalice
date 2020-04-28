First of all, don't commit `.chalice` that's a nightmare. TODO: What exactly can be found from that file.

Anyways, this is a microservice framework for serverless python apps.

Note that static files (style.css) must be served out of an S3 bucket. If you can live with 403 on local development that's fine, but even the local server needs to pull from S3, which could be a tiny bit expensive. However much it costs to move 522 bytes out of an S3 bucket.

Pretty straightforward otherwise, just clone this repo and install from `requirements.txt`. After that run it locally for an example: 
```
chalice local
```
and browse to `localhost:8000`
