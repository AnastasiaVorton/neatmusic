from mido import MidiFile  # library imports


class MidiParser:
    def __init__(self, file_path):
        self.path = file_path

        #  Parse the file and store the data for the neural network.
        self.output = []
        mid_file = MidiFile(file_path)  # MidiFile object creation specifying the path
        for i, track in enumerate(mid_file.tracks):  # for each track in a file
            # print('Track {}: {}'.format(i, track.name))
            i = 0
            for msg in track:  # print each message in a track
                if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_on':
                    i += 1
                    note = msg.note
                    print(note)
                    note = note % 12
                    print(note)
                    nn_input = [0.0 for x in range(12)]
                    nn_input[note] = 1.0
                    print(nn_input)
                    self.output.append(nn_input)
            print("number of notes = ", i)


outpt = MidiParser('dataset/prima.mid')
print(outpt.output)
