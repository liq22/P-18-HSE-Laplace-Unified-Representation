"""Regenerate the source-supported posterior schematic as editable SVG/PDF/PNG.

The diagram is a proposed inference organization, not an experimental result.
No model/data execution or raster image embedding occurs. Every box, connector
and text object has a semantic ID. Requires cairosvg for PDF/PNG export.
"""
from pathlib import Path
import argparse
import xml.etree.ElementTree as ET
import cairosvg

NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)

def make(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    root=ET.Element('{'+NS+'}svg',viewBox='0 0 1800 1380',width='180mm',height='138mm',role='img')
    def node(tag,parent=root,**attrs):
        return ET.SubElement(parent,'{'+NS+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
    node('title').text='Which missing components may an industrial posterior infer?'
    node('desc').text='Source supports and conditional identification determine the eligible missing target. HSE conditions projected Latent Laplace Diffusion, while observed evidence is retained and globally unsupported outputs are omitted. Separate measurements test posterior, diagnosis, support compliance and attribution.'
    node('style').text='text{font-family:DejaVu Sans,sans-serif;fill:#1f2b3b;font-size:27px}.title{font-size:39px;font-weight:700}.head{font-size:31px;font-weight:700}.small{font-size:23px}.core{font-size:32px;font-weight:700}.muted{fill:#536171}'
    defs=node('defs')
    for name,col in [('arrow','#536171'),('eligible','#157a85')]:
        marker=node('marker',parent=defs,id=name,markerWidth=12,markerHeight=12,refX=10,refY=6,orient='auto',markerUnits='userSpaceOnUse')
        node('path',parent=marker,d='M0,0 L12,6 L0,12 Z',fill=col)
    node('rect',id='canvas',x=0,y=0,width=1800,height=1380,fill='white')
    def text(identity,x,y,lines,cls='',gap=35,anchor='start'):
        t=node('text',id=identity,x=x,y=y,**{'class':cls,'text-anchor':anchor})
        for i,line in enumerate(lines):node('tspan',parent=t,x=x,dy=0 if i==0 else gap).text=line
    def box(identity,x,y,w,h,fill='#f5f7fa',stroke='#aab5c3'):
        node('rect',id=identity,x=x,y=y,width=w,height=h,rx=10,fill=fill,stroke=stroke,stroke_width=2)
    def arrow(identity,path,eligible=False):
        node('path',id=identity,d=path,fill='none',stroke='#157a85' if eligible else '#536171',stroke_width=3,marker_end='url(#eligible)' if eligible else 'url(#arrow)')
    text('main-title',40,62,['Infer the supported missing state — not every missing coordinate'],'title')
    text('subtitle',40,105,['Acquisition support and conditional identifiability determine the generative target.'],'small')
    box('panel-a',40,140,840,365)
    text('panel-a-heading',64,186,['a  Establish the source reference'],'head')
    text('panel-a-note',64,225,['Aligned coordinates; source datasets are not paired events'],'small')
    xs=[400,515,630,745]
    for x,name in zip(xs,['mode 1','mode 2','mode 3','mode 4']):text('column-'+name.replace(' ','-'),x,275,[name],'small',anchor='middle')
    labels=['Source A','Source B','Current view']
    supports=[[1,1,0,0],[1,0,1,0],[1,1,0,0]]
    for row,(label,mask) in enumerate(zip(labels,supports)):
        y=303+row*53;text('row-name-'+str(row),70,y+29,[label])
        for col,value in enumerate(mask):
            box(f'support-{row}-{col}',xs[col]-29,y,58,39,'#d7ecef' if value else '#eceff3','#80949d')
            text(f'support-value-{row}-{col}',xs[col],y+29,[str(value)],anchor='middle')
    text('roles-label',65,484,['Current role:'],'small')
    for x,role in zip(xs,['common','private','missing','global-null']):text('role-'+role,x,484,[role],'small',anchor='middle')
    box('panel-b',920,140,840,365)
    text('panel-b-heading',944,186,['b  Qualify the missing target'],'head')
    text('qualification-lines',953,236,['Missing in the current acquisition','AND observable in the declared source experiment','AND an identified conditional law'],'',gap=44)
    arrow('permission-arrow','M1330,351 L1330,381',True)
    box('eligible-target',964,393,749,75,'#e0f2ef','#157a85')
    text('eligible-target-text',1338,439,['Eligible subspace Iₑ; fixed projector Gₑ'],'core',anchor='middle')
    box('panel-c',40,545,1720,550)
    text('panel-c-heading',64,594,['c  Proposed HSE–LLapDiff inference'],'head')
    box('observed-input',75,645,310,154)
    text('observed-input-title',99,687,['Industrial history'],'head')
    text('observed-input-lines',99,728,['Values + times + mask','Acquisition descriptor aₑ'],'small')
    arrow('input-to-hse','M385,721 L427,721')
    box('hse-condition',445,645,320,154,'#ece8f4','#806b98')
    text('hse-title',471,687,['HSE condition'],'head')
    text('hse-lines',471,728,['Physical support features','Global moment anchor'],'small')
    arrow('hse-to-generative','M765,721 L835,721',True)
    box('llapdiff-core',855,645,445,197,'#e0f2ef','#157a85')
    text('llapdiff-title',885,688,['LLapDiff posterior'],'core')
    text('llapdiff-lines',885,733,['Gaussian latent perturbation','Stable temporal mode synthesis','Eligible-only reverse updates'],'small',gap=37)
    arrow('roles-to-generation','M1330,505 L1330,612 L1080,612 L1080,635',True)
    text('permission-tag',1067,569,['roles + identification'],'small')
    arrow('posterior-output-arrow','M1300,742 L1343,742',True)
    box('posterior-output',1362,645,365,276,'#edf3f8','#63829b')
    text('posterior-title',1387,689,['Posterior features'],'head')
    text('posterior-lines',1387,738,['Observed evidence','Eligible posterior samples','Support + inference status'],'small',gap=40)
    text('posterior-no-guarantee',1387,887,['Source-trained diagnosis'],'small')
    arrow('preserved-observed-path','M605,799 L605,889 L1343,889')
    text('preserve-evidence',652,874,['Preserve observed evidence and its uncertainty'],'small')
    box('unsupported-output',75,956,740,90,'#f0f0f1','#8f9299')
    text('unsupported-lines',100,992,['Globally unsupported / unidentified missing:','no value labelled as recovered'],'small',gap=32)
    box('laplace-boundary',855,956,872,90,'#fff6e9','#b7976e')
    text('laplace-boundary-text',880,992,['Laplace dynamics ≠ Laplace-distributed noise','A physical support mask requires a validated latent-to-mode map.'],'small',gap=32)
    box('panel-d',40,1135,1720,200)
    text('panel-d-heading',64,1182,['d  Test consequences separately'],'head')
    items=[('posterior-metric',75,'Posterior quality',['Same eligible target','Energy Score / known-law KL']),
           ('diagnosis-metric',496,'Unseen-dataset diagnosis',['Original-group LODO','Macro-F1 + balanced accuracy']),
           ('support-metric',917,'Support compliance',['Unsupported emissions','Eligible coverage + utility']),
           ('attribution-metric',1338,'Mechanism and cost',['R / H_A / H_M controls','Gaussian / mixture / diffusion'])]
    for ident,x,title,lines in items:
        text(ident+'-title',x,1230,[title],'small')
        text(ident+'-detail',x,1270,lines,'small',gap=31)
    text('footer',40,1370,['Schematic design and explicit tests; no expected performance curves.'],'small')
    svg=ET.tostring(root,encoding='unicode')
    (output/'motivation.svg').write_text(svg,encoding='utf-8')
    cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(output/'motivation.pdf'))
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(output/'motivation.png'),output_width=4252,output_height=3260)
    return root

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    args=p.parse_args(); make(args.output_dir)
    print('Editable SVG, vector PDF and 600-dpi PNG:',args.output_dir)
