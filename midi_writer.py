from mido import Message, MidiFile, MidiTrack  # library imports


def generate_and_save_midi(file_path, music, initial_track):
    scaled_composition = scale_parts(music)
    write_file(file_path, scaled_composition, initial_track)


def scale_parts(music):
    """
    Scales values of pitches of each track depending on the associate instrument.
    :param music: a dictionary of generated tracks (already parsed by music_parser(music))
    :return: generated tracks with scaled values of pitches
    """

    for instrument, track in music.items():
        offset = 0
        if instrument == 1:
            offset = 12 * (4 - 2 + 1)
        elif instrument == 26:
            offset = 12 * (3 - 2 + 1)
        elif instrument == 33:
            offset = 12 * (4 - 2 + 1)
        for chord_tuple in track:
            for i in range(len(chord_tuple[0])):
                chord_tuple[0][i] = chord_tuple[0][i] + offset
    return music


def write_file(file_path, music, initial_track):
    """
    Writes the generated music to a midi file
    :param file_path: path to the file where midi will be stored
    :param music: the generated tracks
    :param initial_track: the initial track (not affected by any parser)
    """
    mid_file = MidiFile()
    mid_file.ticks_per_beat = 16
    ticks_per_bar = 16 * 4
    i = 0
    mid_file.tracks.append(initial_track)
    for instrument, track in music.items():
        mid_track = MidiTrack()
        mid_file.tracks.append(mid_track)
        mid_track.append(Message('control_change', channel=i, control=0))
        i = i + 1
        mid_track.append(Message('program_change', channel=i, program=instrument))
        velocity = 100
        possible_pause_offset = 0
        for chord, duration, _ in track:
            if len(chord) == 0:
                possible_pause_offset = int(duration * ticks_per_bar)
            for i in range(len(chord)):
                if i == 0:
                    mid_track.append(Message('note_on', note=chord[i], velocity=velocity, time=possible_pause_offset))
                    possible_pause_offset = 0
                else:
                    mid_track.append(Message('note_on', note=chord[i], velocity=velocity, time=0))

            for i in range(len(chord)):
                if i == 0:
                    mid_track.append(Message('note_off', note=chord[i], velocity=velocity,
                                             time=int(duration * ticks_per_bar)))
                else:
                    mid_track.append(Message('note_off', note=chord[i], velocity=velocity, time=0))
    mid_file.save(file_path)
