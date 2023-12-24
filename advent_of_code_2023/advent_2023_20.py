# Oh noes, it's a tree again.
# DISCLAIMER:
# I have done it all by myself!
# Triple wheeeeeeeeeee!
import math


class Pulse:
    LOW = 'low_pulse'
    HIGH = 'high_pulse'


class Module:
    PULSES = {Pulse.LOW: 0, Pulse.HIGH: 0}

    def __init__(self, name):
        self.name = name
        self.input_list = list()
        self.destination_list = list()

    def count_pulse(self, pulse):
        self.PULSES[pulse] += 1

    def transfer_pulse(self, pulse, input_module_name):
        self.count_pulse(pulse)

    def add_input(self, input_module_name):
        self.input_list.append(input_module_name)

    def add_destinations(self, destinations):
        if type(destinations) == str:
            destinations = [destinations]
        self.destination_list += destinations

    def reset(self):
        self.PULSES = {Pulse.LOW: 0, Pulse.HIGH: 0}


class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state_on = False

    def transfer_pulse(self, pulse, input_module_name):
        super().transfer_pulse(pulse, input_module_name)
        if pulse == Pulse.LOW:
            self.state_on = not self.state_on
            output_pulse = Pulse.HIGH if self.state_on else Pulse.LOW
            return [(self.name, module, output_pulse) for module in self.destination_list]

    def reset(self):
        super().reset()
        self.state_on = False


class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.input_list = dict()

    def add_input(self, input_module_name):
        self.input_list[input_module_name] = Pulse.LOW

    def transfer_pulse(self, pulse, input_module_name):
        super().transfer_pulse(pulse, input_module_name)
        self.input_list[input_module_name] = pulse
        output_pulse = Pulse.LOW if all([input_pulse == Pulse.HIGH for input_pulse in self.input_list.values()]) \
            else Pulse.HIGH
        return [(self.name, module, output_pulse) for module in self.destination_list]

    def reset(self):
        super().reset()
        self.input_list = {m: Pulse.LOW for m in self.input_list.keys()}


class Broadcast(Module):
    NAME = 'broadcaster'

    def __init__(self):
        super().__init__(self.NAME)

    def transfer_pulse(self, pulse, input_module_name):
        super().transfer_pulse(pulse, input_module_name)
        return [(self.name, module, pulse) for module in self.destination_list]


class Button(Module):
    NAME = 'button'
    PUSHES = 0
    # Technically this should be done as singleton, but let's leave it as is

    def __init__(self):
        super().__init__(self.NAME)

    def push(self):
        self.PUSHES += 1
        return [(self.name, module, Pulse.LOW) for module in self.destination_list]

    def reset(self):
        super().reset()
        self.PUSHES = 0


with open('20.txt', 'r') as f:
    modules_list = [line.strip() for line in f.readlines()]
    modules = [(module.split('->')[0].strip(),
               [m.strip() for m in module.split('->')[1].strip().split(',')]) for module in modules_list]
    button = Button()
    button.add_destinations(Broadcast.NAME)
    module_objects = {button.NAME: button}
    flipflops = []  # to count their states on/off - works only for the example
    MAX_PUSHES = 1000

    for input_module, output_modules in modules:
        if input_module == Broadcast.NAME:
            module = Broadcast()
            module.add_input(button.NAME)
            module_objects[input_module] = module
        else:
            module = (FlipFlop if input_module.startswith('%') else Conjunction)(input_module[1:])
            module_objects[input_module[1:]] = module
            if input_module.startswith('%'):
                flipflops.append(module)

        module.add_destinations(output_modules)

    for input_module, output_modules in modules:
        for m in output_modules:
            if m not in module_objects:
                module_objects[m] = Module(m)  # For the outputs that don't transfer anything further
            if '%' in input_module or '&' in input_module:
                input_module = input_module[1:]
            module_objects[m].add_input(input_module)

    def part_one():
        queue = button.push()

        while queue:
            input_name, destination, current_pulse = queue.pop(0)
            next_pulses = module_objects[destination].transfer_pulse(current_pulse, input_name)

            if next_pulses:
                queue += next_pulses

            if not queue:
                if button.PUSHES == MAX_PUSHES:
                    break
                if any([module.state_on for module in flipflops]):
                    queue = button.push()

        return math.prod([count * int(1000 / button.PUSHES) for count in Module.PULSES.values()])

    def part_two():
        # To get one single low pulse to rx, we need to get it from &ft.
        # To get it from &ft, we need all the inputs of &ft to be high_pulse
        # Let's find LCM of how many button pushes we need to get each of the inputs to send high pulse

        rx_input = module_objects['rx'].input_list[0]  # [0] Because I know there is single input
        rx_input_inputs = list(module_objects[rx_input].input_list.keys())
        rx_input_inputs_min_pushes = {i: 0 for i in rx_input_inputs}

        for input_ in rx_input_inputs:
            for module in module_objects.values():
                module.reset()

            queue = button.push()

            while queue:
                input_name, destination, current_pulse = queue.pop(0)
                next_pulses = module_objects[destination].transfer_pulse(current_pulse, input_name)

                if next_pulses:
                    if destination == rx_input and module_objects[destination].input_list[input_] == Pulse.HIGH:
                        rx_input_inputs_min_pushes[input_] = button.PUSHES
                        break

                    queue += next_pulses

                if not queue:
                    queue = button.push()

        return math.lcm(*list(rx_input_inputs_min_pushes.values()))

    print(part_one())  # The total number of pulses sent multiplied y each other
    print(part_two())  # The minimum pushes to send a low pulse to rx
