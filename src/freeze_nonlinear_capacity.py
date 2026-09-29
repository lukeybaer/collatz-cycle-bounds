"""Freeze a nonlinear map only after two complete algorithms and exact audits."""
from pathlib import Path
import json,hashlib,argparse
from audit_nonlinear_capacity import audit
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
NAME='nonlinear-capacity-plateau-c3799-c4099-h71-certificate.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main(progression,source):
    path=R/NAME;assert not path.exists(),'Refusing to overwrite a frozen certificate'
    pair=audit(progression=progression,progression_source=source)
    pair_name='nonlinear-capacity-proof-pair-audit.json'
    cert={'kind':'nonlinear_block_restart_native_pair','capacity_certified':True,
          'map_id':pair['map_id'],'linear_coefficient_certified':False,'conditional_only':False,
          'verified_basin':str(2**71),'domain_height_floor':71,
          'definition':'max(delta*y-c1,min(delta*y-c0,y+h*(delta-1)-c0))',
          'parameters':{'c0':'3799/100','c1':'4099/100','h':71,'delta':'log2(3)'},
          'producer':pair['producer'],'progression':progression,'progression_source':source,
          'scope':'Positive Collatz orbit segments avoiding the verified basin; hence all hypothetical nontrivial positive cycles.',
          'proof_notes':['../nonlinear-envelope-lemma.md','../block-restart-capacity.md','../padic-capacity-program.md'],
          'full_python_proof':False,'independent_proof':'Complete inverse-residue and progression-index proofs; sampled Python trajectory checks and exhaustive exact threshold audits.',
          'audit_source_sha256':sha(ROOT/'src'/'audit_nonlinear_capacity.py'),
          'source_dependencies':pair['source_dependencies'],
          'dependencies':dict(pair['dependencies'],**{pair_name:sha(R/pair_name)})}
    path.write_text(json.dumps(cert,indent=2)+'\n')
    print('FROZEN',path,flush=True)
    # Rerun the independent forward profile construction; do not merely flip
    # provisional flags without validating their arithmetic and dependencies.
    from audit_nonlinear_profiles import main as audit_profiles
    audit_profiles()
    proposals=R/'nonlinear-profile-proposals.json';check=R/'nonlinear-profile-proposals-audit.json'
    rows=json.loads(proposals.read_text());validated=json.loads(check.read_text())
    assert validated['status']=='passed' and validated['input_sha256']==sha(proposals)
    for row in rows:
        row.update(capacity_map_proved=True,capacity_certificate=NAME,
                   capacity_certificate_sha256=sha(path),requires_minimum_search=row['minimum_factor']>1,
                   proposal_source_sha256=sha(proposals),proposal_audit_sha256=sha(check),
                   warning='The nonlinear map and profile arithmetic are internally certified. A minimum factor above1 still requires a complete finite exclusion. Mathematical review and priority checks remain pending.')
    (R/'nonlinear-profile-certificates.json').write_text(json.dumps(rows,indent=2)+'\n')
    print('Bound verified nonlinear profiles:',[(r['m'],r['minimum_factor']) for r in rows],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--progression',default='nonlinear-clipped-progression-full')
    p.add_argument('--progression-source',default='ClippedNonlinearProgressionVerifier.cs')
    a=p.parse_args();main(a.progression,a.progression_source)
