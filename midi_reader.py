import os

from mido import MidiFile  # library imports


def dataset_list():
    return [f for f in os.listdir('dataset') if f.endswith('.mid') or f.endswith('.midi')]


def get_original_track(file_path, ticks_per_beat=16):
    """
    retrieves the original track from a midi file without changes
    :param ticks_per_beat:
    :param file_path: path to the file
    :return: the track (as an object of type specified in the mido library)
    """
    mid_file = MidiFile('dataset' + os.sep + file_path)  # MidiFile object creation specifying the path
    ticks_per_atomic_duration = mid_file.ticks_per_beat / ticks_per_beat

    track = mid_file.tracks[0]
    for i in range(len(track)):
        track[i].time = int(track[i].time / ticks_per_atomic_duration)

    return track


def read_file(file_path, number_of_octaves=1, ticks_per_beat=16):
    """
    Parse the file and return the input series for a neural network.
    :param file_path:
    :param number_of_octaves:
    :param ticks_per_beat:
    :return:
    """
    output = []
    mid_file = MidiFile('dataset' + os.sep + file_path)  # MidiFile object creation specifying the path
    ticks_per_atomic_duration = mid_file.ticks_per_beat / ticks_per_beat
    track = mid_file.tracks[0]  # there's only one track in the input midi
    for msg in track:  # print each message in a track
        if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_on' and not msg.time == 0:
            nn_input = [0.0 for _ in range(12 * number_of_octaves)]

            ticks_in_note = msg.time / ticks_per_atomic_duration
            if ticks_in_note.is_integer():
                for _ in range(int(ticks_in_note)):
                    output.append(nn_input)

        if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_off':
            note = msg.note
            note = note % 12 * number_of_octaves
            nn_input = [0.0 for _ in range(12 * number_of_octaves)]
            nn_input[note] = 1.0

            ticks_in_note = msg.time / ticks_per_atomic_duration
            if ticks_in_note.is_integer():
                for _ in range(int(ticks_in_note) - 1):
                    output.append(nn_input)
                if ticks_in_note > 0:
                    output.append([0.0 for _ in range(12 * number_of_octaves)])
    return output


def read_all_dataset(number_of_octaves=1, ticks_per_beat=16):
    """
    Reads the whole dataset into a list of input series
    :param number_of_octaves:
    :param ticks_per_beat:
    :return:
    """
    return [m for m in [read_file(f, number_of_octaves, ticks_per_beat) for f in dataset_list()] if m]
