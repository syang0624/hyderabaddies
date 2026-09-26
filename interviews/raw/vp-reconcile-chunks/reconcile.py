import os,sys,re,json
from google import genai
from google.genai import types
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS",os.path.expanduser("~/.config/carl-life-os/gcloud-tmuc/application_default_credentials.json"))
i=int(sys.argv[1]); n=f"{i:02d}"
prev=open(f"chunk_{n}.gemini.json").read()
P=f"""You are reconciling a verbatim transcript of an interview at the Recruit Holdings hackathon (Sep 26 2026, ~00:10-01:22 PDT). Participants: Carl Kho and Steven Yang (hackathon team, English), a Recruit VP / Head of HR Center of Excellence (Japanese + English), and Shion Kuroda (Recruit recruiter, interpreting JA<->EN).

You get TWO time-aligned recordings of the SAME 8-minute window (chunk {i}, offset {i*8}:00 into the meeting):
- AUDIO A: phone voice recorder on the table (primary).
- AUDIO B: smart glasses mic worn by Carl (closer to Carl, different noise).
And a PRIOR single-source transcript of audio A (may contain errors).

Task:
1. Listen to both. Produce the best verbatim transcript, fixing misheard words using whichever source is clearer. Keep fillers.
2. Label speakers: Carl, Steven, VP, Shion, or Unknown (the prior transcript has none or wrong ones; Carl is often misheard as Karl).
3. For every Japanese utterance: keep the original Japanese in "ja" and give a faithful English translation in "en".
4. Where the two sources still disagree or both are unclear, keep the best guess and list it in "uncertain" with both readings.
Timestamps are MM:SS relative to this chunk start.

Output ONLY JSON:
{{"chunk":{i},"segments":[{{"start":"MM:SS","end":"MM:SS","speaker":"...","text":"(English or original speech)","ja":"(only if Japanese)","en":"(translation, only if Japanese)"}}],"uncertain":[{{"at":"MM:SS","reading_a":"...","reading_b":"...","chosen":"..."}}],"corrections_vs_prior":["short notes of meaningful fixes"]}}

PRIOR TRANSCRIPT:
{prev}"""
c=genai.Client(vertexai=True,project="recruit-hackathon-2026-e",location="us",http_options={"base_url":"https://aiplatform.us.rep.googleapis.com"})
parts=[types.Part.from_text(text="AUDIO A (phone):"),types.Part.from_bytes(data=open(f"chunk_{n}.flac","rb").read(),mime_type="audio/flac"),
       types.Part.from_text(text="AUDIO B (glasses):"),types.Part.from_bytes(data=open(f"gl_{n}.flac","rb").read(),mime_type="audio/flac"),P]
for attempt in range(3):
    r=c.models.generate_content(model="gemini-3.8-flash",contents=parts,config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),response_mime_type="application/json",max_output_tokens=65536))
    try: json.loads(r.text); break
    except Exception as e: print(n,"retry",e,file=sys.stderr)
open(f"recon_{n}.json","w").write(r.text); print("wrote",n)
