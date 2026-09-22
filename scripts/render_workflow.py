"""Render the README figure. Optional dependency: matplotlib (pip install matplotlib)."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(15, 6.4))
fig.patch.set_facecolor('white')
ax.set(xlim=(0, 15), ylim=(0, 6.4))
ax.axis('off')
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ink, muted, rule = '#202B36', '#53616E', '#D8DFE5'
blue, teal, purple = '#356D98', '#387F79', '#766392'

def text(x, y, s, size=11, color=ink, weight='normal', ha='left', va='center'):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight, ha=ha, va=va, linespacing=1.6)

def line(x1,y1,x2,y2,color=rule,lw=1):
    ax.plot([x1,x2],[y1,y2],color=color,lw=lw)

def box(x,y,w,h,color=rule,fill='white',lw=1.2):
    ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor=color,lw=lw))

def arrow(x1,y1,x2,y2,color=muted):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=13,lw=1.25,color=color))

def panel(x,letter,title,subtitle,color):
    text(x,5.92,letter,17,weight='bold')
    text(x+.34,5.92,title,15,weight='bold')
    text(x,5.48,subtitle,10.5,muted)
    line(x,5.13,x+4.15,5.13,color,1.5)

panel(.5,'a','Discover','Daily search → concise email briefing',blue)
panel(5.02,'b','Select','Your reply determines what is saved',teal)
panel(9.56,'c','Read & retain','Linked references and English notes',purple)
line(4.82,1.03,4.82,6.12)
line(9.36,1.03,9.36,6.12)

# Source documents
for x,y in [(.89,3.87),(1.03,3.75),(1.17,3.63)]:
    box(x,y,.66,.9,blue)
    for d in [.22,.36,.50]:line(x+.12,y+.9-d,x+.52,y+.9-d,blue,.8)
text(2.08,4.27,'Research literature',12,weight='bold')
text(2.08,3.89,'Publishers · PubMed\nPreprints',10.5,muted)
arrow(2.54,3.51,2.54,3.05)
box(.9,1.45,3.35,1.48,blue, '#F5F8FC')
text(1.1,2.67,'DAILY PAPER BRIEFING',9,blue,'bold')
for i,y in enumerate([2.29,1.94,1.59],1):
    text(1.13,y,str(i),10,blue,'bold')
    line(1.42,y,3.99 if i!=2 else 3.58,y, '#8197A9',1.7)
text(2.57,1.12,'Headline · takeaway · relevance',9.5,muted,ha='center')
arrow(4.27,2.72,5.4,3.92)

# Selection and verification
box(5.42,3.59,3.55,.94,teal,'#F3F9F7')
text(5.62,4.27,'EMAIL REPLY',9,teal,'bold')
text(5.62,3.91,'“Save papers 1 and 3.”',12,weight='bold')
arrow(7.19,3.57,7.19,2.91)
box(5.42,1.55,3.55,1.29,teal)
text(7.19,2.49,'Resolve & verify',12,weight='bold',ha='center')
text(7.19,2.01,'Match the original issue\nCheck DOI · reuse existing items',10.3,muted,ha='center')
text(7.19,1.11,'Or add a title / DOI directly in chat',9.5,muted,ha='center')
arrow(7.19,1.28,7.19,1.52)
line(8.99,2.24,9.64,2.24,muted,1.25)
line(9.64,2.24,9.64,4.10,muted,1.25)
arrow(9.64,4.10,9.95,4.10)

# Reference record and note
box(9.97,3.69,4.0,.84,purple,'#F8F6FA')
text(10.17,4.25,'ZOTERO',9,purple,'bold')
text(10.17,3.91,'papers collection · metadata · PDF¹',11)
arrow(11.97,3.65,11.97,3.22,purple)
text(12.15,3.45,'Item link',9,muted)
box(9.97,1.26,4.0,1.93,purple)
text(10.17,2.96,'OBSIDIAN',9,purple,'bold')
text(10.17,2.66,'NM: Original paper title',11,weight='bold')
line(10.17,2.44,13.77,2.44)
text(10.17,2.20,'Journal · date · IF · authors',10.3,muted)
text(10.17,1.87,'Key takeaway + why it matters',10.3,muted)
text(10.17,1.54,'One source figure¹',10.3,muted)

line(.5,.78,14.0,.78)
text(.5,.44,'Agent-assisted workflow',10,weight='bold')
text(3.15,.44,'Daily reply check  •  Duplicate checks  •  Resumable imports',10,muted)
text(14,.44,'¹ When available',9,muted,ha='right')
for extension in ['svg','png']:
    fig.savefig(ROOT/'assets'/f'workflow.{extension}',dpi=180,facecolor='white')
plt.close(fig)
