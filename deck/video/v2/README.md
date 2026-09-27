# deck/video/v2: the V2 brief and its inputs

Hand Steven this folder's link; the file to give GPT-6 Astra is `ASTRA_PROMPT.md`.

| File | What |
|---|---|
| `ASTRA_PROMPT.md` | The brief for the V2 build: beats, timing, narration, tooling, TTS on the shared GCP project, rules |
| `CARL_BRIEF_RAW.md` | Carl's dictated revisions, verbatim as his dictation app produced them |
| `carl_brief_2026-09-26_2035.flac` | The audio of that dictation (Mentra glasses lane, 10:04), with Steven's replies |
| `CARL_BRIEF_TRANSCRIPT.md`, `carl_brief_2026-09-26_2035.gemini.json` | Re-transcription of the audio: Gemini 3.8 Flash on Vertex, verbatim JSON style, timestamps and tone tags |
| `narrate_vertex.py` | Narration through Gemini 3.8 Live on Vertex in `recruit-hackathon-2026-e` (no API key); tested |
| `vo/` | Two test lines from that script |

The large assets (b-roll, V1 renders and captures, the V1 cut) are AirDropped as `Pik_video_v2_assets/`; put them at `deck/video/_assets/` (git-ignored). Its `MANIFEST.md` lists every file.
