#!/usr/bin/env python3
"""Locate independent published reservoir simulation parameters; no new calibration."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
def main():
 M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset6_manifest.json').read_text())};pages=json.loads((ROOT/M['D6-22']['page_text_path']).read_text());rows=[]
 for key,value,unit,page,token,kind,note in [
 ('stp_reference_pressure',1343,'psia',14,'1,343','Model initial condition','St. Peter reference depth3294ft; do not mix with Mt.Simon reservoir or pressure datum.'),
 ('stp_reference_depth',3294,'ft',14,'3,294','Model reference depth','Reference initial pressure1343psia.'),
 ('stp_initial_gradient',.40,'psi/ft',14,'0.40','Model initial condition','Under-pressured equilibrium assumption based on MDT data.'),
 ('stp_max_bhp',1980,'psia',15,'1,980','Simulation pressure constraint','At3470ft; borrowed fracture-gradient estimate is a source assumption, not a measured Japanese limit.'),
 ('stp_bhp_depth',3470,'ft',15,'3,470','Simulation pressure-constraint depth','St.Peter interval, not IBDP Mt.Simon injection history.'),
 ('stp_simulation_horizon',20,'years',15,'20-year','Simulation design','No extrapolation to30 years or synthetic interpolation of interior years.'),
 ('stp_target_rate',2000000,'tCO2/year',15,'2 million','Simulation target','Target was constrained by maximum bottomhole pressure; not achieved constant flow.'),
 ('stp_rate_first_year',660000,'tCO2/year',21,'660,000','Simulation output','First-year pressure-limited result; not field measurement.'),
 ('stp_rate_last_year',1164000,'tCO2/year',21,'1,164,000','Simulation output','Twentieth-year result; interior annual values are not invented.'),
 ('stp_rate_average',990000,'tCO2/year',20,'990,000','Simulation output','Twenty-year average rate, not maximum at all years.'),
 ('potosi_initial_model_rate',90000,'tCO2/year',21,'90,000','Simulation output','Initial seismic/log-derived model; later model revisions differ strongly.'),
 ('potosi_homogeneous_target',2000000,'tCO2/year',21,'2 million','Revised simulation design/output','Revised homogeneous case reaches target; cannot substitute for initial model or St.Peter history.')]:
  assert token in pages[page-1]
  rows.append(dict(value_id=key,value=value,unit=unit,document_id='D6-22',pdf_page=page,source_token=token,evidence_type=kind,formation='St.Peter' if key.startswith('stp') else 'Knox-Potosi',limitation=note))
 with (ROOT/'data/ibdp_reservoir_reference_values.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 print('Located',len(rows),'simulation-reference quantities, not observed rate/pressure series.')
if __name__=='__main__':main()
