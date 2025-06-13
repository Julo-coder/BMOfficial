# Funkcjonalności programu BumpMapping

## Folder `shaders`

Folder `shaders` zawiera pliki z kodem shaderów napisanych w języku GLSL, które są wykorzystywane do renderowania grafiki 3D w projekcie. Shadery te odpowiadają za przetwarzanie geometrii, oświetlenie oraz generowanie efektów wizualnych na obiektach i tle sceny. Każdy plik pełni inną funkcję i jest niezbędny do prawidłowego wyświetlania sceny 3D.

Pliki znajdujące się w folderze `shaders`:

- **`vertex_shader.glsl`**  
  Vertex shader obsługujący standardowe obiekty 3D. Przekształca pozycje wierzchołków z przestrzeni lokalnej do świata i kamery, oblicza macierz TBN potrzebną do mapowania normalnych oraz przekazuje dane do kolejnego etapu renderowania. Dzięki temu możliwe jest realistyczne oświetlenie i teksturowanie powierzchni.

- **`fragment_shader.glsl`**  
  Fragment shader, który wylicza końcowy kolor każdego piksela obiektu 3D. Pobiera dane z vertex shadera, korzysta z tekstur i map normalnych, a także oblicza efekty oświetlenia, takie jak światło rozproszone, odbite i otoczenia. Pozwala to uzyskać realistyczny wygląd materiałów na obiektach.

## Folder `textures`

Folder `textures` zawiera podfoldery z teksturami materiałów wykorzystywanych do pokrywania powierzchni obiektów 3D w scenie. Każdy podfolder odpowiada innemu rodzajowi materiału i zawiera dwa pliki graficzne: teksturę koloru (Color) oraz teksturę normalnych (NormalGL), które są używane do realistycznego odwzorowania wyglądu powierzchni.

- **Fabric_048/** – Zawiera tekstury materiału tkaniny: `Fabric048_1K-JPG_Color.jpg` (kolor) oraz `Fabric048_1K-JPG_NormalGL.jpg` (mapa normalnych).
- **Ground_080/** – Zawiera tekstury gruntu: `Ground080_1K-JPG_Color.jpg` (kolor) oraz `Ground080_1K-JPG_NormalGL.jpg` (mapa normalnych).
- **Rock_062/** – Zawiera tekstury skały: `Rock062_1K-JPG_Color.jpg` (kolor) oraz `Rock062_1K-JPG_NormalGL.jpg` (mapa normalnych).

Tekstury te są wykorzystywane przez shadery do nadawania obiektom odpowiedniego wyglądu, koloru oraz efektu wypukłości powierzchni, co znacząco zwiększa realizm wyświetlanej sceny 3D.

## Szczegółowy opis funkcji w pliku `main.py`

### Funkcja `load_shader(vertex_path, fragment_path)`

```python
def load_shader(vertex_path, fragment_path):
```

Funkcja `load_shader` odpowiada za ładowanie i kompilację shaderów z plików tekstowych. Składa się z następujących kroków:

- **Odczyt plików:**  
  ```python
  with open(vertex_path) as f:
      vertex_src = f.read()
  with open(fragment_path) as f:
      fragment_src = f.read()
  ```
  Odczytuje kod źródłowy vertex i fragment shadera z podanych ścieżek.

- **Tworzenie i kompilacja shaderów:**  
  ```python
  shader = glCreateProgram()
  vs = glCreateShader(GL_VERTEX_SHADER)
  fs = glCreateShader(GL_FRAGMENT_SHADER)
  ```
  Tworzy program shaderowy oraz dwa shadery: wierzchołków i fragmentów.

- **Przypisanie źródła i kompilacja:**  
  ```python
  glShaderSource(vs, vertex_src)
  glCompileShader(vs)
  ...
  glShaderSource(fs, fragment_src)
  glCompileShader(fs)
  ```
  Przypisuje kod źródłowy do shaderów i je kompiluje. Sprawdza poprawność kompilacji i zgłasza błąd, jeśli wystąpi.

- **Łączenie shaderów w program:**  
  ```python
  glAttachShader(shader, vs)
  glAttachShader(shader, fs)
  glLinkProgram(shader)
  ```
  Łączy oba shadery w jeden program shaderowy i sprawdza poprawność linkowania.

- **Czyszczenie:**  
  ```python
  glDeleteShader(vs)
  glDeleteShader(fs)
  ```
  Usuwa niepotrzebne już obiekty shaderów.

- **Zwracanie programu:**  
  Funkcja zwraca identyfikator gotowego programu shaderowego.

### Funkcja `load_texture(path, unit)`

```python
def load_texture(path, unit):
```

Funkcja `load_texture` ładuje plik graficzny jako teksturę OpenGL i przypisuje ją do wybranej jednostki teksturującej. Składa się z następujących kroków:

- **Wczytanie i przygotowanie obrazu:**  
  ```python
  img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
  img_data = np.array(img, dtype=np.uint8)
  ```
  Otwiera plik graficzny, obraca go pionowo (zgodnie z konwencją OpenGL) i konwertuje do formatu RGB.

- **Tworzenie tekstury i przypisanie do jednostki:**  
  ```python
  tex = glGenTextures(1)
  glActiveTexture(GL_TEXTURE0 + unit)
  glBindTexture(GL_TEXTURE_2D, tex)
  ```
  Tworzy nową teksturę, aktywuje odpowiednią jednostkę teksturującą i wiąże teksturę.

- **Przesyłanie danych obrazu do GPU:**  
  ```python
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
  glGenerateMipmap(GL_TEXTURE_2D)
  ```
  Przesyła dane obrazu do karty graficznej i generuje mipmapy.

- **Ustawianie parametrów tekstury:**  
  ```python
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
  ```
  Ustawia sposób powielania tekstury oraz filtrowania.

- **Zwracanie identyfikatora tekstury:**  
  Funkcja zwraca identyfikator utworzonej tekstury.

### Funkcja `main()`

```python
def main():
```

Funkcja `main` jest sercem programu i odpowiada za całą logikę działania aplikacji. Składa się z następujących głównych sekcji:

- **Inicjalizacja Pygame i OpenGL:**  
  ```python
  pygame.init()
  pygame.display.gl_set_attribute(...)
  pygame.display.set_mode(...)
  ```
  Ustawia parametry kontekstu OpenGL, tworzy okno, ustawia tytuł, ukrywa kursor i blokuje go w oknie.

- **Tworzenie kamery:**  
  ```python
  camera = Camera(screen_width, screen_height)
  ```
  Tworzy obiekt kamery, który obsługuje ruch i obrót w scenie 3D.

- **Ładowanie shaderów:**  
  ```python
  shader = load_shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
  ```
  Ładuje i kompiluje shadery do renderowania obiektów.

- **Tworzenie obiektów geometrycznych:**  
  ```python
  cube_vao, cube_index_count = create_cube()
  sphere_vao, sphere_index_count = create_sphere()
  ```
  Generuje VAO i indeksy dla sześcianu i kuli.

- **Ładowanie tekstur:**  
  ```python
  textures = {
      "Ground_080": {...},
      "Rock_062": {...},
      "Fabric_048": {...}
  }
  ```
  Ładuje tekstury kolorów i map normalnych dla różnych materiałów i przypisuje je do słownika.

- **Generowanie pozycji obiektów:**  
  ```python
  positions = []
  for _ in range(6):
      ...
      positions.append(glm.vec3(x, y, z))
  ```
  Losuje pozycje dla sześcianów i kul w scenie.

- **Tworzenie listy obiektów w scenie:**  
  ```python
  scene_objects = [
      {"type": "cube", "position": positions[0], "texture": texture_names[0]},
      ...
  ]
  ```
  Tworzy listę słowników opisujących typ, pozycję i teksturę każdego obiektu.

- **Ustawienie projekcji:**  
  ```python
  projection = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)
  ```
  Tworzy macierz projekcji perspektywicznej.

- **Główna pętla renderująca:**  
  ```python
  while running:
      for e in pygame.event.get():
          ...
      keys = pygame.key.get_pressed()
      camera.process_keyboard(keys)
      camera.process_mouse_movement_relative()
      view = camera.get_view_matrix()
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      ...
      for obj in scene_objects:
          ...
          glUniformMatrix4fv(...)
          if obj["type"] == "cube":
              ...
          else:
              ...
      pygame.display.flip()
      clock.tick(60)
  ```
  Obsługuje zdarzenia (wyjście, klawiatura, mysz), aktualizuje kamerę, czyści bufor, ustawia shadery i tekstury, rysuje wszystkie obiekty w scenie, a na końcu odświeża ekran.

- **Zamykanie programu:**  
  ```python
  pygame.quit()
  sys.exit()
  ```
  Po zakończeniu pętli renderującej zamyka aplikację.

## Szczegółowy opis funkcji w pliku `camera.py`

### Konstruktor `__init__(self, window_width=800, window_height=600)`

```python
def __init__(self, window_width=800, window_height=600):
```

Konstruktor klasy `Camera` inicjalizuje wszystkie najważniejsze parametry kamery:

- **Pozycja i wektory kierunkowe:**
  - `self.position` – początkowa pozycja kamery w przestrzeni (domyślnie `[0, 0, 3]`).
  - `self.front` – kierunek patrzenia kamery (domyślnie w stronę osi -Z).
  - `self.up` – wektor "do góry" kamery.
  - `self.right` – wektor "w prawo" kamery (wyliczany później).
  - `self.world_up` – globalny wektor "do góry" (stały, `[0, 1, 0]`).

- **Kąty Eulera:**
  - `self.yaw` – kąt obrotu wokół osi Y (domyślnie -90°, patrzenie w -Z).
  - `self.pitch` – kąt obrotu wokół osi X (domyślnie 0°).

- **Parametry ruchu:**
  - `self.movement_speed` – szybkość ruchu kamery.
  - `self.sensitivity` – czułość myszy.

- **Parametry okna:**
  - `self.window_width`, `self.window_height` – rozmiary okna.
  - `self.center_x`, `self.center_y` – środek okna.

- **Obsługa myszy:**
  - `self.last_x`, `self.last_y` – ostatnia pozycja myszy.
  - `self.first_mouse` – flaga pierwszego ruchu myszy.

- **Inicjalizacja wektorów kierunkowych:**
  - Wywołuje `self.update_camera_vectors()`, aby ustawić poprawne wektory na starcie.

---

### Funkcja `get_view_matrix(self)`

```python
def get_view_matrix(self):
```

Zwraca macierz widoku (view matrix) dla kamery, która jest używana przez OpenGL do przekształcenia sceny względem pozycji i kierunku patrzenia kamery.  
- Wykorzystuje funkcję `glm.lookAt`, przekazując aktualną pozycję kamery, punkt patrzenia (`position + front`) oraz wektor "do góry" (`up`).

---

### Funkcja `process_keyboard(self, keys)`

```python
def process_keyboard(self, keys):
```

Obsługuje ruch kamery za pomocą klawiatury.  
- Sprawdza, które klawisze są wciśnięte (`K_w`, `K_s`, `K_a`, `K_d`, `K_SPACE`, `K_LSHIFT`) i odpowiednio przesuwa kamerę:
  - `K_w` – do przodu (w kierunku `front`)
  - `K_s` – do tyłu
  - `K_a` – w lewo (w kierunku `-right`)
  - `K_d` – w prawo
  - `K_SPACE` – w górę (oś Y)
  - `K_LSHIFT` – w dół (oś Y)

---

### Funkcja `process_mouse_movement(self, x_pos, y_pos)`

```python
def process_mouse_movement(self, x_pos, y_pos):
```

Obsługuje ruch kamery na podstawie absolutnej pozycji myszy (np. gdy korzystamy z klasycznego systemu kursora).  
- Przy pierwszym ruchu ustawia pozycję początkową i nie wykonuje obrotu.
- Oblicza przesunięcie kursora względem poprzedniej pozycji (`x_offset`, `y_offset`).
- Przelicza przesunięcie przez czułość (`sensitivity`).
- Aktualizuje kąty `yaw` i `pitch` (obrót kamery).
- Ogranicza zakres `pitch` do [-89°, 89°], by uniknąć "przekręcenia" kamery.
- Wywołuje `update_camera_vectors()` do przeliczenia nowych wektorów kierunkowych.

---

### Funkcja `process_mouse_movement_relative(self)`

```python
def process_mouse_movement_relative(self):
```

Obsługuje ruch kamery na podstawie relatywnego przesunięcia myszy (np. w trybie FPS, gdy kursor jest ukryty i "zablokowany" w oknie).  
- Pobiera przesunięcie kursora od ostatniej klatki (`pygame.mouse.get_rel()`).
- Przelicza przesunięcie przez czułość (`sensitivity`).
- Aktualizuje kąty `yaw` i `pitch`.
- Ogranicza zakres `pitch` do [-89°, 89°].
- Wywołuje `update_camera_vectors()` do przeliczenia nowych wektorów kierunkowych.

---

#### Funkcja `update_camera_vectors(self)`

```python
def update_camera_vectors(self):
```

Aktualizuje wektory kierunkowe kamery (`front`, `right`, `up`) na podstawie aktualnych kątów `yaw` i `pitch`.  
- Oblicza nowy wektor `front` na podstawie równań trygonometrycznych.
- Normalizuje wektor `front`.
- Wylicza wektor `right` jako iloczyn wektorowy `front` i `world_up`.
- Wylicza wektor `up` jako iloczyn wektorowy `right` i `front`.
- Dzięki temu kamera zawsze patrzy w odpowiednim kierunku, a ruchy są płynne i zgodne z oczekiwaniami użytkownika.

## Szczegółowy opis funkcji w pliku `shapes.py`

### Funkcja `create_quad()`

```python
def create_quad():
```

Funkcja `create_quad` tworzy prostokątny quad (płaski prostokąt) do renderowania w OpenGL. Składa się z następujących etapów:

- **Definicja wierzchołków i indeksów:**
  - `vertices` – tablica floatów opisująca pozycje wierzchołków (x, y, z), współrzędne tekstury (u, v), normalne (nx, ny, nz) oraz tangensy (tx, ty, tz) dla każdego z czterech wierzchołków.
  - `indices` – tablica indeksów określająca, które wierzchołki tworzą dwa trójkąty quada.

- **Tworzenie i wiązanie VAO, VBO, EBO:**
  - `vao = glGenVertexArrays(1)` – tworzy obiekt tablicy wierzchołków (VAO).
  - `vbo = glGenBuffers(1)` – tworzy bufor wierzchołków (VBO).
  - `ebo = glGenBuffers(1)` – tworzy bufor indeksów (EBO).
  - Dane są przesyłane do GPU za pomocą `glBufferData`.

- **Konfiguracja atrybutów wierzchołków:**
  - Pętla `for i, size in enumerate([3, 2, 3, 3])` ustawia wskaźniki atrybutów dla pozycji, tekstury, normalnych i tangensów.
  - `glVertexAttribPointer` i `glEnableVertexAttribArray` aktywują odpowiednie atrybuty.

- **Zakończenie i zwrot:**
  - `glBindVertexArray(0)` – odwiązuje VAO.
  - Funkcja zwraca identyfikator VAO oraz liczbę indeksów (do rysowania quada).

---

### Funkcja `create_cube()`

```python
def create_cube():
```

Funkcja `create_cube` generuje dane i buforuje je w GPU, aby utworzyć sześcian do renderowania w OpenGL. Składa się z następujących etapów:

- **Definicja wierzchołków i indeksów:**
  - `vertices` – tablica floatów opisująca pozycje wierzchołków (x, y, z), współrzędne tekstury (u, v), normalne (nx, ny, nz) oraz tangensy (tx, ty, tz) dla każdej ściany sześcianu.
  - `indices` – tablica indeksów określająca, które wierzchołki tworzą trójkąty każdej ściany sześcianu.

- **Tworzenie i wiązanie VAO, VBO, EBO:**
  - `vao = glGenVertexArrays(1)` – tworzy VAO.
  - `vbo = glGenBuffers(1)` – tworzy VBO.
  - `ebo = glGenBuffers(1)` – tworzy EBO.
  - Dane są przesyłane do GPU za pomocą `glBufferData`.

- **Konfiguracja atrybutów wierzchołków:**
  - Pętla `for i, size in enumerate([3, 2, 3, 3])` ustawia wskaźniki atrybutów dla pozycji, tekstury, normalnych i tangensów.
  - `glVertexAttribPointer` i `glEnableVertexAttribArray` aktywują odpowiednie atrybuty.

- **Zakończenie i zwrot:**
  - `glBindVertexArray(0)` – odwiązuje VAO.
  - Funkcja zwraca identyfikator VAO oraz liczbę indeksów (do rysowania sześcianu).

---

### Funkcja `create_sphere(stacks=20, sectors=20, radius=0.5)`

```python
def create_sphere(stacks=20, sectors=20, radius=0.5):
```

Funkcja `create_sphere` generuje dane i buforuje je w GPU, aby utworzyć sferę do renderowania w OpenGL. Składa się z następujących etapów:

- **Generowanie wierzchołków:**
  - Pętla po `stacks` i `sectors` generuje współrzędne sferyczne każdego wierzchołka.
  - Dla każdego wierzchołka wyliczane są:
    - Pozycja (x, y, z)
    - Współrzędne tekstury (U, V)
    - Wektor normalny (nx, ny, nz)
    - Tangens (tx, ty, tz) – przybliżony, prostopadły do normalnej i znormalizowany
  - Wszystkie dane są dodawane do listy `vertices`.

- **Generowanie indeksów:**
  - Pętla po `stacks` i `sectors` generuje indeksy trójkątów tworzących siatkę sfery.
  - Indeksy są dodawane do listy `indices`.

- **Konwersja do tablic numpy:**
  - `vertices` i `indices` są konwertowane do odpowiednich typów numpy (`np.float32`, `np.uint32`).

- **Tworzenie i wiązanie VAO, VBO, EBO:**
  - `vao = glGenVertexArrays(1)` – tworzy VAO.
  - `vbo = glGenBuffers(1)` – tworzy VBO.
  - `ebo = glGenBuffers(1)` – tworzy EBO.
  - Dane są przesyłane do GPU za pomocą `glBufferData`.

- **Konfiguracja atrybutów wierzchołków:**
  - Pętla `for i, size in enumerate([3, 2, 3, 3])` ustawia wskaźniki atrybutów dla pozycji, tekstury, normalnych i tangensów.
  - `glVertexAttribPointer` i `glEnableVertexAttribArray` aktywują odpowiednie atrybuty.

- **Zakończenie i zwrot:**
  - `glBindVertexArray(0)` – odwiązuje VAO.
  - Funkcja zwraca identyfikator VAO oraz liczbę indeksów (do rysowania sfery).

