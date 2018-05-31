from mido import MidiFile  # library imports

mid_file = MidiFile('dataset/away.mid')  # MidiFile object creation specifying the path
for i, track in enumerate(mid_file.tracks):  # for each track in a file
    # print('Track {}: {}'.format(i, track.name))
    for msg in track:  # print each message in a track
        if not msg.is_meta and hasattr(msg, 'note') and msg.type == 'note_on':
            print(msg.note)
