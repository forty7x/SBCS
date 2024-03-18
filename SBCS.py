#SBCS

import numpy as np
import pygame
import tempfile
import os
import time
from scipy.io.wavfile import write

# Initialize Pygame Mixer to play the chords wav files
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# This function will hep me create a sine wave for a given note
def generate_sine_wave(frequency, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note

# The notes are all from the chromatic scale and the chords will be based on them
def note_to_frequency(note):
    
    note_frequencies = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
        'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
        'A#': 466.16, 'B': 493.88
    }
    return note_frequencies.get(note, 0)

# Utility functions to make  note conversions simpler
# These functions convert between note names and their indices in a chromatic scale:
def note_to_index(note):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes.index(note)

def index_to_note(index):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[index % len(notes)]


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
    # Wait for the chord to finish playing because I noticed program would end before
    # playing the entirety of the chord
    time.sleep(duration + 0.1)  
    
    # Cleanup
    os.remove(temp_file_name)



def generate_and_play_chord(root_note, chord_type='major'):
    # Define intervals for major and minor chords
    # 3,2 for major chords and 2,3 for minor chords
    if chord_type == 'major':
        intervals = [0, 4, 7]

    else:
        intervals = [0, 3, 7]
    note_frequencies = [note_to_frequency(root_note)]

    for interval in intervals[1:]:
         # Calculate the index of the next note
        next_note_index = note_to_index(root_note) + interval
        # Convert the index back to a note name
        next_note_name = index_to_note(next_note_index)
        # Find the frequency of this note and add it to the list
        next_note_frequency = note_to_frequency(next_note_name)
        note_frequencies.append(next_note_frequency)
    play_chord(note_frequencies, duration=2)


def note_to_frequency(note):
    
    note_frequencies = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
        'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
        'A#': 466.16, 'B': 493.88
    }
    return note_frequencies.get(note, 0)

# This function willl synthesize and play a chord based on the specified root note and chord type
def generate_and_play_chord(root_note, chord_type='major'):
    intervals = [0, 4, 7] if chord_type == 'major' else [0, 3, 7]
    note_frequencies = [note_to_frequency(root_note)]

    for interval in intervals[1:]:
         # Calculate the index of the next note
        next_note_index = note_to_index(root_note) + interval
        # Convert the index back to a note name
        next_note_name = index_to_note(next_note_index)
        # Find the frequency of this note and add it to the list
        next_note_frequency = note_to_frequency(next_note_name)
        note_frequencies.append(next_note_frequency)
    play_chord(note_frequencies, duration=2)



#generate_and_play_chord('D', 'major')

# Interactible menu to select a chord based on the major or minor scales
def main_menu():
    print("Welcome to the Chord Synthesizer!")
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
    if scale_selection == 1:
        chord_scale = 'major' 
    else :
        chord_scale = 'minor' 

    # Now, synthesize and play the selected chord based on the major/minor scale
    print(f"\nGenerating and playing the {chord_scale} chord for {root_note}...\n")
    generate_and_play_chord(root_note, chord_scale)

if __name__ == "__main__":
    main_menu()