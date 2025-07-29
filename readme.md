Prompt:
As Mozio expands internationally, we have a growing problem that many transportation suppliers we'd like to integrate, cannot give us concrete zip codes, cities, etc that they serve.
To combat this, we'd like to be able to define custom polygons as their "service area" and we'd like for the owners of these shuttle companies to be able to define and alter their
polygons whenever they want, eliminating the need for Mozio’s employees to do this boring grunt work.

Requirement:
Build a JSON REST API with CRUD operations for Provider (name, email, phone number, language an currency) and ServiceArea (name, price, geojson information)
Create a specific endpoint that takes a lat/lng pair as arguments and returns a list of all polygons that include the given lat/lng. The name of the polygon, provider's name, and price should be returned for each polygon. This operation should be FAST.
Use unit tests to test your code;
Write up some API docs (using any tool you see fit);
Create a Github account (if you don’t have one), push all your code and share the link with us;
Deploy your code to a hosting service of your choice. Mozio is built entirely on AWS, so bonus points will be awarded for the use of AWS.

Considerations:
All of this should be built in Python DjangoRest or FastAPI. 
Use any extra libraries you think will help, choose whatever database you think is best fit for the task, and use caching as you see fit.
If possible also provide an API Gateway with Rate Limiting.
Ensure that your code is clean, follows standard PEP8 style (though you can use 120 characters per line) and has comments where appropriate.