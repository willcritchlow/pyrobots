# pyrobots - Robots.txt parsing on the web

Simple web app to expose open source C++ robots.txt parser on the web.

Uses the version of the [Google open source robots.txt parser](https://github.com/google/robotstxt) in [my branch](https://github.com/willcritchlow/robotstxt/tree/pythoncallingexecutable) that exposes the information I need in structured output as well as the modification to allow passing in [multiple user agents](https://github.com/willcritchlow/robotstxt/tree/multipleuavector) that uses the first UA passed in unless there is no ruleset explicitly targeting that UA, in which case it falls back to the second UA.

Calls the binary executable which needs compiling for whatever OS it is going to run on.

## Run locally

Use `env FLASK_APP=pyrobots.py flask run` to test locally then visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## API usage

Test the API with e.g.:

```
curl -X POST -H "Content-Type: application/json" -d '{
  "robots": "User-agent: *\nDisallow: /foo/\n\nUser-agent: googlebot/1.2\nDisallow: /bar/",
  "ua": "googlebot-image",
  "url": "/bar/"
}' http://127.0.0.1:5000/api/parse/
```

```
curl -X POST -H "Content-Type: application/json" -d '{
  "robots": "User-agent: *\nDisallow: /foo/\n\nUser-agent: googlebot/1.2\nDisallow: /bar/",
  "ua": "adsbot-google",
  "url": "/foo/"
}' http://127.0.0.1:5000/api/parse/
```

## Deploying

See [AWS instructions](AWS-instructions.md). Currently deployed on a lightsail instance in my own AWS account.