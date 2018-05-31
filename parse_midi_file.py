from mido import MidiFile  # library imports


class MidiParser:
    def __init__(self, file_path):
        self.path = file_path

        #  Parse the file and store the data for the neural network.
        self.output = []
        mid_file = MidiFile(file_path)  # MidiFile object creation specifying the path
        for i, track in enumerate(mid_file.tracks):  # for each track in a file
            # print('Track {}: {}'.format(i, track.name))miot3o
            for msg in track:  # print each message in a track
                if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_on':
                    note = msg.note
                    # print(note)
                    note = note % 12
                    print(note)
                    self.output.append(note)


outpt = MidiParser('dataset/prima.mid')
print(outpt.output)
