# BumpMapping - Jak uruchomić aplikację.

## Instalacja

### 1. **Klonowanie repozytorium:**

```bash
git clone git@github.com:Julo-coder/BumpMapping.git
```

### 2. **Instalacja wirtualnego środowiska:**
#### Linux/MacOS
```bash
python3 -m venv env
source env/bin/activate
```

#### Windows
```bash
python -m venv env
PowerShell: env\Scripts\activate
CMD: env\Scripts\activate.bat
```

### 3. **Instalacja potrzebnych bibliotek:**
#### Linux/MacOS
```bash
pip3 install -r requirements.txt
```

#### Windows
```bash
pip install -r requirements.txt
```
## Ważne do działania na Linuxie z Ubuntu
**Należy dodać poniższy kod do górnej części pliku main.py**
```bash
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
```
