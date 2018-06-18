import math
from typing import *

# C major notes
good_notes = [0, 2, 4, 5, 7, 9, 11]
piano = 1
guitar_acoustic = 25
guitar_bass = 33
consonants = [0, 3, 4, 5, 7, 8, 9]
chord_length_threshold = 0.75
chord_limits = {piano: 4, guitar_acoustic: 3, guitar_bass: 1}


def two_tracks_consonance_fitness(track1, track2):
    """
    Calculates fitness of two tracks together regarding how consonant their simultaneous chords are
    :param track1:
    :param track2:
    :return: normalised fitness value in range 0...1
    """
    chords_fitness = 0
    simultaneous_chords = 0
    for chord1 in track1:
        for chord2 in track2:
            if chord1[2] < chord2[2]:
                break
            if chord1[2] == chord2[2]:
                simultaneous_chords = simultaneous_chords + 1
                chords_fitness = chords_fitness + two_chords_consonance_fitness(chord1, chord2)
    return chords_fitness / simultaneous_chords


def two_chords_consonance_fitness(chord1, chord2):
    """
    Calculates fitness of two chords together regarding how consonant they are
    :param chord1:
    :param chord2:
    :return:
    """
    good_intervals = 0
    for pitch1 in chord1[0]:
        for pitch2 in chord2[0]:
            diff = abs(pitch1 % 12 - pitch2 % 12)
            if diff in consonants:
                good_intervals = good_intervals + 1
    return good_intervals / (len(chord1[0]) * len(chord2[0]))


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
        if is_in_tonality(note):
            num_good += 1
    # ratio of good notes to total number of notes
    return num_good / max(len(notes), 1)


def check_notes_number(instrument, separate_track):
    """
    Checks if the number of notes in chord less or equal to 4.
    :return: The value of correctness (in percents).
    """
    value = 0
    limit = chord_limits.get(instrument) or 3
    for pitches, _, _ in separate_track:
        if len(pitches) <= limit:
            value += 1
        else:
            value += 2 ** (limit - len(pitches))
    return value / max(len(separate_track), 1)


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
                    next_chord = separate_track[index + 1]
                    if len(next_chord[0]) == 2 and dissonance_check(chord, next_chord):
                        num_good += 1
    # ratio of good intervals to total number of intervals
    return num_good / max(total_intervals, 1)


def check_timestamp_fitness(main, second, percents):
    #  1 если больше 50% совпадают с аккордом, % есди беньше 50
    # checks if a note in main melody and a chord in an instrument part start simultaneously
    good = 0
    for note in main:
        for chord in second:
            if chord[2] == note[2]:
                good += 1
                # print(note, chord)
    perc_good = good / len(second)
    if perc_good >= percents:
        return 1.0
    else:
        return perc_good

def chord_length(track) -> float:
    """
    Evaluates the track for presence of too long chords
    :param track:
    :return: the ratio of excess length to the track's length
    """
    sum_lengths = 0.0
    bad_lengths = 0.0
    for _, length, _ in track:
        sum_lengths += length
        if length > chord_length_threshold:
            bad_lengths += length - chord_length_threshold
    return bad_lengths / max(sum_lengths, 1.0)


def check_variety(track):
    occurrences = {}
    occurrences[128] = 0
    for chord_tuple in track:
        if len(chord_tuple[0]) == 0:
            occurrences[128] = occurrences[128] + chord_tuple[1] * 64
        for note in chord_tuple[0]:
            if note not in occurrences.keys():
                occurrences[note] = chord_tuple[1] * 64
            else:
                occurrences[note] = occurrences[note] + chord_tuple[1] * 64
    occurrence_list = list(occurrences.values())
    if len(occurrence_list) == 0:
        return 0
    else:
        last_chord = track[len(track) - 1]
        max_occurrence = max(occurrence_list)
        x = max_occurrence/(last_chord[1] * 64 + last_chord[2])

        return x


def fitness_function(music):
    """
    instruments: 33 - bass, 1 - piano, 25 - acoustic guitar
    # DONE - Tonality: Check all notes if they belong to tonality or not
    # DONE - Number of simultaneously played notes
    # DONE - Intervals in chords:
    # DONE Intervals in 2 note combinations
    # DONE Difference in interval between chords. (разрешения)
    . Колина непонятная штука
    # DONE All instruments play in their range
    """
    # TODO correct datatype
    results = {}
    for instr, notes in music.items():
        result = 0.0
        # check for piano and rhythm guitar
        if instr == 1 or instr == 25:
            result += check_tonality(notes)
            result -= chord_length(notes) * 2
            # result += check_notes_number(instr, notes)
            result += check_chord_intervals(instr, notes)
            result -= check_variety(notes) * 2
            # result += check_intervals(notes)
            results[instr] = result
        # check for bass
        elif instr == 33:
            result += check_tonality(notes)
            result -= chord_length(notes) * 2
            # result += check_notes_number(instr, notes)
            results[instr] = result
    main = music.get(0)
    left_hand = music.get(piano)
    results[128] = check_timestamp_fitness(main, left_hand, 0.5)
    return results


def music_parser(part) -> Dict[int, List[Tuple[List[int], float, int]]]:
    """
    Parse list by the beginning.
    :param music: given music
    :return: list of chords, chord is defined as tuple of list of pitches, duration, and start offset
    """
    #  Rectify input music
    for tick in range(len(part)):
        if tick % 2 == 0:
            continue
        for i in range(len(part[tick])):
            if part[tick - 1][i] == 1.0:
                if part[tick - 1][i] != part[tick][i]:
                    part[tick][0] = 2.0
                    break
            if tick == len(part) - 1:
                part[tick][0] = 2.0
    # Parse music
    cnt = 0
    chord = []
    parsed_part = []
    note_start = 0
    for tick in range(len(part)):
        end_of_chord = False
        if tick % 2 == 0:
            cnt += 2
            continue
        if tick != len(part) - 1:
            if part[tick][0] == 2.0:
                part[tick][0] = part[tick - 1][0]
                end_of_chord = True
        if end_of_chord or tick == len(part) - 1:
            for i in range(len(part[tick]) - 1):
                if part[tick - 1][i] == 1.0:
                    chord.append(i % 12)
            parsed_part.append((chord.copy(), float(cnt) / 64, note_start))
            note_start = tick + 1
            chord.clear()
            cnt = 0
    return parsed_part
