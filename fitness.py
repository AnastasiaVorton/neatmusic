import math

# C major notes
good_notes = [0, 2, 4, 5, 7, 9, 11]
piano = 1
guitar_acoustic = 26
guitar_bass = 33


def check_tonality(separate_track):
    """
    This function checks the tonality of notes of melody.
    :return: The value of correctness (in percents).
    """
    num_good = 0
    notes = []
    for chord in separate_track:
        # represent all notes as a single list and represent them as values from 0 to 11
        for note in chord[0]:
            notes.append(note % 12)
    for note in notes:
        if note in good_notes:
            num_good += 1
    # ratio of good notes to total number of notes
    return num_good / max(len(notes), 1)


def check_notes_number(instrument, separate_track):
    """
    Checks if the number of notes in chord less or equal to 4.
    :return: The value of correctness (in percents).
    """
    num_good = 0
    limit = 3
    if instrument == guitar_bass:
        limit = 1
    elif instrument == piano:
        limit = 4
    for chord in separate_track:
        if len(chord[0]) <= limit:
            num_good += 1
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / max(len(separate_track), 1)
    return perc_good


def is_in_tonality(note):
    return note in good_notes


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def check_chord_intervals(instrument, separate_track):
    """
    Checks the difference between notes in each chord.
    :param instrument: instrument id
    :param separate_track:
    :return:
    """
    num_good = 0
    total_chords = 0
    for pitches, _, _ in separate_track:
        if len(pitches) > 2:
            total_chords += 1
            if instrument == piano:
                differences = [j - i for i, j in zip(pitches[:-1], pitches[1:])]
            else:
                pitches = [i % 12 for i in pitches]
                differences = [min(j - i, j - i + 12, j - i - 12) for i, j in zip(pitches[:-1], pitches[1:])]
            badness = 0
            for i in differences:
                if i < 3:
                    badness += (3 - i) / 3
                elif i > 4:
                    badness += min((i - 4) / 3, 1)
            num_good += 1 - badness / len(differences)
    # ratio of good duration of musical units to total number of units
    return num_good / max(total_chords, 1)


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
    return num_good / max(len(notes), 1)


def dissonance_check(first, second):
    stsble = [0, 4, 7]
    #  first is stable
    if (first[0][0] % 12 in stsble) and (second[0][0] == first[0][0]):
        if first[0][1] % 12 == 2 and (second[0][1] % 12 == 0 or second[0][1] % 12 == 4):
            return True
        if first[0][1] % 12 == 5 and (second[0][1] % 12 == 4 or second[0][1] % 12 == 7):
            return True
        if first[0][1] % 12 == 11 and second[0][1] % 12 == 0 :
            return True
    # first is unstable
    if first[0][0] % 12 == 5 and first[0][1] % 12 == 7 and second[0][1] % 12 == 7 and (second[0][0] % 12 == 4 or second[0][0] % 12 == 7):
        return True
    return False


def check_intervals(separate_track):
    num_good = 0
    total_intervals = 0
    for index, chord in enumerate(separate_track):
        if len(chord[0]) == 2:
            total_intervals += 1
            first = chord[0][0]
            second = chord[0][1]
            if is_in_tonality(first % 12):
                #  checks for consonance
                if (second % 12 == first % 12 + 3) or (second % 12 == first % 12 + 4) or (
                                second % 12 == first % 12 + 5) or (second % 12 == first % 12 + 7) or (
                                second % 12 == first % 12 + 8) or (second % 12 == first % 12 + 9) or (
                                second % 12 == first % 12):
                    num_good += 1
                # checks for dissonance
                if index < len(separate_track) - 1:
                    next_chord = separate_track[index+1]
                    if len(next_chord[0]) == 2 and dissonance_check(chord, next_chord):
                        num_good += 1
    # ratio of good intervals to total number of intervals
    return num_good / max(total_intervals, 1)


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
        if len(parsed_part) != 0:
            parsed_music[part] = parsed_part.copy()
    return parsed_music
