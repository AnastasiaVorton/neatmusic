from composition_generator import generate_composition


def main():
    settings = read_settings()
    generate_composition(settings[0], settings[1], settings[2])


def read_settings():
    """
    reads parameters needed for generating music
    :return:
    """
    decision = input("You wanna do it fast? [y/n] ")
    if decision == 'y':
        checkpoint_num = input("Please enter the number of checkpoint ")
        return 'cp-'+checkpoint_num, 'jinglebells2.mid', 'result.mid'
    else:
        checkpoint_path = input("Please enter the path to a checkpoint including the file name ")
        input_midi_path = input("Please enter the path to a midi file with a melody including the file name ")
        output_midi_path = input("Please enter the path where you want to save the result including the file name ")
        return checkpoint_path, input_midi_path, output_midi_path


if __name__ == "__main__":
    main()
