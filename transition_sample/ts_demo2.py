from transitions import State
from transitions.extensions import GraphMachine as Machine

states = [
    "woman_A",
    "woman_B"
]


class Game(object):
    def return_true(self):
        return True
    def return_false_v1(self):
        return False
    def return_false_v2(self):
        return False
    def onA(self):
        print("entered A")
    def onB(self):
        print("entered B")
    def atob(self):
        print("before : a to b")
    def btoa(self):
        print("after : b to a")


woman_bot = Game()
machine = Machine(model=woman_bot, states=states, initial="woman_A", ignore_invalid_triggers=True, title="figure record")

machine.add_transition("a_to_b", "woman_A", "woman_B",
                       conditions="return_true", before="atob")
machine.add_transition("b_to_a", "woman_B", "woman_A",
                       conditions=["return_false_v1"])
machine.add_transition("b_to_a_unless", "woman_B", "woman_A",
                       unless=["return_false_v1", "return_false_v2"], after="btoa")

machine.on_enter_woman_B("onB")
machine.on_enter_woman_A("onA")

woman_bot.a_to_b()
print(woman_bot.state)
# woman_bot.b_to_a()
# print(woman_bot.state)
woman_bot.b_to_a_unless()
print(woman_bot.state)

machine.get_graph().draw("state_diagram.png", prog="dot")
