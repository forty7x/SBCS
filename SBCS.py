import numpy as np
import pygame
import tempfile
import os
import time
from scipy.io.wavfile import write

# Initialize Pygame Mixer to play audio
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# Function to generate a sine wave for a given frequency, amplitude, and phase
def generate_sine_wave(frequency, duration=1, amplitude=1.0, phase=0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(2 * np.pi * frequency * t + phase) * amplitude
    return note

# Function to generate harmonics for a given fundamental frequency
def generate_harmonics(fundamental_freq, num_harmonics=8, sample_rate=44100, duration=1):
    harmonics = np.zeros(int(sample_rate * duration))
    for n in range(1, num_harmonics + 1):
        amplitude = 1.0 / n  # Simple amplitude decay; customize as needed
        harmonic_freq = fundamental_freq * n
        harmonics += generate_sine_wave(harmonic_freq, duration, amplitude, sample_rate=sample_rate)
    return harmonics

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Function to convert note names to frequencies using the A440 tuning standard
def note_to_frequency(note):
    note_frequencies = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
        'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
        'A#': 466.16, 'B': 493.88
    }
    return note_frequencies.get(note, 0)

# Function to play a single sine wave note without harmonics
def play_single_note(frequency, duration=1):
    sample_rate = 44100
    note = generate_sine_wave(frequency, duration, sample_rate=sample_rate)
    note = np.int16((note / np.max(np.abs(note))) * 32767)

    temp_file_name = tempfile.mktemp(suffix='.wav', dir='.')
    write(temp_file_name, sample_rate, note)
    sound = pygame.mixer.Sound(temp_file_name)
    sound.play()
    time.sleep(duration + 0.1)

    os.remove(temp_file_name)

# Function adjusted to play a single note with harmonics using additive synthesis
def play_note_with_harmonics(frequency, duration=1):
    sample_rate = 44100
    note = generate_harmonics(frequency, sample_rate=sample_rate, duration=duration)
    note = np.int16((note / np.max(np.abs(note))) * 32767)

    temp_file_name = tempfile.mktemp(suffix='.wav', dir='.')
    write(temp_file_name, sample_rate, note)
    sound = pygame.mixer.Sound(temp_file_name)
    sound.play()
    time.sleep(duration + 0.1)

    os.remove(temp_file_name)

# This function will help me play a chord based on the notes and specified duration for how long 
# it should play
def play_chord(notes, duration=1):
    sample_rate = 44100
    chord = np.zeros(int(sample_rate * duration))
    for frequency in notes:
        sine_wave = generate_sine_wave(frequency, duration, sample_rate)
        chord += sine_wave
    # Normalize to prevent clipping
    chord = np.int16((chord / np.max(np.abs(chord))) * 32767)

    # Generate a temporary filename in the current directory
    temp_file_name = tempfile.mktemp(suffix='.wav', dir='.')
    write(temp_file_name, sample_rate, chord)
    sound = pygame.mixer.Sound(temp_file_name)
    sound.play()
    # Wait for the chord to finish playing because sometimes the program would end before
    # playing the entirety of the chord
    time.sleep(duration + 0.1)  
    
    # Cleanup
    os.remove(temp_file_name)



def select_chord():
    print("Select a root note for your chord:")
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}")

    note_selection = int(input("Enter the number of your chosen note: ")) - 1
    root_note = notes[note_selection]

    print("\nChoose the type of chord scale:")
    scales = ['Major', 'Minor']
    for i, scale in enumerate(scales, start=1):
        print(f"{i}. {scale}")

    scale_selection = int(input("Enter the number for Major or Minor scale: "))
    chord_scale = 'major' if scale_selection == 1 else 'minor'

    print(f"\nGenerating and playing the {chord_scale} chord for {root_note}...\n")
    generate_and_play_chord(root_note, chord_scale)

# Demo function to play both versions of a note for comparison
def demo_note_versions():
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}")

    note_selection = int(input("Enter the number of your chosen note: ")) - 1
    selected_note = notes[note_selection]
    frequency = note_to_frequency(selected_note)

    print(f"Demoing the note {selected_note} without harmonics.")
    play_single_note(frequency, duration=2)

    print(f"Demoing the note {selected_note} with harmonics.")
    play_note_with_harmonics(frequency, duration=2)

# Function will play the given chord by playing the notes together depending on the 
# chosen scale: minor/major
def generate_and_play_chord(root_note, chord_type='major'):
    if chord_type == 'major':
        intervals = [0, 4, 7] 
    else:
        intervals = [0, 3, 7]
    note_frequencies = [note_to_frequency(root_note)]
    
    for interval in intervals[1:]:
        next_note_index = notes.index(root_note) + interval
        next_note_name = notes[next_note_index % len(notes)]
        next_note_frequency = note_to_frequency(next_note_name)
        note_frequencies.append(next_note_frequency)
    
    play_chord(note_frequencies, duration=2)


# Interactible menu to select a chord or demo note versions
def main_menu():
    print("Welcome to the Chord Synthesizer!")
    print("1. Select a chord")
    print("2. Demo a single note with and without harmonics")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        select_chord()
    elif choice == '2':
        demo_note_versions()
    else:
        print("Invalid choice, please enter 1 or 2.")


if __name__ == "__main__":
    while(1):
        main_menu()
