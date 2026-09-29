"""Typeset the complete fourth-power manuscript without altering its source."""
from pathlib import Path
import hashlib,html,json,re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether,Table,TableStyle

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT.parents[1]/'work'/'research-paper-pdf';WORK.mkdir(parents=True,exist_ok=True)
for name,file in [('ResearchTimes','times.ttf'),('ResearchTimes-Bold','timesbd.ttf'),
                  ('ResearchTimes-Italic','timesi.ttf'),('ResearchTimes-BoldItalic','timesbi.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('ResearchTimes',normal='ResearchTimes',bold='ResearchTimes-Bold',
                             italic='ResearchTimes-Italic',boldItalic='ResearchTimes-BoldItalic')
BODY=ParagraphStyle('Body',fontName='ResearchTimes',fontSize=10.7,leading=13.7,
                    spaceAfter=7,alignment=TA_JUSTIFY)
HEAD=ParagraphStyle('Heading',parent=BODY,fontName='ResearchTimes-Bold',fontSize=12.5,
                    leading=16,spaceBefore=12,spaceAfter=8,keepWithNext=True)
TITLE=ParagraphStyle('Title',parent=BODY,fontName='ResearchTimes-Bold',fontSize=20,
                     leading=24,spaceAfter=13,alignment=TA_CENTER)
META=ParagraphStyle('Metadata',parent=BODY,fontSize=9.3,leading=12,alignment=TA_CENTER,
                    textColor=colors.HexColor('#505050'),spaceAfter=13)
DISPLAY=ParagraphStyle('Equation',parent=BODY,fontSize=11,leading=15.4,
                      alignment=TA_CENTER,spaceAfter=3)
REF=ParagraphStyle('Reference',parent=BODY,fontSize=9.4,leading=12.3)
GREEK={'delta':'δ','beta':'β','epsilon':'ε','lambda':'λ','Phi':'Φ','Lambda':'Λ',
       'ell':'ℓ','alpha':'α','gamma':'γ','Psi':'Ψ'}
URL_LABELS={
 'https://doi.org/10.1017/S0305004199003692':'DOI 10.1017/S0305004199003692',
 'https://irma.math.unistra.fr/~bugeaud/travaux/shopuissdef.ps':'Author-hosted complete PostScript',
 'https://math.deweger.net/papers/%5B35a%5DSidW-3n%2B1-v1.44%5B2010%5D.pdf':'Author-hosted version 1.44',
 'https://arxiv.org/abs/2209.00275':'arXiv:2209.00275',
 'https://www.rs.tus.ac.jp/sutjmath/_userdata/41-1/03-luca.pdf':'Luca: publisher PDF',
 'https://doi.org/10.1007/s11227-025-07337-0':'Barina: DOI 10.1007/s11227-025-07337-0',
 'https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html':'Hercher: journal article and corrigendum',
 'https://doi.org/10.5281/zenodo.21670936':'Wang: Zenodo 21670936',
 'https://doi.org/10.1023/A:1015825809661':'Bugeaud 2002: DOI 10.1023/A:1015825809661'}

def powers(s):
    """Preserve nested parentheses in exponent notation."""
    out='';i=0
    while i<len(s):
        if s[i:i+2]=='^(':
            j=i+2;depth=1
            while j<len(s) and depth:
                depth+=(s[j]=='(')-(s[j]==')');j+=1
            assert depth==0,s
            out+='<super>'+powers(s[i+2:j-1])+'</super>';i=j
        elif s[i]=='^':
            match=re.match(r'-?\d+|[A-Za-zα-ωℓ]',s[i+1:]);assert match,s
            out+='<super>'+match[0]+'</super>';i+=1+len(match[0])
        else:out+=s[i];i+=1
    return out

def rich(s):
    links={}
    codes={}
    def protect(match):
        token=f'CODETOKEN{len(codes)}END';codes[token]=match[1];return token
    s=re.sub(r'`([^`]+)`',protect,s)
    for j,(url,label) in enumerate(URL_LABELS.items()):
        token=f'LINKTOKEN{j}END';links[token]=(url,label);s=s.replace(url,token)
    s=html.escape(s)
    s=s.replace('==&gt;','implies').replace('&lt;=','≤').replace('&gt;=','≥')
    for word,char in GREEK.items():
        s=re.sub(r'(?<![A-Za-z])'+word+r'(?![A-Za-z])',char,s)
    s=s.replace('2delta','2δ').replace('ln2','ln 2').replace('ln3','ln 3')
    s=s.replace('ln800','ln 800').replace('ln264','ln 264').replace('ln10000','ln 10000').replace('ln100','ln 100').replace('ln11','ln 11')
    s=s.replace('lnN','ln N').replace('lnb','ln b').replace('lnJ','ln J').replace('lnu','ln u')
    s=powers(s)
    s=re.sub(r'_\(([^()]*)\)',r'<sub>\1</sub>',s)
    s=re.sub(r'_([A-Za-z]+|\d+)',r'<sub>\1</sub>',s)
    s=re.sub(r'_([+-])',r'<sub>\1</sub>',s)
    s=s.replace('*','·')
    s=re.sub(r'`([^`]+)`',r'<i>\1</i>',s)
    for token,(url,label) in links.items():
        s=s.replace(token,f'<link color="#174c73" href="{html.escape(url,quote=True)}">{html.escape(label)}</link>')
    for token,value in codes.items():s=s.replace(token,'<font face="Courier" size="8">'+html.escape(value)+'</font>')
    return s

source=ROOT/'collatz-paper.md'
lines=source.read_text(encoding='utf-8').splitlines()
story=[];i=0;first=True;reference=False;display_count=0;reference_start=None
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('# '):
        story.append(Paragraph(rich(line[2:]),TITLE));i+=1
        story.append(Paragraph('Prepared for Luke Baer with Codex | 29 September 2026<br/>Private research draft - independent mathematical review pending',META))
        continue
    if line.startswith('### '):
        sub=ParagraphStyle('Subheading',parent=HEAD,fontSize=11,leading=14,spaceBefore=9)
        story.append(Paragraph(rich(line[4:]),sub));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            cells=[c.strip() for c in lines[i].strip('|').split('|')];i+=1
            if all(re.fullmatch(r':?-+:?',c) for c in cells):continue
            rows.append(cells)
        columns=len(rows[0]);assert all(len(r)==columns for r in rows)
        cell=ParagraphStyle('Cell',parent=BODY,fontSize=8.7,leading=11,alignment=0,spaceAfter=0)
        header=ParagraphStyle('TableHeader',parent=cell,fontName='ResearchTimes-Bold')
        formatted=[[Paragraph(rich(v),header if j==0 else cell) for v in row] for j,row in enumerate(rows)]
        weights={7:[.65,1.35,1.0,.7,.7,.5,1.35],4:[.35,1.2,1.4,2.7]}.get(columns,[1]*columns)
        widths=[478*w/sum(weights) for w in weights]
        table=Table(formatted,colWidths=widths,repeatRows=1,hAlign='CENTER')
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf2f5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#68808f')),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#68808f')),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.extend([Spacer(1,5),table,Spacer(1,8)]);continue
    if line.startswith('## '):
        reference=line[3:]=='Primary references'
        if reference:reference_start=len(story)
        story.append(Paragraph(rich(line[3:]),HEAD));i+=1;continue
    if line.startswith('    '):
        block=[Spacer(1,2)]
        while i<len(lines) and lines[i].startswith('    '):
            block.append(Paragraph(rich(lines[i].strip()),DISPLAY));i+=1;display_count+=1
        block.append(Spacer(1,3))
        if story and getattr(story[-1],'_next_display',False):block.insert(0,story.pop())
        story.append(KeepTogether(block));continue
    paragraph=[]
    while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','    ','|')):
        paragraph.append(lines[i]);i+=1
    joined=' '.join(paragraph)
    item=Paragraph(rich(joined),REF if reference else BODY)
    j=i
    while j<len(lines) and not lines[j].strip():j+=1
    if j<len(lines) and lines[j].startswith('    '):item._next_display=True
    story.append(item)

# Explicitly group a heading with the next content item. ReportLab's ordinary
# keepWithNext may lose the connection when that item is itself KeepTogether.
grouped=[];index=0
while index<len(story):
    item=story[index]
    if isinstance(item,Paragraph) and item.style.name in ('Heading','Subheading') and index+1<len(story):
        item.keepWithNext=0
        following=story[index+1]
        content=following._content if isinstance(following,KeepTogether) else [following]
        grouped.append(KeepTogether([item,*content]));index+=2
    else:grouped.append(item);index+=1
story=grouped

OUT=ROOT/'collatz-research-paper.pdf'
def page(canvas,doc):
    canvas.saveState();canvas.setFont('ResearchTimes',8.5)
    canvas.setFillColor(colors.HexColor('#666666'))
    if doc.page>1:canvas.drawString(67,758,'Collatz block growth and finite-cycle exclusions')
    canvas.drawString(67,32,'Private research draft | 29 September 2026 | Independent review pending')
    canvas.drawRightString(545,32,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),rightMargin=67,leftMargin=67,
                      topMargin=49,bottomMargin=48,title='Explicit Collatz block-growth bounds and finite-cycle exclusions',
                      author='Prepared for Luke Baer with Codex',pageCompression=1)
doc.build(story,onFirstPage=page,onLaterPages=page)
receipt={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'pdf_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'display_lines':display_count,
         'scope':'Complete typesetting of the Markdown manuscript; mathematical review remains pending.'}
(WORK/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(OUT,flush=True)
