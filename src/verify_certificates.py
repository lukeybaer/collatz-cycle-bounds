"""Independent checker for stored rational and modular certificates.

No search or certificate-generation routines are called. Log(3) is checked
using log(2)+log(3/2), unlike the producer's direct atanh expansion for3.
Profile costs use a longer Taylor sum and finer height rounding.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from exact_intervals import DLO,DHI,L2LO,L2HI

ROOT=Path(__file__).resolve().parents[1]
X=2**71

def read(name):return json.loads((ROOT/'results'/name).read_text(encoding='utf-8-sig'))

def atanh_log(z,terms=180):
    power=z; total=F(0)
    for j in range(terms):
        total+=2*power/(2*j+1);power*=z*z
    return total,total+2*power/((2*terms+1)*(1-z*z))

ln2lo,ln2hi=atanh_log(F(1,3))
ln32lo,ln32hi=atanh_log(F(1,5))
assert L2LO<=ln2lo<ln2hi<=L2HI
assert DLO<=(ln2lo+ln32lo)/ln2hi
assert DHI>=(ln2hi+ln32hi)/ln2lo

_geometries=[F(0)]
def geom(m):
    while len(_geometries)<=m:_geometries.append(1+DHI*_geometries[-1])
    return _geometries[m]

def verify_farey(row):
    k=row['input_K']; cost=F(row['cost']); width=F(row['width'])
    assert width==cost/(k*L2LO)
    lo=DLO;hi=DHI+width; cert=row['farey']
    a,b=cert['left'];c,d=cert['right'];p=cert['p'];q=cert['q']
    assert b>0 and d>=0 and c*b-a*d==1
    assert F(a,b)<=lo and (d==0 or F(c,d)>=hi)
    assert (p,q)==(a+c,b+d) and lo<F(p,q)<hi
    return max(k,q)

verified_caps={}
def verify_capacity(name):
    cert=read(name)
    assert cert.get('kind')!='conditional_block_restart', 'A conditional capacity requires an explicit minimum hypothesis.'
    if name in verified_caps:return verified_caps[name]
    if cert.get('kind')=='uniform_block_restart_native_pair':
        J=cert['J'];c=F(100*J-1,100)
        assert 31<=J<=41 and cert['capacity_certified'] and F(cert['capacity_c'])==c
        assert not cert['conditional_only'] and int(cert['verified_basin'])==X
        assert 71>c/(F(1584962,10**6)-1)
        for dep,expected in cert['dependencies'].items():
            assert hashlib.sha256((ROOT/'results'/dep).read_bytes()).hexdigest()==expected
        for source,expected in cert['source_dependencies'].items():
            assert hashlib.sha256((ROOT/'src'/source).read_bytes()).hexdigest()==expected
        assert cert['audit_source_sha256']==hashlib.sha256((ROOT/'src'/'audit_native_family_proofs.py').read_bytes()).hexdigest()
        from audit_native_family_proofs import audit
        pair=audit(J,cert['producer'],cert['producer_source'],cert['progression'],write=False)
        assert pair['status']=='passed' and not pair['conditional_only']
        assert F(27660,81)*F(140,100)*F(11,10)/F(69,100)**3<1700
        assert 1700*F(153,10)**2+3<2**19
        verified_caps[name]=(None,c);return None,c
    if cert.get('kind')=='uniform_block_restart':
        J=cert['J'];c=F(100*J-1,100)
        assert 31<=J<=41 and cert['capacity_certified'] and F(cert['capacity_c'])==c
        assert int(cert['verified_basin'])==X and 71>c/(F(1584962,10**6)-1)
        for dep,sha in cert['dependencies'].items():
            assert hashlib.sha256((ROOT/'results'/dep).read_bytes()).hexdigest()==sha
        py=read(f'family-J{J}-python-full.json');cov=read(f'extended-capacity-J{J}-coverage-audit.json')
        data=read(f'extended-capacity-J{J}-classes.json');cpp=read(f'family-J{J}-precise-full-result.json')
        meta=read(f'family-J{J}-precise-full-metadata.json')
        assert py['status']=='passed' and py['full_input'] and cov['status']=='passed' and cpp['capacity_exceptions_discharged']
        assert py['source_sha256']==hashlib.sha256((ROOT/'src'/'verify_family_capacity.py').read_bytes()).hexdigest()
        assert cov['source_sha256']==hashlib.sha256((ROOT/'src'/'audit_extended_coverage.py').read_bytes()).hexdigest()
        assert meta['sourceHash'].lower()==hashlib.sha256((ROOT/'src'/'FamilyCapacityPrecise.cs').read_bytes()).hexdigest()
        assert py['input_sha256']==cov['input_sha256']==meta['inputHash'].lower()
        assert py['seeds']==cov['seeds']==cpp['seeds']==data['seed_count']
        assert py['classes']==cov['classes']==cpp['classes']==len(data['classes'])
        for i,(a,b,case) in enumerate(zip(py['rows'],cpp['rows'],data['classes'])):
            assert a['id']==b['id']==i and b['status']=='complete'
            count=int(case['count']);assert count==int(a['seeds'])==int(b['expected'])
            assert sum(int(a[v]) for v in ('restart','basin','singles'))==count
            assert sum(int(b[v]) for v in ('restart_seeds','basin_seeds','singleton_seeds'))==count
        assert F(27660,81)*F(140,100)*F(11,10)/F(69,100)**3<1700
        assert 1700*F(153,10)**2+3<2**19
        verified_caps[name]=(None,c);return verified_caps[name]
    if cert.get('kind')=='uniform_padic_and_basin':
        assert cert['capacity_certified'] and F(cert['capacity_c'])==F(2999,100)
        assert int(cert['verified_basin'])==X
        for dep,sha in cert['dependencies'].items():
            assert hashlib.sha256((ROOT/'results'/dep).read_bytes()).hexdigest()==sha
        audit=read('strong-capacity-J30-audit-python.json')
        assert audit['status']=='passed' and audit['all_python_trajectories_verified'] and audit['two_csharp_paths_agree']
        assert audit['source_sha256']==hashlib.sha256((ROOT/'src'/'audit_strong_capacity.py').read_bytes()).hexdigest()
        assert audit['class_file_sha256']==hashlib.sha256((ROOT/'results'/'strong-capacity-J30-classes.json').read_bytes()).hexdigest()
        assert audit['global_pairs']==7602147 and audit['seeds']==1929307
        assert F(1584962,10**6)<DLO<DHI<F(1584963,10**6)
        assert F(27660,81)*F(11,10)/F(69,100)**3<1200
        assert 1200*F(73,5)**2+3<2**18
        assert 71>F(2999,100)/(DLO-1)
        verified_caps[name]=(None,F(2999,100));return verified_caps[name]
    m=cert['m'];J=cert['loss_integer'];U=int(cert['K_upper_inclusive'])
    assert 91<=m<=515619 and U>F(14784,10000)*m*DHI**m
    expected={(a,ell) for ell in range(1,J) for a in range(1,2**F(12*(J-ell),7).__ceil__(),2)}
    seen=set();maximum=0
    for row in cert['pairs']:
        a,ell,t=row['a'],row['ell'],row['t'];assert (a,ell) in expected and (a,ell) not in seen
        seen.add((a,ell));target=((1-2**ell)*pow(a,-1,2**t))%(2**t)
        assert int(row['target'])==target
        if row['reason']=='not_in_3_power_group':assert t==3 and target not in (1,3)
        else:
            assert row['reason']=='least_positive_exponent_exceeds_upper'
            r,p=int(row['residue']),int(row['period'])
            assert t>=3 and p==2**(t-2) and 0<=r<p and pow(3,r,2**t)==target
            assert (r if r else p)>U
        assert row['B']==max(0,t-ell-1);maximum=max(maximum,row['B'])
    assert seen==expected and maximum==cert['B']
    c=F(J)-F(1,100);margin=71*DLO-maximum-c*(DLO+1)/(DLO-1)
    assert F(cert['capacity_c'])==c and F(cert['dominance_margin_lower'])==margin
    assert cert['capacity_certified'] and margin>0
    verified_caps[name]=(m,c);return m,c

def verify_scoped_capacity(name,minimum):
    cert=read(name)
    if cert.get('kind')!='conditional_block_restart':return verify_capacity(name)
    # Check scope BEFORE consulting the cache: a prior valid use at a large
    # minimum must never authorize a later use below the conditional threshold.
    assert cert['conditional_only'] and cert['capacity_certified']
    assert int(cert['verified_basin'])==X
    cut=int(cert['assumed_cycle_minimum']);assert minimum>=cut>=X
    if name in verified_caps:return verified_caps[name]
    J=cert['J'];c=F(100*J-1,100);assert F(cert['capacity_c'])==c and 31<=J<=41
    for dep,expected in cert['dependencies'].items():
        assert hashlib.sha256((ROOT/'results'/dep).read_bytes()).hexdigest()==expected
    for source,expected in cert['source_dependencies'].items():
        assert hashlib.sha256((ROOT/'src'/source).read_bytes()).hexdigest()==expected
    assert cert['audit_source_sha256']==hashlib.sha256((ROOT/'src'/'audit_native_family_proofs.py').read_bytes()).hexdigest()
    from audit_native_family_proofs import audit
    pair=audit(J,cert['producer'],cert['producer_source'],cert['progression'],cert['minimum_factor'],write=False)
    assert pair['status']=='passed' and pair['conditional_only'] and int(pair['assumed_cycle_minimum'])==cut
    assert F(27660,81)*F(140,100)*F(11,10)/F(69,100)**3<1700
    assert 1700*F(153,10)**2+3<2**19
    verified_caps[name]=(None,c);return None,c

def verify_suffix(rows,m,minimum,initial=1,capacity_c=F(0)):
    gs=[F(0)]+[geom(t) for t in range(1,m+1)]
    k=initial
    for row in rows:
        assert row['input_K']==k
        c=F(row.get('capacity_c','0'));assert c==capacity_c
        heights=[min(512,((F(t*k,m)+c*(gs[t]-t)/(DHI-1))/gs[t]).__floor__()) for t in range(1,m+1)]
        assert row['height_floors']==heights
        terms=[F(1,max(minimum,2**h-1)) for h in heights]
        allowed=[sum(terms,F(0))]
        method=row.get('method','elementary')
        if method in ('two_block','three_block'):
            assert minimum==X, 'merging bounds require the verified basin threshold'
            allowed.append(F(35*m,54*X))
            for s in range(1,m+1):
                r=m-s
                rest=F(0) if r==0 else (F(1,X) if r==1 else F(35*r+19,54*X))
                allowed.append(rest+sum(terms[:s],F(0)))
            if method=='three_block':
                allowed.append(F(97*m,162*X))
                for s in range(1,m+1):
                    r=m-s
                    rest=F(0) if r==0 else (F(1,X) if r==1 else F(97*r+73,162*X))
                    allowed.append(rest+sum(terms[:s],F(0)))
        else:assert method=='elementary'
        assert F(row['cost'])==min(allowed)
        k=verify_farey(row)
    return k

def log2_lower(n):
    h=n.bit_length()-1
    z=F(n-2**h,n+2**h)
    lo,_=atanh_log(z,120)
    return h+lo/ln2hi

def reciprocal_bound(height):
    # A finer downward rounding and longer positive exponential sum than
    # the producer. The resulting rational still bounds the cost ABOVE.
    den=10**35;y=F((min(height,F(512))*den).__floor__(),den)
    h=y.__floor__();precision=10**160
    compact_ln2=F((ln2lo*precision).__floor__(),precision)
    z=(y-h)*compact_ln2
    term=total=F(1)
    # Downward rounding of each positive term preserves a lower exponential
    # sum and avoids growing rational denominators. No tail is subtracted.
    for j in range(1,65):
        term=F((term*z*precision/j).__floor__(),precision);total+=term
    return 1/(2**h*total-1)

def verify_profile(cert,proved_initial,temporary_assumption=None):
    m=cert['m'];N=int(cert['minimum']);k=cert['initial_K']
    if temporary_assumption is None:assert k<=proved_initial[m]
    else:
        assert cert['purpose']=='temporary_lower_assumption_to_prove_upper' and k==temporary_assumption
        assert N==X and int(cert['conclusion_K_less_than'])==k
    c=F(cert.get('capacity_c',str(1-F(1,2**104))))
    if 'capacity_certificate' in cert:
        mm,cc=verify_scoped_capacity(cert['capacity_certificate'],N);assert (mm is None or m==mm) and c==cc
    else:assert c==1-F(1,2**104)
    shift=c/(DHI-1)
    for row in cert['rows']:
        assert row['input_K']==k
        profile=row['profile']
        if profile['mode']=='minimum_only':
            assert F(row['cost'])==F(m,N)
        else:
            assert profile['mode']=='affine_majorization'
            floor=F(profile['floor']);assert 0<floor<=log2_lower(N+1)
            b=floor-shift;assert b>0 and k>m*floor
            r=profile['ramp_length'];assert 1<=r<=m
            base=(k-m*shift-(m-r)*b)/geom(r)
            assert base>=b and (r==m or base<=DHI*b)
            heights=[floor]*(m-r)+[shift+base*DHI**j for j in range(r)]
            terms=list(map(F,profile['terms']));assert len(terms)==m
            for y,term in zip(heights,terms):assert term>=reciprocal_bound(y)
            assert F(row['cost'])==sum(terms,F(0))
        k=verify_farey(row)
    upper=F(14784,10000)*m*DHI**m
    assert int(cert['upper_ceiling'])==upper.__ceil__()
    assert cert['final_K']==k and cert['conditional_contradiction']==(k>upper.__ceil__())

def main():
    proved={};suffix_count=0;profile_count=0
    groups=[read('K-lower-bound-m96.json')]+read('K-lower-bounds-two-block.json')+read('K-lower-bounds-reproduction.json')+read('K-lower-bounds-lifted.json')+read('K-lower-bounds-strong.json')
    for path in sorted((ROOT/'results').glob('K-lower-bounds-family-J*.json')):groups+=read(path.name)
    for path in sorted((ROOT/'results').glob('family-J*-elementary-lower-bounds.json')):groups+=read(path.name)
    for cert in groups:
        m=cert['m'];minimum=int(cert['minimum']);c=F(0)
        if 'capacity_certificate' in cert:
            mm,c=verify_capacity(cert['capacity_certificate']);assert mm is None or m==mm
        rows=cert.get('rows',cert.get('proof'))
        value=verify_suffix(rows,m,minimum,capacity_c=c)
        assert value==cert['K_proved'];proved[m]=max(proved.get(m,1),value);suffix_count+=1
    print('Verified',suffix_count,'initial suffix certificates',flush=True)
    for cert in read('conditional-final-contradictions.json'):
        m=cert['m'];N=int(cert['assumed_minimum_greater_than']);initial=cert['rows'][0]['input_K']
        assert initial<=proved[m]
        k=verify_suffix(cert['rows'],m,N,initial)
        upper=(F(14784,10000)*m*DHI**m).__ceil__()
        assert int(cert['upper_bound_integer_ceiling'])==upper and int(cert['new_K_lower_bound'])==k
        assert cert['conditional_contradiction']==(k>upper);suffix_count+=1
    profile_names=['affine-profile-conditional-certificates.json','envelope-conditional-certificates.json','strong-envelope-conditional-certificates.json']
    profile_names += [p.name for p in sorted((ROOT/'results').glob('family-J*-conditional-certificates.json'))]
    profile_names += [p.name for p in sorted((ROOT/'results').glob('conditional-J*-profile-certificates.json'))]
    for name in profile_names:
        for cert in read(name):
            verify_profile(cert,proved);profile_count+=1
            print('Verified profile',cert['m'],cert.get('minimum_factor'),flush=True)
    upper_count=0
    upper_path=ROOT/'results'/'improved-K-upper-bounds-J35.json'
    if upper_path.exists():
        for cert in read(upper_path.name):
            verify_profile(cert,{},temporary_assumption=cert['initial_K'])
            assert cert['conditional_contradiction'] and cert['initial_K']<int(cert['upper_ceiling'])
            upper_count+=1
    config_count=0
    for path in sorted((ROOT/'results').glob('native-config-m*.json')):
        cfg=json.loads(path.read_text());m=cfg['m'];K=int(cfg['K']);assert K<=proved[m]
        low=int(cfg['low']);high=int(cfg['high']);assert high>=low>=X
        if cfg.get('capacity_method')!='scoped':assert low==X
        else:
            assert low%2==0 and int(cfg['verified_basin'])==X
            assert F(cfg['lower_factor'])*X==low
            assert (F(cfg['upper_factor'])*X).__floor__()==high
        B=(high+1).bit_length()
        if cfg.get('height_upper_method')=='largest_odd':B=(high if high%2 else high-1).bit_length()
        assert cfg['start_log2_upper']==B
        c=F(cfg.get('affine_c','0'))
        if cfg.get('capacity_method')=='lifted':
            capname=Path(cfg['lifted_certificate']).name;mm,cc=verify_capacity(capname);assert (m,c)==(mm,cc)
        elif cfg.get('capacity_method')=='strong':
            capname=Path(cfg['strong_certificate']).name;mm,cc=verify_capacity(capname);assert mm is None and c==cc
        elif cfg.get('capacity_method')=='scoped':
            mm,cc=verify_scoped_capacity(cfg['capacity_certificate'],low)
            assert (mm is None or mm==m) and c==cc
        else:assert c in (F(0),1-F(1,2**104),F(7,3))
        gs=[geom(i) for i in range(m+1)];hs=[(gs[i]-i)/(DHI-1) for i in range(m+1)]
        for i in range(m+1):
            used=(B*gs[i]-c*hs[i]).__ceil__()
            assert int(cfg['prefix_odd_upper'][i])==used
            h=0 if i==m else max(0,((K-used+c*hs[m-i])/gs[m-i]).__floor__())
            h=min(4096,h)
            assert cfg['height_floors'][i]==h
            if cfg.get('fractional_targets') and i<m:
                raw=max(F(0),min(F(4096),(K-used+c*hs[m-i])/gs[m-i]))
                producer_y=F(cfg['height_lower_rationals'][i]);assert 0<=producer_y<=raw
                y=F((raw*10**35).__floor__(),10**35);whole=y.__floor__()
                precision=10**160;ll=F((ln2lo*precision).__floor__(),precision);z=(y-whole)*ll
                term=total=F(1)
                for j in range(1,65):term=F((term*z*precision/j).__floor__(),precision);total+=term
                independent_lower_target=max(low,(2**whole*total).__ceil__()-1)
                assert max(low,2**h-1)<=int(cfg['targets'][i])<=independent_lower_target
            else:assert int(cfg['targets'][i])==max(low,2**h-1)
        config_count+=1
    out={'status':'passed','suffix_certificates':suffix_count,'profile_certificates':profile_count,
         'capacity_certificates':len(verified_caps),'native_configs':config_count,'improved_upper_certificates':upper_count,
         'constants_check':'independent log(3)=log(2)+log(3/2) enclosure',
         'warning':'This verifies finite arithmetic; written analytic proofs and cited external theorems remain dependencies.'}
    (ROOT/'results'/'independent-certificate-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
