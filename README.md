
### Basic user CRUD, using Fastapi, async DB and Oauth login with Github SSO
- https://github.com/tomasvotava/fastapi-sso
- https://github.com/tiangolo/fastapi

## Key points
- Simplicity, quick workaround using Fastapi
- Oauth login using Github is the only method for now (can be extended/replaced)
- JWT tokens are used for session handling (last for 30 minutes by default)
- No frontend provided, just the `/docs` endpoint with Swagger UI (API calls can be made there too)
- All functions, API endpoints and database calls are async

# Build & Run with Docker
- `docker build -t app -f Dockerfile .`
- `docker run -d -v ${PWD}:/code --name app -p 80:80 app`

# Caveats
- Due a lack of time, the tests are quite small and also
- CI steps are missing and can be added later too (security, Docker registry upload, deployment, ...)

# Usage
- Create your Github Oauth app here: https://github.com/settings/applications/new
- Set the required fields `(the callback should be http(s)://<domain>/auth/callback)`

<img width="505" alt="image" src="https://user-images.githubusercontent.com/11727815/228870948-8d98f28e-48ce-4556-9550-978c87758e5a.png">

- Set the ENV variables (`.env.example`), then rename it onto .env
- Build and run with Docker
- Visit http://localhost/auth/login
- Login using your Github credentials
- Get the auth token and use it with Postman/curl/... OR go to http://localhost/docs to check the API endpoints you can use


