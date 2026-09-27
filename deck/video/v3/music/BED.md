# The music bed (`bed.wav`)

Music: Kosmose Vaikus by Kevin MacLeod, incompetech.com, CC BY 4.0. Carl's pick (Sat Sep 26, ~23:50 PDT); the file is `kosmose_vaikus.m4a` beside this.

- Window: 242.0 s to 338.0 s of the 366 s track, chosen by `music_bed.py` as the flattest 96 s of short-term loudness (std 1.31 LU, max -12.8, mean -15.2, min -18.4 LUFS in the source), so there is no swell under the cut.
- Gain -0.90 dB to -16.0 LUFS integrated (target -16); build_v3.py then multiplies it by the duck envelope (-26 dB under narration, -18 dB in gaps, 2 s fade in, 3 s fade out on the end card).
- Never played here; checked by ffprobe/ebur128 only.

| bed seconds | mean S (LUFS, after gain) | max S |
|---|---|---|
|   0-  8 s |  -17.0 |  -16.0 |
|   8- 16 s |  -14.7 |  -13.7 |
|  16- 24 s |  -14.3 |  -13.7 |
|  24- 32 s |  -14.7 |  -14.3 |
|  32- 40 s |  -15.3 |  -14.7 |
|  40- 48 s |  -15.9 |  -15.4 |
|  48- 56 s |  -16.3 |  -15.7 |
|  56- 64 s |  -17.3 |  -15.9 |
|  64- 72 s |  -17.7 |  -16.6 |
|  72- 80 s |  -16.1 |  -15.6 |
|  80- 88 s |  -16.5 |  -15.5 |
|  88- 96 s |  -17.8 |  -17.3 |
