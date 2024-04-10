# Design Decisions Document

## Project Overview

- **Project Name:** Blog App
- **Description:** A simple application that allows users to create and edit blog posts.

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [Database Design](#database-design)
5. [Security Considerations](#security-considerations)
6. [Scalability](#scalability)
7. [Performance](#performance)
8. [Error Handling](#error-handling)
9. [Deployment Strategy](#deployment-strategy)
10. [Monitoring and Logging](#monitoring-and-logging)
11. [Testing Strategy](#testing-strategy)
12. [Documentation](#documentation)
13. [Future Considerations](#future-considerations)

## 1. Introduction

The purpose of this project was to build a RESTful API for a simple blogging platform. 

## 2. Architecture

The primary application logic is located in [app.py](../app.py), while the remaining components are largely separated based on their place in the MVC framework. Different resources with the same role will be located near one another.

### Models
Data models live in [models/](../src/main/models). Within these classes contain database model information and relationships. Database migrations are generated at [migrations/](../migrations/) via `flask db migrate`.

### Views
API routing takes place in [views/](../src/main/views). This includes routing information, basic Swagger documentation, and response codes. Data shapes expected in requests and returned from endpoints can be found in [views/schemas.py](../src/main/views/schemas.py). Namespaces for the different routes are added to the API blueprint in [api.py](../api.py). This structure supports future versioning of API's.

### Controllers
Controller logic can be found in [controllers/](../src/main/controllers). This is where the bulk of the logic around fetching database objects (definitions found in [models/](../src/main/models/)), handling errors, and returning response objects happens. These functions are called directly from the routing classes in [views/](../src/main/views/).

### Tests
Modules are designed to be independently testable. Tests for a file can be found by following the same file path in [src/test/](../src/test/). Currently only tests for [controllers](../src/test/controllers/) exist, thought this covers nearly all business logic. Coverage can be seen at [index.html](../htmlcov/index.html).

## 3. Technologies Used

### Flask
Flask is the web framework used for this application. Django was considered due to a lot of its built-in structure and out-of-the-box functionality. However Flask is more lightweight, and given the scope of this project, it would be faster to work with.

#### Flask-Jwt
JSON Web Tokens (JWT) are used to authenticate users in this application. By validating a user's password_hash, a user's public_id can be used to authenticate future requests to the API.

#### Flask-restx
Flask-restx provides a lot of useful build-in functionality. For example, it auto-generates Swagger documention for easy API interaction. Additionally, it can be used to define flexible data models and implement strict enforcement of input data shapes.

### Databases
For local development, a simple sqlite database can be used for ease of testing. When `BLOG_APP_ENV` is set to 'test', as it is by default, a sqlite database will be spun up in [instance/](../instance/).

When using docker, a MySQL container is used as a database server. For a more public development environment, MySQL lends itself toward higher scalability and performance.

### Docker-compose
Docker was decided upon rather than just relying on users running the server locally in order to increase consistency in behavior and limit installation issues. Similarly, docker-compose was chosen over vanilla docker to limit the number of commands required to spin up a demo environment. The usage of docker-compose also limits race conditions by requiring the blog-api to wait until the database is ready before trying to execute commands on it.

## 4. Database Design
Extant data models can be found in [models/](../src/main/models/).

### User

| Column_name    | Column_type | Attributes         | Notes                                 |
| -------------- | ----------- | ------------------ | ------------------------------------- |
| id             | int         | primary_key, index |                                       |
| public_id      | String      | unique, index      | JWT ID                                |
| username       | String      | unique, !nullable  |                                       |
| _password_hash | String      |                    | Generated by bcrypt, no direct access |
| email          | String      | unique, !nullable  |                                       |
| admin          | Boolean     |                    |                                       |
| status         | String      |                    | One of 'active','deleted'             |
| created_at     | Date        |         !nullable  |                                       |
| updated_at     | Date        |         !nullable  |                                       |

Notes
- There was consideration for using a status boolean instead of a String; however, the latter was deemed more extensible if additional user statuses were found to be necessary.
- `_password_hash` is set by generating a hash from a user-supplied password via bcrypt

### Post
| Column_name    | Column_type  | Attributes         | Notes                   |
| -------------- | -----------  | ------------------ | ----------------------- |
| id             | int          | primary_key, index |                         |
| title          | String       | !nullable          |                         |
| author_id      | int          | ForeignKey(User)   |                         |
| author         | Relationship |                    |                         |
| content        | Text         |                    |                         |
| status         | String       |                    | One of 'live','deleted' |
| created_at     | Date         | !nullable          |                         |
| updated_at     | Date         | !nullable          |                         |

Notes
- A `publish_date` should be added to the table, but since the functionality for draft posts does not currently exist, once a post is created it is automatically set to a `live` status. In this case, the `created_at` field functionally acts as a `publish_date`.

### Additional Considerations
Some data models were considered but not implemented due to time constraints.

#### Comment
One of the most basic interactions on a blog post would be leaving a comment. A comment object would have the following attributes:

- id (int)
- content (text)
- parent_id (post or comment fk)
- parent (post or comment relationship)

API endpoints would be added to create a comment, linking it to its parent object.

#### Interactions
Certain features could also be added to posts to increase their interactivity. For example, a user could save a post, which would be represented as a relationship on the `user` table. Alternatively, a user could "Like" a post or comment, adding an interaction between them and that piece of media.

## 5. Security Considerations

### User Model
Naturally, the password hash is stored in the database instead of the password itself. The `User` model also provides an authentication check, and prevents a password hash from being viewed directly.

### Decorators
This application supports two api decorators: `@jwt_required` and `@admin_required`. The former checks if the user is authenticated via the `Authorization` header. If the user is logged in, their `User` is passed along to the decorated function. If not, they cannot access the endpoint. The `@admin_required` function behaves similarly, only it also verifies that the user's `admin` field is set to True. 

### Request Verification
By using strict verification of data models, endpoints can avoid users sending additional fields in the json body. This will prevent users from changing unexpected fields, like id, when updating a model.

## 6. Scalability
Deploying multiple instances of the application across multiple servers would allow it to scale horizontally. Though the app currently uses one MySQL server, replicas can be created to distribute the database load across multiple servers. By running multiple instances of the Flask application, a load balancer may be implemented to distribute incoming requests amongst those instances.

Additionally, a message broker/task queue could be implemented for any long-running jobs that may occur. This is discussed in more detail in [Future Considerations](#future-considerations).

## 7. Performance

### Database Indexing
Indices were added to fields that will be queried on often. For example, users are often fetched by id, email, public_id. Posts are often fetched by id and author_id. These are the fields that indices were added to to optimize database querying.

### Caching
Caching is currently used when one fetches a given user's blog posts. In the expected use case, a user's posts may be viewed several times before they are changed. However, if a user's posts do change through an edit, a delete, or a new post, the cache is reset. Caching functionality can be expanded to other use cases; this was just one example.

## 8. Error Handling

### API Errors
Documentation on a given API namespace can be found in its respective routing file, for example [auth_routing.py](../src/main/views/auth_routing.py). The `@api.doc` decorators create Swagger documentation, which can be found when running the app at http://localhost:5000/api/v1. Each error for an endpoint is handled via its respective controller, which will abort the function if certain conditions are met. Unexpected exceptions will be caught, resulting in a generic `500` response code. In this case the logger will warn about the unplanned exception, though most exceptions should be handled explicitly in the controller logic.

## 9. Deployment Strategy

One of the components missing from this project is a good CI/CD pipeline. The next steps for implementing a robust pipeline via GitHub Actions would be integrating pytest and coverage to ensure that unit tests had been written for any changed functionality, and that code coverage stayed above an acceptable threshold for the repository. Additionally, if this project were to grow into a production environment, a deploy step would be added to the pipeline to provide users with the most recent version of the app.

## 10. Monitoring and Logging

A very basic logger can be configured at [logger.py](../logger.py). It is used mostly to report on errors as well as important API interactions like user sign up.

In a future version of this application, logging and monitoring could be configured in certain environments to output to a service like New Relic or Grafana. This would allow for more easy viewing of consolidated logs, viewing response code trends, and tracking down the causes of errors via stack traces.

## 11. Testing Strategy

Modules are designed to be independently testable. Tests for a file can be found by following the same file path in [src/test/](../src/test/). Currently only tests for [controllers](../src/test/controllers/) exist, thought this covers nearly all business logic.

### Fixtures
Pytest fixtures are used to mock data models, function return values, and exceptions. By combining a few of these, test cases can cover a wide swath of application behavior. Fixtures are also used to avoid function calls that require a working application context for the flask app.

### Test Content
Unit tests are written by combining pytest fixtures with calls to functions in the controller classes. By modifying the input fixtures for a given function, multiple cases for each function are tested, such that edge cases are covered comprehensively. For example, one can see what happens when a database error occurs or when a user is not authorized to perform an action.

## 12. Documentation

Documentation on a given API namespace can be found in its respective routing file, for example [auth_routing.py](../src/main/views/auth_routing.py). The `@api.doc` decorators create Swagger documentation, which can be found when running the app at http://localhost:5000/api/v1. Swagger is also used to document the data models for the expected inputs and outputs for a given endpoint.

Most of the remaining code found within this project should be self-documenting. If comments are needed to explain how code works, it is probably not well-written. If behavior seems ambiguous, test cases found in that file's respective test file should clarify the expected behavior.

Information on running the application can be found at [quickstart.md](quickstart.md)

## 13. Future Considerations

### Stricter input verification
Currently, it is possible to input problematic data which still passes input verification in some places. For example:
 
- A blog post can be created with any length of content
- User emails are not verified, or checked to see if they follow an email-like pattern
- There are no password requirements currently

### Additional Testing
Nearly all business logic is currently tested, but [decorators.py](../src/main/views/decorators.py) is not tested at the moment. With more time, it would be the next candidate for increasing test coverage. Additionally, more tests should be written to test the API routes directly, rather than just the business logic. While nearly all cases are covered by controller tests, certain ones may be overlooked, such as verifying bad input returns a 400 error.

### Environment Files
Environment configuration currently lives in [config.py](../config.py). This was a simple way to distinguish between a local test environment and a development environment running in a docker container. These configurations should be moved to distinct .env files and added to the .gitignore such that they are not found in the repo.

### CI/CD
As mentioned in [Deployment Strategy](#deployment-strategy), one of the components missing from this project is a good CI/CD pipeline. The next steps for implementing a robust pipeline would be integrating pytest and coverage to ensure that unit tests had been written for any changed functionality, and that code coverage stayed above an acceptable threshold for the repository. Additionally, if this project were to grow into a production environment, a deploy step would be added to the pipeline to provide users with the most recent version of the app.

### Query parameters/searching
Some of the next API interactions that should be added are allowing users to pass query parameters to certain endpoints, such as `GET /post?title='MyTitle'` to increase filtering capabilities. Ideally, the available query parameters would be limited to prevent users from filtering on disallowed fields like password_hash. Additionally, one would expect 'deleted' users or posts to be omitted from query results. This could be generalized by adding a `POST /<resource>/search` endpoint that accepts a json body with search parameters.

### Pagination
Pagination is used to display a limited set of results based on attributes like page_size and page_number. By adding these as query parameters to certain fetch endpoints, users could fetch a subset of results if `.paginate(page,per_page,error_out=False)` is appended to the pertinent database queries.

### Batch processes
One of the features that should be added to this app is the inclusion of batch processes. It would be handy to be able to edit several blog posts at a given time, or create several users at once from a spreadsheet. Adding batch processes to the API would be relatively simple with flask-jwt models, and could involve using a message broker to avoid overloading the application.

### "Remember Me"
To fully build out the user authentication part of this application, the ability for refresh tokens to be returned from the login endpoint should be included, such that users can avoid logging in to the application frequently.

### Additional Interactions
As mentioned in [Database Design](#database-design), there were some tables that were considered as part of basic blog functionality. As they weren't mentioned in the product spec, they were omitted due to time constraints, so more focus could be spent on code quality and consistency.