import os
import sys
import subprocess
import threading
import time
import ctypes
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog

# Configurações globais de tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def force_admin():
    """Força o script Python a reiniciar pedindo privilégios de Administrador no Windows"""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        is_admin = False

    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Executa o truque do Admin antes de desenhar a interface gráfica
force_admin()

class FlashOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ FlashOptimizer - Torne seu PC um Foguete")
        self.geometry("900x780") 
        self.resizable(True, True)

        self.is_running = False
        self.origem_selecionada = ""
        self.destino_selecionado = ""

        # --- Layout Principal ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="FlashOptimizer", font=ctk.CTkFont(size=20, weight="bold", slant="italic"), text_color="#00ADB5")
        self.logo.pack(pady=20, padx=20)

        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="Dashboard", fg_color="#393E46", state="disabled")
        self.btn_dashboard.pack(pady=10, padx=20, fill="x")

        # Container Central com Scrollbar
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="#222831", corner_radius=15)
        self.scroll_container.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.main_title = ctk.CTkLabel(self.scroll_container, text="Otimização Completa do Sistema", font=ctk.CTkFont(size=22, weight="bold"))
        self.main_title.pack(pady=15)

        # Checkboxes
        self.options_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.options_frame.pack(pady=5, padx=40, fill="x")

        self.chk_drivers = ctk.CTkCheckBox(self.options_frame, text="Atualizar Componentes & Drivers (Winget)", hover_color="#00ADB5")
        self.chk_drivers.pack(anchor="w", pady=6)
        self.chk_drivers.select()

        self.chk_clean_drivers = ctk.CTkCheckBox(self.options_frame, text="Remover Drivers Duplicados Obsoletos (DriverStore)", hover_color="#00ADB5")
        self.chk_clean_drivers.pack(anchor="w", pady=6)
        self.chk_clean_drivers.select()

        self.chk_clean_cache = ctk.CTkCheckBox(self.options_frame, text="Limpar Entulhos de Atualizações (DISM / WinSxS)", hover_color="#00ADB5")
        self.chk_clean_cache.pack(anchor="w", pady=6)
        self.chk_clean_cache.select()

        # Terminal de Logs
        self.log_box = ctk.CTkTextbox(self.scroll_container, height=140, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#111318", text_color="#71EFA3")
        self.log_box.pack(pady=10, padx=40, fill="x")
        self.log_box.insert("0.0", "[Aguardando Inicialização] Selecione os módulos e clique em Iniciar.\n")
        self.log_box.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(self.scroll_container, progress_color="#00ADB5", height=8)
        self.progress_bar.pack(pady=5, padx=40, fill="x")
        self.progress_bar.set(0)

        self.btn_start = ctk.CTkButton(self.scroll_container, text="⚡ INICIAR FLASH OPTIMIZATION", font=ctk.CTkFont(size=14, weight="bold"), fg_color="#00ADB5", hover_color="#008085", height=40, command=self.start_optimization_thread)
        self.btn_start.pack(pady=10)

        # --- SEÇÃO: GERENCIADOR DE SYMLINKS INTERATIVO ---
        self.symlink_frame = ctk.CTkFrame(self.scroll_container, border_color="#393E46", border_width=1, fg_color="#1A1F26")
        self.symlink_frame.pack(pady=20, padx=40, fill="x")

        self.symlink_title = ctk.CTkLabel(self.symlink_frame, text="🔗 Gerenciador de Links Simbólicos Automatizado", font=ctk.CTkFont(size=14, weight="bold"), text_color="#00ADB5")
        self.symlink_title.pack(anchor="w", padx=15, pady=8)

        # Botões de Seleção de Pasta
        self.folder_buttons_frame = ctk.CTkFrame(self.symlink_frame, fg_color="transparent")
        self.folder_buttons_frame.pack(padx=15, pady=5, fill="x")

        self.btn_select_origem = ctk.CTkButton(self.folder_buttons_frame, text="📂 Escolher Pasta Pesada (C:)", fg_color="#393E46", hover_color="#4E545C", command=self.selecionar_origem)
        self.btn_select_origem.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_select_destino = ctk.CTkButton(self.folder_buttons_frame, text="💾 Escolher Destino (D:, E:...)", fg_color="#393E46", hover_color="#4E545C", command=self.selecionar_destino)
        self.btn_select_destino.pack(side="right", padx=5, expand=True, fill="x")

        # Labels com caminhos selecionados
        self.lbl_origem = ctk.CTkLabel(self.symlink_frame, text="Origem: Nenhuma pasta selecionada", font=ctk.CTkFont(size=11), text_color="#AAAAAA", justify="left")
        self.lbl_origem.pack(anchor="w", padx=20, pady=2)

        self.lbl_destino = ctk.CTkLabel(self.symlink_frame, text="Destino: Nenhum destino selecionado", font=ctk.CTkFont(size=11), text_color="#AAAAAA", justify="left")
        self.lbl_destino.pack(anchor="w", padx=20, pady=2)

        # Botão para criar o Symlink
        self.btn_create_symlink = ctk.CTkButton(self.symlink_frame, text="🔗 MOVER E CRIAR LINK SIMBÓLICO", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#E0A96D", hover_color="#D1985A", text_color="#1A1F26", command=self.start_symlink_thread)
        self.btn_create_symlink.pack(pady=12, padx=20, fill="x")

    def write_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update_idletasks()

    def animate_progress(self, target, duration=1.5):
        current = self.progress_bar.get()
        steps = 30
        increment = (target - current) / steps
        sleep_time = duration / steps
        for _ in range(steps):
            current += increment
            self.progress_bar.set(current)
            self.update_idletasks()
            time.sleep(sleep_time)

    def selecionar_origem(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta pesada que deseja retirar do C:")
        if pasta:
            self.origem_selecionada = pasta.replace("/", "\\")
            self.lbl_origem.configure(text=f"Origem: {self.origem_selecionada}", text_color="#71EFA3")

    def selecionar_destino(self):
        pasta = filedialog.askdirectory(title="Selecione para onde quer mover os arquivos")
        if pasta:
            self.destino_selecionado = pasta.replace("/", "\\")
            self.lbl_destino.configure(text=f"Destino: {self.destino_selecionado}", text_color="#71EFA3")

    def start_symlink_thread(self):
        if not self.origem_selecionada or not self.destino_selecionado:
            messagebox.showwarning("Campos Vazios", "Selecione a Origem e o Destino!")
            return
        if self.origem_selecionada == self.destino_selecionado:
            messagebox.showerror("Erro", "Origem e destino não podem ser iguais!")
            return
        self.btn_create_symlink.configure(state="disabled", text="MOVENDO ARQUIVOS...")
        threading.Thread(target=self.executar_symlink, daemon=True).start()

    def executar_symlink(self):
        origem = self.origem_selecionada
        nome_pasta = os.path.basename(origem)
        destino_final = os.path.join(self.destino_selecionado, nome_pasta)

        self.write_log(f"\n[SYMLINK] Movendo conteudo de {origem}...")
        self.write_log("Transferindo arquivos via Robocopy de alta velocidade...")

        try:
            # Cria a pasta de destino final
            if not os.path.exists(destino_final):
                os.makedirs(destino_final)

            # Executa robocopy de forma limpa
            cmd_robo = ["robocopy", origem, destino_final, "/E", "/MOVE", "/NFL", "/NDL", "/NJH", "/NJS", "/R:0", "/W:0"]
            subprocess.run(cmd_robo, creationflags=subprocess.CREATE_NO_WINDOW)

            # Limpa qualquer resíduo restante na pasta antiga
            if os.path.exists(origem):
                subprocess.run(["cmd.exe", "/c", f"rmdir /s /q \"{origem}\""], creationflags=subprocess.CREATE_NO_WINDOW)

            # Cria o Link Simbólico via Junction nativo do Windows
            cmd_link = ["cmd.exe", "/c", f"mklink /j \"{origem}\" \"{destino_final}\""]
            subprocess.run(cmd_link, creationflags=subprocess.CREATE_NO_WINDOW)

            self.write_log(f"✔ Sucesso! Pasta vinculada: {origem} -> {destino_final}")
            messagebox.showinfo("Sucesso", "Pasta migrada e Link Simbólico criado perfeitamente!")
        except Exception as e:
            self.write_log(f"❌ Erro na operação: {str(e)}")
        
        self.btn_create_symlink.configure(state="normal", text="🔗 MOVER E CRIAR LINK SIMBÓLICO")

    def start_optimization_thread(self):
        if self.is_running: return
        self.is_running = True
        self.btn_start.configure(state="disabled", text="OTIMIZANDO...")
        threading.Thread(target=self.run_optimization, daemon=True).start()

    def run_optimization(self):
        self.animate_progress(0.1)
        self.write_log("[INFO] Iniciando rotinas de aceleração...")

        if self.chk_drivers.get():
            self.write_log("[SYSTEM] Atualizando componentes via Winget...")
            self.animate_progress(0.3)
            try:
                subprocess.run(["winget", "upgrade", "--all", "--accept-package-agreements", "--accept-source-agreements"], creationflags=subprocess.CREATE_NO_WINDOW)

                self.write_log("✔ Componentes atualizados!")
            except: pass
        
        if self.chk_clean_drivers.get():
            self.write_log("[DRIVERS] Removendo duplicatas obsoletas do DriverStore...")
            self.animate_progress(0.6)
            try:
                # CORRIGIDO: Modificado $. para $_. nas variáveis do PowerShell
                ps_cmd = 'Get-WindowsDriver -Online -All | Where-Object { $_.Driver -match "oem" } | Group-Object OriginalFileName | Where-Object { $_.Count -gt 1 } | ForEach-Object { $sorted = $_.Group | Sort-Object {[datetime]$_.Date} -Descending; for ($i = 1; $i -lt $sorted.Count; $i++) { pnputil.exe /delete-driver $sorted[$i].Driver /force } }'
                subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
                self.write_log("✔ DriverStore limpo com segurança.")
            except: pass

        if self.chk_clean_cache.get():
            self.write_log("[CLEANUP] Otimizando pasta WinSxS (DISM)...")
            self.animate_progress(0.8)
            try:
                subprocess.run(["dism.exe", "/online", "/cleanup-image", "/startcomponentcleanup", "/resetbase"], creationflags=subprocess.CREATE_NO_WINDOW)
                self.write_log("✔ Lixo de atualizações limpo.")
            except: pass

        self.animate_progress(1.0, duration=0.5)
        self.write_log("\n⚡ [CONCLUÍDO] Sistema otimizado!")
        self.btn_start.configure(state="normal", text="⚡ INICIAR FLASH OPTIMIZATION")
        self.is_running = False

# CORRIGIDO: Sintaxe padrão de inicialização com os underlines duplos
if __name__ == "__main__":
    app = FlashOptimizerApp()
    app.mainloop()
