import nltk
from nltk.tokenize import word_tokenize
import spacy
import threading
import time

## descarga de los paquetes necesarios
nltk.download('punkt_tab')
pln = spacy.load("es_core_news_lg")

## lematización del texto del chat
def lematizar_oracion(oracion):
    tokens = word_tokenize(oracion)
    lematizar_oracion = [token.lemma_ for token in pln(" ".join(tokens))]
    return lematizar_oracion

## tokenización del texto del chat
def tokenizar_oracion(oracion):
    return word_tokenize(oracion)

## lematización con POS
def lematizar_con_POS(texto):
    doc = pln(texto)
    return [(token.text, token.lemma_, token.pos_) for token in doc]

def response_chat(message):
    # Tokenizar el mensaje
    tokens = word_tokenize(message.lower())
    
    # Lematizar el mensaje usando la función proporcionada
    lemas = lematizar_con_POS(message)
    
    # Diccionario de palabras clave por categoría
    keyword_dict = {
        
        "modelo": {
            "keywords": ["modelo", "marca"],
            "response": "Ofrecemos computadoras de las marcas más reconocidas. ¿Tienes alguna en mente?"
        },
        "Hola": {
            "keywords": ["hola", "buenas", "saludos", "como estás"],
            "response": "¡Hola! ¿En qué puedo ayudarte hoy?"
        },
        "precio": {
            "keywords": ["precio", "costo", "cuánto", "valor"],
            "response": "Los precios de nuestras computadoras varían: laptops desde $500, desktops desde $600. ¿Cuál te interesa?"
        },
        "compra": {
            "keywords": ["comprar", "adquirir"],
            "response": "¡Genial! Aquí tienes nuestro listado de computadoras disponibles:\n" +
                        "- Laptop Dell Inspiron: $800, 16GB RAM, 512GB SSD\n" +
                        "- Desktop HP Pavilion: $600, 8GB RAM, 1TB HDD\n" +
                        "- Laptop Lenovo ThinkPad: $1200, 32GB RAM, 1TB SSD\n" +
                        "¿Cuál te interesa o quieres más detalles?"
        },
        "características": {
            "keywords": ["características", "especificaciones", "detalles"],
            "response": "Nuestras computadoras tienen procesadores Intel o AMD, de 8GB a 32GB de RAM y almacenamiento SSD o HDD. ¿Qué características específicas buscas?"
        },
        "computadora": {
            "keywords": ["computadora", "laptop", "escritorio", "pc"],
            "response": "Ofrecemos laptops y computadoras de escritorio de marcas como Dell, HP y Lenovo. ¿Buscas alguna en particular?"
        },
        "gracias": {
            "keywords": ["gracias", "muchas gracias", "te lo agradezco"],
            "response": "¡De nada! Si tienes más preguntas, no dudes en preguntar."
        },
        "dell": {
            "keywords": ["dell", "inspiron"],
            "response": "Dell Inspiron: $800, 16GB RAM, 512GB SSD, tiene el mejor precio y calidad. ¿Quieres pagarla o ver otros modelos?"
        },
        "hp": {
            "keywords": ["hp", "pavilion"],
            "response": "HP Pavilion: $600, 8GB RAM, 1TB HDD, es una opción económica. ¿Quieres pagarla o ver otros modelos?"
        },
        "lenovo": {
            "keywords": ["lenovo", "thinkpad"],
            "response": "Lenovo ThinkPad: $1200, 32GB RAM, 1TB SSD, es la más potente. ¿Quieres pagarla o ver otros modelos?"
        },
        "pagar": {
            "keywords": ["pagar", "comprar", "adquirir"],
            "response": "Para completar tu compra, por favor visita nuestro sitio web o contáctanos directamente al +57 3xxxxxxxxx. ¡Gracias por elegirnos!"
        }
    }
    
    # Buscar palabras clave en los tokens y lemas
    for category, data in keyword_dict.items():
        for keyword in data["keywords"]:
            # Verificar si la palabra clave está en los tokens o lemas
            if keyword in tokens or keyword in lemas:
                return data["response"]
    
    # Respuesta por defecto si no se encuentra ninguna palabra clave
    return "No entiendo lo que quieres. ¿Buscas información sobre precios, modelos, características o cómo comprar una computadora?"

import tkinter as tk
from tkinter import scrolledtext, ttk, font
from datetime import datetime

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_header()
        self.create_chat_area()
        self.create_input_area()
        self.create_status_bar()
        
    def setup_window(self):
        self.root.title("💬 ChatBot Computex - Asistente Virtual")
        self.root.geometry("600x700")
        self.root.minsize(500, 600)
        self.root.configure(bg="#1a1a1a")
        
        # Configurar el icono de la ventana (opcional)
        try:
            self.root.iconbitmap("chat_icon.ico")
        except:
            pass
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Colores profesionales
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3d3d3d',
            'accent': '#0078d4',
            'accent_hover': '#106ebe',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'user_bubble': '#0078d4',
            'bot_bubble': '#2d2d2d',
            'success': '#107c10',
            'border': '#484848'
        }
        
        # Configurar estilos personalizados
        style.configure("Header.TFrame", background=self.colors['bg_secondary'])
        style.configure("Chat.TFrame", background=self.colors['bg_primary'])
        style.configure("Input.TFrame", background=self.colors['bg_secondary'])
        
        style.configure("Send.TButton", 
                       background=self.colors['accent'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       focuscolor="none",
                       padding=(20, 10),
                       font=("Segoe UI", 10, "bold"))
        
        style.map("Send.TButton",
                 background=[("active", self.colors['accent_hover']),
                            ("pressed", "#005a9e")])
        
        style.configure("Modern.TEntry",
                       fieldbackground=self.colors['bg_tertiary'],
                       borderwidth=1,
                       insertcolor=self.colors['text_primary'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'],
                       padding=12,
                       font=("Segoe UI", 11))
    
    def create_header(self):
        # Header con título y estado
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(header_frame, 
                              text="💬 Computex",
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              font=("Segoe UI", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(header_frame,
                                   text="● En línea",
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['success'],
                                   font=("Segoe UI", 10))
        self.status_label.pack(side=tk.RIGHT)
        
        # Línea separadora
        separator = tk.Frame(self.root, height=1, bg=self.colors['border'])
        separator.pack(fill=tk.X)
    
    def create_chat_area(self):
        # Contenedor principal del chat
        chat_container = ttk.Frame(self.root, style="Chat.TFrame")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Área de mensajes con scrollbar personalizada
        self.chat_area = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            font=("Segoe UI", 11),
            bd=0,
            relief="flat",
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground=self.colors['text_primary'],
            padx=15,
            pady=15
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')
        
        # Configurar tags para diferentes tipos de mensajes
        self.chat_area.tag_configure("user_msg", 
                                   background=self.colors['user_bubble'],
                                   foreground=self.colors['text_primary'],
                                   font=("Segoe UI", 11),
                                   wrap="word",
                                   rmargin=80,
                                   relief="flat",
                                   borderwidth=0)
        
        self.chat_area.tag_configure("bot_msg",
                                   background=self.colors['bot_bubble'],
                                   foreground=self.colors['text_primary'],
                                   font=("Segoe UI", 11),
                                   wrap="word",
                                   lmargin1=10,
                                   lmargin2=10,
                                   rmargin=80,
                                   relief="flat",
                                   borderwidth=0)
        
        self.chat_area.tag_configure("timestamp",
                                   foreground=self.colors['text_secondary'],
                                   font=("Segoe UI", 9),
                                   justify="right")
        
        self.chat_area.tag_configure("typing",
                                   foreground=self.colors['text_secondary'],
                                   font=("Segoe UI", 10, "italic"))
        
        # Mensaje de bienvenida
        self.add_welcome_message()
    
    def create_input_area(self):
        # Línea separadora superior
        separator = tk.Frame(self.root, height=1, bg=self.colors['border'])
        separator.pack(fill=tk.X)
        
        # Frame para input
        input_frame = ttk.Frame(self.root, style="Input.TFrame", padding=20)
        input_frame.pack(fill=tk.X)
        
        # Campo de entrada
        self.input_field = ttk.Entry(input_frame, 
                                   style="Modern.TEntry",
                                   font=("Segoe UI", 11))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        # Botón de enviar
        self.send_button = ttk.Button(input_frame,
                                    text="Enviar",
                                    style="Send.TButton",
                                    command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # Eventos
        self.input_field.bind("<Return>", lambda event: self.send_message())
        self.input_field.bind("<KeyPress>", self.on_typing)
        self.input_field.focus_set()
    
    def create_status_bar(self):
        # Barra de estado inferior
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.message_count = tk.Label(status_frame,
                                    text="Mensajes: 0",
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_secondary'],
                                    font=("Segoe UI", 9))
        self.message_count.pack(side=tk.LEFT, padx=10, pady=2)
        
        current_time = tk.Label(status_frame,
                              text=datetime.now().strftime("%H:%M"),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_secondary'],
                              font=("Segoe UI", 9))
        current_time.pack(side=tk.RIGHT, padx=10, pady=2)
    
    def add_welcome_message(self):
        welcome_text = """¡Hola! 👋 Bienvenido a ChatBot Pro.
        
Soy tu asistente virtual y estoy aquí para ayudarte. 
Puedes escribir cualquier mensaje y te responderé de inmediato.

¿En qué puedo asistirte hoy?"""
        
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, welcome_text + "\n\n", "bot_msg")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
    
    def on_typing(self, event):
        # Efecto visual de que el usuario está escribiendo
        self.status_label.config(text="● En línea", fg=self.colors['success'])
    
    def send_message(self):
        message = self.input_field.get().strip()
        if not message:
            return
        
        # Deshabilitar botón temporalmente
        self.send_button.config(state='disabled')
        
        # Mostrar mensaje del usuario
        timestamp = datetime.now().strftime("%H:%M")
        self.display_message(f"Tú • {timestamp}", message, "user")
        
        # Limpiar campo de entrada
        self.input_field.delete(0, tk.END)
        
        # Mostrar indicador de escritura
        self.show_typing_indicator()
        
        # Generar respuesta en segundo plano
        threading.Thread(target=self.generate_response, args=(message,), daemon=True).start()
        
        # Actualizar contador
        self.update_message_count()
    
    def display_message(self, sender, message, msg_type):
        self.chat_area.config(state='normal')
        
        # Agregar espacio entre mensajes
        self.chat_area.insert(tk.END, "\n")
        
        # Información del remitente y timestamp
        self.chat_area.insert(tk.END, f"{sender}\n", "timestamp")
        
        # Mensaje
        tag = "user_msg" if msg_type == "user" else "bot_msg"
        self.chat_area.insert(tk.END, f"{message}\n", tag)
        
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
    
    def show_typing_indicator(self):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "\nBot está escribiendo...", "typing")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)
        self.typing_pos = self.chat_area.index(tk.END + "-1c linestart")
    
    def remove_typing_indicator(self):
        self.chat_area.config(state='normal')
        self.chat_area.delete(self.typing_pos, tk.END)
        self.chat_area.config(state='disabled')
    
    def generate_response(self, user_message):
        # Simular tiempo de procesamiento
        time.sleep(1.5)
        
        # Remover indicador de escritura
        self.root.after(0, self.remove_typing_indicator)
        
        # Generar y mostrar respuesta
        response = response_chat(user_message)
        timestamp = datetime.now().strftime("%H:%M")
        
        self.root.after(0, lambda: self.display_message(f"Bot • {timestamp}", response, "bot"))
        self.root.after(0, lambda: self.send_button.config(state='normal'))
    
    def update_message_count(self):
        current_count = int(self.message_count.cget("text").split(": ")[1])
        self.message_count.config(text=f"Mensajes: {current_count + 1}")

def main():
    root = tk.Tk()
    app = ChatApp(root)
    
    # Centrar ventana en la pantalla
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()