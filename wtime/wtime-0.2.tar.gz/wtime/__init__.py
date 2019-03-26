import argparse, os, os.path, re, shutil, subprocess, sys

__all__ = ('wtime',)

_header = re.compile(r'(.+)\n\n(.+)\n\n').match
_pars = re.compile(r'([\w -]+)\n(.*?)\n\n+', re.S).findall
_days = re.compile(r'(\w+)(?:-(\w+))?').findall
_works = re.compile(r'^(\.\.)?(?:(\()?(\d+)(?::(\d+))?(?(2)\)) )?(?:(.+?) )?'
	r'(\()?(\d+)(?::(\d+))?(?(6)\))(\.\.)?(?: (#?\w+))?$', re.M).findall

ink = shutil.which('inkscape') or 'C:\\Program Files\\Inkscape\\inkscape.exe'
if not os.path.exists(ink): ink = 'C:\\Program Files (x86)\\Inkscape\\inkscape.exe'
if not os.path.exists(ink): ink = None

def wtime(file, flags='', font=None, gap=None, height=None, round=None, size=None, width=None):
	if not os.path.exists(file):
		print(f'missing {file}', file=sys.stderr)
		return 1

	if not (ink or 'k' in flags):
		print('missing inkscape', file=sys.stderr)
		return 2

	with open(file, encoding='utf-8') as f:
		src = f.read() + '\n\n'

	match = _header(src)
	title, d = match.groups()
	src = src[match.end():]
	day_names = d.split()

	index, rows = {}, []
	for i in range(len(day_names)):
		day = day_names[i]
		for j in range(len(day)):
			d = day[:j+1]
			if d not in index: break
		index[d] = i
		rows.append([])

	hour0, min0, work0, color0, colors = 0, 0, '?', 'lightgray', {}
	bounds = []
	for days, works in _pars(src):
		d = []
		for start, end in _days(days):
			d += range(index[start], index[end]+1) if end else [index[start]]

		for cont1, hide1, hour1, min1, work, hide2, hour2, min2, cont2, color in _works(works):
			cont1, cont2 = bool(cont1), bool(cont2)
			show1, show2 = not hide1, not hide2
			min1 = int(min1) if min1 else 0 if hour1 else min0
			hour1 = int(hour1) if hour1 else hour0
			work = work or work0
			hour2 = int(hour2)
			min2 = int(min2) if min2 else 0
			if color: colors[work] = color
			else: color = colors[work] if work in colors else color0
			for i in d:
				show1_, show2_ = show1, show2
				for w in rows[i]:
					if (w[6], w[7]) == (hour1, min1): w[5] = show1_ = False
					if (w[2], w[3]) == (hour2, min2): w[1] = show2_ = False
				rows[i].append([cont1, show1_, hour1, min1, cont2, show2_, hour2, min2, work, color])
			hour0, min0, work0, color0 = hour2, min2, work, color
			bounds.append((60*hour1 + min1, 60*hour2 + min2))

	bounds.sort()
	i = 0
	while i+1 < len(bounds):
		while i+1 < len(bounds) and bounds[i][1] >= bounds[i+1][0]:
			bounds[i:i+2] = [[bounds[i][0], max(bounds[i][1], bounds[i+1][1])]]
		i += 1

	shifts = [(0, bounds[0][0])]
	gap = 60*(1 if gap is None else gap)
	for i in range(1, len(bounds)):
		gap_ = bounds[i][0] - bounds[i-1][1]
		shifts.append((bounds[i][0], shifts[i-1][1] + (max(0, gap_ - gap) if gap else 0)))

	g_day, g_rect, g_work, g_time1, g_time2 = [], [], [], [], []
	round = round or 6
	shifts.reverse()
	for r in range(len(day_names)):
		g_day.append(f'<text x="-100" y="{25*r}">{day_names[r]}</text>')
		for cont1, show1, hour1, min1, cont2, show2, hour2, min2, work, color in rows[r]:
			x1 = 60*hour1 + min1
			for start, shift in shifts:
				if start <= x1: break
			x1 -= shift
			x2 = 60*hour2 + min2 - shift
			y = 25*r
			min1 = f'<tspan>:{min1:02}</tspan>' if min1 else ''
			min2 = f'<tspan>:{min2:02}</tspan>' if min2 else ''
			g_rect.append(f'<rect x="{x1 - 2*round*cont1}" y="{y-15}" '
				f'width="{x2-x1 + 2*round*cont1 + 2*round*cont2}" height="20" rx="{round}" fill="{color}" />')
			g_work.append(f'<text x="{(x1+x2)//2}" y="{y}">{work}</text>')
			if show1: g_time1.append(f'<text x="{x1-2}" y="{y-1}" fill="{color}">{hour1}{min1}</text>')
			if show2: g_time2.append(f'<text x="{x2+3}" y="{y-1}" fill="{color}">{hour2}{min2}</text>')

	width_ = bounds[-1][1] - shifts[0][1] + 160
	height_ = 25*len(day_names) + 65

	svg = f'''\
<svg viewBox="-120 -65 {width_} {height_}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
	<style>
		svg {{ font:{size or 11}pt {font or 'LiberationSans'}; font-variant-numeric:proportional-nums; }}
		text.title {{ font-size:1.3em; font-stretch:normal; text-anchor:middle; }}
		g.work text {{ fill:white; text-anchor:middle; }}
		g.start text, g.end text {{ font-size:.8em; }}
		g.start text {{ text-anchor:end; }}
		text tspan {{ font-size:.8em; }}
	</style>

	<defs>
		<filter id="shadow_rect" x="0" y="0" width="1" height="1">
			<feOffset in="SourceAlpha" dx="2" dy="2" />
			<feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 .5 0" />
			<feGaussianBlur stdDeviation="1" />
		</filter>

		<filter id="shadow_work" x="0" y="0" width="1" height="1">
			<feOffset in="SourceAlpha" dx="1" dy="1" />
			<feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 .3 0" />
			<feGaussianBlur stdDeviation=".5" />
		</filter>

		<g id="rect">
			<rect x="-120" y="-65" width="{width_}" height="{height_}" opacity="0" />
			''' + '\n\t\t\t'.join(g_rect) + f'''
		</g>

		<g id="work" class="work">
			<rect x="-120" y="-65" width="{width_}" height="{height_}" opacity="0" />
			''' + '\n\t\t\t'.join(g_work) + f'''
		</g>
	</defs>

	<text class="title" x="{width_//2 - 120}" y="-35">{title}</text>

	<g>
		''' + '\n\t\t'.join(g_day) + '''
	</g>

	<use xlink:href="#rect" filter="url(#shadow_rect)" />
	<use xlink:href="#rect" />

	<use xlink:href="#work" filter="url(#shadow_work)" />
	<use xlink:href="#work" />

	<g class="start">
		''' + '\n\t\t'.join(g_time1) + '''
	</g>

	<g class="end">
		''' + '\n\t\t'.join(g_time2) + '''
	</g>
</svg>'''

	file = os.path.splitext(file)[0]

	with open(file + '.svg', 'w', encoding='utf-8', newline='\n') as f:
		f.write(svg)

	if 'k' not in flags and not subprocess.run((ink, '-z', file + '.svg') +
			(('-e', file + '.png') if ('p' in flags or height or width) else ('-A', file + '.pdf')) +
			(('-h', str(height)) if height else ()) + (('-w', str(width)) if width else ())).returncode:
		os.remove(file + '.svg')

def main():
	a = argparse.ArgumentParser(None, 'wtime [-kp] [-f F] [-g G] [-h H] [-r R] [-s S] [-w W] file', 'Week Time 0.2', add_help=False)
	a.add_argument('file', nargs='?', help='TXT expanded to SVG rendered to PNG or PDF with Inkscape')
	a.add_argument('-f', '--font', metavar='F', help='font-family (default: LiberationSans)')
	a.add_argument('-g', '--gap', metavar='G', type=int, help='max gap (default: 1, no reduction: 0)')
	a.add_argument('-h', '--height', metavar='H', type=int, help='PNG height (implies -p)')
	a.add_argument('-k', '--keep', action='store_true', help='keep SVG, do not run Inkscape')
	a.add_argument('-p', '--png', action='store_true', help='render to PNG (default: PDF)')
	a.add_argument('-r', '--round', metavar='R', type=int, help='rounded corner radius (default: 6)')
	a.add_argument('-s', '--size', metavar='S', type=int, help='font-size (default: 11)')
	a.add_argument('-w', '--width', metavar='W', type=int, help='PNG width (implies -p)')
	args = a.parse_args()
	if args.file:
		return wtime(args.file, ('k' if args.keep else '') + ('p' if args.png else ''),
			args.font, args.gap, args.height, args.round, args.size, args.width)
	a.print_help()

if __name__ == '__main__':
	exit(main())