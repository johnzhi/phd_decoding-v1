#!/usr/bin/env python3
"""B1-18 printed scaling/skin and structured geometry reconstruction.

No native TOUGH2-MP mesh/connections, Corey/capillary implementation, history
match or prediction reproduced. Source values remain literal. Synthetic error,
radial-flow and pure-water examples are not accepted case calibrations.
"""
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-18.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Decatur history source')
    edge = json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-18_depth_comparison.json').read_text())
    for path_key, sha_key in [('related_path','related_sha256'),('related_input_path','related_input_sha256')]:
        if hashlib.sha256((ROOT/edge[path_key]).read_bytes()).hexdigest() != edge[sha_key]:
            raise ValueError('Stale related-source depth comparison')
    return data, edge


def leverett_factor(k_over_reference, phi_over_reference):
    if not all(math.isfinite(x) and x>0 for x in (k_over_reference,phi_over_reference)):
        raise ValueError('Positive finite permeability and porosity ratios required')
    return math.sqrt(phi_over_reference/k_over_reference)


def skin_permeability_ratio(skin, well_radius, annulus_outer_radius):
    if not all(math.isfinite(x) for x in (skin,well_radius,annulus_outer_radius)):
        raise ValueError('Finite skin/radii required')
    if not 0<well_radius<annulus_outer_radius:
        raise ValueError('Require0<rw<rs')
    logarithm=math.log(annulus_outer_radius/well_radius)
    if logarithm+skin<=0:
        raise ValueError('No finite positive annular permeability for this skin/geometry')
    return logarithm/(logarithm+skin)


def normalized_buildup(buildup, reference_buildup):
    if not all(math.isfinite(x) for x in (buildup,reference_buildup)) or reference_buildup==0:
        raise ValueError('Finite values and nonzero reference buildup required')
    return buildup/reference_buildup


def normalized_gradient(current_pressure_difference, initial_pressure_difference):
    if not all(math.isfinite(x) for x in (current_pressure_difference,initial_pressure_difference)) or initial_pressure_difference<=0:
        raise ValueError('Positive initial lower-minus-upper pressure difference required')
    return current_pressure_difference/initial_pressure_difference


def minmax_normalize(value,lower,upper):
    if not all(math.isfinite(x) for x in (value,lower,upper)) or upper<=lower:
        raise ValueError('Finite value and increasing limits required')
    return (value-lower)/(upper-lower)


def gradient_example_bounds(current_difference, initial_difference, assumed_pressure_error):
    """Conditional four-pressure bounds; no source noise distribution assumed."""
    if assumed_pressure_error<0 or initial_difference<=2*assumed_pressure_error:
        raise ValueError('Assumed error must leave a strictly positive denominator')
    candidates=[(current_difference+a*2*assumed_pressure_error)/(initial_difference+b*2*assumed_pressure_error)
                for a in (-1,1) for b in (-1,1)]
    return min(candidates),max(candidates)


def reconstruct_geometry(data):
    mesh=data['mesh'];radii=[0.0]
    for count,width in zip(mesh['radial_counts'],mesh['radial_widths_m'],strict=True):
        for _ in range(count):radii.append(radii[-1]+width)
    depths=[float(data['model']['bottom_depth_below_MSL_m'])]
    for count,width in zip(mesh['vertical_counts_bottom_up'],mesh['vertical_widths_bottom_up_m'],strict=True):
        for _ in range(count):depths.append(depths[-1]-width)
    rows=[]
    for radial,(ri,ro) in enumerate(zip(radii,radii[1:])):
        for vertical,(bottom,top) in enumerate(zip(depths,depths[1:])):
            per_rad=.5*(ro*ro-ri*ri)*(bottom-top)
            rows.append(dict(geometry_id=f'R{radial:02}Z{vertical:03}',radial_index=radial,vertical_index_bottom_up=vertical,
                             r_inner_m=ri,r_outer_m=ro,depth_top_below_MSL_m=top,depth_bottom_below_MSL_m=bottom,
                             volume_per_radian_m3=per_rad,full_circle_bulk_volume_m3=2*math.pi*per_rad,
                             status='geometric_reconstruction_only_not_native_TOUGH_cell_names_nodes_properties_or_connections'))
    return rows,radii,depths


def depth_comparison(data,edge):
    related=json.loads((ROOT/edge['related_input_path']).read_text())
    ports={p['zone']:p for p in data['physical_geometry']['ports']}
    ground=data['physical_geometry']['VW1_ground_elevation_MSL_m']
    rows=[]
    for old in related['pressures']:
        primary=ports[old['zone']];bgl=primary['depth_below_MSL_m']+ground
        old_converted=old['figure4_depth_ft']*.3048
        rows.append(dict(zone=old['zone'],B1_18_below_MSL_m=primary['depth_below_MSL_m'],B1_18_ground_elevation_MSL_m=ground,
                         B1_18_below_ground_m=bgl,B1_16_figure_depth_ft=old['figure4_depth_ft'],B1_16_figure_depth_converted_m=old_converted,
                         figure_minus_B1_18_below_ground_m=old_converted-bgl,B1_16_prose_depth_m=old['prose_depth_m'],
                         status='related_source_comparison_not_adopted_datum_correction_or_direct_citation_verification'))
    return rows


def source_checks(data,geometry,cross):
    rows=[]
    def add(item,value,unit,locator,note,status='limited_source_arithmetic'):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,calculation_status=status,interpretation=note,
                         scope='not_native_TOUGH_history_match_or_accepted_maximum_service_retention_GHG_input'))
    mesh,model,physical=data['mesh'],data['model'],data['physical_geometry']
    nr=sum(mesh['radial_counts']);nz=sum(mesh['vertical_counts_bottom_up'])
    radius=sum(n*w for n,w in zip(mesh['radial_counts'],mesh['radial_widths_m']))
    height=sum(n*w for n,w in zip(mesh['vertical_counts_bottom_up'],mesh['vertical_widths_bottom_up_m']))
    for item,value,unit in [('radial_cell_count',nr,'radial intervals'),('vertical_cell_count',nz,'vertical intervals'),
                             ('total_geometry_cells',nr*nz,'geometric cells'),('reconstructed_outer_radius',radius,'m'),
                             ('reconstructed_height',height,'m'),('reconstructed_top_MSL_depth',model['bottom_depth_below_MSL_m']-height,'m belowMSL'),
                             ('vertical_resolution_transition_depth',model['bottom_depth_below_MSL_m']-mesh['vertical_counts_bottom_up'][0]*mesh['vertical_widths_bottom_up_m'][0],'m belowMSL'),
                             ('summed_volume_per_radian',sum(r['volume_per_radian_m3'] for r in geometry),'m3/radian geometric'),
                             ('analytic_full_circle_bulk_volume',math.pi*radius**2*height,'m3 bulk under full-circle geometry')]:
        add(item,value,unit,'AppendixA/Table2 p12; Figure2b p6',
            'Source geometry reconstructs67×182=12194 cells. No native node/connection/property/pressure file, pore volume, resource or injection service inferred.','source_geometry_component_reconstructed')
    add('well_cells_with_lateral_connections_if_only4_gap_cells_removed',mesh['high_porosity_well_cells']-mesh['reservoir_disconnected_gap_cells'],
        'cell count under source prose','AppendixA p12','Exact well indices and connection topology remain unverified; not an independently reproduced well implementation.')
    add('conditional_20_one_metre_well_cells_bulk_volume',math.pi*data['skin']['rw_m']**2*mesh['high_porosity_well_cells'],
        'm3 geometric EXAMPLE','AppendixA / analyst geometry','Assumes each specified well cell is in the1m zone; no inferred native storage coefficient or reservoir pore volume.','conditional_well_geometry')
    skin=data['skin'];logarithm=math.log(skin['rs_m']/skin['rw_m']);ratio=skin_permeability_ratio(skin['s'],skin['rw_m'],skin['rs_m'])
    for item,value,unit in [('skin_annulus_log',logarithm,'dimensionless'),('skin_finite_permeability_lower_bound',-logarithm,'dimensionless skin bound'),
                             ('source_skin_above_lower_bound',skin['s']+logarithm,'dimensionless skin margin'),('source_annular_ks_over_k',ratio,'permeability ratio'),
                             ('source_skin_recovered_from_annulus',(1/ratio-1)*logarithm,'dimensionless skin'),
                             ('critical_rs_for_finite_positive_ks',skin['rw_m']*math.exp(-skin['s']),'m conditional threshold')]:
        add(item,value,unit,'Eq2/AppendixA pp6,12','Printed annular component only. Negative skin and largeks/k are not an equal factor in annual reservoir capacity. Exact geometry and calibrated case remain separate.','printed_skin_component_reconstructed')
    for delta in data['analyst_examples']['skin_delta_examples']:
        value=skin_permeability_ratio(skin['s']+delta,skin['rw_m'],skin['rs_m'])
        add(f'analyst_skin_delta_{delta:g}_ks_over_k',value,'ratio at perturbed EXAMPLE skin','Eq2 / analyst perturbation',
            'Sensitivity example, not a confidence interval or measured skin error.','analyst_skin_sensitivity')
    for far in data['analyst_examples']['radial_far_radii_m']:
        clean_log=math.log(far/skin['rw_m']);factor=clean_log/(clean_log+skin['s'])
        add(f'analyst_far_radius_{far:g}_fixed_state_rate_ratio',factor,'single-phase radial rate ratio EXAMPLE','Eq2 / analyst radial identity',
            'Fixed pressure margin/mobility and assumed radius only. Large local permeability factor is not this resistance ratio, a native CO2 model or maximum annual service.','analyst_radial_counterexample')
    for n,example in enumerate(data['analyst_examples']['Leverett_relative_examples'],1):
        add(f'Leverett_relative_example_{n}',leverett_factor(example['k_over_ref'],example['phi_over_ref']),'Pc/Pc_ref ratio EXAMPLE','Eq1 p5',
            'Printed scale factor reconstructed from relative inputs. Berea reference properties/curve, actual units/sign and direction-specific native implementation remain unverified.','printed_Leverett_component_example')
    viscosity_ratio=model['pure_H2O_viscosity_literal_Pa_s']/model['brine_viscosity_literal_Pa_s']
    add('literal_water_to_brine_viscosity_ratio',viscosity_ratio,'ratio','Section3.3 p5','Preserve both printed10^-4 Pa-s values; ratio.7 does not verify absolute viscosities or all salinity effects.')
    add('conditional_inverse_viscosity_scaling',1/viscosity_ratio,'inverse ratio','Section3.3 p5','150mD model/analysis basis remains unresolved; no corrected field permeability adopted.')
    add('capillary_Pmax_in_MPa',model['capillary_Pmax_Pa']/1e6,'MPa CAPILLARY PARAMETER','Section3.3 p5','Not a reservoir fracture/BHP ceiling or pressure-constrained injection service.')
    add('Corey_vs_capillary_Slr_difference',model['Corey_Slr']-model['capillary_Slr'],'saturation fraction difference','Section3.3 p5',
        'Separate relative-permeability/capillary parameterizations. Do not merge them or treat a kr residual as a hard upper bound on every simulated gas saturation.')
    for name,limits in data['log_normalization'].items():
        if isinstance(limits,list):
            add(name+'_normalization_range',limits[1]-limits[0],'API or percentage-point range as key indicates','Figure2 caption p6',
                'Literal caption limits retained. Actual log arrays, facies labels, SDR mapping and native clipping remain unreproduced.')
    for port in physical['ports']:
        if port['zone']<=4:
            add(f'zone{port["zone"]}_physical_BGL_depth',port['depth_below_MSL_m']+physical['VW1_ground_elevation_MSL_m'],'m belowground under source datum','Table1 p3',
                'Physical datum conversion only; model log shift13.1m is a separate imposed alignment.')
            add(f'zone{port["zone"]}_shifted_model_depth',port['depth_below_MSL_m']+model['VW1_log_model_shift_down_m'],'m model depth','Figure2b / Figure5',
                'Candidate if port mapping follows the stated log shift; native sensor extraction remains unverified. Not a corrected physical depth.','conditional_log_to_port_alignment')
    intervals=physical['CCS1_perforations_below_MSL_m']
    for item,value,unit in [('CCS1_gauge_BGL_depth',physical['pressure_gauge_CCS1_depth_below_MSL_m']+physical['CCS1_ground_elevation_MSL_m'],'m belowground'),
                             ('sum_physical_perforated_lengths',sum(b-a for a,b in intervals),'m'),
                             ('whole_perforated_outer_span',intervals[-1][1]-intervals[0][0],'m'),
                             ('gap_between_perforated_intervals',intervals[1][0]-intervals[0][1],'m'),
                             ('gauge_to_upper_perforation_top_interval',intervals[0][0]-physical['pressure_gauge_CCS1_depth_below_MSL_m'],'m')]:
        add(item,value,unit,'Table1 p3','Perforations, active injection-zone thickness, model well cells and gauge have different spatial supports. No pressure-column correction or actual flow inferred.')
    offsets=[r['figure_minus_B1_18_below_ground_m'] for r in cross]
    for item,value in [('related_source_depth_offset_min',min(offsets)),('related_source_depth_offset_max',max(offsets)),('related_source_depth_offset_mean',sum(offsets)/len(offsets))]:
        add(item,value,'m difference between retained labels','B1-18 Table1 vs B1-16 Figure4','Nearly common residual offset is a provenance lead. No guessed KB/datum correction adopted; Zone4 prose conflict stays open.','related_source_depth_comparison_not_citation_edge')
    denominator=data['analyst_examples']['normalized_gradient_example_initial_P_difference_Pa']
    error=data['analyst_examples']['pressure_error_bound_example_Pa']
    for g in (.99,1.01):
        low,high=gradient_example_bounds(g*denominator,denominator,error)
        add(f'analyst_G{g:g}_conditional_lower',low,'normalized gradient EXAMPLE','Sections3.2,4.2 / analyst error example','Assumed±1000Pa bound per measurement is NOT the reported practical resolution or a verified error distribution. No actual flow-sign uncertainty inferred.','analyst_assumed_error_example')
        add(f'analyst_G{g:g}_conditional_upper',high,'normalized gradient EXAMPLE','Sections3.2,4.2 / analyst error example','Demonstrates role of numerator/baseline uncertainty near unity; source raw errors remain missing.','analyst_assumed_error_example')
    add('analyst_reference_drop_spike_ratio',normalized_buildup(.2,.05),'ratio for synthetic buildup','Figure3 / analyst example','A delayed upper response divided by falling reference can spike without new plume height. Not an extracted field point.','analyst_normalization_example')
    return rows


def main():
    import CoolProp
    import CoolProp.CoolProp as CP
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    data,edge=load_inputs();geometry,radii,depths=reconstruct_geometry(data);cross=depth_comparison(data,edge)
    checks=source_checks(data,geometry,cross);property_checks=[]
    for pressure in data['analyst_examples']['pure_water_reference_pressure_Pa']:
        viscosity=CP.PropsSI('V','T',data['model']['temperature_C']+273.15,'P',pressure,'Water')
        property_checks.append(dict(temperature_C=data['model']['temperature_C'],pressure_Pa=pressure,pure_water_viscosity_Pa_s=viscosity,
                                    ratio_to_literal_pure_H2O=viscosity/data['model']['pure_H2O_viscosity_literal_Pa_s'],
                                    status='independent_pure_water_unit_reference_not_actual_brine_or_corrected_author_input'))
    out=ROOT/'outputs/comprehensive_review'
    for name,rows in [('B1-18_checks.csv',checks),('B1-18_depth_comparison.csv',cross),('B1-18_water_unit_reference.csv',property_checks)]:
        with (out/name).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=list(geometry[0]),lineterminator='\n');writer.writeheader();writer.writerows(geometry)
    (out/'B1-18_geometry.csv.gz').write_bytes(gzip.compress(stream.getvalue().encode(),mtime=0))
    fig,axes=plt.subplots(1,2,figsize=(10,5.5))
    for ax in axes:
        ax.vlines(radii,min(depths),max(depths),lw=.4,color='steelblue',alpha=.65)
        ax.hlines(depths,0,max(radii),lw=.35,color='gray',alpha=.45)
        ax.set(ylabel='Depth below MSL (m)',xlabel='Radius (m)')
        ax.invert_yaxis()
    axes[0].set_xscale('log');axes[0].set_xlim(.12,1e5);axes[0].set_ylim(1974,1420)
    axes[0].set_title('Full radial geometry\n(centre column omitted on log axis)',fontsize=10)
    axes[1].set_xlim(0,1.5);axes[1].set_ylim(1942,1914)
    axes[1].set_title('Near-well geometry\n(native connection mapping open)',fontsize=10)
    for a,b in data['physical_geometry']['CCS1_perforations_below_MSL_m']:
        axes[1].axhspan(a,b,color='orange',alpha=.16)
    fig.suptitle('Independent geometry reconstruction from B1-18 Appendix A')
    fig.text(.1,.015,'67 radial × 182 vertical intervals. No native TOUGH node/property/connection files inferred.\nOrange: reported physical perforation intervals; not a reconstruction of model well-cell assignments.',fontsize=8)
    fig.tight_layout(rect=(0,.065,1,.95));fig.savefig(out/'B1-18_geometry.png',dpi=180);plt.close(fig)
    result=dict(study_id='B1-18',source_sha256=data['source_sha256'],check_count=len(checks),geometry_cells=len(geometry),
                components_reconstructed=['AppendixA structured radial/vertical geometry','Eq2 annular permeability/skin relation','Eq1 dimensionless Leverett scale'],
                native_TOUGH_mesh_connections_or_forward_case_reproduced=False,native_history_match_or_prediction_reproduced=False,accepted_inputs_changed=False,
                software=dict(CoolProp=CoolProp.__version__,gitrevision=CP.get_global_param_string('gitrevision'),backend='HEOS/Water',viscosity_BibTeX=CP.get_fluid_param_string('Water','BibTeX-VISCOSITY')),
                viscosity_interpretation='Literal absolute viscosity values are onHOLD; ratio.7 retained. Pure-water reference differs by roughly10x but does not repair native input or brine properties.',
                related_source_comparison=edge,missing=data['missing'])
    (out/'B1-18_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
