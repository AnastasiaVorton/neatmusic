import random


def gen_test(size):
    return [random.choice([0.0, 1.0]) for _ in range(10)]


def answer_test(test):
    return [float((i % 2 != 0) ^ bool(round(j))) for i, j in enumerate(test)]


def is_valid(test) -> bool:
    start = True
    for i, o in test:
        if (o >= 0.5) == (start ^ (i >= 0.5)):
            return False
        start = not start
    return True


def eval_function(net) -> float:
    cur = 0
    for _ in range(10):
        size = random.randint(8, 10)
        val = size
        test = gen_test(size)
        answer = answer_test(test)
        net.reset()
        for i in range(size):
            output = net.activate((test[i],))
            val -= (output[0] - answer[i]) ** 2
        val /= size
        cur += val
    return cur / 10


"""
    NEXT CODE IS IMPLEMENTATION OF FITNESS FUNCTION
"""


def check_tonality(separate_track):
    """
    This function checks the tonality of notes of melody.
    :return: The value of correctness (in percents).
    """
    # Tonality: C
    good_notes = [0, 2, 4, 5, 7, 9, 11]  # C major Tonality notes
    num_good = 0
    num_bad = 0
    notes = []
    for chord in separate_track:
        # represent all notes as a single list and represent them as values from 0 to 11
        for note in chord[0]:
            notes.append(note % 12)
    for note in notes:
        if note in good_notes:
            num_good += 1
        else:
            num_bad += 1
    print('good: ', num_good, 'bad: ', num_bad)
    # ratio of good notes to total number of notes
    perc_good = num_good / len(notes)
    return perc_good


def check_notes_number(instrument, separate_track):
    """
    Checks if the number of notes in chord less or equal to 4.
    :return: The value of correctness (in percents).
    """
    num_good = 0
    num_bad = 0
    # check if bass guitar
    if instrument == 33:
        for chord in separate_track:
            if len(chord[0]) >= 2:
                num_bad += 1
            else:
                num_good += 1
    else:  # check if piano or rhythm guitar
        for chord in separate_track:
            if len(chord[0]) >= 5:
                num_bad += 1
            else:
                num_good += 1
    print('good: ', num_good, 'bad: ', num_bad)
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / len(separate_track)
    return perc_good


def is_in_tonality(note):
    good_notes = [0, 2, 4, 5, 7, 9, 11]
    if note in good_notes:
        return True
    else:
        return False


def check_chord_intervals(separate_track):
    """
        Checks the difference between notes in each chord.
        :param separate_track:
        :return:
        """
    num_good = 0
    total_chords = 0
    for chord in separate_track:
        if len(chord[0]) == 3:
            total_chords += 1
            first = chord[0][0]
            second = chord[0][1]
            third = chord[0][2]
            if is_in_tonality(first % 12):
                # check if C dur
                if first % 12 == 0 and second == first + 4 and third == second + 3:
                    num_good += 1
                # check if D moll
                elif first % 12 == 2 and second == first + 3 and third == second + 4:
                    num_good += 1
                # check if E moll
                elif first % 12 == 4 and second == first + 3 and third == second + 4:
                    num_good += 1
                # check if F dur
                elif first % 12 == 5 and second == first + 4 and third == second + 3:
                    num_good += 1
                # check if G dur
                elif first % 12 == 7 and second == first + 4 and third == second + 3:
                    num_good += 1
                # check if A moll
                elif first % 12 == 9 and second == first + 3 and third == second + 4:
                    num_good += 1
                # check if H moll reduced
                elif first % 12 == 11 and second == first + 3 and third == second + 3:
                    num_good += 1
        elif len(chord[0]) == 4:
            total_chords += 1
            first = chord[0][0]
            second = chord[0][1]
            third = chord[0][2]
            fourth = chord[0][3]
            # assuming natural C major and accepting only half-diminished leading seventh chords
            if is_in_tonality(first % 12):
                # check if MVII7
                if first % 12 == 11 and second == first + 3 and third == second + 3 and fourth == third + 3:
                    num_good += 1
                # check if MVII65
                if first % 12 == 2 and second == first + 3 and third == second + 3 and fourth == third + 2:
                    num_good += 1
                # check if MVII43
                if first % 12 == 5 and second == first + 4 and third == second + 2 and fourth == third + 3:
                    num_good += 1
                # check if MVII2
                if first % 12 == 9 and second == first + 2 and third == second + 3 and fourth == third + 4:
                    num_good += 1
    print('good: ', num_good)
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / total_chords
    return perc_good


def fitness_function(music):
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
            result += check_tonality(notes)
            result += check_notes_number(instr, notes)
            result += check_chord_intervals(notes)
            results[instr] = result
        # check for bass
        elif instr == 33:
            result += check_tonality(notes)
            result += check_notes_number(instr, notes)
            results[instr] = result
    return results


def music_parser(music):
    """
    Parse list by the beginning.
    :param music: given music
    :return: parsed list of notes
    """
    parsed_music = {}
    for part in range(len(music)):
        cnt = 1
        chord = []
        parsed_part = []
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
                parsed_part.append((chord.copy(), float(cnt) / 64))
                chord.clear()
                cnt = 0
            cnt += 1
        parsed_music[part] = parsed_part.copy()
    return parsed_music.copy()
