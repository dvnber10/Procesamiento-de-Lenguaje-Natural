import nltk
from nltk.tokenize import word_tokenize
import spacy
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

# Descargar recursos de NLTK
nltk.download('punkt_tab')
pln = spacy.load("es_core_news_lg")

def lematizar_oracion(oracion):
    tokens = word_tokenize(oracion)
    lematizar_oracion = [token.lemma_ for token in pln(" ".join(tokens))]
    return lematizar_oracion

def lematizar_con_POS(texto):
    doc = pln(texto)
    return [(token.text, token.lemma_, token.pos_) for token in doc]

def tokenizar_oracion(oracion):
    return word_tokenize(oracion)

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat de Procesamiento de Lenguaje Natural")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo para la tabla
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilo para la tabla
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")
        style.map('Treeview', background=[('selected', '#347083')])
        
        style.configure("Treeview.Heading",
                        background="#4CAF50",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3D9140')])
        
    def setup_ui(self):
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de chat
        self.chat_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.chat_frame, text="Chat")
        
        # Pestaña de resultados POS
        self.pos_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.pos_frame, text="Análisis POS")
        
        self.setup_chat_tab()
        self.setup_pos_tab()
        
        # Mostrar mensaje inicial
        self.add_message("Sistema", "Hola, ¿qué quieres hacer? Puedes:\n- Lematizar una oración\n- Tokenizar una oración\n- Analizar POS de una oración\n- Escribe 'salir' para terminar", "system")
        
    def setup_chat_tab(self):
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame, 
            wrap=tk.WORD, 
            width=70, 
            height=20,
            font=('Arial', 10),
            bg='white',
            fg='black'
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_area.config(state=tk.DISABLED)
        
        # Frame de entrada
        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill=tk.X)
        
        # Etiqueta de entrada
        ttk.Label(input_frame, text="Tu mensaje:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Campo de entrada
        self.input_entry = ttk.Entry(input_frame, width=50, font=('Arial', 10))
        self.input_entry.pack(fill=tk.X, pady=5)
        self.input_entry.bind('<Return>', lambda event: self.process_input())
        
        # Botón de enviar
        send_button = ttk.Button(
            input_frame,
            text="Enviar",
            command=self.process_input
        )
        send_button.pack(pady=5)
        
        # Configurar etiquetas de texto para el chat
        self.chat_area.tag_config("system_sender", foreground="blue", font=('Arial', 10, 'bold'))
        self.chat_area.tag_config("system_message", foreground="black")
        self.chat_area.tag_config("user_sender", foreground="green", font=('Arial', 10, 'bold'))
        self.chat_area.tag_config("user_message", foreground="black")
        
    def setup_pos_tab(self):
        # Frame para la tabla POS
        table_frame = ttk.Frame(self.pos_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear Treeview (tabla)
        self.pos_tree = ttk.Treeview(table_frame, columns=('Palabra', 'Lema', 'POS'), show='headings')
        
        # Configurar columnas
        self.pos_tree.heading('Palabra', text='Palabra Original')
        self.pos_tree.heading('Lema', text='Lema')
        self.pos_tree.heading('POS', text='Etiqueta POS')
        
        self.pos_tree.column('Palabra', width=200, anchor=tk.W)
        self.pos_tree.column('Lema', width=200, anchor=tk.W)
        self.pos_tree.column('POS', width=150, anchor=tk.W)
        
        # Añadir scrollbar a la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.pos_tree.yview)
        self.pos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.pos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Etiqueta para la oración analizada
        self.sentence_label = ttk.Label(self.pos_frame, text="Oración analizada: ", font=('Arial', 10, 'bold'))
        self.sentence_label.pack(anchor=tk.W, pady=(10, 5))
        
    def add_message(self, sender, message, msg_type="user"):
        self.chat_area.config(state=tk.NORMAL)
        
        if msg_type == "system":
            self.chat_area.insert(tk.END, f"{sender}: ", "system_sender")
            self.chat_area.insert(tk.END, f"{message}\n\n", "system_message")
        else:
            self.chat_area.insert(tk.END, f"{sender}: ", "user_sender")
            self.chat_area.insert(tk.END, f"{message}\n\n", "user_message")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def process_input(self):
        entrada = self.input_entry.get().strip()
        if not entrada:
            return
            
        self.input_entry.delete(0, tk.END)
        self.add_message("Tú", entrada)
        
        # Procesar en un hilo separado para no bloquear la interfaz
        threading.Thread(target=self.process_message, args=(entrada,), daemon=True).start()
        
    def process_message(self, entrada):
        if entrada.lower() == 'salir':
            self.add_message("Sistema", "Saliendo del chat...", "system")
            self.root.after(1000, self.root.quit)
            return
            
        lematizar = lematizar_oracion(entrada)
        
        if 'lematizar' in lematizar:
            self.root.after(0, self.ask_for_input, "Escribe una oración para lematizar:", "lematizar")
        elif 'tokenizar' in lematizar:
            self.root.after(0, self.ask_for_input, "Escribe una oración para tokenizar:", "tokenizar")
        elif 'POS' in lematizar or 'analizar' in lematizar:
            self.root.after(0, self.ask_for_input, "Escribe una oración para analizar:", "analizar")
        else:
            self.add_message("Sistema", "No entiendo lo que quieres hacer. Escoge entre: lematizar, tokenizar o analizar.", "system")
            
    def ask_for_input(self, message, action_type):
        # Crear ventana emergente para entrada específica
        popup = tk.Toplevel(self.root)
        popup.title("Entrada requerida")
        popup.geometry("400x200")
        popup.configure(bg='#f0f0f0')
        popup.transient(self.root)
        popup.grab_set()
        
        ttk.Label(
            popup, 
            text=message, 
            background='#f0f0f0',
            font=('Arial', 10, 'bold'),
            wraplength=350
        ).pack(pady=10)
        
        entry_var = tk.StringVar()
        entry = ttk.Entry(popup, textvariable=entry_var, width=40, font=('Arial', 10))
        entry.pack(pady=10)
        entry.focus()
        
        def submit():
            texto = entry_var.get().strip()
            if texto:
                popup.destroy()
                self.process_specific_action(action_type, texto)
            else:
                messagebox.showwarning("Advertencia", "Por favor, ingresa un texto válido.")
                
        def cancel():
            popup.destroy()
            
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame, 
            text="Enviar", 
            command=submit
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=cancel
        ).pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda event: submit())
        
    def process_specific_action(self, action_type, texto):
        if action_type == "lematizar":
            resultado = lematizar_oracion(texto)
            self.add_message("Sistema", f"Oración lematizada: {resultado}", "system")
        elif action_type == "tokenizar":
            resultado = tokenizar_oracion(texto)
            self.add_message("Sistema", f"Oración tokenizada: {resultado}", "system")
        elif action_type == "analizar":
            resultado = lematizar_con_POS(texto)
            
            # Mostrar en el chat
            resultado_str = "\n".join([f"Palabra: {t[0]}, Lema: {t[1]}, POS: {t[2]}" for t in resultado])
            self.add_message("Sistema", f"Análisis de la oración:\n{resultado_str}", "system")
            
            # Mostrar en la tabla de la pestaña POS
            self.show_pos_results(texto, resultado)
            
    def show_pos_results(self, sentence, results):
        # Cambiar a la pestaña de análisis POS
        self.notebook.select(1)
        
        # Actualizar la etiqueta con la oración analizada
        self.sentence_label.config(text=f"Oración analizada: {sentence}")
        
        # Limpiar tabla existente
        for item in self.pos_tree.get_children():
            self.pos_tree.delete(item)
            
        # Insertar nuevos datos
        for word, lemma, pos in results:
            self.pos_tree.insert('', tk.END, values=(word, lemma, pos))

def main():
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()