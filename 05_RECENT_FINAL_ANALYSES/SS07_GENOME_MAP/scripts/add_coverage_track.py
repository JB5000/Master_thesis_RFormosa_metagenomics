import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=[]
for line in (root/'coverage/SS-07_S_24_04_16_10kb_mean_depth.tsv').read_text().splitlines():
    c,s,e,v=line.split('\t'); d.append((c,int(s),float(v)))
offset={'ctg11872':0,'ctg158740':2759014}
x=json.loads((root/'proksee_variants/SS-07_MIMAG_RNA.cgview.json').read_text())
c=x['cgview']; pos=[offset[a]+b for a,b,v in d]; scores=[v for a,b,v in d]
c['plots']=[{'name':'Read depth (10-kb windows; S_24_04_16; display capped at 250x)','source':'read-depth-10kb','positions':pos,'scores':scores,'baseline':0,'axisMin':0,'axisMax':250,'legend':'Read depth (0–250x)','favorite':True}]
c['legend']['items'].append({'name':'Read depth (0–250x)','swatchColor':'rgba(126,34,206,1)','decoration':'arc'})
c['tracks'].insert(0,{'name':'Read depth (10-kb windows; S_24_04_16; display capped at 250x)','position':'outside','dataType':'plot','dataMethod':'source','dataKeys':'read-depth-10kb','thicknessRatio':4.5})
(root/'proksee_variants/SS-07_MIMAG_RNA_coverage.cgview.json').write_text(json.dumps(x,indent=2)+'\n')
