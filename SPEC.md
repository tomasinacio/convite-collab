# SPEC: the user's exact requirements

Source of truth for `spec-guardian`. Quoted verbatim (typos kept), in the order given, from the chat of 2026-11-09. Nothing below is paraphrased except the "Derived" section, which is marked.

## Verbatim

<!-- vale off -->
### Message 1

> I want to make a dynamic wedding invitation. I want it to look like a lightly decorated whit closed envelope that when the first touch occurs it opens. As it does opn I want some drawyins, maybe wtercolors or something to slowly and elegantly be drawn in real time. I already have the website built, jsut need this one thing. It must be accessible to all 150 guests.

### Message 2

> And colors shoudl maybe be pastel, baije, greenish, light brown, but summery, maybe like suuthern Italy/portugal mediterranean campestre vibes

### Message 3

> Remember you are to focus solely on the actual face of the invitation. Not the website as a whole

### Message 4

> Definetly implement:
> Taste Skill
> Vercel web-design-guidelines (thought we had it already)
> Qwen-Image-Layered
> the best of -> Rive, SVGator and Lottie Creator
> Emil Kowalski's animation skills
>
> for image generation, ideally free. But that don't look super AI generated. Maybe even different assets in the same style one creation at a time and then just use the asset in question extracted from each picture.
>
> Also we can use openrouter and or omniroute for any free models that do this.
>
> And also you can control my pc to use my copilot app though the pc mcp to control it and write there and download and manage this shit

### Message 5

> Add the stuff to agent-config of course. If you think an agentic pipeline is better than jsut any individual skill, plan it as such.

### Message 6

> ANd remember like in the claude md or like a subagents.md actually, that actual artwork and the aesthetic part of design should be done by an opus 5.5 high agent. As it is much much better than sonnet

### Message 7

> Don't be stingy. As I said I will wnat you to have access to, and actually use at least: Taste Skill, Vercel web-design-guidelines (thought we had it already), Qwen-Image-Layered, the best of -> Rive, SVGator and Lottie Creator, Emil Kowalski's animation skills. So please build it so that when I use this folder (or a specific subfolder just for this project if you think it's better) to sactually work on this invite

### Message 8

> Actually think of the best approach for how I should work on this, so these tools I mentioned, plus any others you think relevant, in a scenario where they would actually be employed, in a specialized new folde you can create for this project, with appropriate scafolding. ANd best models and shit. All super optimized like an super advance web designer master using AI for this prcise purpose.
>
> ANd then you build it.
>
> ANd make sure above all that you can use the copilot to generate photos too. Link any free image creation models too if you want for when copiulot ends the credits.
>
> So if needed, research more, than plan and then build it. I will go to bed now but I expect this to be perfect when I wake up and functional so that I can start work right away.
>
> If you want, create a subagent now from this prompt so in the end when you finish all your work he will be looking for this exact specifications I am giving now, so you can correct in case you diverge. Basically he will be my eyes and enforce this prompt.

### Message 9

> ANd yeah contain this to it's own folder so no need for all these skills in normal /agents-config use

### Message 10

> And of course don't just anchor on my shti. I am no web designer. Also think of how they would tackle this. Like maybe there are specific plsces for inspirstion and or free assets, or even google stuff and cut from google images. Thst kinds stuff. Research hoe a top notch web designer would approach this and also complement what I said with that.
>
> But vomplement. Not substitute

### Message 11

> And test ylu do with pictures gemerated are ok, and fon't need to be suepr ellaborate. But the definition cannot be super grainy, ai sloppish and or crappy overall. So keep thst in mind. Tests must actuslly servr their purpose

### Message 12

> Out names are Maya e Tomás btw. And if you think it's good. After finished ankther clean slate ppus agent could receive the presentstion I gave you and the invitstion fsce and red team it. See where it diverges. If i's super contrastant and if it is too all over the palce. Stuff like that. As the invite should be clean and elegant, get it? And then he gives you feedback and the designer opus choose what to implement from that feedback. Makes sense?
> And keep in mind you should only work on the invitstion opening up and bottom. Not envelope style or side opening. So that people can then scroll down

### Messages of 2026-11-10 (same rules: verbatim, in the order given)

### Message 13

> Facts: the couple are Maya e Tomás. Date and place are not decided yet, keep them as TODO(user). The opening is vertical only: the flap opens up and the invitation continues down so people scroll. No side opening.

### Message 14

> Rules: artwork and every aesthetic decision go to an Opus 5.5 agent at high effort. The invite must be clean and elegant, not contrasty or all over the place.

### Message 15

> My reference examples will be in references/. Ask me for them before choosing the final direction. Do not start the art pipeline beyond the style tile until I approve it.

### Message 16

> Designer should br opus using the skills we added od course

### Message 17

> Don't forget and this should be durable and frequently implemented. Regarding design. Always ask me using the claude ui otpions whsr I want/prefer

### Message 18

> You never design btw. Always opus

### Message 19

> Bro, check out the presentstion I made. Focus on it. Try to come as close to it as possible

### Message 20

> Folded paper vertically with wax seal thst is opened upon touch

### Message 21

> Do some experimenting. Create an html with concepts and I'll choose. At least 2 when you sre unsure. I am not a web designer so I do not know how to answrr this without visuals

### Message 22

> Ideally the tomás maya part would not solely have letters. Bur also some animations.
>
> And altough the style fo the animations is good, everything is still kinda janky, don't know if this is just the rpototype and you will add more stuff

### Message 23

> Not just the nsmes themselves. But the overall block of the page whete the nsmes are. Like around them. Not super dense but more lively I guess

### Message 24

> Date is 10 of July
> Place is Quinta do agrilo, Milharado
>
> Don't know qhat mongram is.
>
> I have this is from the quinta. If you are able to reproduce it digitally but super close to tjis.
>
> Also you cn have some blue azulejo details. Make som concepts of this. And your htlm is good but maybe much less plain text and more proof of concepts ideas

(The photo with that last message is saved as `references/quinta-do-grilo-sign.jpg`: a yellow wall with a blue azulejo plaque reading "Quinta do Grilo". The date and place above replace "not decided yet" from the first message of this list. The year is not given.)

### Message 25

> I wanna see both of those examples seperstely

(Said of the azulejo details B4, the plaque closing the invitation, and B3, the tile lining under the lifting panel, chosen from the concepts page; it also picked the date style set as on the sign, D3.)

### Message 26

> Monograms is worst than just names i thibk. Maybe no need for it

### Message 27

> And I was thinking 2 folds. On on top and one in the bottom. But look for inspiration online and see how this is usually done. Like similar concepts

(Chosen from the fold concepts page: concept 2, the top lifts then the bottom drops.)

### Message 28

> You azulejo looks super super crappy. Dont know if just prototype or actuslly bad. But for it to work it must be pretty. So just make an jtm to make sure you get it right. Buth the azulejo details but also the quinta do grilo. Not prototype, actusl reafy level I guess

### Message 29

> Cant get sharper but you can increase resolution

(Said of the plaque photo.)

### Message 30

> And regarsing the main openijg. Super cool, most suff but the bottom part has aninations allover the place. Like thr drawings. Maybe stsrt to consolidste this too

### Message 31

> You csn research for similar examples, of course. Espcially examples where the blue azulejo is somehow mixed with some vegetstion elegantly. For example the names could themselves be in an azulejo panel. Like several tiles. Msybe the Quinta do Grilo as it shows in the picture but slightly smallet in comparison to the names

### Messages of 2026-11-12 about the RSVP (same rules: verbatim, in the order given)

### Message 32

> What I want: the guests (about 150, sent one by one on WhatsApp, in pt-PT, en and es) answer from the invitation page, and Maya and I can see the answers easily on our phones. Every technical decision is yours to make and solve, not mine: pick the backend (GitHub Pages cannot run server code; the earlier idea was Cloudflare Pages Functions plus D1, but a Google Sheet or Supabase are options; choose what is simplest, free, safe for 150 guests and easy for two non-developers to read), how a guest is identified (the plan is a personal link per family with a private code, so the form already knows the family and how many seats), the fields (default: yes or no per person, food needs and allergies, optional message), the deadline, spam and privacy handling, and the data layout. Decide with a short written recommendation and the trade-offs, then go. Come back to me only for what only I can do or decide: creating or logging into any account (never create one, never read or type credentials; stop and tell me exactly which login and which steps), the RSVP wording, the guest list, and the visual choice of the form.

### Message 33

> I actually want you to pur a swarm of resesrcher agents researching what the best pravitces compatible with our ecosystem are. Ideally free of course. Then present me a plan for the "pipeline/stack"
>
> Only then will wr think of implementstion anf skills and tools, etc...
> Don't I need to approve the plan?

### Message 34

> Did you keep in mind that we want something more local and above all free and that we can use however we find it best?

### Message 35

> I want this to fill and excel file which has eberything such as the the guests and all other stuff

(Answer to how the couple want to hear about new answers. The same reply picked hybrid hosting, a free Cloudflare receiver with the couple's own machine as the real copy.)

### Message 36

> Bro check these examples and make your suggestions based on theirs: <https://www.thedigitalyes.com/demo/nautical>
>
> <https://www.thedigitalyes.com/demo/dolce-vita>
>
> <https://www.thedigitalyes.com/demo/mediterranean-edition>
>
> <https://www.thedigitalyes.com/demo/secret-garden>
>
> <https://www.thedigitalyes.com/demo/floral>

(Answer to how guests should give food needs and allergies.)

### Message 37

> Good plan. However super super importsnt. Put a swarm of free agents resesrching the best skills and tools and subagents.md for this specific type of work and add rhem to the folder where you will be working from

### Message 38

> Make sure to use the examples I gave you as gold standsrd state od the art references. The stuff they have, how ghry are structularly organized, aesthetics (especiaply dolce vita). Anfd try to adapt our aesthetics and shit to this

### Message 39

> Adress: <https://maps.app.goo.gl/7gWufo1vMswyDxfbA?g_st=ac>
>
> Ask me what other informstion you may need from me

(The venue map link, for the location card. Wording: `TODO(user)`.)

### Message 40

> You csn fake all data you don't have to test. Just make sure to mark it as such somehow so I know all I have to replace

(Rule: every invented test value is marked `FAKE` in the file and listed in `rsvp/REPLACE-ME.md`.)

### Message 41

> You can remove fechar e ver de novo.
>
> Timings are kinda off. Evertthing taks too long to appear I thinkm like the plants and shit  and the leaf falling
>
> And compared to the examoles I thi k it is missing a lot of stuff. Like a really big chunk of stuff no?
>
> And the point of the grapes and shit was to have relevamt information in the middle.
>
> I think this is really light compared to whst it should be.
>
> And please keep with the aesthetic. Make sure the opus designer maintains it.
>
> And the paper kinds chsnges color frombthe first part to the 2nd. Overall this ishawty work. Have you been using the reviewer tools for this work?

### Message 42

> Sections wanted: Countdown, Location and map, Schedule of the day, Dress code, "And the link to add to calendar". Also: Gifts, FAQ. "For gifts we mostly want money so see portuguese wedding invitation references thst have ghe IBAN. Here is ours PT50 0023 0000 4582 0590 0509 4". Layout: no preference. Opening time: about 5 seconds.

(The IBAN is the couple's own, given on purpose to be shown to guests. Account holder name: `TODO(user)`.)

### Message 43 (cost)

> Why 3 concepts man? We are ri h now? Didn't get the memo. Since when dow e have infinite tokens?
>
> I mean, aproveita what he already did I guess. But br more conservativr

### Message 44 (no repeats)

> And makr sure not to repeat several times stufd such as dates, locations, etc...

### Message 45

> And ehy is there repeated shit everywhrre? Like the date and locstion. I gave you the fucking heads up man. Chek the ehads up I gave you in the messages as you clrsrly ignored some. And ask me stuff you thi k I might know.
>
> And really try to keep the fucking aesthetics coherent. Create an occasional red tram made to find inconsistrncies of aesthetics, color, repetitions, this kinda shit.

### Message 46

> Make sure to use aesthetically similar and beautiful assets across the presrntstion. Shit like bees, tree trunks, mushrooms (emphasis on mushrooms).
>
> Like stuff coming from the sides. More things like flying bees, falling leaves, wind oseilating leaves and brsnces,  etc...
>
> Make it feel alive and beautiful. Give me prompts for what the opus designer feels would be nice additions to keep the aesthetics pleasing and similsr to the beggining

### Message 47

> The azulejos you added are really super chrap looking. Not the half realistic half handrawn hald watercolor vibe we hsve been going for.
>
> You csn keep like one or tw. Maybe the small center one.
>
> A rodapé (research for inspirstion for this, i think we already have some azulejos resrsrch). Anf maybe a bigger plaque that csn contsin informstion. A,ulejo too kinda likrethe same style as tomád and maya, liek maybe in the space in grapes panel/are

(Also from the user: "Can add rocks too of course", for the new painted assets.)

### Message 48

> Just like also see if you need to make more sesrcher agents to research shit based on whst zi just said. And mske sure you register each observstion so they sre not lost

### Message 49

> Give me the ui anser thing for open answer when you need them. Not a giant ass fuvking message for me toa nswer to

### Message 50

> And another long term olsn. Csn be one of the finsl things.
>
> Specifically for Pedro Rodrigues. Put it in the bscklog. For his specifically I want his invite to be invaded by shreks. Like dsncing shreks, ugly shreks, rtc... we'll think of this muvh later once everything is basicslly finished snd srt up

### Message 51

> I like these mushrooms too btw. Also some mroe wild flowers would be nice. Ideally nativ eto portugal
>
> (three mushroom pictures attached, saved in `references/inspiration/mushrooms/`)

### Message 52

> Use the better copilot model for the image generstion
> And summer

### Message 53

> Not spexificslly those btw, but laike kinda those formats/species. You csn vary colors and style to match our mood of course
> Also you can add one of those tied together hot pepper bunches common in rural portugal

### Message 54

> I think the images may be a tiny slightly bit too Ai slop realistic. Maybe a bit morr watercolor/drawing like may be better

### Message 55

> Actually finish aht you are working on and then stop. Basically my girlfriend has already set up most of the website infrastructure for the RSVP. SO I want to merge our frontpage and what we have with hers. So fior now focus only on the actual aesthetics of the invitation. We'll deal with merging the backend stuff later

<!-- vale on -->

## Derived (decisions made earlier in the research chat; not verbatim)

- Tap a labelled wax seal to open; 8 to 12 s; plays once; Skip button; reduced-motion and weak-phone fallback is a fade.
- Personalised link per guest and family; sent individually on WhatsApp; languages Portuguese (PT-PT), English, Spanish.
- Art: ink line art draws, then watercolor washes bloom; flowers and foliage, monogram or names, a scene or landmark.
- Palette: paper `#F6EFDF`, sand `#E6D6B8`, ink `#3B2F25`, deep olive `#4F5F2E`, terracotta `#9A4C32`, brown `#6B4F34`, sage `#9DAE82`, twine `#B8946A`, clay `#C98B6B`, lemon `#EBDDA0`, `azulejo` `#7F9BA8`. Text pairs must reach 4.5:1.

## Requirement list the guardian checks

| ID | Requirement | Pass when |
| --- | --- | --- |
| R1 | Taste Skill installed and used | `.claude/skills/design-taste-frontend/SKILL.md` resolves; a pipeline stage names it |
| R2 | Vercel web-design-guidelines usable | `.claude/skills/web-design-guidelines/SKILL.md` reads a local rules file that exists |
| R3 | Qwen-Image-Layered usable | `scripts/qwen_layers.py` exists, venv has `gradio_client`, route documented with its limits |
| R4 | Best of Rive, `SVGator`, Lottie Creator picked by use | `motion-authoring` skill plus `motion/BAKEOFF.md` scaffold |
| R5 | Emil `Kowalski` skills present | 8 skills resolve under `.claude/skills/` |
| R6 | Free image generation, not AI-looking, one asset per image, extraction | `asset-factory` skill, `scripts/free_image.py`, `scripts/extract_asset.py`, look rules |
| R7 | Copilot app via the PC MCP generates images, with free fallbacks | `copilot-image` skill, `desk` path documented with its real status, 2+ free routes in `free_image.py` |
| R8 | OpenRouter or OmniRoute route linked | a route in `free_image.py` and `asset-factory` |
| R9 | Opus 5.5 high for artwork and aesthetic design | stated in project `CLAUDE.md` and the pipeline skill |
| R10 | Agentic pipeline, planned and scaffolded | `illustrated-reveal` skill with stages, owners, gates; folders and seed docs exist |
| R11 | Contained in its own folder | no new or changed files under `shared/`, `~/.claude`, `~/.config/opencode` from this work |
| R12 | Functional on waking | `scripts/doctor.sh` runs; `README.md` quick start; every FAIL listed with a fix |
| R13 | Face of the invitation only | no site-wide design work in the pipeline |
| R15 | A top designer's approach complements (does not replace) the user's tools | `designer-playbook` skill: references, style tile, sourcing order, Google Images rule, free asset sources; ranks AI as one source among several |
| R16 | Test images are good quality: not grainy, not AI-sloppy, not crappy; tests prove something | `scripts/image_quality.py --selftest` passes with correct verdicts; end-to-end test used a real scan; the free keyless route is labelled concept-only |
| R17 | The couple's names are Maya e Tomás; no other copy invented | names appear as Maya and Tomás (`e` in Portuguese); the date is 10 July and the place `Quinta do Grilo`, `Milharado` (user, 2026-11-10); no monogram (user, 2026-11-10); year and opening line stay `TODO(user)` |
| R20 | The `Quinta do Grilo` `azulejo` plaque is reproduced digitally, as close as possible to the user's photo, with blue `azulejo` details, shown as concepts | `references/quinta-do-grilo-sign.jpg` exists; a concepts page shows the plaque and `azulejo` details; the designer is Opus |
| R21 | Concept pages are visual: little plain text, more proof-of-concept ideas | pages are mostly live demos and drawings with short labels |
| R22 | The `azulejo` work is finished quality, not prototype; the names may sit in a multi-tile `azulejo` panel mixed with vegetation, and the `Quinta do Grilo` plaque is slightly smaller than the names | `comps/azulejo-lab.html` shows names panel plus plaque compositions beside the user's photo; traced from the photo, logged in `assets/LOG.md`; the designer is Opus |
| R23 | Two folds, one at the top and one at the bottom, vertical only; the lower part of the page animates as one choreographed sequence | the tile opens top then bottom; `comps/MOTION-NOTES.md` has the timeline |
| R18 | Red team loop | a clean-slate Opus agent reviews the face against the brief only (divergence, contrast, visual noise, clean and elegant), then the designer Opus decides what to apply; both recorded in `comps/REDTEAM.md` |
| R19 | Opening is up and down only | flap opens upward and the invitation continues downward so guests scroll; no side opening, no card sliding out sideways |
| R14 | Repo rules followed | rulebook commands run on changed files; `INDEX.md` fresh; map check status reported honestly |
| R24 | RSVP backend is free, local-first and proven by tests (M32, M34) | `rsvp/PLAN.md` states the choice; `node --test` in `rsvp/worker` is green and covers: valid answer stored, changed answer updates, wrong or missing code refused, duplicates, floods, no data leak between families |
| R25 | Guests are identified by a personal link with a private code (M32) | code is in the URL fragment, long and random, stored only as a hash; unknown, malformed and missing codes look identical |
| R26 | The couple read everything in one Excel workbook that also holds the guest list (M35) | `rsvp/guests` has a template workbook with guests, links, answers, pending, messages and summary sheets; no invented guests; phone numbers stay local |
| R27 | The RSVP form sits at the end of the scroll after the gate and details, designed by the Opus agent, look chosen by the user, face untouched (M32, M36) | form section is after the details; the designer was Opus; the user picked; the face files and opening timing are unchanged |
| R28 | RSVP wording is the user's: placeholders `TODO(user)` in pt-PT, en and es; no invented guest names (M32) | no unmarked invented sentence in the form, the no-JavaScript message or the errors |
| R29 | The form is accessible and robust (M32, M1) | real labels, `fieldsets`, keyboard use, 4.5:1 contrast, errors that say what to fix, no lost answers when the network or JavaScript fails, a no-JavaScript path, reduced motion, first load under 1500 KB |
| R30 | Privacy and credentials (M32) | no credential read, typed or copied; no guest or couple detail in any outside request; guest data git-ignored; purpose notice and retention date are `TODO(user)` |
| R31 | A vetted kit of skills, tools and subagents is in this folder (M33, M37) | `vendor/SOURCES.md` pins each item with licence and review; `rsvp/SUBAGENTS.md` and `rsvp/kit/INDEX.md` exist |
| R32 | Accounts and deploys wait for the user (M32) | nothing is deployed or pushed before the user confirms the account step; no account is created by the assistant |
| R33 | Final checks before done (M32) | `spec-guardian`, a clean-slate review of the form, a phone-size Playwright run, a no-JavaScript run, and an honest list of what was not tested (iPhone Safari, WhatsApp browser) |
| R34 | Each fact appears once on the whole page (M44, M45) | a script over the rendered text finds the date, the venue name, the town, the street address, the names and the deadline once each, in every language |
| R35 | The page is one coherent aesthetic (M38, M41, M45) | one paper tone with no seam, palette tokens only, one type system, one ornament language; `consistency-red-team` has run on the whole page and its findings are fixed |
| R36 | Spend is conservative (M43) | one concept at a design gate, reviewers used where they pay off, no repeated captures or rebuilds without need |
| R37 | Ask the user what they might know (M39, M45) | open questions (times, schedule, dress code, FAQ answers, account holder, contact link, deadline) are asked in plain words before they are invented |
| R38 | Mushrooms follow the user's three reference pictures, and the page gets more wild flowers native to Portugal (M51) | `rsvp/comps/ASSET-PROMPTS.md` lists mushroom prompts in the reference style (soft wash, a few broken ink lines, gills and stem texture) and a wildflower set of species that grow wild in Portugal, checked at source; the page uses them |
| R39 | Images are made with the better Copilot model, and the season is summer (M52) | `assets/LOG.md` rows say the Copilot mode used (Think Deeper); the flowers and plants in `rsvp/comps/ASSET-PROMPTS.md` are ones in bloom or leaf in Portugal in July, with a source |
| R40 | The mushroom pictures are a format and species guide, not exact copies; colors and style may change to fit our mood; add one tied bunch of hot peppers as seen in rural Portugal (M53) | `rsvp/comps/ASSET-PROMPTS.md` has mushrooms of those shapes in our palette and one hanging bunch of dried hot peppers tied together; it is painted in the same style |
| R41 | The painted assets read as hand-made watercolor with a few soft ink lines, less realistic and less AI-glossy (M54) | the style lock in `rsvp/comps/ASSET-PROMPTS.md` asks for loose translucent washes, a few broken hand-drawn ink lines and no photographic shading (the canonical lock is in `DESIGN-SPEC.md`); the generated assets are judged against the user's three mushroom pictures before use |
| R42 | For now work only on the aesthetics of the invitation; the RSVP backend is set up by the partner and is merged later (M55) | no backend work (Worker, D1, workbook, deploy) is started before the user reopens it; asset and page art continue |
