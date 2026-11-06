# Paper 1: Tomakomai / EXCOOL Original-Source Verification Memo
Date: 2026-11-06.

## Scope and access status
This is a follow-up to the user-supplied `partial_primary_source_leads.csv`. The links were inspected using the public publisher-hosted PDFs rendered as web-extracted text; the Japan CCS 2020 source was also inspected as rendered slide images. The Tomakomai June/July monthly PDF and ClassNK screenshot requests failed, and the original binary PDF files could not be downloaded into this workspace; therefore do **not** describe the package as containing original PDFs or as completing visual/attachment review. The Mar 2019 PDF failed access and remains unverified. The users' /workspace/phd_decoding-v1 paths are not mounted here; original Word/excel files were not edited. The 54 pre-existing checks were not re-executed because their test runner/workspace was inaccessible. No previous modeled climate results changed.

## Original source links
1. Report named June (May injection/end-May cumulative): https://www.jccs-tomakomai-monitoring.com/JCCS/wp-content/uploads/2019/06/201906_ENG.pdf — p.12.
2. Report named July (June injection/end-June cumulative/pressure/temp): https://www.jccs-tomakomai-monitoring.com/JCCS/wp-content/uploads/2019/07/201907_ENG.pdf — pp.12, 17, 18.
3. ClassNK EXCOOL paper: https://www.classnk.or.jp/hp/pdf/research/rd/2026/12_e05.pdf — p.5 Table 3 (printed -39-), p.4 particulars.
4. Japan CCS 2020 webinar: https://www.japanccs.com/wp/wp-content/uploads/2020/09/Tomakomai-CCS-Demonstration-Project-Achievements-and-Future-Outlook_Shoichi-Ishii.pdf — slides 10 and 11 (PDF pp.10-11).

## June 2019 98.1-t source discrepancy
The June-report May-end row labelled Moebetsu is 260,414.4 tonnes; the following July-report June-end Moebetsu row is 261,631.7 tonnes; the June injection is 1,315.4 tonnes. Formations-as-labelled delta: 261,631.7 - 260,414.4 = 1,217.3, a 98.1 t shortfall.
Yet the total June 29 cumulative amount is 261,729.8 tonnes, and 261,729.8 - 260,414.4 = 1,315.4 tonnes exactly. The Takinoue cumulative listed in both tables is 98.2 tonnes. The June two-formation sum 261,631.7+98.2=261,729.9 tonnes is 0.1 t from the header total. **Hypothesis:** May's Moebetsu-labelled 260,414.4 may actually be the combined cumulative amount; formation-specific May should be approximately 260,316.2. This is a plausible categorization error but it is NOT established by an authoritative erratum. Do not replace source values silently. For provisional observed *total* June mass only, the 1,315.4-tonne value is independently consistent with overall cumulative change. The formation-level baseline remains UNRESOLVED.

## June paired physical observations
The July 2019 report labels its June monitoring, reporting Moebetsu injector average bottom-hole pressure 9.64 MPa at depth 930 m and temperature 41.3 C at 930 m (pp.17-18). Units are printed MPa (not explicitly MPaG in this monthly panel). Do not subtract this from the 12.6 MPaG pressure limit shown in the 2020 webinar until pressure reference is reconciled.

## EXCOOL evidence boundary
ClassNK Table 3 reports seven CO2 loading-condition tests spanning July 2024 to July 2025, summarized in `excool_loading_tests_classnk_2026.csv`. EXCOOL has two 725 m3 tanks and stated maximum CO2 load 850 tonnes; 750 tonnes was a specific port-restricted test. Do not treat trial loads as annual throughput, mass delivered to storage, voyage count, voyage fuel duty or port turnaround distribution. The ClassNK text does not publish a complete annual fuel/maintenance/port calendar.

## Remaining data
- Full native timestamped injection-rate + BHP + temperature + operating/shutdown controls from Tomakomai for 2016-2019;
- Independent injection ceilings from reservoir simulations (particularly Higashi-Niigata Case A/B) and calibrated constraints;
- ClassNK / NGL / terminal operator: loading/unloading time, main/auxiliary-engine fuel, distance, start/end voyage dates, downtime, actual yearly trip counts;
- Capture-site utilities and boundary-consistent lifecycle GHG inventory.

## Interpretation
This improves the provenance for monthly observations and ClassNK loading experiments but **does not add independent annual geological injection ceilings, vessel availability or regional net CO2 break-even evidence**. Original model findings unchanged.
