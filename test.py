import random

chords = []

notes = []
for i in range(60, 128):
    notes.append(i)

durations = [1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1]
chords.append(([60], 1 / 16))
for i in range(15):
    p = random.uniform(0.0, 1.0)
    if 0.0 < p < 0.2:
        chords.append(([random.choice(notes)], random.choice(durations)))
    elif 0.2 < p < 0.4:
        chords.append(([random.choice(notes), random.choice(notes)], random.choice(durations)))
    elif 0.4 < p < 0.6:
        chords.append(([random.choice(notes), random.choice(notes), random.choice(notes)], random.choice(durations)))
    elif 0.6 < p < 0.8:
        chords.append(([random.choice(notes), random.choice(notes), random.choice(notes), random.choice(notes)],
                       random.choice(durations)))
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


print('tonality fitness: ', check_tonality(chords))
print('number of notes fitness', check_notes_number(chords))