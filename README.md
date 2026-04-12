# pramodtidke.github.io

Personal portfolio website for Pramod Tidke — DevOps / Cloud / SRE Engineer.

**Live site:** https://pramodtidke.in

## Stack

- Pure HTML + CSS + Vanilla JS — zero dependencies, zero build step
- JetBrains Mono + Inter from Google Fonts
- Hosted on GitHub Pages

## Features

- Terminal-style hero with typewriter animation
- Animated CI/CD pipeline visualization
- Scroll-triggered reveal animations
- Skill bars with count-up on scroll
- Fully responsive (mobile, tablet, desktop)
- Dark theme with grid overlay and scanlines

## Deploy to GitHub Pages (5 minutes)

### Option A — dedicated repo (recommended for custom domain)

1. Create a new repo named exactly: `pramodtidke.github.io`
2. Push all files:

```bash
git init
git add .
git commit -m "feat: launch portfolio"
git branch -M main
git remote add origin https://github.com/pramodtidke/pramodtidke.github.io.git
git push -u origin main
```

3. GitHub Pages auto-deploys from `main` branch root.
4. Site live at: `https://pramodtidke.github.io`

### Option B — existing repo with /docs folder or gh-pages branch

1. Go to repo → **Settings → Pages**
2. Source: `Deploy from a branch`
3. Branch: `main`, Folder: `/ (root)`
4. Save → wait ~60 seconds

### Custom domain (pramodtidke.in)

1. In repo root, create a file named `CNAME` containing:
   ```
   pramodtidke.in
   ```
2. In your domain DNS settings, add:
   - **A records** pointing to GitHub Pages IPs:
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - **CNAME record**: `www` → `pramodtidke.github.io`
3. In GitHub: Settings → Pages → Custom domain → enter `pramodtidke.in`
4. Check "Enforce HTTPS" once DNS propagates (~5–30 min)

## Project structure

```
pramodtidke.github.io/
├── index.html          ← entire site (single file)
├── CNAME               ← custom domain (pramodtidke.in)
├── README.md           ← this file
└── pramod_tidke_resume.pdf  ← resume download (add this)
```

## Resume download

Place your resume PDF in the root folder named `pramod_tidke_resume.pdf`.
The "download resume" button already links to it.

## Updating content

All content is in `index.html`. Search for the section you want to change:
- `<!-- ═══ HERO ═══ -->` — hero section
- `<!-- ═══ ABOUT ═══ -->` — about section
- `<!-- ═══ PROJECTS ═══ -->` — projects
- `<!-- ═══ SKILLS ═══ -->` — skills
- `<!-- ═══ EXPERIENCE ═══ -->` — experience
- `<!-- ═══ CONTACT ═══ -->` — contact

## License

MIT — feel free to fork and adapt.
