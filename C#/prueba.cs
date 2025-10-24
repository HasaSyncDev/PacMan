import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import sys

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PacMan Desktop - Aplicación Principal")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a2e')
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_styles(self):
        """Configurar estilos para la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores personalizados
        style.configure('Title.TLabel', 
                       font=('Arial', 24, 'bold'),
                       foreground='#ffd700',
                       background='#1a1a2e')
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 14),
                       foreground='#ffffff',
                       background='#1a1a2e')
        
        style.configure('Game.TButton',
                       font=('Arial', 12, 'bold'),
                       foreground='#ffffff',
                       background='#2d4a22')
        
        style.configure('Utility.TButton',
                       font=('Arial', 10),
                       foreground='#ffffff',
                       background='#4a4a4a')
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título principal
        title_label = ttk.Label(main_frame, 
                               text="PACMAN DESKTOP",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Subtítulo
        subtitle_label = ttk.Label(main_frame,
                                  text="Selecciona una opción para comenzar",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 40))
        
        # Frame para botones de juegos
        games_frame = tk.Frame(main_frame, bg='#1a1a2e')
        games_frame.pack(pady=20)
        
        # Botón para ejecutar PacMan original
        pacman_btn = ttk.Button(games_frame,
                                text="🎮 JUGAR PACMAN",
                                style='Game.TButton',
                                command=self.run_pacman_game)
        pacman_btn.pack(pady=10, padx=20, ipadx=20, ipady=10)
        
        # Botón para ejecutar PacMan copia
        pacman_copy_btn = ttk.Button(games_frame,
                                    text="🎮 JUGAR PACMAN (COPIA)",
                                    style='Game.TButton',
                                    command=self.run_pacman_copy)
        pacman_copy_btn.pack(pady=10, padx=20, ipadx=20, ipady=10)
        
        # Separador
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=30)
        
        # Frame para utilidades
        utils_frame = tk.Frame(main_frame, bg='#1a1a2e')
        utils_frame.pack(pady=20)
        
        # Botón para abrir carpeta del proyecto
        open_folder_btn = ttk.Button(utils_frame,
                                    text="📁 Abrir Carpeta del Proyecto",
                                    style='Utility.TButton',
                                    command=self.open_project_folder)
        open_folder_btn.pack(pady=5, padx=20, ipadx=10, ipady=5)
        
        # Botón para ver información del sistema
        system_info_btn = ttk.Button(utils_frame,
                                   text="ℹ️ Información del Sistema",
                                   style='Utility.TButton',
                                   command=self.show_system_info)
        system_info_btn.pack(pady=5, padx=20, ipadx=10, ipady=5)
        
        # Botón para configuraciones
        settings_btn = ttk.Button(utils_frame,
                                 text="⚙️ Configuraciones",
                                 style='Utility.TButton',
                                 command=self.open_settings)
        settings_btn.pack(pady=5, padx=20, ipadx=10, ipady=5)
        
        # Frame para información
        info_frame = tk.Frame(main_frame, bg='#1a1a2e')
        info_frame.pack(side='bottom', fill='x', pady=(40, 0))
        
        # Información de estado
        self.status_label = ttk.Label(info_frame,
                                     text="Listo para jugar",
                                     style='Subtitle.TLabel')
        self.status_label.pack()
        
        # Información de versión
        version_label = ttk.Label(info_frame,
                                text="Versión 1.0 - Desktop App",
                                font=('Arial', 8),
                                foreground='#888888',
                                background='#1a1a2e')
        version_label.pack()
    
    def run_pacman_game(self):
        """Ejecutar el juego PacMan principal"""
        try:
            self.status_label.config(text="Iniciando PacMan...")
            self.root.update()
            
            # Verificar si el archivo existe
            pacman_file = "pacman.py"
            if os.path.exists(pacman_file):
                subprocess.Popen([sys.executable, pacman_file])
                self.status_label.config(text="PacMan iniciado correctamente")
                messagebox.showinfo("Éxito", "PacMan se ha iniciado correctamente!")
            else:
                messagebox.showerror("Error", f"No se encontró el archivo {pacman_file}")
                self.status_label.config(text="Error: Archivo no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar PacMan: {str(e)}")
            self.status_label.config(text="Error al iniciar el juego")
    
    def run_pacman_copy(self):
        """Ejecutar la copia del juego PacMan"""
        try:
            self.status_label.config(text="Iniciando PacMan (Copia)...")
            self.root.update()
            
            # Verificar si el archivo existe
            pacman_copy_file = "pacman - copia.py"
            if os.path.exists(pacman_copy_file):
                subprocess.Popen([sys.executable, pacman_copy_file])
                self.status_label.config(text="PacMan (Copia) iniciado correctamente")
                messagebox.showinfo("Éxito", "PacMan (Copia) se ha iniciado correctamente!")
            else:
                messagebox.showerror("Error", f"No se encontró el archivo {pacman_copy_file}")
                self.status_label.config(text="Error: Archivo no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar PacMan (Copia): {str(e)}")
            self.status_label.config(text="Error al iniciar el juego")
    
    def open_project_folder(self):
        """Abrir la carpeta del proyecto en el explorador"""
        try:
            project_path = os.getcwd()
            if sys.platform == "win32":
                os.startfile(project_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", project_path])
            else:  # Linux
                subprocess.run(["xdg-open", project_path])
            
            self.status_label.config(text="Carpeta del proyecto abierta")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la carpeta: {str(e)}")
    
    def show_system_info(self):
        """Mostrar información del sistema"""
        import platform
        
        info = f"""
Información del Sistema:

Sistema Operativo: {platform.system()} {platform.release()}
Arquitectura: {platform.machine()}
Procesador: {platform.processor()}
Python: {platform.python_version()}

Archivos del Proyecto:
"""
        
        # Listar archivos del proyecto
        files = os.listdir(".")
        for file in files:
            if file.endswith(('.py', '.cs')):
                info += f"• {file}\n"
        
        messagebox.showinfo("Información del Sistema", info)
        self.status_label.config(text="Información del sistema mostrada")
    
    def open_settings(self):
        """Abrir ventana de configuraciones"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configuraciones")
        settings_window.geometry("400x300")
        settings_window.configure(bg='#1a1a2e')
        
        # Centrar la ventana
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Título
        title = ttk.Label(settings_window,
                         text="Configuraciones",
                         style='Title.TLabel')
        title.pack(pady=20)
        
        # Frame para opciones
        options_frame = tk.Frame(settings_window, bg='#1a1a2e')
        options_frame.pack(expand=True, fill='both', padx=20)
        
        # Opción de tema
        theme_label = ttk.Label(options_frame,
                               text="Tema:",
                               style='Subtitle.TLabel')
        theme_label.pack(anchor='w', pady=5)
        
        theme_var = tk.StringVar(value="Oscuro")
        theme_combo = ttk.Combobox(options_frame,
                                  textvariable=theme_var,
                                  values=["Oscuro", "Claro", "Automático"])
        theme_combo.pack(fill='x', pady=5)
        
        # Opción de idioma
        lang_label = ttk.Label(options_frame,
                              text="Idioma:",
                              style='Subtitle.TLabel')
        lang_label.pack(anchor='w', pady=(20, 5))
        
        lang_var = tk.StringVar(value="Español")
        lang_combo = ttk.Combobox(options_frame,
                                 textvariable=lang_var,
                                 values=["Español", "English", "Français"])
        lang_combo.pack(fill='x', pady=5)
        
        # Botones
        buttons_frame = tk.Frame(options_frame, bg='#1a1a2e')
        buttons_frame.pack(side='bottom', fill='x', pady=20)
        
        save_btn = ttk.Button(buttons_frame,
                            text="Guardar",
                            style='Game.TButton',
                            command=lambda: self.save_settings(theme_var.get(), lang_var.get()))
        save_btn.pack(side='right', padx=5)
        
        cancel_btn = ttk.Button(buttons_frame,
                              text="Cancelar",
                              style='Utility.TButton',
                              command=settings_window.destroy)
        cancel_btn.pack(side='right', padx=5)
    
    def save_settings(self, theme, language):
        """Guardar configuraciones"""
        messagebox.showinfo("Configuraciones", 
                           f"Configuraciones guardadas:\nTema: {theme}\nIdioma: {language}")
        self.status_label.config(text="Configuraciones guardadas")

def main():
    """Función principal"""
    root = tk.Tk()
    app = DesktopApp(root)
    
    # Configurar el icono (si existe)
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    # Centrar la ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"800x600+{x}+{y}")
    
    # Ejecutar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()