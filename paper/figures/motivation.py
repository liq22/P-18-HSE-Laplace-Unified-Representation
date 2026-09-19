"""Draw the problem concept and method overview as editable SVG/PDF/600-dpi PNG.

One drawing source owns both figures. Neutral blocks are inherited components;
colored blocks identify this paper's target qualification and restricted process.
The figures are schematics, not empirical performance panels.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import cairosvg

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def draw(output: Path, name: str) -> None:
    height = 640 if name == 'motivation' else 1320
    root = ET.Element(f'{{{NS}}}svg', viewBox=f'0 0 1800 {height}',
                      width='180mm', height=f'{height / 10}mm', role='img')

    def node(tag, parent=root, **attrs):
        return ET.SubElement(parent, f'{{{NS}}}{tag}',
                             {k.replace('_', '-'): str(v) for k, v in attrs.items()})

    node('title').text = ('Observation overlap and conditional identification' if name == 'motivation'
                          else 'Source-qualified conditional latent inference')
    node('desc').text = ('Problem-only source support and two indistinguishable binary worlds.'
                         if name == 'motivation' else
                         'Source preparation, measured evidence, observed uncertainty, restricted reverse updates and diagnosis.')
    node('style').text = ('text{font-family:DejaVu Sans,sans-serif;fill:#243345;font-size:27px}'
                         '.title{font-size:37px;font-weight:700}.head{font-size:30px;font-weight:700}'
                         '.small{font-size:24px}.role{font-size:21px}.label{font-size:25px;font-weight:700}')
    defs = node('defs')
    marker = node('marker', parent=defs, id='arrow', markerWidth=12, markerHeight=12,
                  refX=10, refY=6, orient='auto', markerUnits='userSpaceOnUse')
    node('path', parent=marker, d='M0,0 L12,6 L0,12 Z', fill='#526778')
    node('rect', id='canvas', x=0, y=0, width=1800, height=height, fill='white')

    def text(identity, x, y, lines, cls='', gap=35, anchor='start'):
        t = node('text', id=identity, x=x, y=y, **{'class': cls, 'text-anchor': anchor})
        for i, line in enumerate(lines):
            node('tspan', parent=t, x=x, dy=0 if i == 0 else gap).text = line

    def box(identity, x, y, w, h, new=False, dashed=False):
        attrs = dict(id=identity, x=x, y=y, width=w, height=h, rx=8,
                     fill='#e3f1ee' if new else '#f3f5f7',
                     stroke='#347b74' if new else '#8b9aa7', stroke_width=2)
        if dashed:
            attrs['stroke_dasharray'] = '9 6'
        node('rect', **attrs)

    def arrow(identity, path, dashed=False):
        attrs = dict(id=identity, d=path, fill='none', stroke='#526778',
                     stroke_width=2.8, marker_end='url(#arrow)')
        if dashed:
            attrs['stroke_dasharray'] = '9 6'
        node('path', **attrs)

    if name == 'motivation':
        text('concept-title', 35, 55, ['Observation overlap does not identify every conditional'], 'title')
        box('support-panel', 35, 105, 825, 420)
        box('ambiguity-panel', 905, 105, 860, 420)
        text('support-heading', 60, 152, ['a  Source-relative observation support'], 'head')
        text('support-scope', 60, 192, ['Aligned coordinates; events are not paired across sources'], 'small')
        xs = [390, 515, 640, 755]
        for j, (x, label) in enumerate(zip(xs, ['C', 'P', 'M', 'N₀'])):
            text(f'coordinate-{j}', x, 240, [label], 'label', anchor='middle')
        for i, (label, support) in enumerate([
            ('Source A', [1, 1, 0, 0]), ('Source B', [1, 0, 1, 0]),
            ('Current view', [1, 1, 0, 0])]):
            y = 268 + 60 * i
            text(f'source-name-{i}', 65, y + 32, [label])
            for j, value in enumerate(support):
                box(f'support-{i}-{j}', xs[j] - 27, y, 54, 43, new=bool(value))
                text(f'value-{i}-{j}', xs[j], y + 32, [str(value)], anchor='middle')
        for j, (x, role) in enumerate(zip(xs, ['common', 'private', 'missing', 'global-null'])):
            text(f'role-{j}', x, 490, [role], 'role', anchor='middle')
        text('ambiguity-heading', 930, 152, ['b  Identical source laws, opposite answers'], 'head')
        text('bit-assumptions', 930, 198, ['C and P are independent fair bits'], 'small')
        box('world-plus', 935, 223, 350, 76)
        box('world-minus', 1320, 223, 415, 76)
        text('plus-law', 1110, 270, ['World +: M = P'], anchor='middle')
        text('minus-law', 1527, 270, ['World −: M = 1 − P'], anchor='middle')
        text('equal-source-laws', 935, 346, ['p₊(O_src) = p₋(O_src)',
                                         'Same common-view conditional p(M | C)'], 'small', gap=38)
        text('different-full-conditionals', 935, 440,
             ['p₊(M=1 | C=1,P=1) = 1', 'p₋(M=1 | C=1,P=1) = 0'], gap=38)
        text('problem-object', 35, 579,
             ['Required object: the joint target p(zₒ,w₀ | C_F), under the complete available observation.'], 'label')
        text('concept-boundary', 35, 622,
             ['Support is a geometric property. Conditional identification depends on the source observation law.'], 'small')
    else:
        text('overview-title', 35, 55, ['Source-qualified conditional latent inference'], 'title')
        box('legend-inherited', 1155, 25, 34, 28)
        text('legend-inherited-text', 1203, 49, ['Inherited'], 'small')
        box('legend-proposed', 1385, 25, 34, 28, new=True)
        text('legend-proposed-text', 1435, 49, ['Proposed restriction'], 'small')
        text('source-heading', 35, 111, ['a  Source-only preparation'], 'head')
        box('source-reference', 35, 145, 490, 157, dashed=True)
        text('source-reference-title', 60, 187, ['Recordings and reference'], 'label')
        text('source-reference-content', 60, 227,
             ['Split original groups first', 'Reference targets are training-only'], 'small')
        arrow('source-to-target', 'M525,224 L578,224', dashed=True)
        box('qualified-target', 595, 145, 600, 157, new=True, dashed=True)
        text('qualified-target-title', 620, 187, ['Joint target + actual condition'], 'label')
        text('qualified-target-content', 620, 227,
             ['Joint source tuple (C_F,zₒ,w₀)', 'Bₑ = Qₑ null(AₑQₑ); Gₑ = BₑBₑᵀ'], 'small')
        arrow('target-to-source-fit', 'M1195,224 L1248,224', dashed=True)
        box('source-fit', 1265, 145, 500, 157, dashed=True)
        text('source-fit-title', 1290, 187, ['Fit and freeze on sources'], 'label')
        text('source-fit-content', 1290, 227,
             ['Anchor, observed readout, head', 'Trainable generator; fixed readouts'], 'small')
        text('deployment-heading', 35, 380, ['b  Deployment: no reference target or target labels'], 'head')
        box('measured-input', 35, 425, 350, 135)
        text('measured-title', 60, 466, ['Measured record C_F'], 'label')
        text('measured-content', 60, 507, ['Values / times / masks', 'Acquisition descriptor a'], 'small')
        arrow('input-to-hse', 'M385,492 L435,492')
        box('hse-condition', 450, 425, 345, 135)
        text('hse-title', 475, 466, ['HSE + moment anchor'], 'label')
        text('hse-content', 475, 507, ['Generative condition C_T', 'R / H_A / H_M control'], 'small')
        box('sampler', 850, 415, 915, 440, new=True)
        text('sampler-heading', 875, 456, ['Eligible-only reverse process'], 'head')
        text('sampler-initialization', 875, 495, ['Initialize w_K ~ N(0,I); zₒ fixed within each draw'], 'small')
        box('reverse-state', 880, 535, 240, 115, new=True)
        text('state-title', 900, 573, ['State w_k'], 'label')
        text('state-content', 900, 612, ['Bₑw_k'], 'small')
        arrow('state-to-denoiser', 'M1120,592 L1155,592')
        box('temporal-denoiser', 1170, 535, 270, 115)
        text('denoiser-title', 1190, 573, ['Time denoiser'], 'label')
        text('denoiser-content', 1190, 610, ['Physical time t', 'Ordinary / Laplace'], 'small', gap=30)
        arrow('denoiser-to-conversion', 'M1440,592 L1470,592')
        box('velocity-conversion', 1485, 535, 250, 115)
        text('conversion-title', 1505, 573, ['Convert v̂'], 'label')
        text('conversion-content', 1505, 611, ['ŵ₀ = αw_k − σv̂', 'ε̂ = σw_k + αv̂'], 'small', gap=30)
        arrow('conversion-to-update', 'M1610,650 L1610,708')
        box('restricted-update', 1200, 723, 535, 97, new=True)
        text('update-title', 1220, 759, ['DDIM update in the admitted basis'], 'label')
        text('update-content', 1220, 798, ['w_s = α_s ŵ₀ + σ_s ε̂; z_s = Bₑw_s'], 'small')
        arrow('reverse-loop', 'M1200,771 L1000,771 L1000,665')
        text('reverse-loop-label', 1018, 709, ['next k = s'], 'small')
        arrow('condition-to-denoiser', 'M625,425 L625,400 L1305,400 L1305,522')
        arrow('qualified-target-to-sampler', 'M895,302 L895,331 L1748,331 L1748,407', dashed=True)
        text('basis-edge-label', 1340, 322, ['Frozen target / basis'], 'small')
        arrow('input-to-observed-readout', 'M210,560 L210,625')
        box('observed-readout', 35, 642, 350, 165)
        text('observed-title', 60, 684, ['Observed uncertainty'], 'label')
        text('observed-content', 60, 725, ['qₒ(zₒ | C_F)', 'Sample zₒ once per draw', 'No clean-value clamping'], 'small', gap=31)
        arrow('observed-draw-to-sampler', 'M385,724 L837,724')
        text('observed-edge-label', 454, 707, ['Same zₒ in every reverse step'], 'small')
        box('coherent-tuple', 450, 960, 470, 151)
        text('tuple-title', 475, 1004, ['Conditional partial-state draw'], 'label')
        text('tuple-content', 475, 1043, ['(zₒ, Bₑw₀) + support status', 'No value for unestimated entries'], 'small')
        arrow('observed-draw-to-tuple', 'M210,807 L210,1034 L435,1034')
        arrow('generated-draw-to-tuple', 'M1468,855 L1468,900 L685,900 L685,946')
        text('generated-edge-label', 993, 887, ['Eligible missing sample Bₑw₀'], 'small')
        arrow('tuple-to-head', 'M920,1034 L1020,1034')
        box('fixed-diagnostic-head', 1035, 960, 360, 151)
        text('diagnostic-title', 1060, 1004, ['Fixed source head hψ'], 'label')
        text('diagnostic-content', 1060, 1043, ['Same observed code R', 'Same source-label training'], 'small')
        arrow('hse-observed-bypass', 'M795,533 L813,533 L813,929 L1215,929 L1215,947')
        text('bypass-label', 850, 919, ['R: retained observed evidence'], 'small')
        arrow('head-to-prediction', 'M1395,1034 L1465,1034')
        box('predictive-output', 1480, 960, 285, 151)
        text('output-title', 1500, 1004, ['Average L draws'], 'label')
        text('output-content', 1500, 1043, ['Class probability p̂(y)', 'No target fitting'], 'small')
        text('process-rule', 35, 1173,
             ['Restriction r acts during fitting and every reverse update, not only on the final output.'], 'label')
        text('effect-readout', 35, 1220,
             ['r × temporal structure ℓ: same scored target; separate posterior, diagnosis, coverage and cost.'], 'small')
        text('empty-rule', 35, 1270,
             ['Empty eligibility → no missing-state sampler; use the separately trained observed-only classifier.'], 'small')

    svg = ET.tostring(root, encoding='unicode')
    (output / f'{name}.svg').write_text(svg, encoding='utf-8')
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(output / f'{name}.pdf'))
    width_px = round(180 / 25.4 * 600)
    height_px = round((height / 10) / 25.4 * 600)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(output / f'{name}.png'),
                    output_width=width_px, output_height=height_px)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name in ('motivation', 'overview'):
        draw(args.output_dir, name)
    print('Regenerated problem and method SVG/PDF/PNG:', args.output_dir)


if __name__ == '__main__':
    main()
