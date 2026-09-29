"""Complete J40 consequences, including contradictions reached before profiling.

The freeze script already produced the valid capacity descriptor before its
optional floating-point exploration exhausted a precomputed Farey list.
This continuation uses exact arithmetic throughout and does not rewrite it.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
from exact_intervals import cycle_lower_bound,DHI
from affine_profile_certificates import certificate
import verify_certificates as check

ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results';X=2**71
CAP='family-capacity-J40-native-pair-certificate.json';C=F(3999,100)
assert check.verify_capacity(CAP)==(None,C)
def existing(name):
    p=R/name
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else []
lower=existing('K-lower-bounds-family-J40-native-pair.json')
profiles=existing('family-J40-native-pair-conditional-certificates.json')
direct=existing('family-J40-direct-contradictions.json');unavailable=[]
def save(name,data):
    (R/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
for m in range(96,111):
    upper=(F(14784,10000)*m*DHI**m).__ceil__()
    previous=next((r for r in lower if r['m']==m),None)
    if previous:k,rows=previous['K_proved'],previous['rows']
    else:k,rows=cycle_lower_bound(m,X,method='elementary',capacity_c=C,stop_upper=upper)
    assert check.verify_suffix(rows,m,X,capacity_c=C)==k
    if previous is None:lower.append({'m':m,'minimum':str(X),'K_proved':k,'rows':rows,'capacity_certificate':CAP})
    save('K-lower-bounds-family-J40-native-pair.json',lower)
    if k>upper:
        if not any(r['m']==m for r in direct):direct.append({'m':m,'K_proved':str(k),'upper_ceiling':str(upper),'status':'contradiction_at_verified_basin'})
        save('family-J40-direct-contradictions.json',direct)
        print('DIRECT SUFFIX CONTRADICTION',m,k,'>',upper,flush=True)
        continue
    if m>106:continue
    previous_profile=next((r for r in profiles if r['m']==m),None)
    if previous_profile:
        check.verify_profile(previous_profile,{m:k})
        continue
    lo,hi=1,128;cache={}
    def trial(factor):
        if factor not in cache:cache[factor]=certificate(m,factor*X,k,C)
        return cache[factor]['conditional_contradiction']
    if not trial(hi):
        unavailable.append({'m':m,'maximum_factor_tested':hi,'status':'no_profile_contradiction_in_tested_range'})
        print('NO PROFILE CONTRADICTION',m,'at factor',hi,flush=True)
        continue
    while lo<hi:
        mid=(lo+hi)//2
        if trial(mid):hi=mid
        else:lo=mid+1
    trial(lo);row=cache[lo]
    row.update(capacity_certificate=CAP,minimum_factor=lo,
               warning='Conditional until the complete minimum window is excluded.')
    check.verify_profile(row,{m:k})
    profiles.append(row);save('family-J40-native-pair-conditional-certificates.json',profiles)
    print('EXACT PROFILE',m,lo,row['final_K'],flush=True)
save('family-J40-consequences-audit.json',{
    'status':'passed','capacity_certificate':CAP,'direct_contradictions':direct,
    'profiles':[[r['m'],r['minimum_factor']] for r in profiles],
    'unavailable_profiles':unavailable,
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'Internally checked arithmetic consequences. Written proof and external inputs still require review.'})
