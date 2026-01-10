# Picked Acoustic XY Instrument Setup

## Create the XY Instrument

1. Open Bitwig Studio
2. Create a new Instrument Track
3. Add XY Instrument device
4. Rename track to "Picked Acoustic XY"

## Set Up Chain A (Bottom-Left: Intimate Fingerpicked)

5. Click chain slot A
6. Add Kontakt 8
7. Load Session Guitarist Picked Acoustic
8. Set articulation to Open (click Open button or send C1 once to lock it)
9. Set Mic to Ribbon
10. Set Mic Distance to Close
11. After Kontakt, add Compressor (2:1 ratio, slow attack)
12. Add EQ (cut 80Hz, boost 3kHz)
13. Add Reverb (small room, 0.8s decay, 20% wet)

## Set Up Chain B (Bottom-Right: Open Strummed)

14. Click chain slot B
15. Add Kontakt 8
16. Load Session Guitarist Picked Acoustic
17. Set articulation to Open
18. Set Mic to Condenser
19. Set Mic Distance to Medium
20. After Kontakt, add Chorus (0.5Hz rate, 15% depth)
21. Add EQ (boost 12kHz for air)
22. Add Reverb (plate, 1.5s decay, 25% wet)

## Set Up Chain C (Top-Left: Muted Percussive)

23. Click chain slot C
24. Add Kontakt 8
25. Load Session Guitarist Picked Acoustic
26. Set articulation to Muted
27. Set Mic to Dynamic
28. Set Mic Distance to Close
29. After Kontakt, add Saturator (tape mode, subtle)
30. Add Transient Shaper (+2dB attack)
31. Add EQ (cut 400Hz, boost 2kHz)
32. Add Delay (80ms slap, 15% wet)

## Set Up Chain D (Top-Right: Flageolet Harmonics)

33. Click chain slot D
34. Add Kontakt 8
35. Load Session Guitarist Picked Acoustic
36. Set articulation to Flageolet
37. Set Mic to Condenser
38. Set Mic Distance to Far
39. After Kontakt, add Chorus (0.3Hz rate, 30% depth)
40. Add Phaser (0.1Hz rate)
41. Add EQ (boost 8kHz shelf)
42. Add Reverb (hall, 3.5s decay, 40% wet)
43. Add Delay (dotted 8th ping pong, 30% wet)

## Add Slow Drift LFO Modulation

44. Click the X knob on XY Instrument
45. Add LFO modulator
46. Set Shape to Sine
47. Set Rate to 16 bars (or 0.026 Hz in free mode)
48. Set Amount to 70%
49. Click the Y knob on XY Instrument
50. Add second LFO modulator
51. Set Shape to Sine
52. Set Rate to 12 bars (or 0.035 Hz in free mode)
53. Set Phase to 90 degrees (25% offset)
54. Set Amount to 70%

## Import Test MIDI

55. Drag picked-acoustic-test.mid onto the track
56. Set transport tempo via OSC or manually (100 BPM for Folk feel)
57. Press play

## XY Layout Reference

```
Y=1  C: Muted      D: Harmonics
Y=0  A: Intimate   B: Strummed
     X=0           X=1
```

## Test MIDI Contents

- 8 bars in Am
- Bars 1-2: Fingerpicked arpeggios (CC1=20)
- Bars 3-4: Rhythmic pattern (CC1=0)
- Bars 5-6: Strummed chords (CC1=30)
- Bars 7-8: High melody (CC1=60)
- No keyswitches (each chain has fixed articulation)
- No tempo (set via transport)
