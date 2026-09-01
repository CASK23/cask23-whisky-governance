#!/usr/bin/env python3
import json
from pathlib import Path

src=Path('PROJECT_ZERO_SENSORY_MASTER.json')
out=Path('PROJECT_ZERO_SENSORY_GAP_LIST_v1.1.json')
data=json.loads(src.read_text(encoding='utf-8'))
rows=data['records']
assert len(rows)==262
ids=[r['beverageId'] for r in rows]
assert len(set(ids))==262

gaps=[]
for r in rows:
    desc=list(r.get('descriptors') or [])
    note=r.get('tastingNarrative')
    status=r.get('governanceStatus')
    reasons=[]
    if status=='ABSENT_UNRESOLVED': reasons.append('ABSENT_UNRESOLVED')
    if status=='WITHHELD': reasons.append('WITHHELD')
    if not desc and note: reasons.append('MISSING_DESCRIPTORS_HAS_NARRATIVE')
    if desc and not note: reasons.append('MISSING_NARRATIVE_HAS_DESCRIPTORS')
    if reasons:
        gaps.append({
            'beverageId':r['beverageId'],
            'officialName':r['officialName'],
            'currentDescriptors':desc,
            'currentDescriptorFamilies':r.get('descriptorFamilies') or {},
            'currentTastingNarrative':note,
            'currentGovernanceStatus':status,
            'withholdReasons':r.get('withholdReasons') or [],
            'sources':r.get('sources') or [],
            'gapReasons':reasons,
        })

payload={
  'project':'PROJECT_ZERO_SENSORY_GAP_LIST',
  'version':'1.1-pre-research',
  'sourceMasterVersion':data.get('version'),
  'recordCount':len(gaps),
  'metrics':{
    'absentUnresolved':sum(1 for r in rows if r.get('governanceStatus')=='ABSENT_UNRESOLVED'),
    'withheld':sum(1 for r in rows if r.get('governanceStatus')=='WITHHELD'),
    'missingDescriptorsHasNarrative':sum(1 for r in rows if not (r.get('descriptors') or []) and r.get('tastingNarrative')),
    'missingNarrativeHasDescriptors':sum(1 for r in rows if (r.get('descriptors') or []) and not r.get('tastingNarrative')),
  },
  'records':gaps,
}
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(payload['metrics']|{'recordCount':len(gaps)},indent=2))
