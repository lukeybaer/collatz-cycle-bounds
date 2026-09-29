"""Render the standalone analytic note for mathematical review.

Uses ReportLab and Matplotlib mathtext; scratch images remain under work/.
The Markdown derivation is the complete readable source of the paper.
"""
from pathlib import Path
import hashlib,html,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[1]/'work'
sys.path.insert(0,str(WORK/'pdf-libs'))
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,KeepTogether

SCRATCH=WORK/'analytic-pdf';SCRATCH.mkdir(parents=True,exist_ok=True)
for name,file in [('TimesCustom','times.ttf'),('TimesCustom-Bold','timesbd.ttf'),
                  ('TimesCustom-Italic','timesi.ttf'),('TimesCustom-BoldItalic','timesbi.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('TimesCustom',normal='TimesCustom',bold='TimesCustom-Bold',
                             italic='TimesCustom-Italic',boldItalic='TimesCustom-BoldItalic')
BODY=ParagraphStyle('Body',fontName='TimesCustom',fontSize=10.7,leading=13.8,
                    spaceAfter=7,alignment=TA_JUSTIFY)
HEADING=ParagraphStyle('Heading',parent=BODY,fontName='TimesCustom-Bold',fontSize=12.5,
                       leading=16,spaceBefore=12,spaceAfter=8,keepWithNext=True)
TITLE=ParagraphStyle('Title',parent=BODY,fontName='TimesCustom-Bold',fontSize=21,
                     leading=25,spaceAfter=14,alignment=TA_CENTER)
META=ParagraphStyle('Meta',parent=BODY,fontSize=9.5,leading=12,alignment=TA_CENTER,
                    textColor=colors.HexColor('#444444'),spaceAfter=12)
SMALL=ParagraphStyle('Small',parent=BODY,fontSize=9.1,leading=12)
GREEK={'delta':'δ','beta':'β','epsilon':'ε','lambda':'λ','Phi':'Φ','Lambda':'Λ','ell':'ℓ','mu':'μ'}

def prose(s):
    s=html.escape(s)
    for word,char in GREEK.items():s=re.sub(r'(?<![A-Za-z])'+word+r'(?![A-Za-z])',char,s)
    s=s.replace('&lt;=','≤').replace('&gt;=','≥').replace('!=','≠')
    s=re.sub(r'\^\(([^()]*)\)',r'<super>\1</super>',s)
    s=re.sub(r'\^(-?\d+|[A-Za-zα-ωℓ])',r'<super>\1</super>',s)
    s=re.sub(r'_\(([^()]*)\)',r'<sub>\1</sub>',s)
    s=re.sub(r'_([A-Za-z]+|\d+)',r'<sub>\1</sub>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="TimesCustom-Italic">\1</font>',s)
    s=re.sub(r'(?<!\S)\*([^*]+)\*(?=[,.\s]|$)',r'<i>\1</i>',s)
    s=s.replace('*','·')
    return s

def tex(s):
    s=s.strip()
    if s=='A_1=9, A_2=2^((24/7)(J+1)).':
        return r'$A_1=9,\qquad A_2=2^{(24/7)(J+1)}$'
    # Non-formula labels inside the parameter display are set upright.
    labels={'valuation base':r'valuation\ base','theorem parameter':r'theorem\ parameter',
            'exponents':'exponents','and':'and','for':'for'}
    for word,rendered in labels.items():
        s=re.sub(r'\b'+word+r'\b',lambda m:r'\quad\mathrm{'+rendered+r'}\ ',s)
    for word in ('delta','beta','epsilon','lambda','Phi','Lambda','ell','mu'):
        s=re.sub(r'\b'+word+r'\b',lambda m:'\\'+word,s)
    s=re.sub(r'\balpha_',r'\\alpha_',s)
    s=re.sub(r'\bln(?=[(28\d]|\b)',r'\\ln\,',s)
    s=s.replace('log_2',r'\log_2').replace('v_2',r'\nu_2').replace('v_8',r'\nu_8')
    s=s.replace('sqrt',r'\sqrt').replace('max(',r'\max(')
    s=s.replace('<=',r'\leq ').replace('>=',r'\geq ').replace('!=',r'\ne ')
    s=s.replace('*',r'\cdot ')
    s=re.sub(r'\^\(([^()]*)\)',r'^{\1}',s)
    s=re.sub(r'\^(-?\d+)',r'^{\1}',s)
    s=re.sub(r'_\(([^()]*)\)',r'_{\1}',s)
    s=s.replace('_min',r'_{\min}')
    # Adjacent spelled-out symbols need a separating token before replacement.
    s=s.replace('2delta',r'2\delta').replace('4ln',r'4\ln').replace('2ln',r'2\ln')
    s=s.replace('13.3a_0',r'13.3a_0')
    s=s.rstrip('.')
    return '$'+s+'$'

equations=[]
def equation(line):
    formula=tex(line)
    name=hashlib.sha256(formula.encode()).hexdigest()[:20]+'.png'
    path=SCRATCH/name
    matplotlib.rcParams['mathtext.fontset']='stix'
    math_to_image(formula,str(path),prop=FontProperties(size=11.3),dpi=300,format='png',color='black')
    with PILImage.open(path) as im:w,h=im.size
    width,height=w*72/300,h*72/300
    if width>459:
        height*=459/width;width=459
    item=Image(str(path),width=width,height=height);item.hAlign='CENTER'
    equations.append({'source':line.strip(),'tex':formula,'width_points':width})
    return item

source=ROOT/'sharper-exponential-bound.md'
lines=source.read_text(encoding='utf-8').splitlines()
story=[];i=0;first=True
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('# '):
        story.append(Paragraph(prose(line[2:]),TITLE));i+=1;continue
    if line.startswith('## '):
        story.append(Paragraph(prose(line[3:]),HEADING));i+=1;continue
    if line.startswith('    '):
        block=[Spacer(1,2)]
        while i<len(lines) and lines[i].startswith('    '):
            block.extend([equation(lines[i]),Spacer(1,3)]);i+=1
        story.append(KeepTogether(block));continue
    paragraph=[]
    while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','    ')):
        paragraph.append(lines[i]);i+=1
    joined=' '.join(paragraph)
    if first:
        joined='Private working draft prepared for Luke Baer with Codex | 29 September 2026. Independent mathematical review and priority investigation pending.'
    # Long source URLs become clickable bibliographic labels in the PDF.
    joined=re.sub(r'https://doi.org/10.1023/A:1015825809661',
        'DOI: 10.1023/A:1015825809661',joined)
    joined=re.sub(r'https://math.deweger.net/\S+', 'Author-hosted version 1.44.',joined)
    joined=joined.replace('https://arxiv.org/abs/2209.00275','arXiv:2209.00275.')
    style=META if first else (SMALL if joined.startswith(('[1]','[2]','[3]')) else BODY)
    first=False
    rendered=prose(joined)
    rendered=rendered.replace('DOI: 10.1023/A:1015825809661',
        '<link href="https://doi.org/10.1023/A:1015825809661">DOI: 10.1023/A:1015825809661</link>')
    rendered=rendered.replace('Author-hosted version 1.44.',
        '<link href="https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf">Author-hosted version 1.44.</link>')
    rendered=rendered.replace('arXiv:2209.00275.',
        '<link href="https://arxiv.org/abs/2209.00275">arXiv:2209.00275.</link>')
    item=Paragraph(rendered,style)
    following=i
    while following<len(lines) and not lines[following].strip():following+=1
    if following<len(lines) and lines[following].startswith('    '):item.keepWithNext=True
    story.append(item)

OUT=ROOT/'collatz-exponential-growth-review.pdf'
def page(canvas,doc):
    canvas.saveState()
    canvas.setFont('TimesCustom',8.5);canvas.setFillColor(colors.HexColor('#666666'))
    if doc.page>1:canvas.drawString(76.5,758,'An explicit smaller growth base for Collatz blocks')
    canvas.drawString(76.5,32,'Private working draft | 29 September 2026 | Independent review pending')
    canvas.drawRightString(535.5,32,str(doc.page))
    canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),rightMargin=76.5,leftMargin=76.5,
                      topMargin=49,bottomMargin=48,title='An explicit smaller growth base for Collatz blocks',
                      author='Prepared for Luke Baer with Codex',pageCompression=1)
doc.build(story,onFirstPage=page,onLaterPages=page)
(SCRATCH/'equations.json').write_text(json.dumps(equations,indent=2),encoding='utf-8')
print(OUT,flush=True)
