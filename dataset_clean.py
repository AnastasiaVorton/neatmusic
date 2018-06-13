import glob
from mido import MidiFile

good_notes = [0, 2, 4, 5, 7, 9, 11]
in_c_major = 0
total_tracks = 0

for filename in glob.iglob('dataset/*.mid'):
    total_tracks += 1
    mid_file = MidiFile(filename)
    total_notes = 0
    in_tonality = 0
    for i, track in enumerate(mid_file.tracks):  # for each track in a file
        # print('Track {}: {}'.format(i, track.name))
        for msg in track:  # print each message in a track
            if not msg.is_meta and msg.type == 'note_on':
                total_notes += 1
                if msg.note % 12 in good_notes:
                    in_tonality += 1
        if total_notes == in_tonality:
            in_c_major += 1
        if not (total_notes == in_tonality):
            print(filename)

print('total: ', total_tracks, ', in tonality: ',  in_c_major)
