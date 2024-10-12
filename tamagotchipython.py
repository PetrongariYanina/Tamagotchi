class Tamagotchi():
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.happy_level = 100
        self.hunger_level = 100
        self.energy_level = 100
    
    def feed(self):
        self.hunger_level += 10
        self.energy_level -= 5
        print (f'The {self.type} has been fed!')
        

class Dog(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, type = 'dog')

    def bark(self):
        self.happy_level += 5
        self.energy_level -= 5
        print ('The dog barked')

    def rest(self):
        self.energy_level += 25
        self.hunger_level -= 15
        print ('The dog has rested')

class Cat(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, type = 'cat')   

    def meow(self):
        self.happy_level += 3
        self.energy_level -= 8
        print ('The cat has Meow!')   

    def rest(self):
        self.energy_level += 15
        self.hunger_level -= 10 
        print ('The cat has rested')

class Bear(Tamagotchi):
    def __init__(self, name):
        super().__init__(name, type = 'bear')

    def roar(self):
        self.happy_level += 2
        self.energy_level -= 3
        print ('The bear roared!')

    def rest(self):
        self.energy_level += 20
        self.hunger_level -= 15
        print ('The bear has rested')




tama1 = input('What is the name to your Tamagotchi?: ')

print(f'Hello!, I am {tama1}')

tama_type1 = input('Now say me whith is my type: dog, cat or bear: ')

type_ok = ['dog' , 'cat', 'bear']
while tama_type1 not in type_ok:
    print('Your Tamagotchi need a type = dog, cat or bear ')
    tama_type1 = input('Whith is my type: dog, cat or bear: ')

print(f'The type of Tamagotchi is {tama_type1}')

if tama_type1 == 'dog':
    tamagochi = Dog(tama1)
elif tama_type1 == 'cat':
    tamagochi = Cat(tama1)
else:
    tamagochi = Bear(tama1)

# Cree el tmagochi

action = ['feed', 'rest', 'exit']
extra_action = {
    'dog': 'bark',
    'cat': 'meow',
    'bear': 'roar'
}
action.append(extra_action[tama_type1])

while True:
# lo q ejecuto dentro del loop
# le doy opciones que puede usar

    user_action = input (f'What are you do? Put: {action} ')
    # manejo de errores
    while user_action not in action:
        # decir que es un error
        print(f'Your should be one of this actions: {action} ')
        # que lo vuelva a intentar
        user_action = input(f'What are you do? Put: rest or feed or exit: {action} ')
    
    print(f'Your Tamagotchi has {user_action}')
    if user_action == 'exit':
        break
    else:
    # ejecutar la accion
        selected_action = getattr(tamagochi, user_action)
        selected_action()


        # mostrar estado actual del tamagochi
        print(f' Hungry: {tamagochi.hunger_level}')
        print(f' Happy: {tamagochi.happy_level}')
        print(f' Energy: {tamagochi.energy_level}')
        #meter dentro del loop



# accion en funcion del type






    
        

