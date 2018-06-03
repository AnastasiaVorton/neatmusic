from mido import MidiFile  # library imports


class MidiParser:
    def __init__(self, file_path, number_of_octaves=1, ticks_per_bit=4):
        self.path = file_path
        self.number_of_octaves = number_of_octaves

        #  Parse the file and store the data for the neural network.
        self.output = []
        mid_file = MidiFile(file_path)  # MidiFile object creation specifying the path
        ticks_per_atomic_duration = mid_file.ticks_per_beat / ticks_per_bit
        track = mid_file.tracks[0]  # there's only one track in the input midi
        self.track_to_nn_inputs(track, ticks_per_atomic_duration)

    def track_to_nn_inputs(self, track, ticks_per_atomic_duration):
        for msg in track:  # print each message in a track
            if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_on' and not msg.time == 0:
                nn_input = [0.0 for _ in range(12 * self.number_of_octaves)]

                ticks_in_note = msg.time / ticks_per_atomic_duration
                print(ticks_in_note, nn_input)
                if ticks_in_note.is_integer():
                    for _ in range(int(ticks_in_note)):
                        self.output.append(nn_input)

            if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_off':
                note = msg.note
                note = note % 12 * self.number_of_octaves
                nn_input = [0.0 for _ in range(12 * self.number_of_octaves)]
                nn_input[note] = 1.0

                ticks_in_note = msg.time / ticks_per_atomic_duration
                print(ticks_in_note, nn_input)
                if ticks_in_note.is_integer():
                    for _ in range(int(ticks_in_note)):
                        self.output.append(nn_input)


output = MidiParser('dataset/X Files.mid', 2, 8)
print(output.output)
