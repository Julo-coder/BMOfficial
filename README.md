# BumpMapping - Jak uruchomic aplikacje.

## Instalacja

1. **Sklonuj repozytorium:**

```bash
git clone git@github.com:Julo-coder/BMOfficial.git
cd MyPythonApp
```

2. **Instalacja wurtialnego srodowiska:**
#### Linux/MacOS
```bash
python3 -m venv env
source env/bin/activate
```

#### Windows
```bash
python -m venv env
env\Scripts\activate
```

3. **Instalacja potrzebnych bibliotek:**
#### Linux/MacOS
```bash
pip3 install -r requirements.txt
```

#### Windows
```bash
pip install -r requirements.txt
```
## Wazne do działania na Linuxie z Ubuntu
**Należy dodać poniższy kod do górnej części pliku main.py**
```bash
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
```
