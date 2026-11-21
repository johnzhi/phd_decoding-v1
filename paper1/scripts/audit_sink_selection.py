#!/usr/bin/env python3
"""B2-01 published decision-tree inference and limited dimensional checks.

No native ICCSEM optimization, training/accuracy validation, dynamic reservoir or
complete avoidance-cost model reproduced. Tree outputs are not optimal labels.
"""
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-01.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale sink-selection source')
    edge=json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-01_citation_check.json').read_text())
    for path,sha in [('citing_path','citing_sha256'),('cited_path','cited_sha256')]:
        if hashlib.sha256((ROOT/edge[path]).read_bytes()).hexdigest()!=edge[sha]:
            raise ValueError('Stale cited-source check')
    return data,edge


def predict(tree,features):
    if any(not math.isfinite(v) or v<=0 for v in features.values()):
        raise ValueError('Positive finite ratios/costs required')
    if 'R' in features and not 0<features['R']<1:
        raise ValueError('Finite small-sink scenario requires0<R<1')
    current=tree;trace=[]
    while 'outcome' not in current:
        feature=current['feature'];value=features[feature]
        branch='ge' if value>=current['threshold'] else 'lt'
        trace.append(dict(node=current['id'],feature=feature,value=value,threshold=current['threshold'],branch=branch))
        current=current[branch]
    return dict(outcome=current['outcome'],leaf_id=current['id'],trace=trace,
                scope='printed_inference_only_not_native_optimality_or_accuracy_validation')


def entropy(counts):
    if not counts or any(not math.isfinite(c) or c<0 for c in counts) or sum(counts)<=0:
        raise ValueError('Nonnegative finite counts with positive total required')
    total=sum(counts)
    return -sum((c/total)*math.log2(c/total) for c in counts if c)


def geometry_threshold(L1,L2):
    if not all(math.isfinite(x) and x>0 for x in (L1,L2)):
        raise ValueError('Positive finite source-sink distances required')
    return math.acos(min(L1/(2*L2),L2/(2*L1)))


def well_capital(flow_Mtpa,injectivity_Mtpa_per_well,well_MAUD):
    if not all(math.isfinite(x) and x>0 for x in (flow_Mtpa,injectivity_Mtpa_per_well,well_MAUD)):
        raise ValueError('Positive finite flow,injectivity and wellcost required')
    return flow_Mtpa/injectivity_Mtpa_per_well*well_MAUD


def inference_grid(data):
    rows=[]
    for scenario,keys in [('scenario1',['L2_over_L1','I1_over_I2','W']),('scenario2',['R','L2_over_L1','I1_over_I2','W'])]:
        grid=data['grid1' if scenario=='scenario1' else 'grid2']
        for values in itertools.product(*(grid[k] for k in keys)):
            features=dict(zip(keys,values,strict=True));result=predict(data['trees'][scenario],features)
            rows.append(dict(scenario=scenario,R=features.get('R',''),L2_over_L1=features['L2_over_L1'],
                             I1_over_I2=features['I1_over_I2'],W=features['W'],outcome=result['outcome'],leaf_id=result['leaf_id'],
                             trace=json.dumps(result['trace'],separators=(',',':')),native_optimal_label='',
                             scope='published_diagram_inference_on_feature_grid; no_training_labels_or_accuracy_test'))
    return rows


def calculate(data):
    rows=[];a=data['assumptions']
    def add(item,value,unit,locator,status,note):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,status=status,interpretation=note,
                         scope='not_native_ICCSEM_or_accepted_physical_service_retention_GHG_input'))
    for flow in data['grid1']['F']:
        add(f'F{flow}_25year_mass',flow*a['life_years']/1000,'Gt','Table1/Section2.2 pp2–4','unit_component',
            'Constant suppliedflow over25years; physical cumulative stock, not maximum feasible reservoir service.')
    for R in data['grid2']['R']:
        add(f'R{R:g}_earliest_fullflow_fill',R*a['life_years'],'year','Nomenclature/Table1','unit_component',
            'Earliest fill if entire constantflow enters smallsink; not an optimized SWITCH date or BOTH allocation.')
    case=data['case2'];R=1000*case['C1_Gt']/(a['life_years']*case['F'])
    add('case2_dimensionally_converted_R',R,'dimensionless','Nomenclature/Table4 pp2,9','HOLD_GT_MT_NOTATION',
        'C1[Gt] must be converted toMt before dividing by25F[Mt]. Literal mixed-unit quotient omits1000; source Table4 supportsR=.5.')
    for name,scenario in [('case1','scenario1'),('case2','scenario2')]:
        allowed=('R','L2_over_L1','I1_over_I2','W')
        features={k:v for k,v in data[name].items() if k in allowed}
        result=predict(data['trees'][scenario],features)
        add(name+'_published_tree_outcome',result['outcome'],'class','Figures6/8/Table4 pp7–9','published_inference_reconstructed',
            'Matches reported example class only. Not an independently optimized route or validation accuracy.')
        add(name+'_comparison_count',len(result['trace']),'tree decisions','Figures6/8','published_inference_reconstructed','Literal>=/< boundaries retained; no retraining or new optimal labels.')
    for i,(r1,r2) in enumerate(zip(data['timing']['case1_tree_s'],data['timing']['case2_tree_s'],strict=True),1):
        add(f'case1_reported_time_speedup_v{i}',data['timing']['case1_ICCSEM_s']/r1,'ratio','Table5 p9','reported_output_arithmetic','Rounded source timing, not a fresh benchmark or hardware-independent complexity guarantee.')
        add(f'case2_reported_time_speedup_v{i+4}',data['timing']['case2_ICCSEM_s']/r2,'ratio','Table5 p9','reported_output_arithmetic','Cost of training/label generation not supplied; timings do not validate prediction quality.')
    min_I,max_I=a['injectivity_stated_Mtpa_per_well_range']
    add('minimum_ratio_within_stated_absolute_I_range',min_I/max_I,'ratio','Table1/Section2.2 pp3–4','HOLD_ABSOLUTE_GRID_MAPPING','Minimum.2 exceeds listed Scenario1 ratio1/6 and Scenario2 ratio.1; absolute pairing/case mapping missing.')
    add('Figure5_I1_minus_stated_minimum',data['figure5']['I1']-min_I,'Mtpa/well','Figure5 p6 / Section2.2','HOLD_EXAMPLE_DOMAIN','Illustrative.125 lies below stated.3Mtpa/well minimum; do not force it into training inputs.')
    fig=data['figure4'];anchor=fig['sink1_storage_AUD_per_t'][0]
    for ratio,label in zip(fig['injectivity_ratios'],fig['sink1_storage_AUD_per_t'],strict=True):
        capital=well_capital(fig['F'],ratio*fig['I2'],fig['W'])
        add(f'Figure4_ratio{ratio:g}_linear_well_capital',capital,'MAUD upfront component','Section2.2/Figure4 pp4–5','printed_well_cost_component',
            'F/I timesW with no interference or integer rounding; not complete discounted storage cost or calibrated injection physics.')
        predicted=anchor*fig['injectivity_ratios'][0]/ratio
        add(f'Figure4_ratio{ratio:g}_conditional_inverse_I_label_residual',predicted-label,'AUD/t','Figure4/Section2.2','HOLD_STORAGE_COST_BREAKDOWN',
            'Anchored to printed3.4 at ratio.1; assumes common cost timing and same-pipeline denominator. Middle bars do not follow inverseI; native decomposition needed. No corrected bar adopted.')
    for ratio in sorted(set(data['grid1']['L2_over_L1']+data['grid2']['L2_over_L1'])):
        add(f'ratio{ratio:g}_valid_angle_threshold',math.degrees(geometry_threshold(1,ratio)),'degree','Section2.1/5 pp2,9','analyst_geometry_derivation',
            'From law ofcosines: cos(theta)<min(L1/(2L2),L2/(2L1)). Handles ratios where one printed arccos argument exceeds1; does not validate network shortcut optimality.')
    for counts in ([4,0],[2,2],[1,1,1]):
        add('analyst_entropy_'+str(counts),entropy(counts),'bit','Eq4 p5 / analyst counts','analyst_entropy_example','0log0 limit handled; not actual training entropy, held-out error or physical safety probability.')
    ex=data['analyst_counterexample'];well1=well_capital(ex['F_Mtpa'],ex['I1_Mtpa_per_well'],ex['W_MAUD']);well2=well_capital(ex['F_Mtpa'],ex['I2_Mtpa_per_well'],ex['W_MAUD'])
    for multiplier in ex['common_pipeline_multipliers']:
        costs=[multiplier*p+w for p,w in zip(ex['pipeline_costs_MAUD'],(well1,well2),strict=True)]
        add(f'analyst_common_multiplier{multiplier}_cost_difference',costs[0]-costs[1],'MAUD synthetic','Section3.3 p8 / analyst counterexample','analyst_cost_tradeoff_counterexample',
            'Common multiplier on pipeline costs does not multiply wellcost; ranking can reverse with unchanged distance/injectivity ratios. Not an original ICCSEM case or measured price scenario.')
    add('average_recompression_30percent_effect',data['recompression_statement']['average_transport_share']*.3*100,'percent','Section3.3 p8','conditional_share_arithmetic','9%average share times30%=2.7%average. Source4.5%maximum can use another share; no contradiction inferred from average versus maximum.')
    return rows


def main():
    data,edge=load_inputs();rows=calculate(data);grid=inference_grid(data);out=ROOT/'outputs/comprehensive_review'
    for name,values in [('B2-01_checks.csv',rows),('B2-01_published_tree_grid.csv',grid)]:
        with (out/name).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(values[0]),lineterminator='\n');writer.writeheader();writer.writerows(values)
    result=dict(study_id='B2-01',source_sha256=data['source_sha256'],diagnostic_count=len(rows),inference_grid_rows=len(grid),
                components_reconstructed=['Published Figures6/8 inference with literal branch boundaries','Linear F/I timesW well-capital component','Entropy/unit/timing arithmetic'],
                native_ICCSEM_optimization_or_tree_training_accuracy_reproduced=False,physical_reservoir_or_retention_model_reproduced=False,
                accepted_inputs_changed=False,citation_check=edge,missing=data['missing'])
    (out/'B2-01_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
