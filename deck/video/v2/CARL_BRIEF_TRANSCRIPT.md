# Carl's V2 brief, re-transcribed (Gemini 3.8 Flash on Vertex, verbatim JSON style)

Audio: `carl_brief_2026-09-26_2035.flac` (10:04), cut from the Mentra glasses lane, Sat Sep 26 2026 ~20:35 to ~20:45 PDT, at the hackathon venue (DG717). Speaker: Carl, dictating to Claude with Steven beside him; Steven's replies are on the tape too (the thesis restatement at ~02:00 is Steven's). Raw model output with timestamps and tone tags: `carl_brief_2026-09-26_2035.gemini.json`. The dictation as Claude received it (Carl's dictation app's text) is `CARL_BRIEF_RAW.md`; where the two differ, trust the audio.

## Summary (model's)

In this recording, a speaker outlines detailed revisions and structural requirements for creating version two (V2) of a 90-second product demo video featuring an AI system called 'Meet Pick' and GPT-6 Astra. While discussing the project with a colleague in a bustling public area with noticeable background chatter, the speaker walks through each slide and scene of the presentation, emphasizing team formation, dynamic task forces, UI animation adjustments, and integration with platforms like Slack and Gmail. The speaker instructs how to package the prompt, handle video assets to avoid GitHub file size constraints, configure Cloud Platform (GCP) resources, and utilize text-to-speech audio, all aimed at delivering a cleaner, narrative-driven pitch presentation.

## Segments

| start | end | text | tone |
|---|---|---|---|
| 00:00 | 00:15 | [throat-clearing] [ambient: background chatter] I'm going to be giving the task of creating V2 iteration of the video to GPT-6 Astra. Which effort should we use for this one? And, more importantly, here are my revisions for V2. | focused |
| 00:15 | 00:30 | And, we're still doing it 90 seconds. For a demo video, should be self-explanatory, and it should, um, speak a bit faster now. So, the first slide is like, the line is blurring. It, oh, also, | instructional |
| 00:30 | 00:46 | omit the videos I've downloaded, so you don't have to redownload again, and then be very specific with instructions. So, the first slide is like, the lines are blurring between the, uh, [ambient: background chatter] | matter-of-fact |
| 00:46 | 01:03 | between what one person can do in a post-LLM world. We've asked, maybe this is the part where we add in photos, or not even photos. We just ask like recruits, we asked people around Recruit Holdings for what their biggest problems in HR is, and then something about team mobility, | brainstorming |
| 01:03 | 01:19 | uh, internal mobility, and team formation, and how that's a very complicated problem. Bring context from the meeting with you as you make decisions for this video, because I am braindead to even think about that shit. | exhausted |
| 01:19 | 01:34 | Anyway, I want you to not, maybe not use these videos, but I appreciate the fact that Claude implemented the slide up with masking text animation, | evaluative |
| 01:34 | 01:47 | but what I want to emphasize here is like the whole, "Who is the best person for X, Y, and Z?" These are stuff I made up on a whim, and I actually want this to advance our thesis even more. What our thesis was? You figure it out. [laughter] | amused |
| 01:47 | 01:54 | No, like, uh, what was our thesis again? | inquisitive |
| 01:54 | 01:56 | In terms of? | casual |
| 01:56 | 01:58 | Like, um, | hesitant |
| 01:58 | 02:08 | team formation. Oh, that that, basically, that because of the AI, the um, the boundaries of the roles will be removed, like will be destroyed. So like, even the software engineers can like, you know, do something like outside the software engineering field, HR can do software engineering, too, | explanatory |
| 02:08 | 02:18 | because like we're just using AI. So, what we're going to do is like, instead of just like having a fixed team for just like doing certain tasks, it's more like uh for each task every task has like a different task force or something. | explanatory |
| 02:18 | 02:30 | Task-task force specific. But thanks for putting that concisely. [chuckle] Uh, yeah. So, make sure that every example we have and every use case we showcase reinforces the mission. | affirming |
| 02:30 | 02:46 | So, "Who is the best person for?" You've kind of nailed it. Not sure about the video choices, but you do you. And then after that we do the Meet Pick. I like the animation, "The company intelligence that works wherever you are." We are not sure about this phrase. | critical |
| 02:46 | 02:54 | So, given the mission, and given the interviews, um, make a better one. | direct |
| 02:54 | 03:10 | And then have Meet Pick, um, extend its antenna to pull in the Slack UI. And I'm going to be chopping off the Slack UI actually. So like, the table you see, the reactions, the name, even the profile channel gets sucked in and is replaced with just the black thing. | descriptive |
| 03:10 | 03:26 | Because I think that makes it very clear and reduces visual clutter. So, "What else can I learn about Adachi-san?" To emphasize text changes, make use the typewriter, in effect. And then, do a little jump. | instructive |
| 03:26 | 03:41 | And then, the scene changes into Gmail, which, I'm not sure if this is the best UI for it. Maybe I should just show sent messages, or simulate that. But what we're trying to see here is plus info on Adachi's recent, | reflective |
| 03:41 | 03:57 | on Adachi's emails. Adachi-san's emails, and then make a little remark based on what you think helps reinforce, how it, uh, reinforces our thesis. What I'm thinking about right now is something along the lines of, | brainstorming |
| 03:57 | 04:14 | "Oh, cool. She cares about English, or expanding the team, or construction." I really don't know. Again, the construction example is placeholder. We can talk about talent acquisition, because it's more on theme, and especially, our judges. | deliberative |
| 04:14 | 04:29 | Then, Kirby sucks them out again. I'm going to cut out, um, the header, the name, and the body text of the email. And then, we can make another plus, and then, "I see. So she does, also does X, Y, and Z." And then with said information, Pick can help a team. | instructive |
| 04:29 | 04:47 | Now, the You- This is the Meet integration UI. We have changed the UI to be a more dense, network graph-based thing. And so, | serious |
| 04:47 | 05:03 | what I want you to do, which is what I've instructed the new UI change to do, and actually, Steven's going to be pushing a new version of the UI that tells a story for these, um, for the different orders in where, in which we are displaying them. | informative |
| 05:03 | 05:19 | [ambient: background chatter] So, so make sure that fits into the theme, and for the Meet, we actually, we actually want to | thoughtful |
| 05:19 | 05:35 | do a live demo. And as I've said, the, for the live demo, it's hard-coded, and actually it's going to be a share screen of a video that's playing, and we just time it, we time to speak when the video fosters something up, to make it seem like magic. | scheming |
| 05:35 | 05:48 | And that's like separate from the actual demo. You get what I'm trying to say? So there's just giving me that. Cool. And then, um, and then for the "See who's best fit to lead the team," | collaborative |
| 05:48 | 06:05 | Slack, uh, I think we can do better for this one. Maybe add a bit more UI elements from Slack. I'll let you- I'll leave you to it. And then organizing the Recruit hackathon, | suggestive |
| 06:05 | 06:21 | again, these are examples. If there are better scenarios, take over. I encourage you, cuz I don't think I'm convinced by this. But what I want you to do, as well, is for the UI refresh, is use your Figma skills to actually build out a replica of what seems to be Jira, Notion, Linear, and then, | direct |
| 06:21 | 06:36 | I want the AI feature to sort of highlight itself after, like you, like the name of the brief and the tasks are like typed in, and then it's like, | descriptive |
| 06:36 | 06:51 | in like its assignees, specifically for the UI refresh where it would be sitting, is the labels page. And then for task like assignees, and then it would, the drop-down would open itself and select, | precise |
| 06:51 | 07:07 | and then, there is a button, a tool tip with a question mark, that then explains why with the receipts UI that we have, albeit, [sigh] more mini version. And then after that, we actually have the second dashboard screening, | detailed |
| 07:07 | 07:18 | that I think it's better if the story is tailored towards how this could be extended to other industries. Like, what were your examples again? Hospitals? | curious |
| 07:18 | 07:29 | Hospitals, airlines. Like in hospitals for like the surgeons, airlines for the pilots, and more like lots of vertical that you could think of. | helpful |
| 07:29 | 07:44 | Yep, okay, so other verticals, basically. And then we end with a splash. So, I'll just wait for your UltraCode to finish. And then, | patient |
| 07:44 | 07:48 | and then you can You might not able to send that large file through UltraCode. | cautious |
| 07:48 | 07:54 | Oh, okay. No, it's fine. I'm going to [laughter] email me? I'm thinking of, um, pushing this to GitHub, actually. | amused |
| 07:54 | 07:59 | Just like, it's going to package itself, along with the videos. Okay. | matter-of-fact |
| 07:59 | 08:14 | So basically once that once that UltraCode is like ready, that means like, you know, we have the UI dashboard that's going to like get back to living. Yeah, and then like, make the new video. Is G [ambient: background chatter] | coordinating |
| 08:14 | 08:29 | [ambient: background chatter] | silent |
| 08:29 | 08:44 | Okay, that was my prompt. Now I want you to upload the raw version of this prompt, and, um, transcribe it again, which I may flash transcribe the audio, | instructive |
| 08:44 | 08:59 | into GitHub, into video, maybe directory video or deck video V2, and just surface the link so I can just give it to Stephen. Once this UltraCode is Uh, once this, um, yeah, table 5.1 UltraCode is ready, cuz it's going to be using GPT-6 Astra, to, | planning |
| 08:59 | 09:14 | specifically use computer use and Figma MCP, whichever is the best, to make a better version of this video. And, | focused |
| 09:14 | 09:30 | also, upload the videos, or at least proxy links to it. I'm not sure if I should just like, oh, maybe, I think I have a better idea. I'm going to be, to avoid GitHub large storage, | problem-solving |
| 09:30 | 09:44 | I'm going to be AirDropping him the videos. Just package the folder neatly, and then make sure your prompt for Astra references said folder so all the videos are in there. And then, | practical |
| 09:44 | 09:54 | not sure Um, also, did you set up Did you set up the GCP? To be like accessible by a computer? Yeah, yeah. I did, I did. [ambient: background chatter] | inquiring |
| 09:54 | 10:04 | Since we have the same GCP, we're in the same GCP group, um, that Recruit Holdings allocated to us, have him actually, uh, have the model also use TTS for the demo video. | concluding |
