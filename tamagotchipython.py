import time
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class TamagotchiApp:
    def __init__(self, tamagochi):
        self.tamagochi = tamagochi
        
        # Crear ventana principal
        self.window = tk.Tk()
        self.window.title("Welcome to Tamagotchi!!")
        
        # Cierre por x

        self.window.protocol("WM_DELETE_WINDOW", self.exit_app)

        # Etiquetas de información
        self.name_label = tk.Label(self.window, text=f"Tamagotchi: {tamagochi.name}", font=("Arial", 20))
        self.name_label.pack()

        # Cargar la imagen según el tipo de Tamagotchi
        if tamagochi.type == 'dog':
            self.tama_image = ImageTk.PhotoImage(Image.open('dog.png'))
        elif tamagochi.type == 'cat':
            self.tama_image = ImageTk.PhotoImage(Image.open('cat.png'))
        elif tamagochi.type == 'bear':
            self.tama_image = ImageTk.PhotoImage(Image.open('bear.png'))

        # Mostrar la imagen
        self.image_label = tk.Label(self.window, image=self.tama_image)
        self.image_label.pack()
        
        #start  
        self.stats_label = tk.Label(self.window, text=self.tamagochi.get_stats(), font=("Arial", 14))
        self.stats_label.pack()
        
    
        # Crear botones para las acciones principales
        for action in self.tamagochi.actions:
            button = tk.Button(self.window, text=action.capitalize(), command=getattr(self, f"{action}_tamagotchi"))
            button.pack()

        # Agregar acciones extra si existe
        tama_type = self.tamagochi.type
        if tama_type in self.tamagochi.extra_actions:
            for extra_action in self.tamagochi.extra_actions[tama_type]:
                button = tk.Button(self.window, text=extra_action.capitalize(), command=getattr(self, f"{extra_action}_tamagotchi"))
                button.pack()

        # Botón para cerrar
        self.exit_button = tk.Button(self.window, text="Exit", command=self.exit_app)
        self.exit_button.pack()

        # Iniciar el bucle de tiempo en un hilo separado
        self.tamagochi_thread = threading.Thread(target=self.tamagochi.start_time_loop)
        self.tamagochi_thread.start()
        
        # Iniciar la actualización de la interfaz gráfica
        self.update_gui()
        
        # Iniciar la aplicación
        self.window.mainloop()


    def update_gui(self):
        # Actualizar las estadísticas en la interfaz gráfica
        self.stats_label.config(text=self.tamagochi.get_stats())
        self.window.after(1000, self.update_gui)  # Actualizar cada 1 segundo
    
    def feed_tamagotchi(self):
        self.tamagochi.feed()
        messagebox.showinfo("Feeding", f"{self.tamagochi.name} has been fed!!")

    def rest_tamagotchi(self):
        self.tamagochi.rest()
        messagebox.showinfo("Resting", f"{self.tamagochi.name} is now resting!")

    def play_tamagotchi(self):
        self.tamagochi.play()
        messagebox.showinfo("Playing", f"{self.tamagochi.name} is playing!")

    def clean_tamagotchi(self):
        self.tamagochi.clean()
        messagebox.showinfo("Cleaning", f"{self.tamagochi.name} is now clean!")

    def bark_tamagotchi(self):
        self.tamagochi.bark()
        messagebox.showinfo("Barking", f"The dog {self.tamagochi.name} barked!")

    def meow_tamagotchi(self):
        self.tamagochi.meow()
        messagebox.showinfo("Meowing", f"The cat {self.tamagochi.name} meowed!")

    def roar_tamagotchi(self):
        self.tamagochi.roar()
        messagebox.showinfo("Roaring", f"The bear {self.tamagochi.name} roared!")
    
    def health_check_tamagotchi(self):
        self.tamagochi.health_check()
        messagebox.showinfo("Health Check", f"{self.tamagochi.get_stats()}")
    
    def exit_app(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.tamagochi.stop_time_loop()  # Detener el bucle de Tamagotchi
            self.window.destroy()  # Cerrar la ventana de Tkinter
            self.tamagochi.live = False

# Lógica del Tamagotchi (Separada de la interfaz gráfica)
class Tamagotchi():
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.happy_level = 100
        self.hunger_level = 100
        self.energy_level = 100
        self.cleanliness = 100
        self.live = True

        # Acciones principales
        self.actions = ['health_check','feed', 'play', 'clean']

        # Diccionario para acciones extra según el tipo
        self.extra_actions = {
            'dog': ['bark', 'rest'],
            'cat': ['meow', 'rest'],
            'bear': ['roar', 'rest']
        }
        

    def get_stats(self):
        return (f"Hunger: {self.hunger_level}\n"
                f"Happiness: {self.happy_level}\n"
                f"Energy: {self.energy_level}\n"
                f"Cleanliness: {self.cleanliness}")

    def feed(self):
        self.hunger_level += 10
        self.energy_level -= 5
        print(f'{self.name} has been fed!')
    
    def play(self):
        self.happy_level += 10
        self.energy_level -= 5
        print(f'{self.name} has been playing!')
    
    def clean(self):
        self.cleanliness += 25
        self.energy_level -= 10

    def health_check(self):
        print(f'Health check to: {self.name}.')

    def start_time_loop(self):
        def decrease_stats():
            while self.live:
                self.happy_level -= 1
                self.hunger_level -= 1
                self.energy_level -= 1
                self.cleanliness -= 1
                
                # Evitar que los niveles sean menores de 0
                self.happy_level = max(self.happy_level, 0)
                self.hunger_level = max(self.hunger_level, 0)
                self.energy_level = max(self.energy_level, 0)
                self.cleanliness = max(self.cleanliness, 0)
                
                time.sleep(5)  # Intervalo de tiempo entre cada actualización de los estados
                
                # Verifica si los niveles son muy bajos
                if self.happy_level <= 20 or self.hunger_level <= 20 or self.energy_level <= 20 or self.cleanliness <= 20:
                    messagebox.showwarning("Warning!", f"{self.name} is not feeling well. Take action!")
                
                if self.happy_level == 0 or self.hunger_level == 0 or self.energy_level == 0 or self.cleanliness == 0:
                    self.stop_time_loop()  # Detener el hilo y finalizar
                    messagebox.showerror("Game Over", f"Sorry, your Tamagotchi {self.name} is dead :(")
                    break  # Salir del bucle para detener el hilo

        # Crear e iniciar el hilo
        self.thread = threading.Thread(target=decrease_stats)
        self.thread.start()

    def stop_time_loop(self):
        self.live = False  # Detener el hilo    
        

class Dog(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, type='dog')

    def bark(self):
        self.happy_level += 5
        self.energy_level -= 5
        print('The dog barked!')

    def rest(self):
        self.energy_level += 25
        self.hunger_level -= 15
        print('The dog has rested.')

class Cat(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, type='cat')

    def meow(self):
        self.happy_level += 3
        self.energy_level -= 8
        print('The cat meowed!')

    def rest(self):
        self.energy_level += 15
        self.hunger_level -= 10
        print('The cat has rested.')

class Bear(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, type='bear')

    def roar(self):
        self.happy_level += 2
        self.energy_level -= 3
        print('The bear roared!')

    def rest(self):
        self.energy_level += 20
        self.hunger_level -= 15
        print('The bear has rested.')

# Código principal (independiente de la interfaz gráfica)
tama_name = input('What is the name of your Tamagotchi?: ')
tama_type = input('Now tell me the type (dog, cat, or bear): ')

# Validar tipo de Tamagotchi
while tama_type not in ['dog', 'cat', 'bear']:
    print('Invalid type! Please choose either dog, cat, or bear.')
    tama_type = input('What is the type of your Tamagotchi?: ')

# Crear el Tamagotchi correcto según el tipo
if tama_type == 'dog':
    tamagochi = Dog(tama_name)
elif tama_type == 'cat':
    tamagochi = Cat(tama_name)
else:
    tamagochi = Bear(tama_name)

# Iniciar la aplicación gráfica
app = TamagotchiApp(tamagochi)
