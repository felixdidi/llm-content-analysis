# Tutorial data

10 short texts hand-picked from the **Real World Worry Waves Dataset (RW3D)**,
van der Vegt & Kleinberg (2023), *Scientific Data*, 10(1), 537.
<https://doi.org/10.1038/s41597-023-02438-y>. Data: <https://osf.io/9b85r/> —
licensed **CC-BY 4.0**.

`text` is each respondent's own short free-text response about how the
COVID-19 situation made them feel; `self_reported_emotion` is the single
emotion they themselves chose as the best fit (RW3D's `emotion_gold`
column), kept here only as a reference — the tutorial itself only reads the
`text` column. 5 texts were chosen where the self-reported emotion is
`fear`, and 5 where it clearly is not (`happiness` or `relaxation`), so the
worked examples in the tutorial have a clean mix to compare model
predictions against.

When using this data, please cite van der Vegt & Kleinberg (2023) per the
license.
