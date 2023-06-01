
# Basic user CRUD, using Fastapi, async and Oauth login with Github SSO
- https://github.com/tomasvotava/fastapi-sso
- https://github.com/tiangolo/fastapi

## Key points
- Simplicity, quick workaround using Fastapi
- Oauth login using Github is the only method for now (can be extended/replaced)
- JWT tokens are used for session handling (last for 30 minutes by default)
- No frontend provided, just the `/docs` endpoint with Swagger UI (API calls can be made there too)
- All functions, API endpoints and database calls are async, for better performance

# Build & Run with Docker
- `docker build -t app -f Dockerfile .`
- `docker run -d -v ${PWD}:/code --name app -p 80:80 app`

# Usage
- Create your Github Oauth app [here](https://github.com/settings/applications/new) and set the required fields as the example below `(the callback should be http(s)://<domain>/auth/callback)`
- <img width="505" alt="image" src="https://user-images.githubusercontent.com/11727815/228870948-8d98f28e-48ce-4556-9550-978c87758e5a.png">

- Set the ENV variables (`.env.example`), then rename it onto `.env`
- Build and run with Docker
- Go to http://localhost/auth/login
- Get the auth token and use it with Postman/curl/... OR go to http://localhost/docs to check the API endpoints you can use with the token

# Caveats due a lack of time (TO-DO)
- Tests are quite small.
- Missing CI/CD steps (security, Docker registry upload, deployment, ...)
