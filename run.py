import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path(__file__).parent
LANG_DIR = BASE_DIR / "lang"
CONFIG_PATH = BASE_DIR / "config" / "configs.json"

class ConfigEditor:
    def __init__(self, root):
        self.root = root
        self.translations = {}
        self.current_lang = "en"  # Idioma predeterminado: inglés
        self.data = {}
        
        # Cargar configuración e interfaz
        self.load_config()
        self.setup_ui()
        self.load_language()
        self.update_interface()
        
    def setup_ui(self):
        """Configura la interfaz gráfica base"""
        self.root.title("Configuration Editor")
        self.root.geometry("1000x700")
        
        # Barra de menú
        self.menubar = tk.Menu(self.root)
        self.setup_lang_menu()
        self.root.config(menu=self.menubar)
        
        # Pestañas principales
        self.notebook = ttk.Notebook(self.root)
        self.setup_repos_tab()
        self.setup_urls_tab()
        self.setup_servers_tab()
        self.setup_path_tab()
        self.notebook.pack(expand=1, fill="both")
        
    def setup_lang_menu(self):
        """Configura el menú de idioma"""
        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        self.lang_menu.add_command(label="Español", command=lambda: self.change_language("es"))
        self.menubar.add_cascade(label="Language", menu=self.lang_menu)
        
    def setup_repos_tab(self):
        """Configura la pestaña de repositorios"""
        self.repos_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.repos_tab, text="Repositories")
        
        # Lista de repositorios
        self.repo_list = ttk.Treeview(self.repos_tab, columns=("name", "url"), show="headings")
        self.repo_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Controles
        self.repos_control_frame = ttk.Frame(self.repos_tab)
        self.repos_control_frame.pack(side=tk.RIGHT, padx=5, fill=tk.Y)
        
        self.add_repo_btn = ttk.Button(self.repos_control_frame, command=self.add_repo)
        self.edit_repo_btn = ttk.Button(self.repos_control_frame, command=self.edit_repo)
        self.delete_repo_btn = ttk.Button(self.repos_control_frame, command=self.delete_repo)
        
        self.add_repo_btn.pack(fill=tk.X, pady=2)
        self.edit_repo_btn.pack(fill=tk.X, pady=2)
        self.delete_repo_btn.pack(fill=tk.X, pady=2)
        
    def setup_urls_tab(self):
        """Configura la pestaña de URLs"""
        self.urls_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.urls_tab, text="URLs")
        
        self.url_list = ttk.Treeview(self.urls_tab, columns=("type", "url"), show="headings")
        self.url_list.pack(fill=tk.BOTH, expand=True)
        
        self.urls_control_frame = ttk.Frame(self.urls_tab)
        self.urls_control_frame.pack(pady=5)
        self.edit_url_btn = ttk.Button(self.urls_control_frame, command=self.edit_url)
        self.edit_url_btn.pack(side=tk.LEFT, padx=2)
        
    def setup_servers_tab(self):
        """Configura la pestaña de servidores"""
        self.servers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.servers_tab, text="Servers")
        
        columns = ("name", "address", "port")
        self.server_list = ttk.Treeview(self.servers_tab, columns=columns, show="headings")
        self.server_list.pack(fill=tk.BOTH, expand=True)
        
        self.servers_control_frame = ttk.Frame(self.servers_tab)
        self.servers_control_frame.pack(pady=5)
        
        self.add_server_btn = ttk.Button(self.servers_control_frame, command=self.add_server)
        self.edit_server_btn = ttk.Button(self.servers_control_frame, command=self.edit_server)
        self.delete_server_btn = ttk.Button(self.servers_control_frame, command=self.delete_server)
        
        self.add_server_btn.pack(side=tk.LEFT, padx=2)
        self.edit_server_btn.pack(side=tk.LEFT, padx=2)
        self.delete_server_btn.pack(side=tk.LEFT, padx=2)
        
    def setup_path_tab(self):
        """Configura la pestaña de rutas"""
        self.path_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.path_tab, text="Paths")
        
        self.path_label = ttk.Label(self.path_tab)
        self.path_entry = ttk.Entry(self.path_tab, width=80)
        self.save_path_btn = ttk.Button(self.path_tab, command=self.save_path)
        
        self.path_label.pack(pady=5)
        self.path_entry.pack(pady=5, padx=10)
        self.save_path_btn.pack()
        
    def load_config(self):
        """Carga la configuración desde el archivo"""
        try:
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                self.current_lang = self.data.get("language", "en")
            else:
                self.create_default_config()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading configuration:\n{str(e)}")
            self.create_default_config()
            
    def create_default_config(self):
        """Crea una configuración por defecto"""
        self.data = {
            "repos": [],
            "urls": [],
            "servers": [],
            "posixPathExtension": "",
            "language": "en"
        }
        self.save_config()
        
    def save_config(self):
        """Guarda la configuración en el archivo"""
        try:
            CONFIG_PATH.parent.mkdir(exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving configuration:\n{str(e)}")
            
    def load_language(self):
        """Carga las traducciones del idioma seleccionado"""
        lang_file = LANG_DIR / f"lang_{self.current_lang}.json"
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            self.apply_language()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Language file not found: {lang_file}")
            
    def apply_language(self):
        """Aplica las traducciones a toda la interfaz"""
        # Títulos principales
        self.root.title(self.tr("app_title"))
        self.notebook.tab(0, text=self.tr("repositories"))
        self.notebook.tab(1, text=self.tr("urls"))
        self.notebook.tab(2, text=self.tr("servers"))
        self.notebook.tab(3, text=self.tr("paths"))
        
        # Menú
        self.menubar.entryconfig(1, label=self.tr("language"))
        self.lang_menu.entryconfig(0, label="English")
        self.lang_menu.entryconfig(1, label="Español")
        
        # Repositorios
        self.repo_list.heading("name", text=self.tr("name"))
        self.repo_list.heading("url", text=self.tr("url"))
        self.add_repo_btn.config(text=self.tr("add"))
        self.edit_repo_btn.config(text=self.tr("edit"))
        self.delete_repo_btn.config(text=self.tr("delete"))
        
        # URLs
        self.url_list.heading("type", text=self.tr("type"))
        self.url_list.heading("url", text=self.tr("url"))
        self.edit_url_btn.config(text=self.tr("edit"))
        
        # Servidores
        self.server_list.heading("name", text=self.tr("name"))
        self.server_list.heading("address", text=self.tr("address"))
        self.server_list.heading("port", text=self.tr("port"))
        self.add_server_btn.config(text=self.tr("add"))
        self.edit_server_btn.config(text=self.tr("edit"))
        self.delete_server_btn.config(text=self.tr("delete"))
        
        # Rutas
        self.path_label.config(text=f"{self.tr('path')}:")
        self.save_path_btn.config(text=self.tr("save"))
        
    def tr(self, key):
        """Obtiene la traducción para una clave"""
        return self.translations.get(key, key)
        
    def change_language(self, lang):
        """Cambia el idioma de la aplicación"""
        self.current_lang = lang
        self.data["language"] = lang
        self.save_config()
        self.load_language()
        
    def update_interface(self):
        """Actualiza los datos mostrados en la interfaz"""
        # Repositorios
        self.repo_list.delete(*self.repo_list.get_children())
        for repo in self.data.get("repos", []):
            self.repo_list.insert("", "end", values=(repo.get("repo_name", ""), repo.get("url", "")))
            
        # URLs
        self.url_list.delete(*self.url_list.get_children())
        for url in self.data.get("urls", []):
            self.url_list.insert("", "end", values=(url.get("type", ""), url.get("url", "")))
            
        # Servidores
        self.server_list.delete(*self.server_list.get_children())
        for server in self.data.get("servers", []):
            self.server_list.insert("", "end", values=(
                server.get("name", ""),
                server.get("address", ""),
                server.get("duelport", "")
            ))
            
        # Ruta
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.data.get("posixPathExtension", ""))
        
    def add_repo(self):
        """Abre ventana para añadir repositorio"""
        self.edit_repo_window()
        
    def edit_repo(self):
        """Abre ventana para editar repositorio"""
        selected = self.repo_list.selection()
        if selected:
            index = self.repo_list.index(selected[0])
            self.edit_repo_window(index)
            
    def delete_repo(self):
        """Elimina repositorio seleccionado"""
        selected = self.repo_list.selection()
        if selected:
            index = self.repo_list.index(selected[0])
            self.data["repos"].pop(index)
            self.save_config()
            self.update_interface()
            
    def edit_repo_window(self, index=None):
        """Ventana de edición de repositorio"""
        window = tk.Toplevel(self.root)
        window.title(self.tr("edit_repository") if index is not None else self.tr("add_repository"))
        
        fields = [
            ("repo_name", self.tr("repo_name") + ":"),
            ("url", self.tr("url") + ":"),
            ("repo_path", self.tr("local_path") + ":"),
            ("has_core", self.tr("has_core") + ":", "check"),
            ("core_path", self.tr("core_path") + ":"),
            ("data_path", self.tr("data_path") + ":"),
            ("script_path", self.tr("script_path") + ":"),
            ("should_update", self.tr("auto_update") + ":", "check"),
            ("should_read", self.tr("auto_read") + ":", "check")
        ]
        
        entries = {}
        for row, (field, label, *type_) in enumerate(fields):
            ttk.Label(window, text=label).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            if type_ and type_[0] == "check":
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(window, variable=var)
                cb.grid(row=row, column=1, sticky="w")
                entries[field] = var
            else:
                entry = ttk.Entry(window, width=40)
                entry.grid(row=row, column=1, padx=5, pady=2)
                entries[field] = entry
        
        if index is not None:
            repo_data = self.data["repos"][index]
            for field, widget in entries.items():
                if isinstance(widget, ttk.Entry):
                    widget.insert(0, repo_data.get(field, ""))
                elif isinstance(widget, tk.BooleanVar):
                    widget.set(repo_data.get(field, False))

        def save_changes():
            new_data = {}
            for field, widget in entries.items():
                if isinstance(widget, tk.BooleanVar):
                    new_data[field] = widget.get()
                else:
                    new_data[field] = widget.get()
            
            if index is not None:
                self.data["repos"][index] = new_data
            else:
                self.data["repos"].append(new_data)
            
            self.save_config()
            self.update_interface()
            window.destroy()
        
        ttk.Button(window, text=self.tr("save"), command=save_changes).grid(row=len(fields)+1, columnspan=2, pady=10)

    def edit_url(self):
        """Abre ventana para editar URL"""
        selected = self.url_list.selection()
        if selected:
            index = self.url_list.index(selected[0])
            self.edit_url_window(index)
            
    def edit_url_window(self, index=None):
        """Ventana de edición de URL"""
        window = tk.Toplevel(self.root)
        window.title(self.tr("edit_url") if index is not None else self.tr("add_url"))
        
        ttk.Label(window, text=self.tr("type") + ":").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        type_combo = ttk.Combobox(window, values=["pic", "field", "cover"], state="readonly")
        type_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(window, text=self.tr("url") + ":").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        url_entry = ttk.Entry(window, width=40)
        url_entry.grid(row=1, column=1, padx=5, pady=2)
        
        if index is not None:
            url_data = self.data["urls"][index]
            type_combo.set(url_data["type"])
            url_entry.insert(0, url_data["url"])

        def save_changes():
            new_data = {
                "type": type_combo.get(),
                "url": url_entry.get()
            }
            
            if index is not None:
                self.data["urls"][index] = new_data
            else:
                self.data["urls"].append(new_data)
            
            self.save_config()
            self.update_interface()
            window.destroy()
        
        ttk.Button(window, text=self.tr("save"), command=save_changes).grid(row=2, columnspan=2, pady=10)

    def add_server(self):
        """Abre ventana para añadir servidor"""
        self.edit_server_window()
        
    def edit_server(self):
        """Abre ventana para editar servidor"""
        selected = self.server_list.selection()
        if selected:
            index = self.server_list.index(selected[0])
            self.edit_server_window(index)
            
    def delete_server(self):
        """Elimina servidor seleccionado"""
        selected = self.server_list.selection()
        if selected:
            index = self.server_list.index(selected[0])
            self.data["servers"].pop(index)
            self.save_config()
            self.update_interface()
            
    def edit_server_window(self, index=None):
        """Ventana de edición de servidor"""
        window = tk.Toplevel(self.root)
        window.title(self.tr("edit_server") if index is not None else self.tr("add_server"))
        
        fields = [
            ("name", self.tr("name") + ":"),
            ("address", self.tr("address") + ":"),
            ("duelport", self.tr("duel_port") + ":"),
            ("roomaddress", self.tr("room_address") + ":"),
            ("roomlistprotocol", self.tr("protocol") + ":"),
            ("roomlistport", self.tr("list_port") + ":")
        ]
        
        entries = {}
        for row, (field, label) in enumerate(fields):
            ttk.Label(window, text=label).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(window, width=30)
            entry.grid(row=row, column=1, padx=5, pady=2)
            entries[field] = entry
        
        if index is not None:
            server_data = self.data["servers"][index]
            for field, entry in entries.items():
                entry.insert(0, str(server_data.get(field, "")))

        def save_changes():
            new_data = {}
            try:
                for field, entry in entries.items():
                    value = entry.get()
                    if "port" in field:
                        new_data[field] = int(value)
                    else:
                        new_data[field] = value
                
                if index is not None:
                    self.data["servers"][index] = new_data
                else:
                    self.data["servers"].append(new_data)
                
                self.save_config()
                self.update_interface()
                window.destroy()
            except ValueError:
                messagebox.showerror(self.tr("error"), self.tr("port_number_error"))
        
        ttk.Button(window, text=self.tr("save"), command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def save_path(self):
        """Guarda la ruta POSIX"""
        self.data["posixPathExtension"] = self.path_entry.get()
        self.save_config()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigEditor(root)
    root.mainloop()