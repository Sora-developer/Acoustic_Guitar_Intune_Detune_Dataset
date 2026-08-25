# Guitar Notes Dataset

- This dataset consists of arround 446 acoustic guitar notes encompassing every possible note on a standard 6-string guitar up to the 16th fret
- The notes range from D2 being the lowest note, up to Gsharp5 being the highest, with a frequency range of 73.42 hZ to 830.61 hZ
- Each recording is exactly 2 seconds in length at a 44.1 kHz sampling frequency and has been converted to mono format.

## Directory mapping

- intune -> contains recordings of all the notes when the guitar is <i>intune</i>
- detune -> contains recordings of all the notes when the guitar is <i>detuned</i>
- the names of folders inside the above 2 folders are given after the notes(e.g. A2, A3, A4,...)
- what you can interpret from the names A2, A3, A4 and soon?
  1. the first letter of the name (e.g. A, B, E, G) denotes the pitch name
  2. the number preceding the letter denotes the octave to be played
- the notes folders (e.g. A2, A3, A4,....) contain files with name '{note} {f/n} {number}.wav'
  1. An 'f' denotes that the string was plucked with a finger or thumb.
  2. An 'n' denotes that the string was plucked with a nail.
  3. The number at the end is the count of {note}\_{f/n}.

## Dataset Creation

- Used <b>Signature Gogos Guitar</b> with steel strings for the recordings
- The recordings where done in a quiet room with mobile phone
- RecForge II application was used to record
- The recorder was kept at a distance of ~20 to 30cm for every recording
- Audacity was used to further trim, normalize volume and reduce the noise
- Detuned recordings are detuned of about ~5 to 30 cents from the intune ones
