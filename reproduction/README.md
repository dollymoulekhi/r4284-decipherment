# R4284 literal-decoding tools

Python 3.9+; standard library only. No AI API, downloads, or input writes.
These tools apply a caller-supplied alphabet to a caller-supplied transcription.
They do not infer a key or verify a historical decipherment.

## Scope of this download

Code and synthetic tests only. Full R4284 transcriptions, R4325 key data,
line ledger and control inputs are published separately in the
[text-only review package](https://gist.github.com/dollymoulekhi/a6eb279347dcbbf9c80aa0b0e23ca676),
following permission to reproduce the inherited transcription with credit.
You cannot reproduce the full reported experiment from this download alone.
Do not treat the synthetic tests as historical evidence.

[Cyphersolver's 26 October review](https://github.com/dbourdeau/cyphersolver/issues/98#issuecomment-6406612222)
independently checked the alphabet and accepted the match. Its separate statistical
test was underdetermined, not a pass. Full word separation and translation remain
unfinished; the review does not certify this code or every input token.

## Run

Extract the archive into its own folder and open a terminal there:

```text
python -B -m unittest test_decoder.py
python -B decoder.py --transcription YOUR_TRANSCRIPTION.txt --key YOUR_KEY.json
```

The JSON output contains counts, coverage, literal lines, unresolved groups,
unapplied exact partitions, and SHA-256 fingerprints of the supplied inputs.
It never reports verified accuracy. It does not run the retrospective
shuffle experiments described in the article.

## Input conventions

The UTF-8 key JSON has an `alphabet` object mapping numeric strings to labels.
For example, this SYNTHETIC example is not an R4325 transcription:

```json
{"alphabet": {"1": "a", "2": "b", "12": "c"}}
```

The UTF-8 transcription uses whitespace-separated numbers and `[clear words]`.
Question marks indicate uncertainty, e.g. `4?` or `??`. Lines beginning with
`#` are metadata. Parenthetical notes are ignored. Bare commas, semicolons,
colons and periods are accepted separators. Other notation is rejected rather
than silently interpreted. Do not supply editorial word guesses as cipher tokens.

For compatibility with the local working input, processing stops at a heading
beginning `## IMG_R4284_I25751_P_hi.jpeg right`, which introduces separate
alphabetic-cipher material. The numerical-letter continuation precedes it.
Physical input-file line numbers are retained.

## Source and attribution

- Riksarkivet, Sweden: DECODE R4284, Chifferklaver låda II:114.
  https://de-crypt.org/decrypt-web/RecordsView/4284
- Candidate alphabet: R4325, Chifferklaver låda II:152; horizontal strip on I25940.
  https://de-crypt.org/decrypt-web/RecordsView/4325
- Prior attempt and inherited working-input provenance: Daniel Bourdeau.
  https://dbourdeau.github.io/cyphersolver/riksarkivet4284.html

The present code was prepared with AI assistance for Dolly Moulekhi's
candidate-match study. No third-party scans or transcription files are bundled.
No blanket open-source license is asserted at this draft stage. See RIGHTS.md.
