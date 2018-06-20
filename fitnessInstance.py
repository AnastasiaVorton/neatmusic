class Fitness:
    def set_tonality(self, val):
        if self.tonality == 0:
            self.tonality = val
            self.fitness_value += val
        else:
            self.fitness_value += val
            self.fitness_value -= self.tonality
            self.tonality = val

    def set_chord_len(self, val):
        if self.chord_length == 0:
            self.chord_length = val
            self.fitness_value -= val
        else:
            self.fitness_value += self.chord_length
            self.chord_length = val
            self.fitness_value -= val

    def set_chord_intervals(self, val):
        if self.chord_intervals == 0:
            self.chord_intervals = val
            self.fitness_value += self.chord_intervals
        else:
            self.fitness_value += val
            self.fitness_value -= self.chord_intervals
            self.chord_intervals = val

    def set_notes_intervals(self, val):
        if self.notes_intervals == 0:
            self.notes_intervals = val
            self.fitness_value += val
        else:
            self.fitness_value += val
            self.fitness_value -= self.notes_intervals
            self.notes_intervals = val

    def set_notes_num(self, val):
        if self.notes_number == 0:
            self.notes_number = val
            self.fitness_value += val
        else:
            self.fitness_value += val
            self.fitness_value -= self.notes_number
            self.notes_number = val

    def set_variety(self, val):
        if self.variety == 0:
            self.variety = val
            self.fitness_value -= val
        else:
            self.fitness_value += self.variety
            self.variety = val
            self.fitness_value -= self.variety

    def __init__(self, value = 0):
        self.fitness_value = value
        self.tonality = 0
        self.chord_length = 0
        self.chord_intervals = 0
        self.notes_number = 0
        self.notes_intervals = 0
        self.variety = 0
        return

    def __lt__(self, other): return self.fitness_value < other.fitness_value

    def __le__(self, other): return self.fitness_value <= other.fitness_value

    def __eq__(self, other): return self.fitness_value == other.fitness_value

    def __ne__(self, other): return self.fitness_value != other.fitness_value

    def __gt__(self, other): return self.fitness_value > other.fitness_value

    def __ge__(self, other): return self.fitness_value >= self.fitness_value

    def __str__(self): return 'Fitness = ' + str(self.fitness_value)

    def __add__(self, other): return self.fitness_value + other.fitness_value

    def __sub__(self, other): return self.fitness_value - other.fitness_value

    def __copy__(self):
        temp = self.__class__
        result = temp.__new__(temp)
        result .__dict__.update(self.__dict__)
        return result