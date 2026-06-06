# 🪻 GitHub-Garden
GitHub Garden is a custom, animated SVG visualization that transforms GitHub contribution data into a **lilac-themed garden**, where each day grows a small flower based on activity.
It is designed to be embedded in a GitHub profile README as a visual alternative to the default contribution graph.
<p align="center">
  <img src="https://github.com/sukhada20/GitHub-Garden/blob/main/garden.svg?raw=true">
</p>

---

## ✨ Features
* **Daily Contribution Blocks**
  Each day is represented as a bordered square, aligned to GitHub’s weekly grid.
* **Lilac Color Palette**
  Contribution intensity is mapped to a soft, accessible lilac gradient.
* **Blooming Flower Animation**
  Days with activity grow animated flowers that bloom sequentially and loop continuously.
* **Month & Day Labels**
  * Month labels (Jan–Dec) appear at correct boundaries
  * Day labels (Mon, Wed, Fri) improve readability
* **GitHub-Safe SVG**
  No JavaScript, no external CSS — fully compatible with GitHub Actions and profile READMEs.

---

## 🛠️ How It Works
1. A GitHub Actions workflow runs on a schedule or manually
2. The workflow:

   * Queries GitHub’s GraphQL API for contribution data
   * Generates an animated `garden.svg`
   * Commits the updated SVG back to the repository
3. The SVG is embedded into the profile README using a raw GitHub URL

---

## 📂 Repository Structure
```
GitHub-Garden/
├── .github/
│   └── workflows/
│       └── garden.yml        # GitHub Actions workflow
├── generate_garden.py        # SVG generator script
├── garden.svg                # Auto-generated output
└── README.md                 # Project documentation
```

---

## 🔐 Authentication
This project uses a **Fine-grained GitHub Personal Access Token**.
**Required permissions:**
* **Contents: Read & Write**
The token must be added as a repository secret:
```
GH_TOKEN
```
> The secret must exist **only in this repository**, as GitHub Actions cannot access secrets from other repositories.

---

## 🚀 Setup Instructions
### 1. Fork or Clone the Repository
```bash
git clone https://github.com/<your-username>/GitHub-Garden.git
cd GitHub-Garden
```
### 2. Add Repository Secret
* Go to **Settings → Secrets and variables → Actions**
* Add:
  * **Name:** `GH_TOKEN`
  * **Value:** your fine-grained GitHub token
### 3. Update Username
Edit `generate_garden.py`:
```python
USERNAME = "<your-github-username>"
```
### 4. Run the Workflow
* Go to **Actions → GitHub Garden Workflow**
* Click **Run workflow**
This generates and commits `garden.svg`.
### 5. Embed in Profile README
In your profile repository, add:
```html
<img src="https://github.com/<username>/GitHub-Garden/blob/main/garden.svg?raw=true&v=1">
```
> Increment `v=` when regenerating to bypass GitHub’s image cache.

---

## 🎨 Customization Options
You can easily customize:
* Block size and spacing
* Color palette
* Animation speed and delay
* Flower size and density
* Label placement
> All configuration lives at the top of `generate_garden.py`.

---

## 📌 Design Philosophy
* **Visual clarity over raw numbers**
* **GitHub-native constraints respected**
* **No client-side scripting**
* **Professional, subtle animation**
> The goal is to enhance a profile without breaking accessibility or platform rules.

---

## 📄 License
This project is released under the **MIT License**.
You are free to use, modify, and adapt it with attribution.

---

## 🙌 Acknowledgements
Inspired by GitHub’s contribution graph and the growing ecosystem of profile visualizations — with a focus on elegance, restraint, and technical correctness.

---

~ sukhada20
