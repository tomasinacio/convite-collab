# README for Tomas: how to feed this zip to Claude on your PC

What is in the zip: everything a Claude on your PC needs to build the cinematic opening video and add it to the current invitation page.
- `START-HERE/` : the instructions for Claude (`FIRST-PROMPT.txt`, `PC-PLAN.md`, `DECISIONS.md`)
- `project/` : the current page (`comps/prototype.v10.html` and the one-file phone version), all the art (cut-outs and the full-size Copilot images), your references and the reference openings, the plans (`briefs/`), your exact words (`SPEC.md`), the scripts and the skills.

## Steps
1. Unzip `wedding-opening-pack.zip` to a short path without spaces, for example `C:\wedding-opening-pack`.
2. Install Claude Code on the PC if it is not installed (code.claude.com, needs your account; you log in yourself). Open a terminal in `C:\wedding-opening-pack` and run `claude`. (If you use VS Code: open that folder, then open Claude Code there.)
3. Open `START-HERE\FIRST-PROMPT.txt`, copy all of it, paste it into Claude and send. That is the only thing you have to write.
4. Claude will tell you in 5 lines what it understood and ask you choices with the picker. It is allowed to install free tools (Blender, FFmpeg, Node, Python); say yes to installs. It must never ask you for passwords or create accounts; if a site needs a login, it stops and tells you which one.
5. It will show you frames (a contact sheet) before it makes the final video. Pick what you prefer. Then it builds `comps\prototype.v11.html` and `comps\prototype.v11.single.html`.
6. To bring it back here: zip or upload these into the `wed_in` folder on the VM (same names): `comps/prototype.v11.html`, `comps/prototype.v11.single.html`, `comps/art/v11/` (the video files and poster), `comps/V11-NOTES.md`, and any new scripts it made in `scripts/`. I will then check it (red team, spec guardian, measurements) and we continue.

## Tips
- Rendering may take 1 to 4 hours on a PC without a GPU; Claude will tell you the estimate. You can leave it running.
- The page also has a few things waiting (copy fixes: 2027 and "Local:" on the plaque; the continuity art fixes). They are listed in `START-HERE\DECISIONS.md`; tell Claude if you want them done in the same go.
- Higgsfield: if you want to try it as well, Claude will give you the start and end stills and the prompt; you run it on your account and give the mp4 back.
- Test the one-file version on your phone and in WhatsApp (open the link inside WhatsApp, not only the browser).
