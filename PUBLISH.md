# How to publish this repo to GitHub

This folder is a **standalone Git repo** (briefings only). To put it on GitHub:

1. **Create a new public repo on GitHub**
   - Go to [github.com/new](https://github.com/new).
   - Repository name: e.g. `sam-news-briefings` (or your preferred name).
   - Visibility: **Public**.
   - Do **not** add a README, .gitignore, or license (this repo already has them).
   - Click **Create repository**.

2. **Add the remote and push** (from this folder):

   ```bash
   cd /path/to/Sam_news/sam-news-briefings
   git remote add origin https://github.com/YOUR_USERNAME/sam-news-briefings.git
   git push -u origin main
   ```

   If your default branch is `master` instead of `main`, use:

   ```bash
   git push -u origin master
   ```

3. **Before every push**, run through [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md).

To add new briefings: from the main Sam_news repo run `python3 scripts/copy_briefings_to_public.py --all` (or a single date), then `git add`, `commit`, `push` from this folder.
