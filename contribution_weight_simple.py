from math import factorial

K = 3

def order_pattern(authorlist):
	if sorted(authorlist) == authorlist:
		print 'CASE0'
		return 1
	elif sorted(authorlist) != authorlist:
		fst = []
		fst.append(authorlist[0])
		del authorlist[0]
		div = []
		div_ovr = 0
		while len(fst) >= 1:
			fst.append(authorlist[0])
			if sorted(fst) == fst:
				del authorlist[0]
				if len(authorlist) == 0:
					div.append(len(fst))
					if len(fst) >= 3:
						div_ovr += 1
						if div_ovr >= 2:
							print 'CASE1; div_ovr'+str(div_ovr)
							print div
							return 1
						elif div_ovr == 1:
							print 'CASE2; div_ovr'+str(div_ovr)
							print div
							return 2
					elif len(fst) == 2 and div_ovr == 1:
						print 'CASE3; div_ovr'+str(div_ovr)
						print div
						return 2
					elif len(fst) == 2 and div_ovr >= 2:
						print 'CASE4; div_ovr'+str(div_ovr)
						print div
						return 1
					else:
						print 'CASE5; div_ovr'+str(div_ovr)
						print div
						return 0
					break
			elif sorted(fst) != fst:
				div.append(len(fst)-1)
				if len(fst)-1 >= 3:
					div_ovr += 1
				fst = []
				fst.append(authorlist[0])
				del authorlist[0]
				if len(authorlist) == 0:
					div.append(1)
					if div_ovr == 1:
						print 'CASE6; div_ovr'+str(div_ovr)
						print div
						return 2
					elif div_ovr >= 2:
						print 'CASE7; div_ovr'+str(div_ovr)
						print div
						return 1
					else:
						print 'CASE8; div_ovr'+str(div_ovr)
						print div
						return 0
					break

def cweight(order_pattern, rearranged_author_list, name):
	if order_pattern == 2:#temporal version
		order_pattern = 1
	print
	print 'order_pattern:',order_pattern
	print 'name:', name
	authors = rearranged_author_list[0] + rearranged_author_list[1]
	authors = [x.lower() for x in authors]
	n = len(authors)
	print 'authors:', n
	for num,i in enumerate(authors):
		if name.lower() in i:#list of names?
			order = num
	print 'order:', order +1
	if order_pattern == 1 and n >= 4:
		print 'fractional contribution weight:'
		contribution_weight = float(1)/n
		print contribution_weight
		return contribution_weight
	else:
		cw = []
		pf = 0
		for r in range(1, len(rearranged_author_list[0])+1):#Case: First
			p = (n**(-float(1)/K)) * (r**(-(1-float(1)/K)))
			pf += p
		pf = pf/len(rearranged_author_list[0])
		if order_pattern == 1:
			pf = (1-float(1)/factorial(n)) * (float(1)/n) + (float(1)/factorial(n)) * pf
		for c in range(0, len(rearranged_author_list[0])):
			cw.append(pf)
		for num,i in enumerate(rearranged_author_list[1]):#Case: Not first
			r = len(rearranged_author_list[0]) + num + 1
			p = (n**(-float(1)/K)) * (r**(-(1-float(1)/K)))
			if order_pattern ==1:
				p = (1-float(1)/factorial(n)) * (float(1)/n) + (float(1)/factorial(n)) * p
			cw.append(p)
		sp = sum(cw)
		p_author = cw[order]
		contribution_weight = float(p_author)/sp
		nn = 0
		for i in cw:
			nn += 1
			print nn,i/sp
		print
		print contribution_weight
		return contribution_weight

alist1 =['Matsuno,J', 'Mizokawa,T', 'Fujimori,A', 'Zatsepin,DA', 'Galakhov,VR', 'Kurmaev,EZ', 'Kato,Y', 'Nagata,S']
alist2 =[['Matsuno,J'], ['Mizokawa,T', 'Fujimori,A', 'Zatsepin,DA', 'Galakhov,VR', 'Kurmaev,EZ', 'Kato,Y', 'Nagata,S']]
name = ¡ÆKato,Y¡Ç

cweight(order_pattern(alist1),alist2,name)
