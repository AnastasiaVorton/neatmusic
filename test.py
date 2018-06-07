import random

chords = []

notes = []
for i in range(0, 36):
    notes.append(i)

durations = [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1]
chords.append(([60 % 12], 1 / 16))
for i in range(15):
    p = random.uniform(0.0, 1.0)
    if 0.0 < p < 0.2:
        chords.append(([random.choice(notes)], random.choice(durations)))
    elif 0.2 < p < 0.4:
        chords.append(([random.choice(notes), random.choice(notes)], random.choice(durations)))
    elif 0.4 < p < 0.6:
        chords.append(([random.choice(notes), random.choice(notes), random.choice(notes)], random.choice(durations)))
        chords.append(([60 % 12, 64 % 12, 67 % 12], random.choice(durations)))
    elif 0.6 < p < 0.8:
        chords.append(([random.choice(notes), random.choice(notes), random.choice(notes), random.choice(notes)],
                       random.choice(durations)))
        chords.append(([59 % 12, 62 % 12, 65 % 12, 68 % 12], random.choice(durations)))
    elif 0.8 < p < 1.0:
        chords.append(([random.choice(notes), random.choice(notes), random.choice(notes), random.choice(notes),
                        random.choice(notes)], random.choice(durations)))

print('length: ', len(chords), 'chords: ', chords)


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
    print('tonality fitness: ', 'good: ', num_good, 'bad: ', num_bad)
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
    print('notes number fitness: ', 'good: ', num_good, 'bad: ', num_bad)
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / len(separate_track)
    return perc_good


def is_in_tonality(note):
    good_notes = [0, 2, 4, 5, 7, 9, 11]
    if note in good_notes:
        return True
    else:
        return False


def check_chord_intervals(instrument, separate_track):
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
                if (instrument == 1 and first % 12 == 0 and second == first + 4 and third == second + 3) or (
                                        instrument == 26 and first % 12 == 0 and second % 12 == first % 12 + 4 and third % 12 == second % 12 + 3):
                    num_good += 1
                # check if D moll
                elif (instrument == 1 and first % 12 == 2 and second == first + 3 and third == second + 4) or (
                                        instrument == 26 and first % 12 == 2 and second % 12 == first % 12 + 3 and third % 12 == second % 12 + 4):
                    num_good += 1
                # check if E moll
                elif (instrument == 1 and first % 12 == 4 and second == first + 3 and third == second + 4) or (
                                        instrument == 26 and first % 12 == 4 and second % 12 == first % 12 + 3 and third % 12 == second % 12 + 4):
                    num_good += 1
                # check if F dur
                elif (instrument == 1 and first % 12 == 5 and second == first + 4 and third == second + 3) or (
                                        instrument == 26 and first % 12 == 5 and second % 12 == first % 12 + 4 and third % 12 == second % 12 + 3):
                    num_good += 1
                # check if G dur
                elif (instrument == 1 and first % 12 == 7 and second == first + 4 and third == second + 3) or (
                                        instrument == 26 and first % 12 == 7 and second % 12 == first % 12 + 4 and third % 12 == second % 12 + 3):
                    num_good += 1
                # check if A moll
                elif (instrument == 1 and first % 12 == 9 and second == first + 3 and third == second + 4) or (
                                        instrument == 26 and first % 12 == 9 and second % 12 == first % 12 + 3 and third % 12 == second % 12 + 4):
                    num_good += 1
                # check if H moll reduced
                elif (instrument == 1 and first % 12 == 11 and second == first + 3 and third == second + 3) or (
                                        instrument == 26 and first % 12 == 11 and second % 12 == first % 12 + 3 and third % 12 == second % 12 + 3):
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
                if (
                                            instrument == 1 and first % 12 == 11 and second == first + 3 and third == second + 3 and fourth == third + 3) or (
                                            instrument == 26 and first % 12 == 11 and second % 12 == first % 12 + 3 and third % 12 == second % 12 + 3 and fourth % 12 == third % 12 + 3):
                    num_good += 1
                # check if MVII65
                if (
                                            instrument == 1 and first % 12 == 2 and second == first + 3 and third == second + 3 and fourth == third + 2) or (
                                            instrument == 1 and first % 12 == 2 and second % 12 == first % 12 + 3 and third % 12 == second % 12 + 3 and fourth % 12 == third % 12 + 2):
                    num_good += 1
                # check if MVII43
                if (
                                            instrument == 1 and first % 12 == 5 and second == first + 4 and third == second + 2 and fourth == third + 3) or (
                                            instrument == 26 and first % 12 == 5 and second % 12 == first % 12 + 4 and third % 12 == second % 12 + 2 and fourth % 12 == third % 12 + 3):
                    num_good += 1
                # check if MVII2
                if (
                                            instrument == 1 and first % 12 == 9 and second == first + 2 and third == second + 3 and fourth == third + 4) or (
                                            instrument == 26 and first % 12 == 9 and second % 12 == first % 12 + 2 and third % 12 == second % 12 + 3 and fourth % 12 == third % 12 + 4):
                    num_good += 1
    print('chords fitness: ', 'good: ', num_good)
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / total_chords
    return perc_good


def check_octave_pitch(num_of_octaves, instrument, separate_track):
    num_good = 0
    notes = []
    for chord in separate_track:
        # represent all notes as a single list and represent them as values from 0 to 11
        for note in chord[0]:
            notes.append(note)
    if instrument == 1:  # piano should be lower than rhythm guitar
        for note in notes:
            if num_of_octaves == 2:
                if note in range(0, int(num_of_octaves * 0.75 * 12)):
                    num_good += 1
            if num_of_octaves == 3:
                if note in range(0, 25):
                    num_good += 1
            if num_of_octaves == 4:
                if note in range(0, 31):
                    num_good += 1
    elif instrument == 26:  # piano should be lower than rhythm guitar
        for note in notes:
            if num_of_octaves == 2:
                if note in range(6, num_of_octaves * 12 + 1):
                    num_good += 1
            if num_of_octaves == 3:
                if note in range(12, num_of_octaves * 12 + 1):
                    num_good += 1
            if num_of_octaves == 4:
                if note in range(17, num_of_octaves * 12 + 1):
                    num_good += 1
    # ratio of good notes to total number of notes
    perc_good = num_good / len(notes)
    return perc_good


def check_intervals(separate_track):
    num_good = 0
    total_intervals = 0
    for chord in separate_track:
        if len(chord[0]) == 2:
            total_intervals += 1
            first = chord[0][0]
            second = chord[0][1]
            if is_in_tonality(first%12):
                if second % 12 == (first % 12 + 3 or first % 12 + 4 or first % 12 + 5 or first % 12 + 7 or first % 12 + 8 or first % 12 + 9 or first % 12):
                    num_good += 1
    print('interval fitness: ', 'good: ', num_good)
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / total_intervals
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
            result += check_tonality(notes)
            result += check_notes_number(instr, notes)
            result += check_chord_intervals(instr, notes)
            if num_of_octaves >= 2:
                result += check_octave_pitch(num_of_octaves, instr, notes)
            result += check_intervals(notes)
            results[instr] = result
        # check for bass
        elif instr == 33:
            result += check_tonality(notes)
            result += check_notes_number(instr, notes)
            results[instr] = result
    return results


music = {26: chords}
# print('tonality fitness: ', check_tonality(chords))
# print('number of notes fitness', check_notes_number(chords))
# print(check_chord_intervals(chords))
print(check_intervals(notes))
oktaves = 3

# print(fitness_function(oktaves, music))
