from transitions import State
from transitions.extensions import GraphMachine as Machine

states = [
    'first',
    'second',
    'third'
]

transitions = [
    ['go_to_second', 'first', 'second'],
    ['go_to_third', 'second', 'third']
]


class Game(object):
    def return_true(self):
        return True
    def return_false_v1(self):
        return False
    def return_false_v2(self):
        return False


life_bot = Game()
machine = Machine(model=life_bot, states=states, transitions=transitions, initial="first")

# method to do transition
print(life_bot.state)

life_bot.go_to_second()
life_bot.go_to_third()

print(life_bot.state)

life_bot.to_first()
print(life_bot.state)

life_bot.trigger("go_to_second")
print(life_bot.state)
life_bot.trigger("go_to_third")
print(life_bot.state)

machine.set_state("first")
print(life_bot.state)

# add state and transitions
machine.add_state("red")
machine.add_states(["green", "blue"])

# alternate machine.add_transition(trigger= ?, source=?, dest=?)
# machine.add_transition("r_to_b", "red", "blue")
machine.add_transition("other_to_r", ["blue", "green"], "red")



