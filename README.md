# PMO Suite — Build Guide

## Running from source (development)

```bash
pip install -r requirements.txt
python main.py
```

---

## Building the Windows `.exe` via GitHub Actions

GitHub's servers have full internet access and will install all dependencies
and compile the `.exe` automatically. Your Windows machine needs nothing installed.

### One-time setup (do this once)

#### Step 1 — Create a GitHub repository

1. Go to [github.com](https://github.com) → **New repository**
2. Name it `pmo-suite` (or anything you like)
3. Set it to **Private** (recommended — your source code stays private)
4. Click **Create repository**

#### Step 2 — Push the project files

Open a terminal (PowerShell or Command Prompt) in the `pmo_app` folder:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pmo-suite.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

#### Step 3 — Watch the build

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You will see **"Build Windows EXE"** running automatically
4. Wait ~5–8 minutes for it to complete (green checkmark = success)

#### Step 4 — Download the `.exe`

1. Click on the completed workflow run
2. Scroll down to **Artifacts**
3. Click **PMO_Suite_vX_Windows** to download the zip
4. Extract it anywhere → double-click `PMO_Suite.exe`

---

## Releasing a new version

Tag any commit to trigger a **GitHub Release** with the zip attached:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

The release will appear under **Releases** on your GitHub repo page, with a
direct download link you can share with users.

---

## Triggering a manual build

1. GitHub → **Actions** tab
2. Click **"Build Windows EXE"** in the left sidebar
3. Click **"Run workflow"** → **Run workflow**

---

## Default credentials

| Username | Password | Role  |
|----------|----------|-------|
| admin    | admin123 | Admin |

**Change the password immediately after first login** via the Accounts page.

## Data location

All data (SQLite database) is stored in:
```
C:\Users\<YourName>\pmo_app_data\pmo_database.db
```
This folder is created automatically on first run. Back it up regularly.
