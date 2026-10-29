# Nutmeg and Ginger's Cottage: Truth or Crumbs?

Local cooperative party-game prototype. Requires Python 3.10+; no downloads or dependencies.

Run `python3 server.py`, then open http://localhost:3000 in your browser. Create a room. Open a second tab and join using the room code with another player name. For phones on the same Wi-Fi, open http://YOUR-COMPUTER-LAN-IP:3000 (allow local network access through your firewall if needed). Set PORT to change the port.

Each tab uses a separate session. Duplicating a tab may copy its session; use Leave screen in the duplicate, then join as a new player. Leave screen only clears that tab's credentials; it does not remove the participant during an active game. Reloading reconnects to the same player. The host controls start and replay. Inactive players receive automatic guesses. Rooms and membership live in server memory and reset when it restarts. This is a local prototype, not a production hosting configuration.

Rules: 2–8 players, 20 seconds per question, 8-second automatic reveals, up to 10 rounds. Cottage starts at 50%; round delta is 30 × fraction correct − 10. At zero, spend one of two buttons to rebuild to 25%. At 100%, win; at zero without buttons or after round 10 below 100%, lose.

Run checks: `python3 -m unittest -v test_game.py`.

Cottage explorer: choose Outside or Floor Plan, switch between First Floor and Second Floor, then enter any of six rooms. Inspect the room features or click furniture. Built and missing features follow the shared percentage; exploring does not alter the score. Run `node test_cottage.cjs` for construction/destruction checks.

Music: original, softly rendered piano-and-string-style instrumental, bundled as a local WAV recording. Starts on the first click/tap unless muted; each player has an independent Music On/Off control.

Rescues are optional: before a loss, remaining gumdrops trigger a paused decision. Any player can spend a selected gumdrop for +25 percentage points. Only the host can decline. Final-round rescues must finish the cottage within round 10; no extra rounds are added.

Maker Results: use the footer button and your configured maker password to preview Win or Loss without changing a live room. Use Close Preview in the footer to leave preview mode.

Character reactions: click or keyboard-activate any character portrait for a rotating playful line. Reactions dismiss after 4.5 seconds. Built furniture is interactive: click the Peppermint Fridge to open/close it, Toffee Fireplace to light/extinguish it, and Lollipop Lamp or Pretzel Desk to switch their lamps on/off. These personal touches never change team progress. Run `node test_interactions.cjs` for interaction checks.

Reveal extras: perfect-round icing celebrations; and result-specific Prince Fondant dialogue. Round 10 has a three-second introduction, then the full 20 seconds to answer. Run `node test_social.cjs` for display checks.

Additional furniture actions: Chocolate Oven opens with steam, Tootsie Wardrobe opens, Rock Candy Curio sparkles, Cotton Candy Bed bounces, Taffy Sink runs, Mint Cabinet opens, Gummy Bear Shelf makes its gummy bears hop, and Fudge Workbench presents wiggle. Click again to stop or close. Reduced-motion preferences are respected.

More click animations: Espresso-Bean Maker pours, Marshmallow Sofa squishes, Wafer Shelf books sway, Candyfloss Rug ripples, Teacup Bath bubbles, and Truffle Trolley rolls. The living-room Jawbreaker Shelf stores candy in jars; the pantry Gummy Bear Shelf holds nine pastel gummy bears.

Furniture styling uses a shared shallow three-quarter depth, consistent cocoa edges, soft contact shadows, and coordinated pastel materials. Kitchen table and espresso maker placements are aligned to the floor and tabletop; stripe patterns do not inherit furniture outlines.

Question packs: the host selects Royal Riddles, Sweet Secrets, Fairytale Mischief, or All Fairytales in the lobby. Each themed pack has 20 authored questions. Games draw five Yes and five No answers, shuffled, and avoid the immediately previous game’s questions when replayed in the same room. Pack selection stays with the team on replay.

Detail interactions: click the cake independently of its oven door, and desk books independently of the lamp. The Jawbreaker Shelf jars and Pretzel Chair also animate. Ending artwork includes clickable bows, gumdrop buttons, crown, cherry, awards, jars, toolboxes, chocolate and candy; each preserves the artwork’s transforms and supports keyboard activation and reduced motion.

Room header: Copy Room Code copies the code and confirms success, with a legacy clipboard fallback and manual code display if copying is unavailable. Main Menu returns to the entry screen. Discovery hints identify interactive room artwork, characters, and ending details. Nutmeg and Ginger use proportional upper-body portraits based on the celebration artwork.

Peppermint Fridge: click the upper freezer door or lower fridge door to open and close them independently. Each door also supports keyboard activation.

The scrapbook has a celebration hint. Cupcake icing, Timber’s feather and icing tubes are clickable. Successful room-code copying displays a temporary 1.6-second confirmation.

Display modes: use Computer or Mobile in the header. The first visit automatically selects a layout from screen width; explicit choices are remembered on the device. Both modes play together in the same rooms. Mobile mode includes larger text and touch controls, fixed answer buttons, compact rescues, collapsible round reviews, and contained artwork enlargement. Switching modes preserves room membership and entered answers. Run `node test_display_modes.cjs` for preference and state-preservation checks.

Sound: use the independent Sound On/Off control for gentle click chimes, including clickable ending artwork. The preference is remembered separately from music. Ages 8+ is a static label. Player count is visible in both modes and follows the room’s player list.



Finalized sound set: all 63 effects use additive sine tones and gentle amplitude envelopes only, with no noise, filters, recordings or stock samples. Room items retain 36 distinct tones. Every ending-art interaction type has its own mapping; storybook pages, rings, hearts and gemstone are interactive and have matching tones. All profiles share the magical-light arpeggio. The palette uses lower pitches, softer attacks, longer fades and reduced playback volume. Open /sound-library to hear the finalized sounds and optionally record future change requests.
