# Contributing to TruthInBite 🍎

Thank you for considering contributing to **TruthInBite**, an AI-powered food label analyzer! 🎉 We welcome your help in building a high-quality dataset of food labels and nutrition facts.

Please read the following guidelines carefully before contributing.

---

## 📌 Contribution Rules

* ✅ **Main Branch Only**: All contributions must be made to the `main` branch.
* ✅ **Valid Contributions**: Only **food label images with clear nutrition facts** will be accepted.
* ❌ **Invalid Contributions**: Changes to README, documentation, or code will **not** count as valid contributions.

---

## 📂 Dataset Contribution Format

* Place all images inside the `dataset/` folder.
* File naming convention:

  ```
  itemname.jpg
  itemname.jpeg
  itemname.webp
  ```
* Use lowercase letters for filenames (no spaces, use hyphens or underscores if needed).
* Example:

  ```
  dataset/
  ├── lays-classic.jpg
  ├── amul-milk.jpeg
  └── maggi-noodles.webp
  ```

---

## 🚀 How to Contribute

1. **Fork the Repository**

   ```bash
   git fork https://github.com/vipu18/TruthInBite.git
   ```

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/<your-username>/TruthInBite.git
   cd TruthInBite
   ```

3. **Create/Use the `main` Branch**

   ```bash
   git checkout main
   ```

4. **Add Your Food Label Image(s)**

   * Place your food label image(s) in the `dataset/` folder.
   * Ensure correct filename format.

5. **Stage and Commit Your Changes**

   ```bash
   git add dataset/<your-file>.jpg
   git commit -m "Add <item-name> food label image"
   ```

6. **Push Your Contribution**

   ```bash
   git push origin main
   ```

7. **Open a Pull Request (PR)**

   * Go to the original repo: [TruthInBite](https://github.com/vipu18/TruthInBite)
   * Click **New Pull Request**
   * Select your fork’s `main` branch
   * Add a short title and description
   * Submit your PR 🎉

---

## ✅ Contribution Checklist

Before submitting your PR, make sure:

* [ ] File is inside `dataset/` folder
* [ ] Filename follows correct format (`itemname.jpg/jpeg/webp`)
* [ ] Image is clear and nutrition facts are readable
* [ ] No unnecessary files are changed

---

## 🤝 Contribution Example

```bash
git add dataset/amul-butter.jpg
git commit -m "Add Amul Butter food label image"
git push origin main
```

Then open a PR with the title:

```
Add Amul Butter food label image
```

---

## 🔒 Guidelines

* Do not upload duplicate images.
* Do not upload copyrighted or watermarked images.
* Only contribute original food label images suitable for AI training.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the **MIT License** of this repository.

---

## 📞 Support

For help or questions:

* Open an [issue](https://github.com/vipu18/TruthInBite/issues)
* Tag @vipu18 in discussions

🙏 Thank you for contributing to TruthInBite! Your contributions help make healthy food analysis accessible for everyone. 🚀
