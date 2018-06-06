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


def check_notes_number(separate_track):
    """
    Checks if the number of notes in chord less or equal to 4.
    :return: The value of correctness (in percents).
    """
    num_good = 0
    num_bad = 0
    for chord in separate_track:
        if len(chord[0]) >= 5:
            num_bad += 1
        else:
            num_good += 1
    print('good: ', num_good, 'bad: ', num_bad)
    # ratio of good duration of musical units to total number of units
    perc_good = num_good / len(separate_track)
    return perc_good


def check_intervals(separate_track):
    """
    Checks the difference between notes in each chord and between neighbour chords.
    :param separate_track:
    :return:
    """
    # CHECK 'result' VALUE
    result = 0.0
    for chord in separate_track:
        chord.sort()
    # Inside of each chord.
    for chord in separate_track:
        for i in range(len(chord)):
            temp = len(chord)
            if i >= (temp - 1): break
            if abs(chord[i] - chord[i + 1]) > 12:
                result += 200
    # Interval between chords.
    for i in range(len(separate_track)):
        if i == (len(separate_track) - 1):
            break
        if abs(separate_track[i][0] - separate_track[i + 1][0]) > 12:
            result += 300
    return result


def fitness_function(music):
    # CHECK 'result' VALUE
    """
        # DONE - Tonality: Check all notes if they belong to tonality or not
        # DONE - Number of simultaneously played notes 
        . Intervals in chords:
        . Intervals in 2 note combinations
        . Difference in interval between
        . Difference in interval between chords.
        # TODO - All instruments play in their range
    """
    # 'music' is a map of lists.
    # Check for tonality
    results = []
    parsed_music = music_parser(music)
    result = 0.0
    for s_track in music:
        result += check_tonality(music[s_track])
        result += check_notes_number(music[s_track])
        result += check_intervals(music[s_track])
        results.append(result)
    return result


# {0: [[1, 3, 5], [13, 3, 5], [15, 3, 2], [5]]}

def music_parser(music):
    """
    Parse list by the beginning.
    :param music: given music
    :return: parsed list of notes
    """
    # music = [[1, 3, 5], [13, 3, 5], [15, 3, 2]]
    parsed_music = []
    i = 0
    for note in range(len(music)):
        note = i + 1
        if note == len(music):
            break
        chord = []
        while i < len(music):
            if i == len(music) - 1:
                chord.append(music[i][0])
                parsed_music.append(chord.copy())
                i += 1
                break
            if music[i][1] != music[i + 1][1]:
                chord.append(music[i][0])
                parsed_music.append(chord.copy())
                i += 1
                break
            else:
                chord.append(music[i][0])
            i += 1
    return parsed_music