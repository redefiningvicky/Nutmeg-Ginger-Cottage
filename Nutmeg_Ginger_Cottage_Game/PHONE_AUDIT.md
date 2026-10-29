# Computer and Mobile mode verification

The mobile improvements are implemented in this copy. The separate gingy-sugar-game project remains the original backup.

## Display modes

- Computer: the existing side-by-side cottage and question layout on wide screens.
- Mobile: a single-column layout with larger text and touch controls, fixed Yes/No choices, and a sticky round timer.
- Computer/Mobile buttons are available in the header at all times.
- First visit chooses a layout from screen width. An explicit choice is remembered in browser storage.
- Switching display modes preserves form input, room membership, and the player’s saved answer. Both modes use the same server and question packs.

## Implemented mobile improvements

- Cottage description wraps at 15px; main question text remains 18px.
- Character names 14px, titles 12px, room item labels 14px.
- Discovery hints 12px, smaller than 16px artwork captions.
- Larger navigation and gumdrop controls; separate touch buttons for freezer/fridge, cake and desk books.
- Room and ending artwork can be enlarged inside contained scrolling areas.
- Existing gumdrops move into a compact rescue section near the top during a rescue.
- Completed-round details collapse on rescue and ending screens; they remain open in Computer mode.

## Verification

22 screen states were measured at 320, 375, 390 and 430px in Mobile mode, and at 1280px in Computer mode: 110 viewport checks. No horizontal page overflow was found. In a 740px viewport, Mobile Yes/No controls remain visible at the bottom; rescue gumdrops appeared around 312px from the top.

A live two-player browser check confirmed a Computer player and Mobile player could join the same room, start a round, and save an answer. Switching the answering player’s mode preserved that answer. Form input was also preserved when switching modes.

20 Python tests and the Node cottage, furniture, ending-artwork, social-display and display-mode checks passed. Physical iPhone/Android testing, virtual-keyboard behavior and device audio behavior are still recommended before public release.

## Final layout refinement — 2026-10-28

Moved the badge star inline, added safe wrapping for header controls and long labels, reduced character-card spacing in Mobile mode, and improved keyboard-focus contrast on the cream keepsake background. All six Node verification suites and 25 Python tests pass. These are layout and behavior checks, not physical-device certification. Earlier viewport measurements predate these final scrapbook changes; test the final version on real iPhone/Safari and Android/Chrome before public release.

## Natural spacing and mobile type pass

Ending columns now use content height without stretch or automatic gap filling. Storybook artwork enlarged 8% inside its unchanged frame. Captions use natural document flow, with stars contained within the artwork area. Mobile profile roles and hints are 13px, character quotes 15px, result labels 14px, character names 15px. Character cards can wrap when needed. Automated behavior checks pass; these changes still need visual confirmation on physical phones.
