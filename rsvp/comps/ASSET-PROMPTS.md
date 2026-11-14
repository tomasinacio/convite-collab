# New painted assets: prompts for the user to approve

Owner: Tomas. Written 2026-11-12 by the Opus designer (v16). Review date: 2026-11-19. Rollback: `rm rsvp/comps/ASSET-PROMPTS.md`.

The user asked for more life in the same painted look (Messages 46, 51 to 53): mushrooms first, bees, tree trunks, falling and swaying leaves, branches from the sides, rocks, July wildflowers, a bunch of dried peppers. Nothing here is generated yet: the main session runs the prompts in `Copilot` (Think Deeper mode) after the user approves them, then `scripts/extract_asset.py` cuts each one out and `scripts/image_quality.py` gates it. Every file gets its row in `assets/LOG.md`.

The motion hooks already exist in `rsvp/page/info.css` (`ASSET SLOTS`), empty and hidden (`PENDING`) so no stand-in ever shows. When a painting arrives, only its slot line changes (`url(@@ART:art/v17/<file>.webp@@)`), its class leaves the `PENDING` list, and its aspect ratio changes if the shape differs.

## Season: July in Portugal

The wedding is on 10 July: dry Iberian summer, harvested wheat, dry grass, cicadas and bees, warm low light. Only plants in flower or in leaf then, and mushrooms that can fruit in summer.

- Kept, in flower or in leaf in July: wild fennel and wild carrot (both on a July flower list for southern Iberia; a Portuguese wild-fennel note is dated 31 July), Spanish oyster thistle (same July list; it flowers in the hottest weather), garden lavender (`alfazema`), olive, cork oak, fig with its early figs, harvested wheat and dry wild oats, field bindweed (already in the art).
- Left out, spring flowers that are over by July: poppy (`papoila`), bee orchid (`Ophrys apifera`), hoop-petticoat daffodil (`Narcissus bulbocodium`), wild gladiolus, viper's bugloss (`Echium`), rock-rose (`esteva`, `Cistus ladanifer`), Spanish lavender (`rosmaninho`, flowers February to June). St John's wort peaks in May and June in Lisbon, so it is out too.
- Mushrooms are mostly autumn in Portugal. Summer ones were chosen: Caesar's mushroom (`Amanita caesarea`, July to November in chestnut woods, summer to autumn in the `montado`), the dark `porcini` of the cork-oak woods (`Boletus aereus`, June to August in one `montado` guide), the parasol (`Macrolepiota procera`, summer to autumn in chestnut woods; autumn in other guides). They grow in the oak shade after a summer rain: a small, true-to-life license. Saffron milk cap (`Lactarius deliciosus`) is autumn only and is left out. Fly agaric (`Amanita muscaria`) starts in late summer: optional, marked below.
- Not verified at a source this pass (general knowledge, check before generating): the `inkcap` season, the cicada, the fig's early crop, garden lavender's flowering months. `Flora-On` (the Portuguese flora site) could not be reached from here; its species pages are the place to confirm each plant.

Sources used: a July flower list for southern Iberia (wildsideholidays.co.uk), a Portuguese wild-fennel note (pigletinportugal.com), Lisbon wildflower notes (somethingintheyard.blogspot.com), Portuguese mushroom habitat guides (cogumelos-backup.pages.dev, chestnut and `montado` pages), `Algarve` plant lists (first-nature.com), Portuguese park flora guides (`uevora.pt`).

## Why the first two read too realistic (the user, Message 54)

The two `Copilot` mushrooms (`assets/inbox/mush-caesar-pair.png`, `m5-mush-fly-agaric-pair.png`) are scientific plates, not sketches:

- Full 3D modelling: each stem is shaded like a lit cylinder, each cap like a lit dome, with a smooth gradient from light to dark.
- Gloss: white specular dots on the orange egg and on the caps, so they look wet and photographed.
- Machine-even detail: hundreds of fine, evenly spaced gill lines, and earth crumbs and volva skin with photographic texture.
- One crisp hairline outline of even weight that follows every edge exactly; the colour never leaves the line.
- Saturated, solid colour fields; almost no bare paper inside the shapes.
- A perfect, centred, catalogue pose.

The user's pictures and the face's own art do the opposite: a slightly wobbly pen line of varying weight, a few strokes where the plate has a hundred, flat or lightly graded washes that bleed past the line or stop short of it, white paper left inside the forms, almost no shading, small accidents.

Correction, 2026-11-14: looked at side by side, the face's own art has almost no line at all (washes with soft wet edges); the wobbly pen line belongs to the user's mushroom pictures only. The page follows the face.

## Style lock and judging

The style lock and the judging rules now live in one place: `DESIGN-SPEC.md` section 6 (canonical lock, allowed and forbidden traits, toning at cut-out) and section 12 (red-team checklist). The ready-to-paste prompts, lock included, are `rsvp/comps/PASTE-PROMPTS.md`. The sketchbook pen-and-watercolour lock that stood here on 2026-11-12 is retired: it drew a heavy pen outline round every form (user, 2026-11-14). Attach `comps/art/v16/olive.webp` as the look to match, not the mushroom pictures.

Each subject below goes into that lock at `[SUBJECT]`. Aspect is the image to ask for; display is the size on the page (u is 1% of the phone column, about 3.9 pixels).

## Mushrooms (the emphasis)

Status 2026-11-14 (user): at most two mushroom pieces on the page, M5 and M1 kept; M2 and M3 rejected as too detailed; M4 dropped.

At the foot of sections, in small clusters, never over text. Static, or a 1 deg sway of the whole cluster at most: they are rooted.

- **M1** `mush-caesar-pair.webp`. Subject: `two Caesar's mushrooms, Amanita caesarea, one open with a pale warm orange cap, a few loose yellow gill strokes beneath, a pale yellow stem with a ragged ring, the other still a closed egg half out of its white cup-shaped volva, a frayed base with a few dots of earth`. Square 1:1. Display 14u wide, foot of the countdown, left. Motion: none.
- **M2** `mush-porcini-trio.webp`. Subject: `three dark porcini, Boletus aereus, of different sizes, rounded bronze-brown caps in a flat pale wash, cream pores beneath shown with a few ink dots, thick pale stems with three or four net strokes, one small one leaning on the big one, frayed bases`. Landscape 4:3. Display 18u, foot of the schedule, left (replaces the rock-rose stand-in `--ia-mush`). Motion: none.
- **M3** `mush-parasol-tall.webp`. Subject: `one tall parasol mushroom, Macrolepiota procera, a wide flat cap with brown scales drawn as a few ink flecks on a pale buff ground, a slender stem with a loose zigzag pattern and a loose double ring, a bulbous frayed base`. Tall portrait 1:2. Display 11u wide, the larger one, beside the gifts card on the right base. Motion: sway 0.6 deg, 7.3 s, from 1.2 s after the section is seen.
- **M4** `mush-inkcaps.webp`. Subject: `a small cluster of five slender grey inkcap mushrooms on tall thin white stems, bell-shaped blue-grey caps with a few ink gill strokes, two caps dark and curling at the rim, frayed bases together`. Portrait 2:3. Display 10u, by the mossy stone at the foot of the questions, left. Season to verify. Motion: none.
- **M5 (optional, late summer)** `mush-fly-agaric-pair.webp`. Subject: `two fly agarics, Amanita muscaria, a rounded dusty terracotta-red cap with white flecks left as bare paper and a smaller one half open, pale gills in a few ink strokes, white stems with a ragged skirt and a bulbous base, a few dots of earth at the base`. Square 1:1. Display 12u. Only if the user wants it: it fruits from late summer, so it bends the July rule.

## Bees, a cicada, and what flies

- **B1** `bee-flying.webp`. Subject: `one honeybee in flight seen from the side, three-quarter view, translucent wings drawn in fine ink with a pale wash, a golden-brown banded body, legs tucked`. Square 1:1. Display 5u. Countdown section: it flies in from the right once (2.4 s, ease-out) and settles into a 2.3 s hover bob (slot `--ia-bee`).
- **B2** `bee-on-lavender.webp`. Subject: `three tall stems of garden lavender, alfazema, with purple flower spikes, one honeybee resting on the middle spike`. Portrait 1:3. Display 12u, schedule section, right base (replaces the lavender slot `--ia-lav`). Motion: sway 1.4 deg, 6.1 s; the bee rides it.
- **B3** `cicada-on-twig.webp`. Subject: `one cicada, Cicada orni, resting on a short dry olive twig, clear veined wings in fine ink, a mottled grey-brown body`. Landscape 3:2. Display 9u, the dress-code section, left edge, half off the screen. Motion: none (a cicada sits still); season to verify.

## Tree trunks and branches from the sides

- **T1** `trunk-cork-oak.webp`. Subject: `the lower trunk of a cork oak, sobreiro, the lower half freshly stripped of its cork and painted warm cinnamon red, the upper half thick grey furrowed cork bark, one low branch with small dark leaves, the trunk cut off at the top and bottom edges`. Tall portrait 1:3. Display 22u wide, at the left edge of the gifts section, half off the screen (cork is harvested in summer, so the red stripped trunk is July itself). Motion: enters from the left (1.2 s), no sway (a trunk does not sway).
- **T2** `trunk-olive.webp`. Subject: `the gnarled twisting trunk of an old olive tree, silver-grey bark with deep hollows, two small sprouts of narrow leaves at its base, cut at the top edge`. Tall portrait 1:2. Display 20u, right edge of the questions section, half off the screen. Motion: enters from the right, no sway.
- **L1** `branch-olive-side.webp`. Subject: `one olive branch growing in from the left edge, eighteen narrow silver-green leaves, a few small green olives, the cut end at the left edge`. Landscape 3:1. Display 34u, top left of the gifts section (replaces `--ia-branch-l`). Motion: enters from the left, then sways 1.6 deg about the cut end, 5.7 s.
- **L2** `branch-fig-side.webp`. Subject: `one fig branch growing in from the right edge, three large lobed fig leaves and two ripe purple-green early figs, the cut end at the right edge`. Landscape 3:2. Display 30u, right of the dress-code section (replaces the orange branch stand-in `--ia-branch-r`). Motion: enters from the right, sways 0.9 deg, 6.7 s. Season to verify (early figs, `lampos`, ripen around June and July).
- **L3** `leaves-falling.webp`. Subject: `six separate single leaves, well apart and not touching: three narrow olive leaves, two glossy orange-tree leaves, one small dry cork-oak leaf, each whole and slightly curled`. Square 1:1; cut into six files. Display 3u to 4u. One falls in a section when it is first seen and then every 24 s (2.9 s fall, sway 1.3 s, turn 1 s), dress-code and questions sections (slot `--ia-leaf`).

## July wildflowers

- **F1** `thistle-oyster.webp`. Subject: `two stems of Spanish oyster thistle, Scolymus hispanicus, spiny grey-green leaves and bright lemon-yellow flower heads, one bud`. Portrait 1:2. Display 12u, schedule section, left base beside the `porcini`. Motion: sway 1 deg, 5.6 s.
- **F2** `fennel-flowering.webp`. Subject: `one tall stem of wild fennel in flower, feathery thread-like leaves and flat yellow umbels like small parasols`. Tall portrait 1:3. Display 14u, page foot, left, standing on the `rodapé` (slot `--ia-fennel`). Motion: sway 1.2 deg, 5.9 s.
- **F3** `wild-carrot.webp`. Subject: `three stems of wild carrot, Daucus carota, lacy flat white umbels, one with a tiny dark purple centre floret, one curled into a nest as it goes to seed`. Portrait 2:3. Display 15u, page foot, right (slot `--ia-carrot`). Motion: sway 1 deg, 6.4 s.
- **F4** `wheat-sheaf.webp`. Subject: `a small hand-tied sheaf of harvested golden wheat and dry wild oats, tied with a twist of straw, the stalk ends cut straight`. Portrait 2:3. Display 16u, schedule section, left base (replaces the wheat clump stand-in `--ia-wheat`). Motion: sway 1.1 deg, 5.3 s.

## Rocks (static)

- **R1** `stone-single.webp`. Subject: `one rounded pale limestone stone, warm grey with ochre patches and a few dots of lichen, flat underside`. Landscape 3:2. Display 9u, gifts section, right base.
- **R2** `pebbles-cluster.webp`. Subject: `a small low cluster of seven pebbles of different sizes, warm grey, sand and rust tones, a dry olive leaf lying across two of them`. Landscape 3:1. Display 20u, page foot between the fennel and the carrot (slot `--ia-stones`) and the gifts base (slot `--ia-rock`).
- **R3** `stone-mossy.webp`. Subject: `one larger rounded stone with a cushion of dry summer moss on its shaded side, olive and straw green, a honeybee resting on top`. Square 1:1. Display 13u, the questions section foot, beside the `inkcaps` (M4). Static; the bee does not move.

## Peppers

- **P1** `peppers-hanging.webp`. Subject: `a bunch of dried red hot peppers, piri-piri, hanging from a loop of rough twine, twelve long thin wrinkled peppers in deep terracotta red and dark red tied at their stalks, as hung to dry on a Portuguese farmhouse wall`. Tall portrait 1:3. Display 7u wide, hanging from the top edge of the countdown section, left, under the plaque's buttons (slot `--ia-peppers`). Motion: settles in (0.9 s), then sways 2.2 deg about the twine loop, 4.3 s, like a weight on a string.

## Placement rules (all assets)

- Scale: 5u to 34u on the page, never wider than a third of the column; every piece sits at a section's side or base and never over its text column or a button.
- Sides alternate down the page: countdown left (peppers), schedule left and right base, dress code right, gifts left top and right base, questions right, page foot both ends.
- Motion is transform and opacity only, starts when a section is first seen, pauses out of view, and is off in reduced motion (the pieces stay, at rest; the falling leaf is hidden). Nothing touches the 5 s opening.
- Weight: each piece is applied one screen before its section (`.near`), so none adds to the first load. Aim for 15 KB to 45 KB each as `WebP` at 3x of its display size.
