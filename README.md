# SBCS
Sample-Based Chord Synthesizer


SBCS is a program that is primarily based on chord synthesis and additive synthesis. It can synthesize chords by playing different notes together using either the major or minor scales. This program is fully interactive as it has a menu to control everything related to its functionality. It is built in python and uses the numpy library for numerical operations and pygame library for audio wav file playback. 

### How it works

So the two major functions are the chord synthesizer and the additive synthesizer:
- The chord generation works by first selecting a root note then chord type. Then the program will pick the corresponding notes' frequencies depending on what scale is chosen next.These frequencies are from the A440 pitch standard. Then the program will synthesize these chords and play them together to form a chord. The resulting wav file will be created as a temporary file and then immediately deleted after playback is done.

- The second feature is the additive synthesizer. The program demonstrates this by using harmonics. It will show the difference between a single note sound with and without harmonics. In the first case, it will be playing a single note as a pure sine wave, then again play the same note but using harmonics. This is done by using a decay function of 1/n as default when n is the current harmonic number. The user can switch different decay functions like linear, exponential and inverse to hear their difference. This means that each successive harmonic will be quieter than the last one. After adding all these up, the resulting sound will be a much more rich sound than just a simple sine wave. 

### What worked well
The chord synthesizer works really well and produces clear sounds with recognizable chords. The user interaction works well with the program too. It kind of works like a control panel with the functionality of adjusting everything from the main menu. 

### Challenges and Limitations
As expected, due to time constraints, the original idea was too complicated for the time alloted. But I have implemented the two most important features according to the TA notes on my project proposal. The chord synthesizer using additive synthesis. Another idea I had was to synthesize real word instrument sounds like guitar but again I wasnt able due to lack of time. I would like to implement these features in the future and be able to play realisitc sounding instrument sounds.



