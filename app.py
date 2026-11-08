import json
import ctypes
import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path

# ---------- Файлы настроек ----------
CONFIG_FILE  = Path.home() / ".ferestruct_config.json"
PRESETS_FILE = Path.home() / ".ferestruct_presets.json"

# ---------- Шрифт (переопределяется в __main__) ----------
FONT = "Segoe UI"

# ---------- Палитры ----------
THEMES = {
    "dark": {
        "BG": "#0f1115", "BG_TOP": "#131722", "BG_BOT": "#0b0d12",
        "BG_CARD": "#181b22", "BG_INPUT": "#20242e", "BORDER": "#2a2f3a",
        "TEXT": "#e6e8ee", "TEXT_DIM": "#8b93a7",
        "ACCENT": "#5b8cff", "ACCENT_H": "#7aa2ff",
        "SUCCESS": "#2fbf71", "SUCCESS_H": "#3fd884",
        "BTN_TEXT": "#ffffff", "ARROW": "#e6e8ee",
        "HEADER_G1": "#5b8cff", "HEADER_G2": "#8b5cf6",
        "CREATE_G1": "#2fbf71", "CREATE_G2": "#5b8cff",
    },
    "light": {
        "BG": "#f4f6fb", "BG_TOP": "#ffffff", "BG_BOT": "#e8ecf5",
        "BG_CARD": "#ffffff", "BG_INPUT": "#eef1f7", "BORDER": "#d3d9e3",
        "TEXT": "#1b1f27", "TEXT_DIM": "#6b7385",
        "ACCENT": "#2f6bff", "ACCENT_H": "#4c82ff",
        "SUCCESS": "#1f9d57", "SUCCESS_H": "#28b866",
        "BTN_TEXT": "#ffffff", "ARROW": "#1b1f27",
        "HEADER_G1": "#2f6bff", "HEADER_G2": "#8b5cf6",
        "CREATE_G1": "#1f9d57", "CREATE_G2": "#2f6bff",
    },
}

# =====================================================================
#  Списки файлов и папок
# =====================================================================
ALL_FILES = [
    # Python
    "main.py", "__init__.py", "app.py", "run.py", "manage.py",
    "config.py", "settings.py", "utils.py", "models.py", "views.py",
    "test_main.py", "conftest.py", "requirements.txt", "requirements-dev.txt",
    "setup.py", "setup.cfg", "pyproject.toml", "Pipfile", "poetry.lock",
    "tox.ini", ".flake8", ".pylintrc", "mypy.ini",
    # Веб
    "index.html", "about.html", "404.html",
    "style.css", "main.css", "reset.css", "styles.scss",
    "app.js", "main.js", "index.js", "script.js", "bundle.js",
    "package.json", "package-lock.json", "tsconfig.json", "vite.config.js",
    # Конфиги
    ".gitignore", ".gitattributes", ".editorconfig",
    ".env", ".env.example", "config.json", "config.yaml", "config.yml",
    "Dockerfile", "docker-compose.yml", ".dockerignore",
    "Makefile", "Procfile", ".pre-commit-config.yaml",
    # Документация
    "README.md", "README.rst", "LICENSE", "CHANGELOG.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    # Данные
    "data.csv", "data.json", "data.xml", ".gitkeep",
]

ALL_FOLDERS = [
    "src", "app", "lib", "bin", "build", "dist", "out",
    "tests", "test", "docs", "doc", "examples", "samples",
    "scripts", "tools", "utils", "helpers",
    "config", "configs", "settings",
    "assets", "static", "public", "media", "images", "img", "fonts", "icons",
    "templates", "layouts", "components", "partials",
    "data", "database", "db", "migrations", "fixtures", "seeds",
    "logs", "tmp", "temp", "cache",
    "vendor", "third_party", "external",
    "plugins", "resources", "themes", "entities", "lighting",
    "sprites", "textures", "audio", "sounds", "music", "shaders",
    "maps", "levels", "scenes", "animations", "ui",
    "core", "api", "services", "repositories", "interfaces",
    "models", "views", "controllers", "routes", "middleware",
    "handlers", "validators", "schemas", "serializers",
]

# =====================================================================
#  Пресеты
# =====================================================================
BUILTIN_PRESETS = {
    "Python-проект (базовый)": {
        "files": ["main.py", "__init__.py", "README.md", "requirements.txt", ".gitignore"],
        "folders": ["src", "tests", "docs"],
    },
    "Python-проект (полный)": {
        "files": ["main.py", "__init__.py", "README.md", "requirements.txt",
                  "requirements-dev.txt", "pyproject.toml", ".gitignore",
                  ".env.example", "LICENSE", "CHANGELOG.md", "conftest.py"],
        "folders": ["src", "tests", "docs", "scripts", "config", "data", "logs"],
    },
    "Веб-проект (простой)": {
        "files": ["index.html", "style.css", "app.js", "README.md"],
        "folders": ["static", "templates", "assets"],
    },
    "Веб-проект (полный)": {
        "files": ["index.html", "about.html", "404.html",
                  "style.css", "main.css", "reset.css",
                  "app.js", "main.js", "package.json",
                  "README.md", ".gitignore"],
        "folders": ["css", "js", "img", "fonts", "components",
                    "pages", "assets", "static", "templates", "public"],
    },
    "Игровой проект (пиксель-арт)": {
        "files": ["main.py", "README.md", "requirements.txt", "config.json", ".gitignore"],
        "folders": ["scripts", "plugins", "resources", "themes",
                    "entities", "lighting", "sprites", "textures",
                    "audio", "sounds", "maps", "levels", "scenes", "ui"],
    },
    "Data Science / ML": {
        "files": ["main.py", "README.md", "requirements.txt",
                  "pyproject.toml", ".gitignore", "data.csv", "config.yaml"],
        "folders": ["data", "notebooks", "models", "scripts",
                    "src", "tests", "docs", "logs", "config"],
    },
    "Django-проект": {
        "files": ["manage.py", "requirements.txt", "README.md",
                  ".gitignore", ".env.example", "settings.py", "config.py"],
        "folders": ["app", "apps", "core", "api", "static",
                    "media", "templates", "migrations",
                    "tests", "docs", "scripts"],
    },
    "FastAPI / Backend": {
        "files": ["main.py", "requirements.txt", "README.md",
                  "pyproject.toml", ".gitignore", ".env.example",
                  "Dockerfile", "docker-compose.yml"],
        "folders": ["app", "api", "core", "models", "schemas",
                    "services", "repositories", "middleware",
                    "tests", "docs", "scripts"],
    },
    "Пусто (всё вручную)": {"files": [], "folders": []},
}


# =====================================================================
#  Загрузка шрифта
# =====================================================================
def load_font(font_path: Path) -> bool:
    if sys.platform != "win32" or not font_path.exists():
        return False
    FR_PRIVATE, FR_NOT_ENUM = 0x10, 0x20
    try:
        path_buf = ctypes.create_unicode_buffer(str(font_path))
        added = ctypes.windll.gdi32.AddFontResourceExW(
            ctypes.byref(path_buf), FR_PRIVATE | FR_NOT_ENUM, 0)
        return added > 0
    except Exception as e:
        print(f"[font] Ошибка: {e}")
        return False


def resource_path(relative: str) -> Path:
    try:
        base = Path(sys._MEIPASS)
    except AttributeError:
        base = Path(__file__).parent
    return base / relative


# =====================================================================
#  Градиенты
# =====================================================================
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((int(r1 + (r2 - r1) * t),
                       int(g1 + (g2 - g1) * t),
                       int(b1 + (b2 - b1) * t)))

def draw_h_gradient(canvas, x1, y1, x2, y2, c1, c2, steps=200):
    w = x2 - x1
    if w <= 0: return
    step_px = max(1, w // steps)
    x = x1
    while x < x2:
        t = (x - x1) / w
        canvas.create_rectangle(x, y1, x + step_px + 1, y2,
                                fill=lerp_color(c1, c2, t), outline="")
        x += step_px

def draw_v_gradient(canvas, x1, y1, x2, y2, c1, c2, steps=200):
    h = y2 - y1
    if h <= 0: return
    step_px = max(1, h // steps)
    y = y1
    while y < y2:
        t = (y - y1) / h
        canvas.create_rectangle(x1, y, x2, y + step_px + 1,
                                fill=lerp_color(c1, c2, t), outline="")
        y += step_px


# =====================================================================
#  Градиентная кнопка
# =====================================================================
class GradientButton(tk.Canvas):
    def __init__(self, parent, text, command, role="success",
                 height=44, radius=12, font=None):
        super().__init__(parent, highlightthickness=0, bd=0, cursor="hand2")
        self.app = parent.winfo_toplevel()
        self.command = command
        self.role = role
        self._radius = radius
        self._text = text
        self._font = font or (FONT, 11, "bold")
        self._btn_h = height
        self._btn_w = 300
        self._hovered = False
        self.configure(height=height)
        self.bind("<Configure>", self._on_resize)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", lambda e: self.command())
        self.after_idle(self.redraw)

    def _on_resize(self, e):
        self._btn_w = max(e.width, 2)
        self._btn_h = max(e.height, 2)
        self.redraw()

    def _colors(self):
        c = self.app.c
        if self.role == "success": return c("CREATE_G1"), c("CREATE_G2"), c("BTN_TEXT")
        if self.role == "accent":  return c("ACCENT"), c("ACCENT_H"), c("BTN_TEXT")
        return c("BG_INPUT"), c("BORDER"), c("TEXT")

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2,
               x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
        return self.create_polygon(pts, smooth=True, **kw)

    def redraw(self):
        try:
            bg = self.app.c("BG_TOP")
            self.configure(bg=bg)
        except Exception:
            return
        self.delete("all")
        w, h = self._btn_w, self._btn_h
        if w < 4 or h < 4: return
        g1, g2, fg = self._colors()
        if self._hovered:
            g1 = lerp_color(g1, "#ffffff", 0.12)
            g2 = lerp_color(g2, "#ffffff", 0.12)
        r = min(self._radius, w // 2, h // 2)
        self._round_rect(1, 1, w-1, h-1, r, fill=g1, outline="")
        steps = max(100, w // 2)
        for i in range(steps):
            t = i / (steps - 1)
            x1 = 1 + (w - 2) * i / steps
            x2 = 1 + (w - 2) * (i + 1) / steps + 1
            self.create_rectangle(x1, 1, x2, h-1,
                                  fill=lerp_color(g1, g2, t), outline="")
        bgcol = bg
        self.create_polygon(1, 1, 1+r, 1, 1, 1+r, fill=bgcol, outline=bgcol)
        self.create_polygon(w-1, 1, w-1-r, 1, w-1, 1+r, fill=bgcol, outline=bgcol)
        self.create_polygon(1, h-1, 1+r, h-1, 1, h-1-r, fill=bgcol, outline=bgcol)
        self.create_polygon(w-1, h-1, w-1-r, h-1, w-1, h-1-r, fill=bgcol, outline=bgcol)
        self.create_text(w/2, h/2, text=self._text, fill=fg, font=self._font)

    def _on_enter(self, _=None):
        self._hovered = True
        self.redraw()

    def _on_leave(self, _=None):
        self._hovered = False
        self.redraw()


# =====================================================================
#  Чекбокс
# =====================================================================
class NiceCheck(tk.Frame):
    def __init__(self, parent, text, variable):
        self.app = parent.winfo_toplevel()
        super().__init__(parent, bd=0, highlightthickness=0)
        self.var = variable
        self.box = tk.Canvas(self, width=18, height=18,
                             highlightthickness=0, bd=0, cursor="hand2")
        self.box.pack(side="left", padx=(2, 8), pady=2)
        self.label = tk.Label(self, text=text, font=(FONT, 10),
                              cursor="hand2", anchor="w")
        self.label.pack(side="left", fill="x", expand=True)
        for w in (self.box, self.label):
            w.bind("<Button-1>", self._toggle)
        self.var.trace_add("write", lambda *_: self._render())
        self.after_idle(self._render)

    def _toggle(self, _=None):
        self.var.set(not self.var.get())

    def _render(self):
        try:
            self.box.delete("all")
            if self.var.get():
                self.box.create_rectangle(1, 1, 17, 17,
                                          fill=self.app.c("ACCENT"),
                                          outline=self.app.c("ACCENT"))
                self.box.create_line(4, 9, 8, 13, 14, 5, fill="white", width=2,
                                     capstyle="round", joinstyle="round")
            else:
                self.box.create_rectangle(1, 1, 17, 17,
                                          fill=self.app.c("BG_INPUT"),
                                          outline=self.app.c("BORDER"), width=1)
        except Exception:
            pass

    def apply_theme(self):
        self.configure(bg=self.app.c("BG_CARD"))
        self.box.configure(bg=self.app.c("BG_CARD"))
        self.label.configure(bg=self.app.c("BG_CARD"), fg=self.app.c("TEXT"))
        self._render()


# =====================================================================
#  Дерево предпросмотра (справа)
# =====================================================================
class PreviewTree(tk.Frame):
    def __init__(self, parent, app):
        self.app = app
        super().__init__(parent, bd=0, highlightthickness=0)
        self._edit_buttons = []
        self._build()

    def _build(self):
        c = self.app.c
        self.configure(bg=c("BG_CARD"), highlightthickness=1,
                       highlightbackground=c("BORDER"))

        self.header = tk.Label(self, text="Структура проекта",
                               font=(FONT, 11, "bold"), anchor="w")
        self.header.pack(fill="x", padx=12, pady=(10, 4))
        self.subtitle = tk.Label(self, text="Предпросмотр из галочек",
                                 font=(FONT, 9), anchor="w")
        self.subtitle.pack(fill="x", padx=12, pady=(0, 8))

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas)
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        self.scroll.pack(side="right", fill="y", pady=(0, 8), padx=(0, 4))

    def update_preview(self, files, folders, project_path=None, is_created=False):
        self.apply_theme()
        for w in self.inner.winfo_children():
            w.destroy()
        self._edit_buttons.clear()
        c = self.app.c

        root_name = project_path.name if project_path else "проект"
        self._add_line(f"📁 {root_name}/", bold=True, color=c("ACCENT"))

        if is_created and project_path:
            self._add_real_tree(project_path, level=1)
        else:
            if not folders and not files:
                self._add_line("(пусто)", italic=True, color=c("TEXT_DIM"), level=1)
                return
            for f in sorted(folders):
                self._add_line(f"📁 {f}/", level=1, color=c("TEXT"))
            for f in sorted(files):
                self._add_line(f"📄 {f}", level=1, color=c("TEXT"))

    def _add_real_tree(self, root: Path, level=1):
        try:
            items = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except Exception:
            return
        if not items:
            return
        for p in items:
            if p.is_dir():
                self._add_line(f"📁 {p.name}/", level=level, color=self.app.c("TEXT"),
                               path=p)
                self._add_real_tree(p, level + 1)
            else:
                self._add_line(f"📄 {p.name}", level=level, color=self.app.c("TEXT"),
                               path=p)

    def _add_line(self, text, level=0, bold=False, italic=False,
                  color=None, path=None):
        c = self.app.c
        color = color or c("TEXT")
        row = tk.Frame(self.inner, bg=c("BG_CARD"))
        row.pack(fill="x", padx=(8 + level*16, 8), pady=1)

        lbl = tk.Label(row, text=text, font=(FONT, 10, "bold" if bold else "normal"),
                       bg=c("BG_CARD"), fg=color, anchor="w",
                       cursor="hand2" if path else "arrow")
        lbl.pack(side="left", fill="x", expand=True)

        if path:
            pencil = tk.Label(row, text="✏", font=(FONT, 10),
                              bg=c("BG_CARD"), fg=c("TEXT_DIM"),
                              cursor="hand2", padx=6)
            pencil.pack(side="right")
            pencil.bind("<Button-1>", lambda e, p=path: self._rename(p))
            pencil.bind("<Enter>", lambda e, w=pencil: w.configure(fg=self.app.c("ACCENT")))
            pencil.bind("<Leave>", lambda e, w=pencil: w.configure(fg=self.app.c("TEXT_DIM")))
            self._edit_buttons.append(pencil)

            lbl.bind("<Double-Button-1>", lambda e, p=path: self._rename(p))

    def _rename(self, path: Path):
        old_name = path.name
        new_name = simpledialog.askstring(
            "Переименовать",
            f"Новое имя для «{old_name}»:",
            initialvalue=old_name,
            parent=self.app,
        )
        if not new_name or new_name == old_name:
            return
        try:
            new_path = path.parent / new_name
            if new_path.exists():
                messagebox.showwarning("Ошибка",
                    f"«{new_name}» уже существует", parent=self.app)
                return
            path.rename(new_path)
            self.app.refresh_preview()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось переименовать:\n{e}",
                                 parent=self.app)

    def apply_theme(self):
        c = self.app.c
        self.configure(bg=c("BG_CARD"), highlightbackground=c("BORDER"))
        self.header.configure(bg=c("BG_CARD"), fg=c("TEXT"))
        self.subtitle.configure(bg=c("BG_CARD"), fg=c("TEXT_DIM"))
        self.canvas.configure(bg=c("BG_CARD"))
        self.inner.configure(bg=c("BG_CARD"))


# =====================================================================
#  Главное приложение
# =====================================================================
class FereStruct(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FereStruct — конструктор проектов")
        self.geometry("1200x900")
        self.minsize(1000, 780)
        self.resizable(True, True)
        self.configure(bg=THEMES["dark"]["BG"])

        # --- Установка иконки окна ---
        try:
            icon_path = resource_path("ferestruct.ico")
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"[icon] Не удалось загрузить иконку: {e}")

        self.config_data = self._load_config()
        self.theme = self.config_data.get("theme", "dark")
        self.file_vars = {name: tk.BooleanVar() for name in ALL_FILES}
        self.folder_vars = {name: tk.BooleanVar() for name in ALL_FOLDERS}
        self.user_presets = self._load_presets()

        self.created_project_path = None

        for var in list(self.file_vars.values()) + list(self.folder_vars.values()):
            var.trace_add("write", lambda *_: self._schedule_preview_update())

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self._build_ui()
        self._apply_preset("Python-проект (базовый)")
        self._apply_theme()

    def c(self, key):
        return THEMES[self.theme][key]

    def _load_config(self):
        if CONFIG_FILE.exists():
            try: return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            except Exception: return {}
        return {}

    def _save_config(self):
        CONFIG_FILE.write_text(json.dumps(self.config_data, ensure_ascii=False, indent=2),
                               encoding="utf-8")

    def _load_presets(self):
        if PRESETS_FILE.exists():
            try: return json.loads(PRESETS_FILE.read_text(encoding="utf-8"))
            except Exception: return {}
        return {}

    def _style_combobox(self):
        self.style.configure("TCombobox",
                             fieldbackground=self.c("BG_INPUT"),
                             background=self.c("BG_INPUT"),
                             foreground=self.c("TEXT"),
                             arrowcolor=self.c("ARROW"),
                             bordercolor=self.c("BORDER"),
                             lightcolor=self.c("BORDER"),
                             darkcolor=self.c("BORDER"),
                             padding=6, font=(FONT, 10))
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", self.c("BG_INPUT"))],
                       foreground=[("readonly", self.c("TEXT"))])
        self.option_add("*TCombobox*Listbox.background", self.c("BG_INPUT"))
        self.option_add("*TCombobox*Listbox.foreground", self.c("TEXT"))
        self.option_add("*TCombobox*Listbox.selectBackground", self.c("ACCENT"))
        self.option_add("*TCombobox*Listbox.font", (FONT, 10))

    def _entry(self, parent):
        return tk.Entry(parent, bg=self.c("BG_INPUT"), fg=self.c("TEXT"),
                        insertbackground=self.c("TEXT"), relief="flat",
                        font=(FONT, 11), highlightthickness=1,
                        highlightbackground=self.c("BORDER"),
                        highlightcolor=self.c("ACCENT"))

    def _button(self, parent, text, command, role="accent", font_size=10, pady=6):
        b = tk.Button(parent, text=text, command=command, relief="flat",
                      bd=0, font=(FONT, font_size, "bold"), cursor="hand2",
                      padx=14, pady=pady)
        b._role = role
        return b

    def _build_ui(self):
        self._style_combobox()

        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.header = tk.Canvas(self, height=90, highlightthickness=0, bd=0)
        self.header.place(x=0, y=0, relwidth=1)
        self.header.bind("<Configure>", self._draw_header)

        self.theme_btn = tk.Button(self, text=self._theme_label(),
                                   command=self._toggle_theme, relief="flat",
                                   bd=0, font=(FONT, 9, "bold"),
                                   cursor="hand2", padx=14, pady=6)
        self.theme_btn.place(relx=1.0, x=-24, y=30, anchor="ne")
        self.theme_btn._role = "ghost"

        self.content = tk.Frame(self)
        self.content.place(x=0, y=100, relwidth=1, relheight=1, height=-100)

        self.split = tk.Frame(self.content)
        self.split.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        self.left_panel = tk.Frame(self.split)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.right_panel = tk.Frame(self.split, width=380)
        self.right_panel.pack(side="right", fill="both")
        self.right_panel.pack_propagate(False)

        self.lbl_name = tk.Label(self.left_panel, text="Имя проекта",
                                 font=(FONT, 9, "bold"), anchor="w")
        self.lbl_name.pack(fill="x", pady=(0, 4))
        self.name_entry = self._entry(self.left_panel)
        self.name_entry.pack(fill="x", pady=(0, 10), ipady=4)
        self.name_entry.insert(0, "my_project")

        self.lbl_path = tk.Label(self.left_panel, text="Куда создать",
                                 font=(FONT, 9, "bold"), anchor="w")
        self.lbl_path.pack(fill="x", pady=(0, 4))
        self.path_frame = tk.Frame(self.left_panel)
        self.path_frame.pack(fill="x", pady=(0, 10))
        self.path_entry = self._entry(self.path_frame)
        self.path_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.path_entry.insert(0, str(Path.home() / "Projects"))
        self.choose_btn = self._button(self.path_frame, "Выбрать…",
                                       self._choose_folder, role="ghost")
        self.choose_btn.pack(side="left", padx=(8, 0))

        self.lbl_preset = tk.Label(self.left_panel, text="Пресет",
                                   font=(FONT, 9, "bold"), anchor="w")
        self.lbl_preset.pack(fill="x", pady=(0, 4))
        self.preset_frame = tk.Frame(self.left_panel)
        self.preset_frame.pack(fill="x", pady=(0, 8))
        self.preset_var = tk.StringVar()
        names = list(BUILTIN_PRESETS.keys()) + list(self.user_presets.keys())
        self.preset_combo = ttk.Combobox(self.preset_frame, textvariable=self.preset_var,
                                         values=names, state="readonly")
        self.preset_combo.pack(side="left", fill="x", expand=True, ipady=2)
        self.preset_combo.bind("<<ComboboxSelected>>",
                               lambda e: self._apply_preset(self.preset_var.get()))
        self.save_preset_btn = self._button(self.preset_frame, "Сохранить",
                                            self._save_current_as_preset, role="ghost")
        self.save_preset_btn.pack(side="left", padx=(8, 0))

        self.toolbar = tk.Frame(self.left_panel)
        self.toolbar.pack(fill="x", pady=(0, 8))
        self.bulk_buttons = []
        for text, store, val in [
            ("Все файлы", self.file_vars, True),
            ("Снять файлы", self.file_vars, False),
            ("Все папки", self.folder_vars, True),
            ("Снять папки", self.folder_vars, False),
        ]:
            b = self._button(self.toolbar, text,
                             lambda s=store, v=val: self._toggle_all(s, v),
                             role="ghost", font_size=9, pady=4)
            b.pack(side="left", padx=(0, 6))
            self.bulk_buttons.append(b)

        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(fill="both", expand=True, pady=(0, 10))

        self.files_tab = tk.Frame(self.notebook, bg=self.c("BG_CARD"))
        self.notebook.add(self.files_tab, text="  Файлы  ")
        self._fill_checkbox_tab(self.files_tab, ALL_FILES, self.file_vars)

        self.folders_tab = tk.Frame(self.notebook, bg=self.c("BG_CARD"))
        self.notebook.add(self.folders_tab, text="  Папки  ")
        self._fill_checkbox_tab(self.folders_tab, ALL_FOLDERS, self.folder_vars)

        self.create_btn = GradientButton(
            self.left_panel, "Создать проект", self._create_project,
            role="success", height=52, font=(FONT, 13, "bold"),
        )
        self.create_btn.pack(fill="x", pady=(0, 8))

        self.preview = PreviewTree(self.right_panel, self)
        self.preview.pack(fill="both", expand=True)

        self.after(100, self.refresh_preview)

    def _fill_checkbox_tab(self, tab, items, store):
        canvas = tk.Canvas(tab, bg=self.c("BG_CARD"), highlightthickness=0)
        scroll = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=self.c("BG_CARD"))
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", pady=8)

        cols = 3
        for i, name in enumerate(items):
            row, col = i // cols, i % cols
            cb = NiceCheck(inner, name, store[name])
            cb.grid(row=row, column=col, sticky="w", padx=6, pady=1)
        for c in range(cols):
            inner.grid_columnconfigure(c, weight=1)

        tab._canvas = canvas
        tab._inner = inner

    def _schedule_preview_update(self):
        if hasattr(self, "_preview_job") and self._preview_job:
            try: self.after_cancel(self._preview_job)
            except Exception: pass
        self._preview_job = self.after(100, self.refresh_preview)

    def refresh_preview(self):
        self._preview_job = None
        if not hasattr(self, "preview"):
            return
        files = [f for f, v in self.file_vars.items() if v.get()]
        folders = [d for d, v in self.folder_vars.items() if v.get()]

        is_created = (self.created_project_path is not None
                      and self.created_project_path.exists())

        self.preview.update_preview(
            files=files, folders=folders,
            project_path=self.created_project_path,
            is_created=is_created,
        )

    def _draw_header(self, event=None):
        w = self.header.winfo_width() or 1200
        h = 90
        self.header.delete("all")
        draw_h_gradient(self.header, 0, 0, w, h,
                        self.c("HEADER_G1"), self.c("HEADER_G2"), steps=300)
        self.header.create_text(24, h/2 - 8, text="FereStruct", anchor="w",
                                fill="#ffffff", font=(FONT, 26, "bold"))
        self.header.create_text(24, h/2 + 20, text="каркас проектов в один клик",
                                anchor="w", fill="#eef1ff", font=(FONT, 10))

    def _draw_bg(self):
        w = self.winfo_width() or 1200
        h = self.winfo_height() or 900
        self.bg_canvas.delete("all")
        draw_v_gradient(self.bg_canvas, 0, 0, w, h,
                        self.c("BG_TOP"), self.c("BG_BOT"), steps=300)

    def _theme_label(self):
        return "Тёмная тема" if self.theme == "dark" else "Светлая тема"

    def _toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.config_data["theme"] = self.theme
        self._save_config()
        self._apply_theme()

    def _apply_theme(self):
        c = self.c
        self.configure(bg=c("BG"))
        self._draw_bg()
        self._draw_header()
        self.theme_btn.configure(text=self._theme_label())

        for lbl in (self.lbl_name, self.lbl_path, self.lbl_preset):
            lbl.configure(bg=c("BG_TOP"), fg=c("TEXT_DIM"))

        self.content.configure(bg=c("BG_TOP"))
        self.split.configure(bg=c("BG_TOP"))
        self.left_panel.configure(bg=c("BG_TOP"))
        self.right_panel.configure(bg=c("BG_TOP"))

        for e in (self.name_entry, self.path_entry):
            e.configure(bg=c("BG_INPUT"), fg=c("TEXT"), insertbackground=c("TEXT"),
                        highlightbackground=c("BORDER"), highlightcolor=c("ACCENT"))

        for fr in (self.path_frame, self.preset_frame, self.toolbar):
            fr.configure(bg=c("BG_TOP"))

        self._style_combobox()
        self._recolor_buttons(self)

        self.style.configure("TNotebook", background=c("BG_TOP"), borderwidth=0)
        self.style.configure("TNotebook.Tab",
                             background=c("BG_INPUT"), foreground=c("TEXT"),
                             padding=(16, 8), font=(FONT, 10, "bold"))
        self.style.map("TNotebook.Tab",
                       background=[("selected", c("ACCENT"))],
                       foreground=[("selected", c("BTN_TEXT"))])

        for tab in (self.files_tab, self.folders_tab):
            tab.configure(bg=c("BG_CARD"))
            tab._canvas.configure(bg=c("BG_CARD"))
            tab._inner.configure(bg=c("BG_CARD"))
            self._retheme_checks(tab._inner)

        self.create_btn.redraw()
        self.preview.apply_theme()
        self.refresh_preview()

    def _recolor_buttons(self, widget):
        c = self.c
        for w in widget.winfo_children():
            if isinstance(w, tk.Button) and hasattr(w, "_role"):
                if w._role == "accent":
                    w.configure(bg=c("ACCENT"), fg=c("BTN_TEXT"),
                                activebackground=c("ACCENT_H"),
                                activeforeground=c("BTN_TEXT"))
                elif w._role == "success":
                    w.configure(bg=c("SUCCESS"), fg=c("BTN_TEXT"),
                                activebackground=c("SUCCESS_H"),
                                activeforeground=c("BTN_TEXT"))
                else:
                    w.configure(bg=c("BG_INPUT"), fg=c("TEXT"),
                                activebackground=c("BORDER"),
                                activeforeground=c("TEXT"))
            self._recolor_buttons(w)

    def _retheme_checks(self, frame):
        for child in frame.winfo_children():
            if isinstance(child, NiceCheck):
                child.apply_theme()
            else:
                self._retheme_checks(child)

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.path_entry.get() or str(Path.home()))
        if folder:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)

    def _toggle_all(self, store, value):
        for var in store.values():
            var.set(value)

    def _apply_preset(self, name):
        preset = BUILTIN_PRESETS.get(name) or self.user_presets.get(name)
        if not preset: return
        for f, var in self.file_vars.items():
            var.set(f in preset["files"])
        for d, var in self.folder_vars.items():
            var.set(d in preset["folders"])
        self.preset_var.set(name)

    def _save_current_as_preset(self):
        name = simpledialog.askstring("Сохранить пресет", "Название пресета:", parent=self)
        if not name: return
        self.user_presets[name] = {
            "files": [f for f, v in self.file_vars.items() if v.get()],
            "folders": [d for d, v in self.folder_vars.items() if v.get()],
        }
        PRESETS_FILE.write_text(
            json.dumps(self.user_presets, ensure_ascii=False, indent=2),
            encoding="utf-8")
        self.preset_combo["values"] = list(BUILTIN_PRESETS.keys()) + list(self.user_presets.keys())
        self.preset_var.set(name)
        messagebox.showinfo("Готово", f"Пресет «{name}» сохранён", parent=self)

    def _create_project(self):
        name = self.name_entry.get().strip()
        parent = Path(self.path_entry.get().strip())
        if not name:
            messagebox.showwarning("Ошибка", "Введите имя проекта", parent=self); return
        if not parent.exists():
            messagebox.showwarning("Ошибка", f"Папка не существует:\n{parent}", parent=self); return
        project_path = parent / name
        if project_path.exists():
            messagebox.showwarning("Ошибка", f"Папка уже существует:\n{project_path}", parent=self); return
        try:
            project_path.mkdir(parents=True)
            created_folders, created_files = [], []
            for folder, var in self.folder_vars.items():
                if var.get():
                    (project_path / folder).mkdir(exist_ok=True)
                    created_folders.append(folder)
            for file, var in self.file_vars.items():
                if var.get():
                    (project_path / file).touch()
                    created_files.append(file)

            self.created_project_path = project_path
            self.refresh_preview()

            msg = (f"Проект создан:\n{project_path}\n\n"
                   f"Папок: {len(created_folders)}\n"
                   f"Файлов: {len(created_files)}\n\n"
                   f"Кликните ✏ рядом с файлом/папкой в предпросмотре,\n"
                   f"чтобы переименовать.")
            messagebox.showinfo("Готово", msg, parent=self)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать:\n{e}", parent=self)


# =====================================================================
#  Точка входа
# =====================================================================
if __name__ == "__main__":
    font_file = resource_path("SchuelerSuperHyperXPPlus.ttf")
    if font_file.exists():
        ok = load_font(font_file)
        print(f"[font] {font_file.name}: {'загружен' if ok else 'не удалось'}")
    else:
        print(f"[font] Файл не найден: {font_file}")

    _probe = tk.Tk()
    _probe.withdraw()
    schueler = [f for f in tkfont.families() if "Schueler" in f]
    print(f"[font] Найдено семейств 'Schueler*': {schueler}")
    if schueler:
        FONT = schueler[0]
        print(f"[font] Использую: {FONT}")
    _probe.destroy()
    globals()["FONT"] = FONT

    FereStruct().mainloop()