import mido
from mido import MidiFile, MidiTrack, Message







def list_midi_ports():
    """List available MIDI ports."""
    inputs = mido.get_input_names()
    outputs = mido.get_output_names()
    print('Input Ports:')
    for i, port in enumerate(inputs):
        print(f"{i}: {port}")
    print('\nOutput Ports:')
    for i, port in enumerate(outputs):
        print(f"{i}: {port}")

def enumerate_controls(input_port_name):
    """Enumerate control numbers from the given input port."""
    with mido.open_input(input_port_name) as inport:
        print(f"Listening to {input_port_name}. Press buttons on your MIDI device...")
        for msg in inport:
            if msg.type == 'control_change':
                print(f"Control number: {msg.control}, Value: {msg.value}")

if __name__ == "__main__":
    
    list_midi_ports()
    port_num = int(input("Enter the number of the input port to listen to: "))
    input_port_name = mido.get_input_names()[port_num]
    enumerate_controls(input_port_name)
