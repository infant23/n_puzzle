#!/usr/bin/env python3


import sys
import random
from functools import reduce


class State():

    goal = []
    actual = []
    prev_states = []
    size = 0
    length = 0
    turn_set = ('r', 'd', 'l', 'u')
    possible_turns = []
    prev_turn = None

    def __init__(self, size):

        self.size = int(size)
        self.length = self.size * self.size
        self.goal = [None] * self.length
        self.set_snail()
        # self.set_zero_first()
        # self.set_zero_last()
        self.actual = self.goal.copy()

    def set_zero_first(self):

        for cell in range(self.length):
            self.goal[cell] = cell

    def set_zero_last(self):

        for cell in range(self.length):
            self.goal[cell] = cell + 1
        self.goal[self.goal.index(self.length)] = 0

    def set_snail(self):

        max_iteration = self.size - (self.size // 2)
        sum_of_perimeters = 1
        for iteration in range(max_iteration):
            side = self.size - 2 * iteration
            half_perimeter = 2 * side - 2
            rb_number = sum_of_perimeters + half_perimeter
            lt_number = rb_number + half_perimeter
            lt_corner = iteration * (1 + self.size)
            rb_corner = self.length - lt_corner - 1
            for cell in range(side):
                self.goal[lt_corner + cell * self.size] = lt_number - cell
                self.goal[rb_corner - cell] = rb_number + cell
                self.goal[rb_corner - cell * self.size] = rb_number - cell 
                self.goal[lt_corner + cell] = sum_of_perimeters + cell
            sum_of_perimeters += 2 * half_perimeter
        self.goal[self.goal.index(self.length)] = 0

    def validate_turn(self, position, turn):

        if position >= self.length or position < 0:
            return False
        if not (turn in self.turn_set):
            return False
        module = position % self.size
        if module == self.size - 1 and turn == 'r':
            return False
        elif module == 0 and turn == 'l':
            return False
        if position < self.size and turn == 'u':
            return False
        elif position >= self.length - self.size and turn == 'd':
            return False
        # if turn == 'r' and self.prev_turn == 'l':
        #     return False
        # elif turn == 'l' and self.prev_turn == 'r':
        #     return False
        # elif turn == 'u' and self.prev_turn == 'd':
        #     return False
        # elif turn == 'd' and self.prev_turn == 'u':
        #     return False
        return True

    def swap_cells(self, state, position_a, position_b):

            buffer_cell = state[position_a]
            state[position_a] = state[position_b]
            state[position_b] = buffer_cell

    def make_turn(self, state, position, turn, with_zero=True):

        if with_zero and self.actual[position]:
            return None
        if self.validate_turn(position, turn):
            if turn == 'r':
                next_position = position + 1
            elif turn == 'l':
                next_position = position - 1
            elif turn == 'u':
                next_position = position - self.size
            elif turn == 'd':
                next_position = position + self.size
            self.swap_cells(state, position, next_position)
            return next_position
        return None

    def mix_sequence(self, steps):

        turns = list(self.turn_set)
        position = self.actual.index(0)
        for step in range(steps):
            random.shuffle(turns)
            i = 0
            next_position = None
            while next_position == None:
                next_position = self.make_turn(self.actual, position, turns[i])
                i += 1
            position = next_position

    def get_manhattan_distance(self, state):

        distance = 0
        for i in range(1, self.length):
            difference = abs(self.goal.index(i) - state.index(i))
            distance += difference % self.size
            distance += difference // self.size
        return distance

    def get_hamming_distance(self, state):

        distance = 0
        for i in range(1, self.length):
            if self.goal.index(i) != state.index(i):
                distance += 1
        return distance

    def get_possible_states(self):

        possible_states = []
        # self.possible_turns = []
        for turn in self.turn_set:
            sequence = self.actual.copy()
            position = sequence.index(0)
            a = self.make_turn(sequence, position, turn)
            if a != None and not sequence in self.prev_states:
                possible_states.append(sequence)
                # self.possible_turns.append(turn)
                # print(position, turn, a)
            # print(self.possible_turns)
        return possible_states

    def heruristic_function(self):

        possible_states = self.get_possible_states()
        man_distances = []
        for state in possible_states:
            d = self.get_manhattan_distance(state)
            # d = self.get_hamming_distance(state)
            man_distances.append(d)
            # print('Dist: ', d, ' and state: ', len(possible_states))
            self.print_2d(state)
        print('man_distances: ', man_distances)
        index = man_distances.index(min(man_distances))
        print('index', index)
        self.actual = possible_states[index].copy()
        self.prev_states.append(self.actual)
        # self.prev_turn = self.possible_turns[index]

    def print_2d(self, state):

        for i in range(self.length):
            print('{:4d}'.format(state[i]), end='')
            # print('   {}'.format(self.goal[i]), end='')
            if (i + 1) % self.size == 0:
                print('\n')

if len(sys.argv) == 2:
    print('Usage: ./generator -s <npuzzle size> [-u] [-h]')
    state = State(sys.argv[1])
    print('Goal:')
    state.print_2d(state.goal)
    state.mix_sequence(20)
    print('Mixed:', state.get_manhattan_distance(state.actual))
    state.print_2d(state.actual)
    step = 0
    while state.goal != state.actual:
        state.heruristic_function()
        step += 1
        print('Step: ', step)
        state.print_2d(state.actual)
    # state.mix_sequence(1)
    # print('Two steps:', state.get_manhattan_distance())
    # state.print_2d()
    # # state.print_2d(goal=True)
    
    # for i in range(state.length):
    #     if state.validate_turn(i, 'l'):
    #         state. goal[i] = 1
    #     else:
    #         state.goal[i] = 0
    # print('left:')
    # state.print_2d()
else:
    print('ERROR')