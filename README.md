# CS340_S25_Leo

## 👥 Team Name: Leo

**Team Members:**
- Adam Rodi
- Bishow Adhikari
- Caleb Vivertio
- Max Del Rio

---

## 📁 Dataset Setup

This project uses a large CSV file (~500MB), which is tracked using **Git Large File Storage (LFS)**.

To clone the repository **with the dataset included**, follow these steps:

### 1. Install Git LFS (one-time setup)

- **macOS (Homebrew):**
  ```bash
  brew install git-lfs
  ```

- **Windows:**
  Download and run the installer from [https://git-lfs.com](https://git-lfs.com)

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt install git-lfs
  ```

Then run:
```bash
git lfs install
```

### 2. Clone the repository

```bash
git clone CS340_S25_Leo
```

This will automatically download the full dataset if Git LFS is installed.

---

### Troubleshooting

If you see a `.csv` file that looks like a pointer file (just a few lines of text), it means Git LFS wasn't set up before cloning. Just run:

```bash
git lfs install
git lfs pull
```

This will fetch the actual dataset.
