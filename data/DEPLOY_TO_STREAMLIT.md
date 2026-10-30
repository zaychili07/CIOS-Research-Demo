# Deploy CIOS to Streamlit Community Cloud

## Repository layout

Upload the contents of this folder to a GitHub repository.

Required files are already included:

```text
app.py
requirements.txt
.streamlit/config.toml
data/
README.md
```

## GitHub

Create a new repository, for example:

`CIOS-Research-Demo`

Upload every file and folder from this package to the repository root.

Recommended visibility: **Public** if you want recruiters, researchers, and LinkedIn visitors to inspect the source without requesting access.

## Streamlit Community Cloud

1. Sign in at `share.streamlit.io` using GitHub.
2. Click **Create app**.
3. Choose **Yup, I have an app**.
4. Select your GitHub repository.
5. Select the branch, normally `main`.
6. Set the entrypoint file to `app.py`.
7. Choose an available `streamlit.app` subdomain.
8. Deploy.

No secrets are required for this demo.

## After deployment

Open the public URL in an incognito/private browser window to verify that it works for someone who is not logged into your accounts.

Recommended final checks:

- Mission Control loads.
- Built-in illustrative demo loads.
- The synthetic-data warning is clearly visible.
- AVG3 metrics render.
- ATR remains HOLD.
- Kaggle scores show 0.868 -> 0.870 public and 0.860 -> 0.863 private.
- Upload mode accepts a small test image.
- No local Windows file paths are required.

## LinkedIn

Use the public `https://<your-name>.streamlit.app/` URL in:
- your CIOS LinkedIn post,
- the LinkedIn Featured section,
- your GitHub README,
- your resume/portfolio if desired.

