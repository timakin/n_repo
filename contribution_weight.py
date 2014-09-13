# coding:utf-8
from math import factorial

K = 3

def order_pattern(authorlist):
	if sorted(authorlist) == authorlist:
		#print 'CASE0'
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
							#print 'CASE1; div_ovr'+str(div_ovr)
							#print div
							return 1
						elif div_ovr == 1:
							#print 'CASE2; div_ovr'+str(div_ovr)
							#print div
							return 2
					elif len(fst) == 2 and div_ovr == 1:
						#print 'CASE3; div_ovr'+str(div_ovr)
						#print div
						return 2
					elif len(fst) == 2 and div_ovr >= 2:
						#print 'CASE4; div_ovr'+str(div_ovr)
						#print div
						return 1
					else:
						#print 'CASE5; div_ovr'+str(div_ovr)
						#print div
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
						#print 'CASE6; div_ovr'+str(div_ovr)
						#print div
						return 2
					elif div_ovr >= 2:
						#print 'CASE7; div_ovr'+str(div_ovr)
						#print div
						return 1
					else:
						#print 'CASE8; div_ovr'+str(div_ovr)
						#print div
						return 0
					break





def cweight(order_pattern, rearranged_author_list, name):
	if order_pattern == 2:#temporal version
		order_pattern = 1
	#print
	#print 'order_pattern:',order_pattern
	#print 'name:', name
	#print rearranged_author_list[0]
	#print rearranged_author_list[1]
	authors = rearranged_author_list[0] + rearranged_author_list[1]
	authors = [x.lower() for x in authors]
	n = len(authors)
	#print 'authors:', n
	for num,i in enumerate(authors):
		if name.lower() in i:#list of names?
			order = num
	#print 'order:', order +1
	if order_pattern == 1 and n >= 4:
		#print 'fractional contribution weight:'
		contribution_weight = float(1)/n
		#print contribution_weight
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
			#print nn,i/sp
		#print
		#print contribution_weight
		return contribution_weight

#alist =[['Matsuno,J'], ['Mizokawa,T', 'Fujimori,A', 'Zatsepin,DA', 'Galakhov,VR', 'Kurmaev,EZ', 'Kato,Y', 'Nagata,S']]
#alist = [['Chekanov,S'], ['Derrick,M', 'Krakauer,D', 'Loizides,JH', 'Magill,S', 'Miglioranzi,S', 'Musgrave,B', 'Repond,J', 'Yoshida,R', 'Mattingly,MCK', 'Antonioli,P', 'Bari,G', 'Basile,M', 'Bellagamba,L', 'Boscherini,D', 'Bruni,A', 'Bruni,G', 'Romeo,GC', 'Cifarelli,L', 'Cindolo,F', 'Contin,A', 'Corradi,M', 'DePasquale,S', 'Giusti,P', 'Iacobucci,G', 'Margotti,A', 'Montanari,A', 'Nania,R', 'Palmonari,F', 'Pesci,A', 'Sartorelli,G', 'Zichichi,A', 'Aghuzumtsyan,G', 'Bartsch,D', 'Brock,I', 'Goers,S', 'Hartmann,H', 'Hilger,E', 'Irrgang,P', 'Jakob,HP', 'Kappes,A', 'Kind,O', 'Meyer,U', 'Paul,E', 'Rautenberg,J', 'Renner,R', 'Schnurbusch,H', 'Stifutkin,A', 'Tandler,J', 'Voss,KC', 'Wang,M', 'Weber,A', 'Bailey,DS', 'Brook,NH', 'Cole,JE', 'Heath,GP', 'Namsoo,T', 'Robins,S', 'Wing,M', 'Capua,M', 'Mastroberardino,A', 'Schioppa,M', 'Susinno,G', 'Kim,JY', 'Kim,YK', 'Lee,JH', 'Lim,IT', 'Pac,MY', 'Caldwell,A', 'Helbich,M', 'Liu,X', 'Mellado,B', 'Ning,Y', 'Paganis,S', 'Ren,Z', 'Schmidke,WB', 'Sciulli,F', 'Chwastowski,J', 'Eskreys,A', 'Figiel,J', 'Galas,A', 'Olkiewicz,K', 'Stopa,P', 'Zawiejski,L', 'Adamczyk,L', 'Bold,T', 'Grabowska-Bold,I', 'Kisielewska,D', 'Kowal,AM', 'Kowal,M', 'Kowalski,T', 'Przybycien,M', 'Suszycki,L', 'Szuba,D', 'Szuba,J', 'Kotanski,A', 'Slominski,W', 'Adler,V', 'Behrens,U', 'Bloch,I', 'Borras,K', 'Chiochia,V', 'Dannheim,D', 'Drews,G', 'Fourletova,J', 'Fricke,U', 'Geiser,A', 'Gottlicher,P', 'Gutsche,O', 'Haas,T', 'Hain,W', 'Hillert,S', 'Kahle,B', 'Kotz,U', 'Kowalski,H', 'Kramberger,G', 'Labes,H', 'Lelas,D', 'Lim,H', 'Lohr,B', 'Mankel,R', 'Melzer-Pellmann,IA', 'Moritz,M', 'Nguyen,CN', 'Notz,D', 'Nuncio-Quiroz,AE', 'Polini,A', 'Raval,A', 'Rurua,L', 'Schneekloth,U', 'Stosslein,U', 'Wolf,G', 'Youngman,C', 'Zeuner,W', 'Viani,ALD', 'Schlenstedt,S', 'Barbagli,G', 'Gallo,E', 'Genta,C', 'Pelfer,PG', 'Bamberger,A', 'Benen,A', 'Karstens,F', 'Dobur,D', 'Vlasov,NN', 'Bell,M', 'Bussey,PJ', 'Doyle,AT', 'Ferrando,J', 'Hamilton,J', 'Hanlon,S', 'Saxon,DH', 'Skillicorn,IO', 'Gialas,I', 'Carli,T', 'Gosau,T', 'Holm,U', 'Krumnack,N', 'Lohrmann,E', 'Milite,M', 'Salehi,H', 'Schleper,P', 'Stonjek,S', 'Wichmann,K', 'Wick,K', 'Ziegler,A', 'Ziegler,A', 'Collins-Tooth,C', 'Foudas,C', 'Goncalo,R', 'Long,KR', 'Tapper,AD', 'Cloth,P', 'Filges,D', 'Kataoka,M', 'Nagano,K', 'Tokushuku,K', 'Yamada,S', 'Yamazaki,Y', 'Barakbaev,AN', 'Boos,EG', 'Pokrovskiy,NS', 'Zhautykov,BO', 'Son,D', 'Piotrzkowski,K', 'Barreiro,F', 'Glasman,C', 'Gonzalez,O', 'Labarga,L', 'delPeso,J', 'Tassi,E', 'Terron,J', 'Vazquez,M', 'Zambrana,M', 'Barbi,M', 'Corriveau,F', 'Gliga,S', 'Lainesse,J', 'Padhi,S', 'Stairs,DG', 'Walsh,R', 'Tsurugai,T', 'Antonov,A', 'Danilov,P', 'Dolgoshein,BA', 'Gladkov,D', 'Sosnovtsev,V', 'Suchkov,S', 'Dementiev,RK', 'Ermolov,PF', 'Golubkov,YA', 'Katkov,II', 'Khein,LA', 'Korzhavina,IA', 'Kuzmin,VA', 'Levchenko,BB', 'Lukina,OY', 'Proskuryakov,AS', 'Shcheglova,LM', 'Zotkin,SA', 'Coppola,N', 'Grijpink,S', 'Koffeman,E', 'Kooijman,P', 'Maddox,E', 'Pellegrino,A', 'Schagen,S', 'Tiecke,H', 'Velthuis,JJ', 'Wiggers,L', 'deWolf,E', 'Brummer,N', 'Bylsma,B', 'Durkin,LS', 'Ling,TY', 'Cooper-Sarkar,AM', 'Cottrell,A', 'Devenish,RCE', 'Foster,B', 'Grzelak,G', 'Gwenlan,C', 'Patel,S', 'Straub,PB', 'Walczak,R', 'Bertolin,A', 'Brugnera,R', 'Carlin,R', 'DalCorso,F', 'Dusini,S', 'Garfagnini,A', 'Limentani,S', 'Longhin,A', 'Parenti,A', 'Posocco,M', 'Stanco,L', 'Turcato,M', 'Heaphy,EA', 'Metlica,F', 'Oh,BY', 'Whitmore,JJ', 'Iga,Y', "D'Agostini,G", 'Marini,G', 'Nigro,A', 'Cormack,C', 'Hart,JC', 'McCubbin,NA', 'Heusch,C', 'Park,IH', 'Pavel,N', 'Abramowicz,H', 'Gabareen,A', 'Kananov,S', 'Kreisel,A', 'Levy,A', 'Kuze,M', 'Fusayasu,T', 'Kagawa,S', 'Kohno,T', 'Tawara,T', 'Yamashita,T', 'Hamatsu,R', 'Hirose,T', 'Inuzuka,M', 'Kaji,H', 'Kitamura,S', 'Matsuzawa,K', 'Ferrero,MI', 'Monaco,V', 'Sacchi,R', 'Solano,A', 'Arneodo,M', 'Ruspa,M', 'Koop,T', 'Martin,JF', 'Mirea,A', 'Butterworth,JM', 'Hall-Wilton,R', 'Jones,TW', 'Lightwood,MS', 'Sutton,MR', 'Targett-Adams,C', 'Ciborowski,J', 'Ciesielski,R', 'Luzniak,P', 'Nowak,RJ', 'Pawlak,JM', 'Sztuk,J', 'Tymieniecka,T', 'Ukleja,A', 'Ukleja,J', 'Zarnecki,AF', 'Adamus,M', 'Plucinski,P', 'Eisenberg,Y', 'Gladilin,LK', 'Hochman,D', 'Karshon,U', 'Riveline,M', 'Kcira,D', 'Lammers,S', 'Li,L', 'Reeder,DD', 'Rosin,M', 'Savin,AA', 'Smith,WH', 'Deshpande,A', 'Dhawan,S', 'Bhadra,S', 'Catterall,CD', 'Fourletov,S', 'Hartner,G', 'Menary,S', 'Soares,M', 'Standage,J']]
#alist =[['Yoshida,K'], []]#

#alist1 = alist[0] + alist[1]
#alist2 = alist
#name = alist2[1][1]


#cweight(order_pattern(alist1),alist2,name)

