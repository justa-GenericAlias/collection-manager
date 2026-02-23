# Collection Manager

## Deployment

### Domain Name + Registrar
- **Domain Name**: movie-collection-manager-42dbff9f12cd.herokuapp.com (Heroku-provided subdomain)
- **Registrar**: Heroku (automatic for apps; for custom domain, use Namecheap or GoDaddy)

### Hosting Provider
- **Provider**: Heroku
- **Plan**: Free tier (Eco dyno, ~$0/month for basic usage)

### Tech Stack
- **Backend**: Flask (Python 3.12), SQLAlchemy ORM
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Deployment Tool**: Gunicorn (WSGI server)
- **Other**: flask-cors for API access

### Database Type + Where Hosted
- **Type**: PostgreSQL
- **Hosted**: Heroku Postgres (managed database service)

### How to Deploy and Update the App
1. **Prerequisites**: Git, Heroku CLI installed and logged in (`heroku login`).
2. **Initial Deploy**:
   - Commit changes: `git add . && git commit -m "Deploy"`
   - Push to Heroku: `git push heroku main`
   - Heroku builds the app, installs dependencies, and starts the server.
3. **Updates**:
   - Make changes, commit, and push: `git push heroku main`
   - Heroku auto-deploys and restarts the app.
4. **Monitor**: Use `heroku logs --tail` for issues; `heroku open` to view.

### How Configuration/Secrets Are Managed (Env Vars)
- **Database Connection**: `DATABASE_URL` (auto-set by Heroku Postgres addon; contains PostgreSQL connection string).
- **Management**: Secrets are stored as environment variables in Heroku (Dashboard > App > Settings > Config Vars). No secrets in code or Git.
- **Local Development**: Use `.env` file (not committed) with `DATABASE_URL=postgresql://...` for local testing.