#!/usr/bin/env python3
"""Extract public primary evidence; never turn achieved rates into capacity.

Rebuilds the new registers from retained native source bytes. No web access,
reservoir simulator, annual interpolation or shipping-conditioning assumption.
"""
from pathlib import Path
from zipfile import ZipFile
import csv
import hashlib
import json
import re
from decimal import Decimal

import fitz

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence/public_followup'
MANIFEST = EVIDENCE / 'source_manifest.json'


def write_csv(path, rows):
    with (ROOT / path).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with (ROOT / path).open(encoding='utf-8') as f:
        return list(csv.DictReader(f))


def verify_sources():
    manifest = json.loads(MANIFEST.read_text())
    for item in manifest['files']:
        path = ROOT / item['path']
        assert path.stat().st_size == item['size_bytes'], path
        with path.open('rb') as f:
            assert hashlib.file_digest(f, 'sha256').hexdigest() == item['sha256'], path
    source = next(x for x in manifest['files'] if x['source_id'] == 'PUB-BJARMELAND')
    with ZipFile(ROOT / source['path']) as z:
        selected = [x for x in manifest['upstream_bjarmeland_archive']['members'] if x['retained']]
        assert set(z.namelist()) == {x['member'] for x in selected}
        for item in selected:
            assert hashlib.sha256(z.read(item['member'])).hexdigest() == item['sha256']
    assert manifest['cemcap']['md5'] == manifest['cemcap']['expected_zenodo_md5']
    return manifest


def extract_capture(manifest):
    item = next(x for x in manifest['files'] if x['source_id'] == 'PUB-CEMCAP')
    pdf = fitz.open(ROOT / item['path'])
    values, by_case = [], [dict(), dict(), dict()]
    cases = ['low_air_leak_interconnected', 'low_air_leak_direct', 'typical_air_leak_interconnected']
    # Table 5.3 is split over physical pages 22/23, printed pages 16/17.
    fields = {
        'Flue gas to be processed, kg/h': ('flue_gas_kg_h', 'kg/h'),
        'Flue gas temperature, oC': ('flue_gas_c', 'degC'),
        'CO2 mole fraction in flue gas (wet basis)': ('feed_co2_fraction', 'mol/mol wet'),
        'CO2 mole fraction in captured CO2 (wet basis)': ('product_co2_fraction', 'mol/mol wet'),
        'Pressure of captured CO2, bar': ('product_pressure_bar_as_printed', 'bar as printed'),
        'CO2 capture rate': ('capture_fraction', 'fraction'),
        'CO2 compression work, MJ/kgCO2': ('compression_mj_kg', 'MJ/kgCO2 captured'),
        'Auxiliary power for capture, MJ/kgCO2': ('auxiliary_mj_kg', 'MJ/kgCO2 captured'),
        'Total work consumption, MJ/kgCO2': ('total_work_mj_kg', 'MJ/kgCO2 captured'),
        'Heat consumption, MJ/kgCO2': ('heat_mj_kg', 'MJ/kgCO2 captured'),
        'Reboiler temperature, oC': ('reboiler_c', 'degC'),
        'Steam pressure, bara': ('steam_bara', 'bar absolute'),
        'Cooling duty, MJ/kgCO2': ('cooling_mj_kg', 'MJ/kgCO2 captured'),
        'Solvent (30wt% MEA) makeup, kgSolvent/tonneCO2': ('solution_makeup_kg_t', 'kg 30wt% solution/tCO2 captured'),
    }
    for page_number in [22, 23]:
        tables = pdf[page_number - 1].find_tables().tables
        assert len(tables) == 1
        table = tables[0]
        for ri, row in enumerate(table.extract()):
            label = ' '.join((row[0] or '').split())
            if label not in fields:
                continue
            key, unit = fields[label]
            # Merged empty columns on p22 must not shift the three source cases.
            cells = [(ci, cell) for ci, cell in enumerate(row[1:], 1) if cell]
            assert len(cells) == 3, (page_number, label, cells)
            for case_index, (ci, token) in enumerate(cells):
                number = Decimal(token.replace(',', ''))
                by_case[case_index][key] = number
                values.append(dict(
                    value_id=f'CEMCAP_{case_index+1}_{key}', source_id='PUB-CEMCAP',
                    case_id=cases[case_index], field=key, value=str(number), source_token=token,
                    unit=unit, physical_page=page_number, printed_page=page_number-6,
                    locator=f'Table 5.3; row {label}; case column {case_index+1}',
                    cell_bbox=json.dumps(table.rows[ri].cells[ci]),
                    source_sha256=item['sha256'], source_url=item['source_url'],
                    status='VERIFIED_NATIVE_TABLE_VISUAL_PAGE_CHECKED',
                    use_as_regional_calibrated_input=False))
    write_csv('data/public_capture_values.csv', values)
    inventory = []
    factors = {x['value_id']: Decimal(x['value']) for x in read_csv('data/reference_inventory_inputs.csv')}
    for case_id, p in zip(cases, by_case):
        assert len(p) == len(fields), (case_id, p)
        assert p['total_work_mj_kg'] == p['compression_mj_kg'] + p['auxiliary_mj_kg']
        work = p['total_work_mj_kg'] * 1000 / Decimal('3.6')
        aux = p['auxiliary_mj_kg'] * 1000 / Decimal('3.6')
        compression = p['compression_mj_kg'] * 1000 / Decimal('3.6')
        heat = p['heat_mj_kg']  # MJ/kg equals GJ/t exactly.
        reporting = heat * factors['JP_R8_heat_fallback'] * 1000 + work * factors['JP_R8_electric_fallback'] * 1000
        inventory.append(dict(
            case_id='CEMCAP_' + case_id, source_id='PUB-CEMCAP',
            heat_gj_per_t_captured=str(heat), capture_aux_kwh_per_t_captured=str(aux),
            compression_kwh_per_t_captured=str(compression), electricity_kwh_per_t_captured=str(work),
            cooling_gj_per_t_captured=str(p['cooling_mj_kg']),
            reboiler_temperature_c=str(p['reboiler_c']), steam_pressure_bara=str(p['steam_bara']),
            product_pressure_bar_as_printed=str(p['product_pressure_bar_as_printed']),
            capture_fraction=str(p['capture_fraction']), product_co2_mol_fraction_wet=str(p['product_co2_fraction']),
            solution_makeup_kg_per_t_captured=str(p['solution_makeup_kg_t']),
            jp_reporting_utility_kgco2_per_t=str(reporting),
            heat_factor_id='JP_R8_heat_fallback', electricity_factor_id='JP_R8_electric_fallback',
            heat_electricity_pair_complete_as_reported=True, full_lifecycle=False,
            eligible_for_regional_lca=False,
            scope='European reference cement-plant MEA simulation, Table 5.3. Total work includes capture auxiliaries and compression to 110 bar; no turbine-derate or duplicate compression/liquefaction addition. Cooling heat rejection is retained separately, never converted to electricity without a cooling-system model. Japanese fallback factors are reporting-only sensitivities. Actual steam supplier, upstream/material/cooling supply and ship conditioning remain unresolved.'))
    write_csv('data/public_capture_inventory.csv', inventory)
    return values, inventory


def parse_rsm(text):
    """Read native fixed-width RSM columns, including well identity and locators."""
    lines = text.splitlines()
    series = {}
    for i, line in enumerate(lines):
        if not line.startswith(' TIME'):
            continue
        fields = line.split()
        width = 13
        names = [lines[i+2][1+j*width:1+(j+1)*width].strip() for j in range(len(fields))]
        units = [lines[i+1][1+j*width:1+(j+1)*width].strip() for j in range(len(fields))]
        rows = []
        for row_index in range(i+5, len(lines)):
            tokens = lines[row_index].split()
            if len(tokens) != len(fields):
                break
            try:
                [Decimal(t) for t in tokens]
            except Exception:
                break
            rows.append((tokens, row_index + 1))
        for j, (field, name, unit) in enumerate(zip(fields, names, units)):
            # Region-only fields also need region number; they are deliberately
            # excluded from this targeted well/field extraction.
            if field.startswith('R'):
                continue
            key = (field, name)
            candidate = dict(unit=unit, header_line=i+1,
                             rows=[(t[0], t[j], line_number) for t, line_number in rows])
            if key in series:
                assert [r[:2] for r in series[key]['rows']] == [r[:2] for r in candidate['rows']], key
            else:
                series[key] = candidate
    return series


def extract_reservoir(manifest):
    item = next(x for x in manifest['files'] if x['source_id'] == 'PUB-BJARMELAND')
    with ZipFile(ROOT / item['path']) as z:
        deck_bytes = z.read('Bjarmeland/CO2_BJ_C07B9.DATA')
        deck = deck_bytes.decode('latin1')
        includes = re.findall(r"\bINCLUDE\s+'([^']+)'", re.sub(r'--[^\n]*', '', deck))
        assert len(includes) == 3
        assert all('Bjarmeland/' + name in z.namelist() for name in includes)
        native = z.read('Bjarmeland/CO2_BJ_C07B9.RSM')
        series = parse_rsm(native.decode('latin1'))
        end_report = z.read('Bjarmeland/CO2_BJ_C07B9.ECLEND').decode('latin1')
    selected = [('FGIR', ''), ('FGIT', ''), ('FPR', ''), ('WBHP', 'GI'),
                ('WGIR', 'GI'), ('WGIT', 'GI'), ('WOPR', 'OP2'), ('WWPR', 'OP2'), ('WGPR', 'OP2')]
    times = [x[0] for x in series[('FGIR', '')]['rows']]
    assert all([x[0] for x in series[key]['rows']] == times for key in selected)
    assert all(Decimal(b) > Decimal(a) for a, b in zip(times, times[1:]))
    history = []
    for i, time in enumerate(times):
        row = dict(case_id='CO2_BJ_C07B9', source_id='PUB-BJARMELAND', time_days=time)
        for key in selected:
            field, well = key
            column = field + ('_' + well if well else '')
            row[column] = series[key]['rows'][i][1]
            row[column + '_source_line'] = series[key]['rows'][i][2]
        row['source_member'] = 'Bjarmeland/CO2_BJ_C07B9.RSM'
        history.append(row)
    write_csv('data/public_reservoir_history.csv', history)
    def section_record(keyword, fragment, meaning, value, unit, status):
        lines = deck.splitlines()
        line = next(i+1 for i, text in enumerate(lines) if fragment in text)
        return dict(value_id='BJ_' + meaning, source_id='PUB-BJARMELAND', keyword=keyword,
                    value=value, unit=unit, source_member='Bjarmeland/CO2_BJ_C07B9.DATA',
                    line_1based=line, source_token=fragment, interpretation=meaning,
                    status=status, use_as_regional_calibrated_input=False)
    parameters = [
        section_record('WCONINJE', 'GI    GAS      OPEN   RATE 1.5E6   1*   225', 'injector_pressure_ceiling', 225, 'bar absolute; RSM WBHP BARSA', 'SOURCE_MODEL_CONTROL'),
        section_record('WCONINJE', 'GI    GAS      OPEN   RATE 1.5E6   1*   225', 'injector_surface_rate_target', '1.5E6', 'SM3/day; RSM WGIR', 'SOURCE_MODEL_CONTROL'),
        section_record('RTEMP', '43 /', 'reservoir_temperature', 43, 'degC', 'SOURCE_MODEL_ASSUMPTION'),
        section_record('EQUALS', 'PRESSURE 151 /', 'initial_pressure', 151, 'bar; METRIC deck', 'SOURCE_MODEL_ASSUMPTION'),
        section_record('EQUALS', 'PORO  0.22', 'base_porosity_before_overrides', '.22', 'fraction', 'SOURCE_MODEL_ASSUMPTION'),
        section_record('EQUALS', 'PERMX  900', 'base_horizontal_permeability', 900, 'mD; METRIC deck', 'SOURCE_MODEL_ASSUMPTION'),
        section_record('EQUALS', 'PERMZ  450', 'base_vertical_permeability', 450, 'mD; METRIC deck', 'SOURCE_MODEL_ASSUMPTION'),
    ]
    write_csv('data/public_reservoir_parameters.csv', parameters)
    pressure = [Decimal(x['WBHP_GI']) for x in history]
    rate = [Decimal(x['WGIR_GI']) for x in history]
    summary = dict(
        source_id='PUB-BJARMELAND', case_id='CO2_BJ_C07B9', paired_records=len(history),
        source_rsm_sha256=hashlib.sha256(native).hexdigest(),
        source_deck_sha256=hashlib.sha256(deck_bytes).hexdigest(),
        first_time_days=times[0], last_time_days=times[-1],
        pressure_reference='BARSA: absolute', max_injector_bhp_bar=str(max(pressure)),
        injection_bhp_ceiling_bar=225, records_above_pressure_ceiling=sum(p > 225 for p in pressure),
        rate_unit='SM3/DAY', min_injection_rate=str(min(rate)), max_injection_rate=str(max(rate)),
        rate_target_sm3_day=1500000, records_below_rate_target=sum(q < 1500000 for q in rate),
        cumulative_injected_sm3_as_printed=history[-1]['WGIT_GI'],
        records_at_pressure_ceiling=sum(p == 225 for p in pressure),
        field_well_injection_series_agree=all(x['FGIR']==x['WGIR_GI'] and x['FGIT']==x['WGIT_GI'] for x in history),
        includes_resolved=includes, source_run_end_report=end_report.strip(),
        warnings=json.loads((EVIDENCE/'bjarmeland_warning_excerpts.json').read_text())['warnings'],
        independently_rerun=False, maximum_service_curve_generated=False,
        mass_conversion_performed=False, regional_model_inputs_replaced=False,
        scope='Norwegian public compositional oil/water/gas model with pure-CO2 injection, initial porosity overrides and 150x edge-pore-volume multipliers. Producer OP2 shut until 2030 then opened. Achieved simulation schedule under a rate target and pressure ceiling, not saline-only validation or maximum injectivity. One GI completion is ignored as inactive; six solver-convergence warnings are retained. No mass conversion, interpolation, permanent-retention credit or oil counterfactual is inferred.')
    (ROOT/'outputs/public_reservoir_audit.json').write_text(json.dumps(summary, indent=2)+'\n')
    return summary


def main():
    manifest = verify_sources()
    values, inventory = extract_capture(manifest)
    reservoir = extract_reservoir(manifest)
    summary = dict(capture_located_values=len(values), capture_paired_cases=len(inventory),
                   reservoir_paired_records=reservoir['paired_records'],
                   public_sources_verified=True, complete_lca_generated=False,
                   existing_operational_results_changed=False)
    (ROOT/'outputs/public_evidence_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
