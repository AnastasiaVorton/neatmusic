import random

notes = []
for i in range(0, 36):
    notes.append(i)

durations = [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1]
start_ticks = [64, 32, 16, 8, 4, 2, 1, 0]


def write_track(type):
    chords = []
    current_tick = 0
    chords.append(([60 % 12], 1 / 16, current_tick))
    for i in range(15):
        p = random.uniform(0.0, 1.0)
        current_tick += random.choice(start_ticks)
        if type == 1:
            chords.append(([random.choice(notes)], random.choice(durations), current_tick))
        elif type == 2:
            if 0.0 < p < 0.2:
                chords.append(([random.choice(notes)], random.choice(durations), current_tick))
            elif 0.2 < p < 0.4:
                chords.append(([random.choice(notes), random.choice(notes)], random.choice(durations), current_tick))
            elif 0.4 < p < 0.6:
                chords.append(
                    ([random.choice(notes), random.choice(notes), random.choice(notes)], random.choice(durations),
                     current_tick))
                chords.append(([60 % 12, 64 % 12, 67 % 12], random.choice(durations), current_tick))
            elif 0.6 < p < 0.8:
                chords.append(
                    ([random.choice(notes), random.choice(notes), random.choice(notes), random.choice(notes), ],
                     random.choice(durations), current_tick))
                chords.append(([59 % 12, 62 % 12, 65 % 12, 68 % 12], random.choice(durations), current_tick))
            elif 0.8 < p < 1.0:
                chords.append(([random.choice(notes), random.choice(notes), random.choice(notes), random.choice(notes),
                                random.choice(notes)], random.choice(durations), current_tick))
    print('length: ', len(chords), 'chords: ', chords)
    return chords


def music_parser(music):
    """      
    Parse list by the beginning.
    :param music: given music
    :return: parsed list of notes
    """
    # Rectify input music
    for part in music.keys():
        for tick in range(len(music[part])):
            if tick % 2 == 0:
                continue
            for i in range(len(music[part][tick])):
                if music[part][tick - 1][i] == 1.0:
                    music[part][tick][i] = 1.0
                else:
                    music[part][tick][i] = 0.0
    # Parse music
    parsed_music = {}
    for part in music.keys():
        cnt = 1
        chord = []
        parsed_part = []
        note_start = 0
        for tick in range(len(music[part])):
            end_of_chord = False
            if tick != len(music[part]) - 1:
                for i in range(len(music[part][tick])):
                    if music[part][tick][i] != music[part][tick + 1][i]:
                        end_of_chord = True
                        break
            if end_of_chord or tick == len(music[part]) - 1:
                for i in range(len(music[part][tick])):
                    if music[part][tick][i] == 1.0:
                        chord.append(i % 12)
                parsed_part.append((chord.copy(), float(cnt) / 64, note_start))
                note_start = tick + 1
                chord.clear()
                cnt = 0
            cnt += 1
        if not len(parsed_part) == 0:
            parsed_music[part] = parsed_part.copy()
    return parsed_music.copy()


def is_in_tonality(note):
    good_notes = [0, 2, 4, 5, 7, 9, 11]
    if note in good_notes:
        return True
    else:
        return False


def dissonance_check(first, second):
    stsble = [0, 4, 7]
    #  first is stable
    if (first[0][0] % 12 in stsble) and (second[0][0] == first[0][0]):
        if first[0][1] % 12 == 2 and (second[0][1] % 12 == 0 or second[0][1] % 12 == 4):
            return True
        if first[0][1] % 12 == 5 and (second[0][1] % 12 == 4 or second[0][1] % 12 == 7):
            return True
        if first[0][1] % 12 == 11 and second[0][1] % 12 == 0:
            return True
    # first is unstable
    if first[0][0] % 12 == 5 and first[0][1] % 12 == 7 and second[0][1] % 12 == 7 and (
                        second[0][0] % 12 == 4 or second[0][0] % 12 == 7):
        return True


def check_intervals(separate_track):
    num_good = 0
    total_intervals = 0
    for index, chord in enumerate(separate_track):
        if len(chord[0]) == 2:
            total_intervals += 1
            first = chord[0][0]
            second = chord[0][1]
            p = random.uniform(0.0, 1.0)
            if is_in_tonality(first % 12):
                #  checks for consonance
                if (second % 12 == first % 12 + 3) or (second % 12 == first % 12 + 4) or (
                                second % 12 == first % 12 + 5) or (second % 12 == first % 12 + 7) or (
                                second % 12 == first % 12 + 8) or (second % 12 == first % 12 + 9) or (
                                second % 12 == first % 12):
                    num_good += 1
                else:  # checks for dissonance
                    next_chord = separate_track[index + 1]
                    if len(next_chord[0]) == 2:
                        if dissonance_check(chord, next_chord):
                            num_good += 1
    print('interval fitness: ', 'good: ', num_good)
    # ratio of good intervals to total number of intervals
    if total_intervals > 0:
        perc_good = num_good / total_intervals
    else:
        perc_good = 0.0
    return perc_good


def check_timestamp_fitness(main, second):
    #  1 если больше 50% совпадают с аккордом, % есди беньше 50
    # checks if a note in main melody and a chord in an instrument part start simultaneously
    good = 0
    for note in main:
        for chord in second:
            if chord[2] == note[2]:
                good += 1
                print(note, chord)
    print('good: ', good, ', total: ', len(second))
    perc_good = good / len(second)
    if perc_good >= 0.5:
        return 1.0
    else:
        return perc_good


def fitness_function(num_of_octaves, music):
    """
        instruments: 33 - bass, 1 - piano, 26 - acoustic guitar
        # DONE - Tonality: Check all notes if they belong to tonality or not
        # DONE - Number of simultaneously played notes 
        # DONE - Intervals in chords:
        . Intervals in 2 note combinations
        . Difference in interval between chords. (разрешения)
        . Колина непонятная штука
        . All instruments play in their range
    """
    results = {}
    for instr, notes in music.items():
        result = 0.0
        # check for piano and rhythm guitar
        if instr == 1 or instr == 26:
            result += check_intervals(notes)
            results[instr] = result
        # check for bass
        elif instr == 33:
            results[instr] = result
    return results


chords1 = write_track(1)
chords2 = write_track(2)
music = {26: chords1}
# print(check_intervals(chords1))
print(check_timestamp_fitness(chords1, chords2))
# oktaves = 3

# print(fitness_function(oktaves, music))
