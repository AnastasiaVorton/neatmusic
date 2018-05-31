import glob
from mido import MidiFile

for filename in glob.iglob('dataset/*.mid'):
    mid_file = MidiFile(filename)
    tpb = mid_file.ticks_per_beat
    for i, track in enumerate(mid_file.tracks):  # for each track in a file
        # print('Track {}: {}'.format(i, track.name))
        for msg in track:  # print each message in a track
            if not msg.is_meta and hasattr(msg, 'time'):
                time = msg.time
                if msg.type == 'note_on' and time > 0:
                    if time/tpb < 1/4:
                        print("pause if smaller than 1/16 in ", filename)
                if msg.type == 'note_off' and time > 0:
                    if time/tpb < 1/4:
                        print("short notes in ", filename)

