# Retrieval-Editing Qualitative Notes

작성일: 2026-06-04

## Summary

The 10C pairwise-selected edit gate produces Coptic-script output, but many predictions are partial edits or shortened copies of the retrieved hint. The output is not an exact-copy baseline, yet it is still retrieval-dominated.

## Examples

### `b.JOH.1.1`

- Source: `In the beginning was the Word, and the Word was with God, and the Word was God.`
- Prediction: `ⲀⲖ ⲪⲎ ⲈⲦⲀⲚⲤⲞⲐⲘⲈϤ ⲪⲎ ⲈⲦⲀⲚⲤⲞⲘⲤ ⲈⲢⲞϤ ⲞⲨⲞϨ ⲀⲚⲈⲚϪⲒϪ ϪⲈⲘϪⲰⲘϤ ⲈⲐⲂⲈ ⲠⲒⲤⲀϪⲒ ⲚⲦⲈⲠⲰⲚϦ`
- Retrieved hint begins: `ⲪⲎ ⲈⲦϢⲞⲠ ⲒⲤϪⲈⲚ ϨⲎ ⲪⲎ ⲈⲦⲀⲚⲤⲞⲐⲘⲈϤ ...`
- Reference begins: `ϦⲈⲚ ⲦⲀⲢⲬⲎ ⲚⲈⲠⲒⲤⲀϪⲒ ...`

Reading: the prediction edits and shortens the retrieved hint but does not recover the source-specific beginning of John 1:1.

### `b.JOH.1.10`

- Source: `He was in the world, and the world was made by him, and the world knew him not.`
- Prediction begins: `РⲒⲔⲞⲤⲘⲞⲤ ⲚⲈⲘ ϮⲈⲠⲒⲐⲨⲘⲒⲀ ⲚⲦⲈⲚⲒⲂⲀⲖ ...`
- Retrieved hint begins: `ϪⲈ ⲈⲚⲬⲀⲒ ⲚⲒⲂⲈⲚ ⲈⲦϦⲈⲚ ⲠⲒⲔⲞⲤⲘⲞⲤ ...`
- Reference begins: `ⲚⲀϤⲬⲎ ϦⲈⲚⲠⲒⲔⲞⲤⲘⲞⲤ ⲠⲈ ...`

Reading: the output drifts into repeated retrieved-hint phrases and even begins with a non-Coptic Cyrillic-looking `Р`, so target-script control is still imperfect.

### `b.JOH.1.11`

- Source: `He came unto his own, and his own received him not.`
- Prediction begins: `ⲀϤⲬⲰⲖⲈⲘ ⲘⲘⲞϤ ⲀϤⲒ ⲈⲠⲈⲤⲎ ⲦⲞⲨⲞϨ ⲀϤϢⲞⲠϤ ... retrieved_coptic: ...`
- Retrieved hint: `ⲞⲨⲞϨ ⲀϤⲬⲰⲖⲈⲘ ⲘⲘⲞϤ ⲀϤⲒ ⲈⲠⲈⲤⲎ ⲦⲞⲨⲞϨ ⲀϤϢⲞⲠϤ ⲈⲢⲞϤ ⲈϤⲢⲀϢⲒ.`
- Reference: `ⲀϤⲒ ϨⲀ ⲚⲎ ⲈⲦⲈⲚⲞⲨϤ ⲞⲨⲞϨ ⲚⲈⲦⲈⲚⲞⲨϤ ⲘⲠⲞⲨϢⲞⲠϤ ⲈⲢⲰⲞⲨ.`

Reading: the prediction includes the literal prompt marker `retrieved_coptic:`, which is a formatting failure and a sign that the model has not learned the edit task cleanly.

## Conclusion

The same-checkpoint controls strengthen the negative conclusion:

- source-only collapses to chrF++ 0.2729;
- retrieved-only reaches chrF++ 18.6220, slightly above correct source+retrieval at 18.3574;
- wrong-shift1 drops to chrF++ 12.8253, so the model is sensitive to retrieval quality;
- feature-selected top8 reaches chrF++ 19.1558, still below the candidate evidence itself.

The current 10C gate should be reported as a failure analysis rather than a positive translation result. The strongest claim remains retrieval selection, not neural editing.
