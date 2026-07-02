# Candidate Decision Selector Error Examples

작성일: 2026-06-04

Selected model: `gradient_boosting`

## 10B improves top1 by >= 10 chrF++

Count: 99

### b.JOH.9.36

- decision: `SWAP_TO_RANK_3`
- selected rank / predicted / chrF++: 3 / 30.09 / 37.84
- top1 chrF++: 0.00
- oracle rank / chrF++: 4 / 43.76
- delta vs top1: 37.84
- gap to oracle: 5.92
- source: He answered and said, Who is he, Lord, that I might believe on him?
- selected matched source: But he answered and said unto him that told him, Who is my mother? and who are my brethren?
- selected candidate: ⲚⲐⲞϤ ⲆⲈ ⲀϤⲈⲢⲞⲨⲰ ⲠⲈϪⲀϤ ⲘⲪⲎ ⲈⲦϪⲰ ⲘⲘⲞⲤ ⲚⲀϤ ϪⲈ ⲚⲒⲘ ⲦⲈ ⲦⲀⲘⲀⲨ ⲒⲈ ⲚⲒⲘ ⲚⲈⲚⲀⲤⲚⲎⲞⲨ.
- oracle candidate: ⲚⲐⲞϤ ⲆⲈ ⲀϤⲈⲢⲞⲨⲰ ⲠⲈϪⲀϤ ϪⲈ ⲀⲚⲞⲔ ⲠⲀϬⲞⲒⲤ ⲞⲨⲞϨ ⲘⲠⲈϤϢⲈ ⲚⲀϤ.
- reference: ⲀϤⲈⲢⲞⲨⲰ ⲠⲈϪⲀϤ ϪⲈ ⲚⲒⲘ ⲠⲈ ⲠⲀϬⲞⲒⲤ ϨⲒⲚⲀ ⲚⲦⲀⲚⲀϨϮ ⲈⲢⲞϤ.

### b.JOH.7.40

- decision: `SWAP_TO_RANK_5`
- selected rank / predicted / chrF++: 5 / 27.63 / 45.83
- top1 chrF++: 18.19
- oracle rank / chrF++: 5 / 45.83
- delta vs top1: 27.65
- gap to oracle: 0.00
- source: Many of the people therefore, when they heard this saying, said, Of a truth this is the Prophet.
- selected matched source: Some of them that stood there, when they heard that, said, This man calleth for Elias.
- selected candidate: ϨⲀⲚⲞⲨⲞⲚ ⲆⲈ ⲈⲂⲞⲖ ϦⲈⲚⲚⲎ ⲈⲦⲞϨⲒ ⲈⲢⲀⲦⲞⲨ ⲘⲘⲀⲨ ⲈⲦⲀⲨⲤⲰⲦⲈⲘ ⲚⲀⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲀϤⲘⲞⲨϮ ⲞⲨⲂⲈ ⲎⲖⲒⲀⲤ.
- oracle candidate: ϨⲀⲚⲞⲨⲞⲚ ⲆⲈ ⲈⲂⲞⲖ ϦⲈⲚⲚⲎ ⲈⲦⲞϨⲒ ⲈⲢⲀⲦⲞⲨ ⲘⲘⲀⲨ ⲈⲦⲀⲨⲤⲰⲦⲈⲘ ⲚⲀⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲀϤⲘⲞⲨϮ ⲞⲨⲂⲈ ⲎⲖⲒⲀⲤ.
- reference: ϨⲀⲚⲞⲨⲞⲚ ⲆⲈ ⲈⲂⲞⲖ ϦⲈⲚⲠⲒⲘⲎϢ ⲈⲦⲀⲨⲤⲰⲦⲈⲘ ⲈⲚⲀⲒⲤⲀϪⲒ ⲚⲀⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲦⲀⲪⲘⲎⲒ ⲪⲀⲒ ⲠⲈ ⲠⲒⲠⲢⲞⲪⲎⲦⲎⲤ.

### b.JOH.15.17

- decision: `SWAP_TO_RANK_6`
- selected rank / predicted / chrF++: 6 / 28.96 / 39.92
- top1 chrF++: 12.53
- oracle rank / chrF++: 2 / 46.65
- delta vs top1: 27.38
- gap to oracle: 6.73
- source: These things I command you, that ye love one another.
- selected matched source: And we have confidence in the Lord touching you, that ye both do and will do the things which we command you.
- selected candidate: ⲠⲈⲚϨⲎⲦ ⲆⲈ ⲐⲎⲦ ϦⲈⲚⲠϬⲞⲒⲤ ⲈϪⲈⲚ ⲐⲎⲚⲞⲨ ϪⲈ ⲚⲎ ⲈⲦⲈⲚϨⲞⲚϨⲈⲚ ⲘⲘⲰⲦⲈⲚ ⲈⲢⲰⲞⲨ ⲦⲈⲦⲈⲚⲒⲢⲒ ⲘⲘⲰⲞⲨ ⲞⲨⲞϨ ⲈⲢⲈⲦⲈⲚⲈⲀⲒⲦⲞⲨ.
- oracle candidate: ϪⲈ ⲪⲀⲒ ⲠⲈ ⲠⲒⲰϢ ⲪⲎ ⲈⲦⲀⲢⲈⲦⲈⲚⲤⲞⲐⲘⲈϤ ⲒⲤϪⲈⲚ ϨⲎ ϨⲒⲚⲀ ⲚⲦⲈⲦⲈⲚⲘⲈⲚⲢⲈ ⲚⲈⲦⲈⲚⲈⲢⲎⲞⲨ
- reference: ⲚⲀⲒ ⲆⲈ ϮϨⲞⲚϨⲈⲚ ⲘⲘⲰⲦⲈⲚ ⲈⲢⲰⲞⲨ ϨⲒⲚⲀ ⲚⲦⲈⲦⲈⲚⲘⲈⲚⲢⲈ ⲚⲈⲦⲈⲚⲈⲢⲎⲞⲨ.

### b.JOH.12.28

- decision: `SWAP_TO_RANK_7`
- selected rank / predicted / chrF++: 7 / 24.62 / 35.84
- top1 chrF++: 10.19
- oracle rank / chrF++: 7 / 35.84
- delta vs top1: 25.64
- gap to oracle: 0.00
- source: Father, glorify thy name. Then came there a voice from heaven, saying, I have both glorified it, and will glorify it again.
- selected matched source: And lo a voice from heaven, saying, This is my beloved Son, in whom I am well pleased.
- selected candidate: ⲞⲨⲞϨ ⲒⲤ ⲞⲨⲤⲘⲎ ⲀⲤϢⲰⲠⲒ ⲈⲂⲞⲖ ϦⲈⲚⲚⲒⲪⲎⲞⲨⲒ ⲈⲤϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲪⲀⲒ ⲠⲈ ⲠⲀϢⲎⲢⲒ ⲠⲀⲘⲈⲚⲢⲒⲦ ⲈⲦⲀⲒϮⲘⲀϮ ⲚϦⲎⲦϤ.
- oracle candidate: ⲞⲨⲞϨ ⲒⲤ ⲞⲨⲤⲘⲎ ⲀⲤϢⲰⲠⲒ ⲈⲂⲞⲖ ϦⲈⲚⲚⲒⲪⲎⲞⲨⲒ ⲈⲤϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲪⲀⲒ ⲠⲈ ⲠⲀϢⲎⲢⲒ ⲠⲀⲘⲈⲚⲢⲒⲦ ⲈⲦⲀⲒϮⲘⲀϮ ⲚϦⲎⲦϤ.
- reference: ⲪⲒⲰⲦ ⲘⲀⲰⲞⲨ ⲘⲠⲈⲔϢⲎⲢⲒ ⲞⲨⲤⲘⲎ ⲀⲤⲒ ⲈⲂⲞⲖ ϦⲈⲚⲦⲪⲈ ⲈⲤϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲀⲒϮⲰⲞⲨ ⲠⲀⲖⲒⲚ ⲞⲚ ϮⲚⲀϮⲰⲞⲨ.

### b.JOH.2.7

- decision: `SWAP_TO_RANK_3`
- selected rank / predicted / chrF++: 3 / 26.02 / 35.18
- top1 chrF++: 12.41
- oracle rank / chrF++: 8 / 36.56
- delta vs top1: 22.77
- gap to oracle: 1.38
- source: Jesus saith unto them, Fill the waterpots with water. And they filled them up to the brim.
- selected matched source: And Jesus said unto them, Can the children of the bridechamber mourn, as long as the bridegroom is with them? but the days will come, when the bridegroom shall be taken from the...
- selected candidate: ⲞⲨⲞϨ ⲠⲈϪⲈ ⲒⲎⲤⲞⲨⲤ ⲚⲰⲞⲨ ϪⲈ ⲘⲎ ⲞⲨⲞⲚ ϢϪⲞⲘ ⲚⲚⲒϢⲎⲢⲒ ⲚⲦⲈⲠⲒⲠⲀⲦϢⲈⲖⲈⲦ ⲈⲈⲢϨⲎⲂⲒ ϨⲰⲤ ⲈϤⲚⲈⲘⲰⲞⲨ ⲚϪⲈⲠⲒⲠⲀⲦϢⲈⲖⲈⲦ ⲤⲈⲚⲎⲞⲨ ⲆⲈ ⲚϪⲈϨⲀⲚⲈϨⲞⲞⲨ ⲈϢⲰⲠ ⲀⲨϢⲀⲚⲰⲖⲒ ⲘⲠⲒⲠⲀⲦϢⲈⲖⲈⲦ ⲈⲂⲞⲖ ϨⲀⲢⲰⲞⲨ ⲦⲞⲦⲈ ⲈⲨⲈⲈⲢⲚⲎ ⲤⲦⲈⲨⲒⲚ.
- oracle candidate: ⲈⲦⲀϤⲒ ⲆⲈ ⲈϦⲞⲨⲚ ⲈⲠⲒⲎⲒ ⲀⲨⲒ ϨⲀⲢⲞϤ ⲚϪⲈⲚⲒⲂⲈⲖⲖⲈⲨ ⲞⲨⲞϨ ⲠⲈϪⲈ ⲒⲎⲤⲞⲨⲤ ⲚⲰⲞⲨ ϪⲈ ⲦⲈⲦⲈⲚⲚⲀϨϮ ϪⲈ ⲞⲨⲞⲚ ϢϪⲞⲘ ⲘⲘⲞⲒ ⲈⲈⲢ ⲪⲀⲒ ⲠⲈϪⲰⲞⲨ ⲚⲀϤ ϪⲈ ⲤⲈ ⲠⲈⲚϬⲞⲒⲤ.
- reference: ⲠⲈϪⲈ ⲒⲎⲤⲞⲨⲤ ⲚⲰⲞⲨ ϪⲈ ⲘⲞϨ ⲚⲚⲒϨⲨⲆⲢⲒⲀ ⲘⲘⲰⲞⲨ ⲞⲨⲞϨ ⲀⲨⲘⲀϨⲞⲨ ϢⲀⲠϢⲰⲒ.

## 10B hurts top1 by <= -10 chrF++

Count: 24

### b.JOH.3.12

- decision: `SWAP_TO_RANK_6`
- selected rank / predicted / chrF++: 6 / 25.94 / 14.96
- top1 chrF++: 30.54
- oracle rank / chrF++: 1 / 30.54
- delta vs top1: -15.58
- gap to oracle: 15.58
- source: If I have told you earthly things, and ye believe not, how shall ye believe, if I tell you of heavenly things?
- selected matched source: (For many walk, of whom I have told you often, and now tell you even weeping, that they are the enemies of the cross of Christ:
- selected candidate: ⲞⲨⲞⲚ ⲞⲨⲘⲎϢ ⲄⲀⲢ ⲀⲨⲘⲞϢⲒ ⲚⲀⲒ ⲈⲦⲀⲒϪⲞⲤ ⲚⲰⲦⲈⲚ ⲈⲐⲂⲎⲦⲞⲨ ⲚⲞⲨⲘⲎϢ ⲚⲤⲞⲠ ⲞⲨⲞϨ ϮⲚⲞⲨ ⲞⲚ ⲈⲒⲢⲒⲘⲒ ϮϪⲰ ⲘⲘⲞⲤ ⲚⲒϪⲀϪⲒ ⲚⲦⲈⲠⲒⲤⲦⲀⲨⲢⲞⲤ ⲚⲦⲈⲠⲬⲢⲒⲤⲦⲞⲤ.
- oracle candidate: ⲈⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲒⲤϪⲈ ⲚⲐⲞⲔ ⲠⲈ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲀϪⲞⲤ ⲚⲀⲚ ⲠⲈϪⲀϤ ⲚⲰⲞⲨ ϪⲈ ⲀⲒϢⲀⲚϪⲞⲤ ⲚⲰⲦⲈⲚ ⲦⲈⲦⲈⲚⲚⲀⲚⲀϨϮ ⲀⲚ.
- reference: ⲒⲤϪⲈ ⲀⲒϪⲈ ⲚⲀ ⲠⲔⲀϨⲒ ⲚⲰⲦⲈⲚ ⲘⲠⲈⲦⲈⲚⲚⲀϨϮ ⲠⲰⲤ ⲀⲒϢⲀⲚϪⲈ ⲚⲀ ⲦⲪⲈ ⲚⲰⲦⲈⲚ ⲦⲈⲦⲈⲚⲚⲀϨϮ.

### b.JOH.7.16

- decision: `SWAP_TO_RANK_3`
- selected rank / predicted / chrF++: 3 / 26.91 / 28.74
- top1 chrF++: 44.23
- oracle rank / chrF++: 1 / 44.23
- delta vs top1: -15.48
- gap to oracle: 15.48
- source: Jesus answered them, and said, My doctrine is not mine, but his that sent me.
- selected matched source: But he answered and said, I am not sent but unto the lost sheep of the house of Israel.
- selected candidate: ⲚⲐⲞϤ ⲆⲈ ⲀϤⲈⲢⲞⲨⲰ ⲠⲈϪⲀϤ ϪⲈ ⲘⲠⲞⲨⲦⲀⲞⲨⲞⲒ ϨⲀ ϨⲖⲒ ⲈⲂⲎⲖ ⲈⲚⲒⲈⲤⲰⲞⲨ ⲈⲦⲤⲞⲢⲈⲘ ⲚⲦⲈⲠⲎⲒ ⲘⲠⲒⲤⲖ.
- oracle candidate: ⲞⲨⲞϨ ⲀϤⲈⲢⲞⲨⲰ ⲚⲰⲞⲨ ⲚϪⲈⲒⲎⲤⲞⲨⲤ ϦⲈⲚϨⲀⲚⲠⲀⲢⲀⲂⲞⲖⲎ ⲈϤϪⲰ ⲘⲘⲞⲤ.
- reference: ⲀϤⲈⲢⲞⲨⲰ ⲚⲰⲞⲨ ⲚϪⲈⲒⲎⲤⲞⲨⲤ ⲞⲨⲞϨ ⲠⲈϪⲀϤ ϪⲈ ⲦⲀⲤⲂⲰ ⲀⲚⲞⲔ ⲐⲰⲒ ⲀⲚ ⲦⲈ.

### b.JOH.13.17

- decision: `SWAP_TO_RANK_4`
- selected rank / predicted / chrF++: 4 / 24.96 / 24.82
- top1 chrF++: 39.88
- oracle rank / chrF++: 1 / 39.88
- delta vs top1: -15.06
- gap to oracle: 15.06
- source: If ye know these things, happy are ye if ye do them.
- selected matched source: Wherefore the rather, brethren, give diligence to make your calling and election sure: for if ye do these things, ye shall never fall:
- selected candidate: ⲈⲐⲂⲈⲪⲀⲒ ⲘⲀⲖⲖⲞⲚ ⲚⲈⲚⲤⲚⲎⲞⲨ ⲒⲎⲤⲞⲨⲤ ⲚⲦⲈⲚ ⲐⲎⲚⲞⲨ ϨⲒⲚⲀ ⲈⲂⲞⲖ ϨⲒⲦⲈⲚ ⲚⲒϨⲂⲎⲞⲨⲒ ⲈⲐⲚⲀⲚⲈⲨ ⲚⲦⲈⲦⲈⲚⲦⲀϪⲢⲈ ⲠⲈⲦⲈⲚⲐⲰϨⲈⲘ ⲚⲈⲘ ⲦⲈⲦⲈⲚⲘⲈⲦⲤⲰⲦⲠ ⲚⲀⲒ ⲄⲀⲢ ⲈⲢⲈⲦⲈⲚⲒⲢⲒ ⲘⲘⲰⲞⲨ ⲚⲚⲈⲦⲈⲚⲤⲖⲀϮ ⲈⲚⲈϨ.
- oracle candidate: ⲀⲖⲖⲀ ⲒⲤϪⲈ ⲦⲈⲦⲈⲚⲈⲢⲠⲔⲈϬⲒⲘⲔⲀϨ ⲈⲐⲂⲈ ϮⲘⲈⲐⲘⲎⲒ ⲰⲞⲨⲚⲒⲀⲦⲈⲚ ⲐⲎⲚⲞⲨ ⲦⲞⲨϨⲞϮ ⲆⲈ ⲘⲠⲈⲢⲈⲢϨⲞϮ ϦⲀⲦⲈⲤϨⲎ ⲞⲨⲆⲈ ⲘⲠⲈⲢϢⲐⲞⲢⲦⲈⲢ.
- reference: ⲒⲤϪⲈ ⲦⲈⲦⲈⲚⲈⲘⲒ ⲈⲚⲀⲒ ⲰⲞⲨⲚⲒⲀⲦⲈⲚ ⲐⲎⲚⲞⲨ ⲈϢⲰⲠ ⲀⲢⲈⲦⲈⲚϢⲀⲚⲀⲒⲦⲞⲨ.

### b.JOH.6.16

- decision: `SWAP_TO_RANK_5`
- selected rank / predicted / chrF++: 5 / 30.78 / 33.12
- top1 chrF++: 47.24
- oracle rank / chrF++: 1 / 47.24
- delta vs top1: -14.12
- gap to oracle: 14.12
- source: And when even was now come, his disciples went down unto the sea,
- selected matched source: And seeing the multitudes, he went up into a mountain: and when he was set, his disciples came unto him:
- selected candidate: ⲈⲦⲀϤⲚⲀⲨ ⲆⲈ ⲈⲚⲒⲘⲎϢ ⲀϤϢⲈ ⲚⲀϤ ⲈⲠϢⲰⲒ ⲈϪⲈⲚ ⲠⲒⲦⲰⲞⲨ ⲞⲨⲞϨ ⲈⲦⲀϤϨⲈⲘⲤⲒ ⲀⲨⲒ ϨⲀⲢⲞϤ ⲚϪⲈⲚⲈϤⲘⲀⲐⲎⲦⲎⲤ.
- oracle candidate: ⲈⲦⲀ ⲢⲞⲨϨⲒ ⲆⲈ ϢⲰⲠⲒ ⲚⲀϤⲢⲞⲦⲈⲂ ⲚⲈⲘ ⲠⲒⲒⲂ ⲘⲘⲀⲐⲎⲦⲎⲤ.
- reference: ⲈⲦⲀ ⲢⲞⲨϨⲒ ⲆⲈ ϢⲰⲠⲒ ⲀⲨⲒ ⲈϦⲢⲎⲒ ⲈⲪⲒⲞⲘ ⲚϪⲈⲚⲈϤⲘⲀⲐⲎⲦⲎⲤ

### b.JOH.4.41

- decision: `SWAP_TO_RANK_5`
- selected rank / predicted / chrF++: 5 / 22.51 / 11.64
- top1 chrF++: 25.47
- oracle rank / chrF++: 6 / 27.29
- delta vs top1: -13.83
- gap to oracle: 15.65
- source: And many more believed because of his own word;
- selected matched source: He that believeth on the Son of God hath the witness in himself: he that believeth not God hath made him a liar; because he believeth not the record that God gave of his Son.
- selected candidate: ⲪⲎ ⲈⲐⲚⲀϨϮ ⲈⲠϢⲎⲢⲒ ⲤϢⲞⲠ ⲚϦⲎⲦϤ ⲚϪⲈϮⲘⲈⲦⲘⲈⲐⲢⲈ ⲚⲦⲈⲪⲚⲞⲨϮ ⲪⲎ ⲈⲦⲈⲚϤⲚⲀϨϮ ⲈⲠϢⲎⲢⲒ ⲘⲪⲚⲞⲨϮ ⲀⲚ ⲀϤⲀⲒϤ ⲚⲤⲀⲘⲈⲐⲚⲞⲨϪ ϪⲈ ⲘⲠⲈϤⲚⲀϨϮ ⲈϮⲘⲈⲦⲘⲈⲐⲢⲈ ⲐⲎ ⲈⲦⲀϤⲈⲢⲘⲈⲐⲢⲈ ⲘⲘⲞⲤ ⲚϪⲈⲪⲚⲞⲨϮ ϦⲀ ⲠⲈϤϢⲎⲢⲒ
- oracle candidate: ⲀⲠⲀⲒϨⲰⲂ ⲆⲈ ⲞⲨⲞⲚϨ ⲈⲂⲞⲖ ϦⲈⲚⲒⲞⲠⲠⲎ ⲦⲎⲢⲤ ⲞⲨⲞϨ ⲞⲨⲘⲎϢ ⲀⲨⲚⲀϨϮ ⲈⲠϬⲞⲒⲤ.
- reference: ⲞⲨⲞϨ ϨⲀⲚⲔⲈⲘⲎϢ ⲚϨⲞⲨⲞ ⲀⲨⲚⲀϨϮ ⲈⲐⲂⲈ ⲠⲈϤⲤⲀϪⲒ.

## 10B misses oracle by >= 15 chrF++

Count: 30

### b.JOH.5.1

- decision: `KEEP_TOP1`
- selected rank / predicted / chrF++: 1 / 42.55 / 13.53
- top1 chrF++: 13.53
- oracle rank / chrF++: 6 / 42.82
- delta vs top1: 0.00
- gap to oracle: 29.29
- source: After this there was a feast of the Jews; and Jesus went up to Jerusalem.
- selected matched source: And when he was twelve years old, they went up to Jerusalem after the custom of the feast.
- selected candidate: ⲞⲨⲞϨ ⲈⲦⲀϤⲈⲢⲒⲂ ⲚⲢⲞⲘⲠⲒ ⲀⲨϢⲈ ⲚⲰⲞⲨ ⲈⲠⲒϢⲀⲒ ⲔⲀⲦⲀ ϮⲔⲀϨⲤ.
- oracle candidate: ⲈϤⲚⲀϢⲈ ⲚⲀϤ ⲚϪⲈⲒⲎⲤⲞⲨⲤ ⲈϨⲢⲎⲒ ⲈⲒⲈⲢⲞⲤⲀⲖⲎⲘ ⲀϤϬⲒ ⲘⲠⲒⲒⲂ ⲞⲨⲦⲰϤ ⲚⲈⲘⲰⲞⲨ ⲞⲨⲞϨ ⲠⲈϪⲀϤ ⲚⲰⲞⲨ ϨⲒ ⲠⲒⲘⲰⲒⲦ.
- reference: ⲘⲈⲚⲈⲚⲤⲀ ⲚⲀⲒ ⲚⲈⲠϢⲀⲒ ⲚⲦⲈⲚⲒⲞⲨⲆⲀⲒ ⲠⲈ ⲞⲨⲞϨ ⲀϤⲒ ⲚϪⲈⲒⲎⲤⲞⲨⲤ ⲈϨⲢⲎⲒ ⲈⲒⲈⲢⲞⲤⲀⲖⲎⲘ.

### b.JOH.6.4

- decision: `KEEP_TOP1`
- selected rank / predicted / chrF++: 1 / 28.12 / 19.95
- top1 chrF++: 19.95
- oracle rank / chrF++: 3 / 47.58
- delta vs top1: 0.00
- gap to oracle: 27.64
- source: And the passover, a feast of the Jews, was nigh.
- selected matched source: Ye know that after two days is the feast of the passover, and the Son of man is betrayed to be crucified.
- selected candidate: ϪⲈ ⲦⲈⲦⲈⲚⲈⲘⲒ ϪⲈ ⲘⲈⲚⲈⲚⲤⲀ ⲔⲈⲈϨⲞⲞⲨ ⲂⲠⲒⲠⲀⲤⲬⲀ ⲚⲀϢⲰⲠⲒ ⲞⲨⲞϨ ⲠϢⲎⲢⲒ ⲘⲪⲢⲰⲘⲒ ⲤⲈⲚⲀⲦⲎⲒϤ ⲈⲐⲢⲞⲨⲀϢϤ.
- oracle candidate: ⲚⲀϤϦⲈⲚⲦ ⲆⲈ ⲠⲈ ⲚϪⲈⲠϢⲀⲒ ⲚⲦⲈⲚⲒⲀⲦϢⲘⲎⲢ ⲪⲎ ⲈⲦⲞⲨⲘⲞⲨϮ ⲈⲢⲞϤ ϪⲈ ⲠⲒⲠⲀⲤⲬ Ⲁ.
- reference: ⲚⲈ ⲀϤϦⲰⲚⲦ ⲆⲈ ⲠⲈ ⲚϪⲈⲠⲒⲠⲀⲤⲬⲀ ⲠϢⲀⲒ ⲚⲦⲈⲚⲒⲒⲞⲨⲆⲀⲒ.

### b.JOH.11.27

- decision: `KEEP_TOP1`
- selected rank / predicted / chrF++: 1 / 33.39 / 20.25
- top1 chrF++: 20.25
- oracle rank / chrF++: 5 / 46.33
- delta vs top1: 0.00
- gap to oracle: 26.09
- source: She saith unto him, Yea, Lord: I believe that thou art the Christ, the Son of God, which should come into the world.
- selected matched source: And when he was come into the house, the blind men came to him: and Jesus saith unto them, Believe ye that I am able to do this? They said unto him, Yea, Lord.
- selected candidate: ⲈⲦⲀϤⲒ ⲆⲈ ⲈϦⲞⲨⲚ ⲈⲠⲒⲎⲒ ⲀⲨⲒ ϨⲀⲢⲞϤ ⲚϪⲈⲚⲒⲂⲈⲖⲖⲈⲨ ⲞⲨⲞϨ ⲠⲈϪⲈ ⲒⲎⲤⲞⲨⲤ ⲚⲰⲞⲨ ϪⲈ ⲦⲈⲦⲈⲚⲚⲀϨϮ ϪⲈ ⲞⲨⲞⲚ ϢϪⲞⲘ ⲘⲘⲞⲒ ⲈⲈⲢ ⲪⲀⲒ ⲠⲈϪⲰⲞⲨ ⲚⲀϤ ϪⲈ ⲤⲈ ⲠⲈⲚϬⲞⲒⲤ.
- oracle candidate: ⲒⲎⲤⲞⲨⲤ ⲆⲈ ⲚⲀϤⲬⲰ ⲚⲢⲰϤ ⲠⲈ ⲞⲨⲞϨ ⲠⲈϪⲈ ⲠⲒⲀⲢⲬⲒⲈⲢⲈⲨⲤ ⲚⲀϤ ϪⲈ ϮⲦⲀⲢⲔⲞ ⲘⲘⲞⲔ ⲘⲪⲚⲞⲨϮ ⲈⲦⲞⲚϦ ϨⲒⲚⲀ ⲚⲦⲈⲔϪⲞⲤ ⲚⲀⲚ ϪⲈ ⲚⲐⲞⲔ ⲠⲈ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲠϢⲎⲢⲒ ⲘⲪⲚⲞⲨϮ ⲈⲦⲞⲚϦ.
- reference: ⲠⲈϪⲀⲤ ⲚⲀϤ ϪⲈ ⲠⲀϬⲞⲒⲤ ⲀⲚⲞⲔ ϮⲚⲀϨϮ ϪⲈ ⲚⲐⲞⲔ ⲠⲈ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲠϢⲎⲢⲒ ⲘⲪⲚⲞⲨϮ ⲪⲎ ⲈⲐⲚⲎⲞⲨ ⲈⲠⲒⲔⲞⲤⲘⲞⲤ.

### b.JOH.14.14

- decision: `KEEP_TOP1`
- selected rank / predicted / chrF++: 1 / 26.63 / 18.37
- top1 chrF++: 18.37
- oracle rank / chrF++: 3 / 44.29
- delta vs top1: 0.00
- gap to oracle: 25.92
- source: If ye shall ask any thing in my name, I will do it.
- selected matched source: For many shall come in my name, saying, I am Christ; and shall deceive many.
- selected candidate: ⲈⲢⲈ ⲞⲨⲘⲎϢ ⲄⲀⲢ ⲒϦⲈⲚ ⲠⲀⲢⲀⲚ ⲈⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲀⲚⲞⲔ ⲠⲈ ⲠⲬⲢⲒⲤⲦⲞⲤ ⲞⲨⲞϨ ⲈⲨⲈⲤⲈⲢⲈⲘ ⲞⲨⲘⲎϢ.
- oracle candidate: ⲞⲨⲞϨ ϨⲰⲂ ⲚⲒⲂⲈⲚ ⲈⲦⲈⲦⲈⲚⲚⲀⲈⲢⲈⲦⲒⲚ ⲘⲘⲞϤ ϦⲈⲚⲞⲨⲠⲢⲞⲤⲈⲨⲬⲎ ⲈⲢⲈⲦⲈⲚⲚⲀϨϮ ⲈⲢⲈⲦⲈⲚⲈϬⲒⲦⲞⲨ.
- reference: ⲪⲎ ⲈⲦⲈⲦⲈⲚⲚⲀⲈⲢⲈⲦⲒⲚ ⲘⲘⲞϤ ϦⲈⲚⲠⲀⲢⲀⲚ ⲪⲀⲒ ϮⲚⲀⲀⲒϤ.

### b.JOH.9.28

- decision: `KEEP_TOP1`
- selected rank / predicted / chrF++: 1 / 24.67 / 12.13
- top1 chrF++: 12.13
- oracle rank / chrF++: 6 / 36.87
- delta vs top1: 0.00
- gap to oracle: 24.74
- source: Then they reviled him, and said, Thou art his disciple; but we are Moses' disciples.
- selected matched source: And Jesus arose, and followed him, and so did his disciples.
- selected candidate: ⲞⲨⲞϨ ⲀϤⲦⲰⲚϤ ⲚϪⲈⲒⲎⲤⲞⲨⲤ ⲀϤⲘⲞϢⲒ ⲚⲤⲰϤ ⲚⲈⲘ ⲚⲈϤⲘⲀⲐⲎⲦⲎⲤ.
- oracle candidate: ⲦⲞⲦⲈ ⲀⲨⲒ ϨⲀⲢⲞϤ ⲚϪⲈⲚⲒⲘⲀⲐⲎⲦⲎⲤ ⲚⲦⲈⲒⲰⲀⲚⲚⲎⲤ ⲈⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲈⲐⲂⲈⲞⲨ ⲀⲚⲞⲚ ⲚⲈⲘ ⲚⲒⲪⲀⲢⲒⲤⲈⲞⲤ ⲦⲈⲚⲈⲢⲚⲎⲤⲦⲈⲨⲒⲚ ⲚϨⲀⲚⲘⲎ ϢⲚⲈⲔⲘⲀⲐⲎⲦⲎⲤ ⲆⲈ ⲚⲐⲰⲞⲨ ⲤⲈⲈⲢⲚⲎ ⲤⲦⲈⲨⲒⲚ ⲀⲚ.
- reference: ⲚⲐⲰⲞⲨ ⲆⲈ ⲀⲨϨⲰⲞⲨϢ ⲈⲢⲞϤ ⲈⲨϪⲰ ⲘⲘⲞⲤ ϪⲈ ⲚⲐⲞⲔ ⲞⲨⲘⲀⲐⲎⲦⲎⲤ ⲚⲦⲈⲪⲎ ⲈⲦⲈⲘⲘⲀⲨ ⲀⲚⲞⲚ ⲆⲈ ⲀⲚⲞⲚ ϨⲀⲚⲘⲀⲐⲎⲦⲎⲤ ⲚⲦⲈⲘⲰⲨⲤⲎⲤ.
