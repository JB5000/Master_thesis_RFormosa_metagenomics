# Experimental protocol photos — with the student's handwritten annotations

**FOR CHATGPT:** These 11 `.jpeg` files ARE the **original experimental (wet-lab) protocols** used in this
thesis — printed manufacturer protocols (QIAGEN DNeasy PowerSoil Pro; Oxford Nanopore Native Barcoding Kit 24
V14, SQK-NBD114.24) **annotated by hand by the student** with the exact parameters and modifications actually
used. **You can open and read these images.** Use them as the primary source for Methods sections 2.1–2.4
(sampling, DNA extraction, library preparation, sequencing/loading). They corroborate and extend
`../METHODS_2_1_TO_2_5_EVIDENCE_BASED_CANDIDATE.md`.

Photos were provided by the student (WhatsApp, 2026-07-13). Handwriting transcribed below as legible; where a
value is uncertain it is marked "(approx/uncertain)". The inventory contains only values visible in the retained images.

## The 11 photos (in protocol order)

| File | Protocol / page | Key handwritten annotations (what was actually done) |
|---|---|---|
| `protocol_01_DNA_extraction_tracking_sheet_nanodrop.jpeg` | **DNA extraction tracking sheet** — all 24 EMO BON RFormosa SO samples (210805…251125) | Per-sample extraction number **[1]–[22]**; NanoDrop **dsDNA (ng/µL)**, A260/280, A260/230. **210805 and 240416 crossed out (X)** = not extracted/sequenced by the student. "1ª batela / 2ª batela" (extraction batches). → 22 barcoded samples. |
| `protocol_02_QIAGEN_PowerSoilPro_steps01-07_sampleprep.jpeg` | **QIAGEN DNeasy PowerSoil Pro**, Quick-Start steps 1–7 | Sample-prep workflow: "Tirar os tubos −80 °C → Meter −20 °C → Meter AT (ambiente) → Anotar consistência → **Centrifugar 8000 RPM 2 min** → Fazer pool do sobrenadante"; "tirar do sample até à linha **~250 mg**"; "Nomear os tubos do kit". |
| `protocol_03_QIAGEN_PowerSoilPro_steps08-17_13200rpm_elution.jpeg` | **QIAGEN PowerSoil Pro**, steps 8–17 (MB Spin Column, EA/C5/C6, elution) | Centrifuge speed used = **13 200 RPM** (in place of the printed 15 000–16 000 × g); final elution of Solution C6 = **~60 µL** (step 16, printed "50–100 µL"). |
| `protocol_04_ONT_NBD114_libprep_endprep_400ng.jpeg` | **ONT SQK-NBD114.24**, p.3 — DCS + DNA end-prep | "For >4 barcodes, aliquot **400 ng per sample**"; make up to 11 µL; end-prep mastermix. Handwritten mastermix scaling: "12 em 24", "**38,5 µL** (22×2)", "**33 µL**". |
| `protocol_05_ONT_NBD114_endprep_cleanup_ampure.jpeg` | **ONT SQK-NBD114.24**, p.4 — end-prep AMPure XP clean-up (steps 7–19) | Thermal cycler 20 °C/65 °C 5 min; AMPure XP (AXP); 80 % ethanol washes. Ethanol prep: "**2,2 × 500 µL = 11 mL → 8,8 mL EtOH + 2,2 mL H₂O**". |
| `protocol_06_ONT_NBD114_native_barcode_ligation.jpeg` | **ONT SQK-NBD114.24** — native barcode ligation (volume tables) | EDTA (blue cap); AMPure XP (For 24 = 230 µL); Hula mixer 10 min. Scaling for 22 samples: "2,2×", "**528 µL**", "22×", "**220 µL**". |
| `protocol_07_ONT_NBD114_barcode_cleanup_SFB.jpeg` | **ONT SQK-NBD114.24** — barcode-ligation clean-up (steps 14–20, Short Fragment Buffer) | Uses **Short Fragment Buffer (SFB)** washes (updated method, not 80 % ethanol). Handwritten "**31**" (elution/step). |
| `protocol_08_ONT_NBD114_pooled_library_qubit.jpeg` | **ONT SQK-NBD114.24** — step 21, pooled barcoded library | "Remove and retain ~~35~~ **31 µL** of eluate into 1.5 mL LoBind; **quantify 1 µL by Qubit**; take forward to adapter ligation." |
| `protocol_09_ONT_NBD114_adapter_ligation_cleanup.jpeg` | **ONT SQK-NBD114.24** — adapter ligation & final clean-up (steps 6–18) | Incubate 20 min RT; final clean-up uses **LFB/SFB** (not ethanol); elute in EB (handwritten "**33**"); incubate 37 °C; retain eluate — "**32 e 1 µL para o Qubit**". |
| `protocol_10_ONT_NBD114_final_library_47ngul_loading.jpeg` | **ONT SQK-NBD114.24** — step 19, final library + flow-cell loading amounts | Final library in 32 µL EB. Flow-cell loading table (very short 100 fmol / short 35–50 fmol / long **300 ng**). **Final library concentration = 47,2 ng/µL**; "→ **6,4 µL**" (volume giving ~300 ng). |
| `protocol_11_ONT_NBD114_flowcell_priming_loading.jpeg` | **ONT SQK-NBD114.24** — flow-cell priming & library loading (steps 7–13) | Priming mix 500 µL; loading mix per flow cell = **Sequencing Buffer 100 µL + Library Beads (LIB) 68 µL + DNA library 32 µL = 200 µL**; load 200 µL via P1000. Loading dilution: "**6,4 µL (47,2 ng/µL) + 25,6 µL H₂O**" (→ 32 µL); 2nd run note: "(2ª run 5 µL)", "(2ª run 27 µL)". |

## Key parameters actually used (consolidated from the annotations)
- **Sampling/thawing:** −80 °C → −20 °C → ambient; note consistency; initial spin **8000 RPM, 2 min**, pool supernatant; ~**250 mg** sediment per extraction.
- **DNA extraction (QIAGEN DNeasy PowerSoil Pro):** centrifugation at **13 200 RPM** throughout; elution ~**60 µL** Solution C6; quantified on **NanoDrop** (ng/µL, A260/280, A260/230) — per-sample values on the tracking sheet (photo 01) and in `../DNA_EXTRACTION_PER_SAMPLE.tsv`.
- **Library prep (ONT Native Barcoding SQK-NBD114.24, V14):** **400 ng** input per sample (>4 barcodes); mastermixes scaled for **22 samples**; ethanol wash prep 8,8 mL EtOH + 2,2 mL H₂O; **SFB/LFB** clean-ups; intermediate elutions ~31–33 µL; Qubit quantification at each clean-up.
- **Final library:** **47,2 ng/µL**; loaded ~**300 ng** (~6,4 µL) diluted with H₂O to the loading volume; loading mix SB 100 + LIB 68 + library 32 = **200 µL**; a **2nd run** (reload) was prepared with a different dilution.
- **Cross-checks:** 22 barcoded samples; 210805 and 240416 excluded (photo 01) — consistent with the 23-sample analysis set and the separately-sequenced 240416.

> These photos are evidence for **Methods 2.1–2.4**. For the computational Methods (2.6–2.12) see `../../02_methods_provenance_2_6_to_2_12/`.
