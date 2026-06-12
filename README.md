# Automated Financial News Portal

This project automatically processes daily newspaper PDFs into structured, MBA-level financial digests using Gemini 1.5 Flash, and publishes them to a Bloomberg-terminal-inspired static website.

## How It Works

1. You upload a daily PDF newspaper to the `/raw_papers/` folder.
2. A GitHub Action automatically triggers.
3. The Action runs `analyze_news.py`, which uploads the PDF to Gemini.
4. Gemini analyzes the paper using the predefined prompt and generates a Markdown digest.
5. The Action saves the Markdown to `/public/digests/`, updates `manifest.json`, and deletes the PDF.
6. The updated site is published to GitHub Pages.

## Next Steps to Publish on GitHub

Now that the code is generated, follow these steps to make it live:

### 1. Initialize Git and Push to GitHub
Open your terminal in this project directory and run:
```bash
git init
git add .
git commit -m "Initial commit: Automated Financial News Portal"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

### 2. Add Your Gemini API Key
For the GitHub Action to work, it needs your Gemini API key.
1. Go to your repository on GitHub.
2. Click **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. Name: `GEMINI_API_KEY`
5. Secret: `paste-your-api-key-here`
6. Click **Add secret**.

### 3. Enable GitHub Pages
The included GitHub Action automatically deploys the `/public` folder to a `gh-pages` branch using `peaceiris/actions-gh-pages`.
For this action to be able to push to the branch:
1. Go to **Settings** > **Actions** > **General**.
2. Under **Workflow permissions**, select **"Read and write permissions"** and click Save.
3. Then, to make GitHub serve from that branch: Go to **Settings** > **Pages**.
4. Under "Build and deployment", set "Source" to **Deploy from a branch**.
5. Select the **`gh-pages`** branch and the `/ (root)` folder.

### 4. Test the Pipeline
1. Drop a sample newspaper `.pdf` file into the `/raw_papers/` folder locally.
2. Commit and push the file to GitHub.
3. Go to the **Actions** tab in your repository to watch the AI process the document!
4. Once completed, your GitHub Pages site will be updated.
