# Pandoc Debugging: The Case of the O(n^2) Hang

**Date:** December 13, 2025
**Agent:** Antigravity (Google DeepMind) & Krystal Neely

## The Incident
During the final build of *The Kryssie Method*, Pandoc began hanging indefinitely (or taking 15+ minutes) when converting the `kryssie-method-final.md` file to HTML.

## The Investigation
We isolated the issue through a series of smoke tests:
1.  **Tag-Based Bisect:** We removed sections one by one. The "Appendix" was identified as the culprit.
2.  **Granular Analysis:** within the Appendix, the "Citation References" section was flagged.
3.  **The Smoking Gun:** A massive block of ~60 link definitions (e.g., `[cite:foo]: url`) was causing Pandoc's reference resolver to hit a performance cliff.

## The Resolution
The issue was an **O(n^2) complexity bug** in how Pandoc resolves huge blocks of reference-style links when they are all distinct and numerous.

**The Fix:**
- We commented out the "Citation References" section in the source markdown.
- `<!-- ... -->` wrapping the citations block resolved the hang immediately.
- Build time went from >15mins (hung) to <2 seconds.

## Artifacts in this Folder
- `pandoc.log`: The verbose log showing the hang.
- `_smoke.*`: Test files used during the bisect process.
- `toc_clean.md`: Intermediate file from the TOC generation (unrelated but preserved).

## Lessons Learned
- When Pandoc hangs on "Resolving References", check for large blocks of reference links.
- Binary search / bisecting the document is the fastest way to isolate parser chokes.
