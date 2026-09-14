import requests
import json
import csv
from difflib import SequenceMatcher
import re

def load_faab_data_with_ids():
    """
    Load FAAB data with IDs from embedded data
    
    Returns:
        dict: Dictionary mapping FAAB ID to player name
    """
    faab_data = """3	Ronald Jones
65	J.D. McKissic
2	Kenyan Drake
44	Julio Jones
49	Jared Goff
51	Matt Ryan
4	Zay Jones
273	Christian McCaffrey
55	Ryan Tannehill
59	Eno Benjamin
57	Mark Ingram
58	Tyler Allgeier
63	Rachaad White
64	Isiah Pacheco
34	Jeff Wilson Jr.
238	Cameron Dicker
46	Gerald Everett
7	Colts D/ST
5	Jamison Crowder
40	James Robinson
48	Marcus Mariota
45	Devin Duvernay
884	Marvin Harrison Jr.
36	Jarvis Landry
191	Darnell Mooney
41	Taysom Hill
42	Jaylen Warren
43	Dontrell Hilliard
274	Ja'Marr Chase
39	Jahan Dotson
84	Logan Thomas
60	Jordan Mason
47	Geno Smith
89	Raheem Mostert
52	Joe Flacco
1	Jameis Winston
90	Michael Gallup
38	Treylon Burks
224	Terrace Marshall Jr.
78	Romeo Doubs
92	Tua Tagovailoa
74	Nico Collins
99	Greg Dortch
80	Corey Davis
94	Trevor Lawrence
95	Carson Wentz
88	Isaiah Likely
67	Garrett Wilson
96	Chris Olave
97	Ashton Dulin
100	Breece Hall
103	David Njoku
105	Russell Gage
82	Hayden Hurst
193	Donovan Peoples-Jones
75	Nelson Agholor
98	Derek Carr
68	Isaiah McKenzie
85	Robert Tonyan
73	Sterling Shepard
107	Harrison Butker
108	Jake Elliott
886	Hollywood Brown
252	Melvin Gordon III
114	DeVante Parker
116	Cole Beasley
288	Davante Adams
276	Cooper Kupp
104	Khalil Herbert
83	Tyler Conklin
225	Demarcus Robinson
72	Noah Brown
76	Mack Hollins
194	Malik Willis
1014	Ashton Jeanty
227	Jordan Wilkins
239	Zonovan Knight
101	Jerick McKinnon
255	Michael Badgley
111	D.J. Chark Jr.
113	Cole Kmet
115	Craig Reynolds
888	Caleb Williams
117	Dak Prescott
226	DeAndre Carter
240	Mike White
192	Andy Dalton
889	Xavier Worthy
890	Jonathon Brooks
232	Ryan Succop
229	Robbie Gould
891	Brock Bowers
248	Matt Breida
257	Ty Johnson
253	DeeJay Dallas
259	Brock Purdy
254	Chigoziem Okonkwo
260	Jelani Woods
258	Daniel Bellinger
261	Younghoe Koo
263	Zamir White
133	Kadarius Toney
277	Travis Kelce
278	Bijan Robinson
151	Latavius Murray
128	Ken Walker III
149	Richie James Jr.
126	Joshua Palmer
1048	Ollie Gordon II
1049	Trevor Etienne
1050	Tahj Brooks
256	Robert Woods
137	Rondale Moore
249	Taylor Heinicke
147	Teddy Bridgewater
155	Brett Maher
162	Randall Cobb
163	Robbie Anderson
146	Wil Lutz
124	Greg Joseph
139	Irv Smith Jr.
135	Deon Jackson
122	Brian Robinson Jr.
132	Chris Boswell
142	Christian Watson
131	Graham Gano
136	Hunter Henry
127	Jameson Williams
130	Mike Boone
152	Mo Alie-Cox
141	Riley Patterson
145	Skyy Moore
153	Caleb Huntley
160	Cade York
158	Greg Zuerlein
279	Tyreek Hill
154	Alec Pierce
892	Rome Odunze
159	Cade Otton
478	Eric Gray
523	Kyle Trask
161	Mason Crosby
180	D'Onta Foreman
177	Tyrion Davis-Price
171	Wan'Dale Robinson
188	Marquise Goodwin
1051	Jalen Royals
144	Daniel Jones
6	Noah Fant
143	Kenny Pickett
125	Matt Prater
156	Nick Folk
148	Greg Dulcich
262	Damien Harris
157	Khalil Shakir
893	Ladd McConkey
166	Mike Gesicki
243	Odell Beckham Jr.
174	Joshua Kelley
175	Parris Campbell
246	Austin Hooper
167	Chase Claypool
179	Bailey Zappe
176	Jason Myers
178	Kyren Williams
169	Mecole Hardman
173	Tyquan Thornton
244	JaMycal Hasty
247	Kendall Hinton
228	Foster Moreau
184	Chuba Hubbard
185	Deshaun Watson
186	Juwan Johnson
187	Sony Michel
189	Jason Sanders
895	Trey Benson
286	Derrick Henry
290	Josh Jacobs
264	Travis Homer
270	Desmond Ridder
894	Brian Thomas Jr.
341	AJ Dillon
291	Rhamondre Stevenson
294	Mark Andrews
296	DeVonta Smith
297	Patrick Mahomes II
302	DK Metcalf
234	Samaje Perine
172	Zach Wilson
170	Mac Jones
976	Carson Steele
300	Jalen Hurts
304	Jahmyr Gibbs
308	Deebo Samuel
313	Joe Burrow
316	Terry McLaurin
318	Dameon Pierce
320	Chris Godwin
321	James Conner
323	Justin Herbert
325	Brandon Aiyuk
303	Aaron Jones
329	David Montgomery
311	Calvin Ridley
327	Mike Williams
315	Jerry Jeudy
266	Chris Moore
309	T.J. Hockenson
896	Blake Corum
337	Alvin Kamara
897	Keon Coleman
289	Amon-Ra St. Brown
287	A.J. Brown
307	Kenneth Walker III
331	Michael Pittman Jr.
380	Michael Carter
355	Michael Thomas
346	Rashaad Penny
399	Leonard Fournette
454	Laviska Shenault Jr.
364	Tyler Boyd
335	Javonte Williams
283	Stefon Diggs
326	Christian Kirk
310	Miles Sanders
306	Keenan Allen
332	Diontae Johnson
379	Cordarrelle Patterson
376	Hunter Renfrow
366	DJ Chark Jr.
349	Courtland Sutton
354	Zach Charbonnet
358	Dalton Schultz
363	Tyler Higbee
369	Matthew Stafford
367	Adam Thielen
350	Jamaal Williams
351	Rashod Bateman
371	Rashid Shaheed
373	Roschon Johnson
377	Isaiah Hodgins
385	Bryce Young
375	Dawson Knox
386	Kyler Murray
898	MarShawn Lloyd
447	Trey Lance
410	Tyler Bass
362	De'Von Achane
393	San Francisco 49ers
394	Dallas Cowboys
405	New York Jets
408	Baltimore Ravens
397	Philadelphia Eagles
435	Marvin Jones Jr.
430	Cleveland Browns
440	Jacksonville Jaguars
449	Seattle Seahawks
434	Marvin Mims Jr.
455	Detroit Lions
427	Miami Dolphins
433	Green Bay Packers
409	Denver Broncos
438	Indianapolis Colts
462	Ronald Jones II
402	Justin Tucker
378	Clyde Edwards-Helaire
382	Jonathan Mingo
414	Sam Howell
400	Mecole Hardman Jr.
468	Ka'imi Fairbairn
500	Darrell Henderson Jr.
474	KJ Hamler
428	Israel Abanikanda
436	Isaiah Spiller
456	Cairo Santos
407	Rashee Rice
412	Josh Downs
422	Chase Brown
419	Michael Mayer
426	Zach Evans
899	Adonai Mitchell
476	Keaontay Ingram
465	Braxton Berrios
466	Kayshon Boutte
473	David Bell
424	Pittsburgh Steelers
423	New Orleans Saints
429	Tampa Bay Buccaneers
451	Tennessee Titans
442	Los Angeles Rams
446	Carolina Panthers
469	Minnesota Vikings
494	Deonte Harty
506	Tyler Scott
517	Chris Rodriguez Jr.
515	Ke'Shawn Vaughn
503	A.T. Perry
525	C.J. Uzomah
538	Marlon Mack
485	Luke Schoonmaker
490	Robbie Chosen
491	Myles Gaskin
493	Tristan Vizcaino
495	Darnell Washington
507	Colt McCoy
459	Nick Westbrook-Ikhine
499	Eddy Pineiro
445	D'Ernest Johnson
472	Hassan Haskins
1015	Omarion Hampton
513	Kevin Harris
518	Brevin Jordan
461	Jake Ferguson
470	Chris Evans
475	Evan Hull
483	Justyn Ross
512	Donald Parham Jr.
480	Will Levis
463	Deuce Vaughn
488	Michael Wilson
458	Ty Chandler
524	Jalen Tolbert
528	Deneric Prince
529	Trent Sherfield
531	Mark Ingram II
534	Kalif Raymond
535	Parker Washington
537	Raheem Blackshear
929	Blake Grupe
511	Houston Texans
509	Atlanta Falcons
481	Arizona Cardinals
504	Chicago Bears
548	Randy Bullock
551	Tre'Quan Smith
553	O.J. Howard
563	Tyler Davis
565	Corey Clement
566	Jamal Agnew
571	Mohamed Ibrahim
578	Shi Smith
581	Tony Jones Jr.
582	Tiyon Evans
585	Brandon Bolden
597	Equanimeous St. Brown
601	Brian Hoyer
602	Dee Eskridge
544	Trey Palmer
545	Anders Carlson
547	Charlie Jones
552	Elliott Fry
554	Chad Ryland
519	Olamide Zaccheaus
521	Harrison Bryant
556	Brock Wright
557	Zack Kuntz
561	Tanner Brown
567	Zach Pascal
568	Cole Turner
573	Dontayvion Wicks
576	Denzel Mims
577	Danny Gray
580	Zane Gonzalez
549	Jordan Akins
583	Jarrett Stidham
584	Brenton Strange
587	Tommy Tremble
590	Hunter Long
591	Caleb Shudak
593	Sammy Watkins
595	Tyler Huntley
596	Dan Arnold
599	Teagan Quitoriano
600	Grant Calcaterra
930	Luke McCaffrey
613	Tre' McKitty
616	T.Y. Hilton
623	Cam Sims
625	Amari Rodgers
631	Brycen Hopkins
664	Mitch Trubisky
665	Devin Asiasi
666	Avery Williams
608	Gary Brightwell
609	John Bates
611	Julius Chestnut
612	Hendon Hooker
615	Ian Thomas
618	Patrick Ricard
619	Giovanni Ricci
621	Dante Pettis
624	Jesper Horsted
626	Davis Mills
628	Drew Sample
570	Elijah Higgins
542	Kylen Granson
629	David Sills V
632	Demetric Felton Jr.
635	Ray-Ray McCloud III
636	Chris Manhertz
638	Shane Zylstra
639	Josh Whyle
641	Juwann Winfree
604	KhaDarel Hodge
643	Parker Hesse
644	James Proche II
646	Jalen Nailor
647	Connor Heyward
649	Byron Pringle
651	Chris Myarick
652	Tommy Sweeney
654	Mike Davis
655	Cameron Brate
657	River Cracraft
659	Anthony Schwartz
660	Dax Milne
662	Case Keenum
667	Damiere Byrd
670	Damien Williams
676	Tim Jones
679	Geoff Swaim
687	Rashard Higgins
691	Aidan O'Connell
669	Armani Rogers
672	Marcus Johnson
673	Mike Strachan
675	Jeff Smith
677	Miles Boykin
680	Jason Moore Jr.
682	Mitchell Wilcox
683	Tylan Wallace
685	Michael Bandy
686	Cody Hollister
689	Zander Horvath
693	Thayer Thomas
690	Tevin Coleman
292	Jaylen Waddle
330	Dallas Goedert
348	Quentin Johnston
356	Zay Flowers
360	Allen Lazard
365	Anthony Richardson
370	Tank Bigsby
368	Kendre Miller
453	Luke Musgrave
372	Dalton Kincaid
374	Jerome Ford
383	Sam LaPorta
931	Dylan Laube
401	Jalin Hyatt
411	C.J. Stroud
353	JuJu Smith-Schuster
522	Ty Montgomery
940	Isaiah Davis
707	Ty Montgomery II
711	C.J. Ham
722	Keith Smith
723	Godwin Igwebuike
728	Nick Bawden
731	Taiwan Jones
441	Kendrick Bourne
464	Tank Dell
460	Sean Tucker
477	Puka Nacua
484	Salvon Ahmed
510	Noah Gray
514	Adam Trautman
546	Justin Watson
498	Ben Skowronek
415	Tyjae Spears
932	Brenden Rice
933	Isaac Guerendo
934	Jacob Cowing
937	Rasheen Ali
939	Erick All Jr.
359	Aaron Rodgers
347	Brandin Cooks
941	Cade Stover
450	Quez Watkins
748	DeMario Douglas
942	Johnny Wilson
943	Jawhar Jordan
250	Jordan Love
69	Jakobi Meyers
710	Alec Ingold
714	Reggie Gilliam
716	Elijah Dotson
709	Patrick Taylor Jr.
720	Michael Burton
724	Emanuel Wilson
725	Khari Blasingame
727	Dare Ogunbowale
729	Darrynton Evans
733	Derrick Gore
734	Jacques Patrick
736	Tarik Cohen
738	Gerrid Doaks
739	Qadree Ollison
741	Dwayne Washington
744	Patrick Laird
745	Xazavian Valladay
746	Alex Armah Jr.
749	Lil'Jordan Humphrey
768	Kirk Merritt
773	Chosen Anderson
774	N'Keal Harry
777	Lynn Bowden Jr.
779	Matthew Slater
786	Cade Johnson
787	T.J. Luther
788	D.J. Montgomery
737	Jashaun Corbin
740	Sincere McCormick
743	Owen Wright
747	Hassan Hall
751	Deven Thompkins
752	Erik Ezukanma
754	Rakim Jarrett
756	Trent Taylor
757	Malik Heath
759	Keith Kirkwood
718	Ronnie Rivers
719	Emari Demercado
761	Kristian Wilkerson
762	Ihmir Smith-Marsette
764	Gunner Olszewski
765	Kearis Jackson
767	Antoine Green
769	Cody Thompson
771	Jason Brownlee
775	Grant DuBose
776	Steven Sims Jr.
780	Colton Dowell
782	Maurice Alexander
783	Mitchell Tinsley
789	Easop Winston Jr.
793	Jared Wayne
797	Seth Williams
807	Alex Erickson
811	Derek Wright
815	Marcell Ateman
820	Devon Allen
825	Isaiah Winstead
826	Terrell Bynum
830	Austin Watkins Jr.
833	Tre'Shaun Harrison
837	Brycen Tremayne
848	Blaine Gabbert
945	Jaheim Bell
852	PJ Walker
853	C.J. Beathard
855	David Blough
794	Kwamie Lassiter II
795	Xavier Smith
798	Nsimba Webster
799	Trishton Jackson
801	Cornell Powell
803	Chris Conley
804	Dylan Drummond
806	Tyrell Shavers
808	Shedrick Jackson
810	Jaelon Darden
813	Joseph Ngata
814	Bryan Thompson
817	Bo Melton
819	Tyron Johnson
821	Laquon Treadwell
823	Keelan Doss
828	Mason Kinsey
831	Dwayne Harris
832	Sean Ryan
835	Willie Snead IV
838	Elijah Cooks
839	Irvin Charles
845	Nick Mullens
847	Skylar Thompson
851	Stetson Bennett
854	Sean Clifford
860	Trevor Siemian
863	Blake Bell
866	Jimmy Graham
868	Trevon Wesco
869	Tyler Kroft
882	Matt Bushman
539	Calvin Austin III
421	Kansas City Chiefs
425	Cincinnati Bengals
431	Washington Commanders
857	Easton Stick
859	Matt Corral
861	Nick Foles
862	Malik Cunningham
841	Tyrod Taylor
870	Payne Durham
871	Davis Allen
873	Charlie Woerner
874	Marcedes Lewis
878	Brayden Willis
880	Curtis Hodges
881	Julian Hill
906	Xavier Legette
439	Baker Mayfield
471	Jake Moody
858	Jake Browning
1097	Jaydn Ott
824	David Moore
844	Cooper Rush
708	Jaleel McLaughlin
907	Brandon Aubrey
850	Tyson Bagent
501	Jauan Jennings
343	Jaxon Smith-Njigba
909	Jermaine Burton
398	Pierre Strong Jr.
562	Keaton Mitchell
487	Kyle Philips
344	Pat Freiermuth
923	Malachi Corley
588	Rico Dowdle
947	Jase McClellan
505	Tucker Kraft
910	Jaylen Wright
912	Ricky Pearsall
913	Troy Franklin
914	Ben Sinnott
916	Roman Wilson
920	Javon Baker
921	Audric Estime
926	Will Shipley
928	Jalen McMillan
840	Joshua Dobbs
396	Allen Robinson II
946	Ainias Smith
949	Frank Gore Jr.
952	Ryan Flournoy
953	Cody Schrader
955	Lucas Krull
957	Jamari Thrash
958	Spencer Rattler
960	Kendall Milton
961	Michael Wiley
963	Trent Sherfield Sr.
964	Emani Bailey
966	AJ Barner
233	Cam Akers
951	Donovan Edwards
1016	TreVeyon Henderson
967	Bub Means
969	Keilan Robinson
971	Anthony Gould
972	Dallin Holker
444	Zack Moss
333	D'Andre Swift
416	Kareem Hunt
924	Tyrone Tracy Jr.
112	K.J. Osborn
361	Devin Singletary
275	Austin Ekeler
381	Ezekiel Elliott
35	Curtis Samuel
129	Dustin Hopkins
406	Zach Ertz
586	Colby Parkinson
730	Royce Freeman
843	Drew Lock
301	Travis Etienne Jr.
340	Jordan Addison
418	Evan McPherson
482	Albert Okwuegbunam
527	Marquez Callaway
543	Rex Burkhead
569	Jeremy Ruckert
592	Samori Toure
607	Tyler Badie
627	Will Mallory
645	Eric Saubert
661	Blake Proehl
324	Tyler Lockett
268	Russell Wilson
182	Elijah Moore
106	Alexander Mattison
181	Gus Edwards
560	Trey Sermon
502	Gardner Minshew II
919	Drake Maye
681	Malcolm Brown
938	Malik Washington
726	Hunter Luepke
755	Derius Davis
772	Racey McMath
792	Daurice Fountain
812	Malik Taylor
834	Tay Martin
53	Jimmy Garoppolo
879	Tyree Jackson
927	Devontez Walker
962	Nyheim Hines
885	Malik Nabers
432	Los Angeles Chargers
533	Las Vegas Raiders
935	Michael Penix Jr.
917	Braelon Allen
404	New England Patriots
900	Ray Davis
66	Darrel Williams
281	Jonathan Taylor
328	Kyle Pitts
420	Chase Edmonds
489	Trayveon Williams
530	Kene Nwangwu
520	Will Dissly
572	Kyle Juszczyk
594	James Mitchell
610	Andrei Iosivas
630	Cameron Latu
648	Andrew Beck
663	Pharaoh Brown
684	MyCole Pruitt
352	Kirk Cousins
732	Snoop Conner
758	Jake Bobo
778	Britain Covey
345	Gabe Davis
796	Matt Landers
816	Greg Ward
836	Kazmeir Allen
864	Ko Kieft
865	Andrew Ogletree
948	Blake Watson
965	Dillon Johnson
285	CeeDee Lamb
312	Lamar Jackson
267	Tutu Atwell
492	Rodrigo Blankenship
532	Durham Smythe
550	Chase McLaughlin
575	Jalen Guyton
598	Scott Miller
614	Tre Tucker
633	Jack Stoll
650	Jody Fortson
668	Breshad Perriman
688	Nick Boyle
712	Jake Funk
735	Jaret Patterson
760	Ronnie Bell
781	Simi Fehoko
800	Andy Isabella
818	Stanley Morgan Jr.
842	Dorian Thompson-Robinson
867	Luke Farrell
634	Trenton Irwin
950	Joshua Karty
968	Tip Reiman
342	Antonio Gibson
236	Trey McBride
298	Joe Mixon
317	Drake London
284	Tony Pollard
384	John Metchie III
452	DeWayne McBride
437	Matt Gay
497	Xavier Hutchinson
536	Joey Slye
555	Kenny Golladay
579	Josh Oliver
603	Ross Dwelley
617	Quintin Morris
637	Phillip Dorsett II
653	Tanner Hudson
671	Kendall Blanton
272	Justin Jefferson
715	Adam Prentice
742	Tyler Goodson
763	Lawrence Cager
784	Johnny Johnson III
802	Braylon Sanders
822	Kaden Davis
846	Kyle Allen
872	Nate Adkins
915	Bucky Irving
954	Jared Wiley
970	Daijun Edwards
295	Tee Higgins
443	Boston Scott
479	Jacoby Brissett
508	Kenny McIntosh
540	Peyton Hendershot
559	Velus Jones Jr.
558	Justice Hill
605	Jalen Reagor
620	Johnny Mundt
640	Zach Gentry
656	Tom Kennedy
674	Bryan Edwards
413	Jayden Reed
717	Jakob Johnson
750	Brandon Johnson
766	Xavier Gipson
319	DeAndre Hopkins
269	Van Jefferson
790	Shaquan Davis
805	Dez Fitzpatrick
827	Andre Baccellia
849	Brandon Allen
875	Ben Sims
918	Kimani Vidal
956	Casey Washington
282	Saquon Barkley
164	Darius Slayton
299	Josh Allen
322	George Kittle
336	Mike Evans
417	Daniel Carlson
467	Malik Davis
516	Justin Jackson
541	Cedrick Wilson Jr.
564	Clayton Tune
589	Trestan Ebner
606	Josiah Deguara
622	Charlie Kolar
642	Bryce Ford-Wheaton
658	Brandon Powell
678	Montrell Washington
936	Theo Johnson
721	Anthony McFarland Jr.
753	KaVontae Turpin
770	Jalen Brooks
791	Raleigh Webb
809	Josh Ali
829	Austin Trammell
856	Brett Rypien
877	David Wells
922	Bo Nix
959	Cornelius Johnson
314	DJ Moore
150	James Cook
911	Ja'Lynn Polk
395	Buffalo Bills
293	Najee Harris
1098	Jordan Watkins
973	Devaughn Vele
974	Jordan Whittington
980	Jeremy McNichols
448	New York Giants
109	George Pickens
339	Dalvin Cook
457	Cedric Tillman
925	Ja'Tavion Sanders
1019	Aaron Jones Sr.
134	Justin Fields
883	Deebo Samuel Sr.
81	Evan Engram
486	Jonnu Smith
280	Nick Chubb
334	Marquise Brown
496	Sam Darnold
1036	Jack Bech
1037	DJ Giddens
1038	Devin Neal
1039	Chig Okonkwo
1040	Kyle Monangai
1041	Mason Taylor
1042	Jaylin Noel
1043	Elijah Arroyo
357	Elijah Mitchell
1044	Anthony Richardson Sr.
1045	Elic Ayomanor
1046	Pat Bryant
1047	Jarquez Hunter
1017	RJ Harvey
1020	Tetairoa McMillan
1022	Quinshon Judkins
1025	Matthew Golden
1027	Bhayshul Tuten
1028	Luther Burden III
1029	Tre' Harris
1030	Jaydon Blue
1032	Jayden Higgins
1035	Cameron Ward
1034	Jake Bates
138	Kenneth Gainwell
1052	Brashard Smith
305	Amari Cooper
574	Dyami Brown
1053	Jordan James
1054	Harold Fannin Jr.
403	Tim Patrick
1055	Woody Marks
1056	Tyler Shough
338	Darren Waller
1057	Xavier Restrepo
1058	Damien Martinez
1059	Terrance Ferguson
1060	Jaxson Dart
1061	Oronde Gadsden II
1062	Tory Horton
1063	Isaac TeSlaa
1064	Phil Mafah
713	Chris Brooks
1065	Tez Johnson
1066	Jacory Croskey-Merritt
1067	Will Reichard
1068	Tyler Loop
1069	Raheim Sanders
1070	Dont'e Thornton Jr.
1071	Shedeur Sanders
1072	Tai Felton
1073	A.J. Dillon
110	Marquez Valdes-Scantling
1074	Jalen Milroe
1075	Isaiah Bond
1076	Savion Williams
168	Josh Reynolds
1077	Chimere Dike
235	Brandon McManus
1078	Cam Little
1079	Gunnar Helm
1080	Kalel Mullings
1081	LeQuint Allen Jr.
1082	Antwane Wells Jr.
526	Ameer Abdullah
1083	Jaylin Lane
1084	Dillon Gabriel
1085	Ja'Quinden Jackson
1086	Theo Wease Jr.
1087	Mason Rudolph
1088	Arian Smith
1089	Luke Lachey
1090	Chris Tyree
1091	Joe Milton III
1092	Will Howard
876	Stone Smartt
1093	Mitchell Evans
1094	KeAndre Lambert-Smith
1095	Kaden Prather
1096	Julian Fleming
1099	Efton Chism III
1100	Marcus Yarns
785	Tyler Johnson
1101	Jimmy Horn Jr.
1102	Lan Larison
887	Jayden Daniels
1018	Kaleb Johnson
1021	Travis Hunter
1023	Cam Skattebo
1024	Tyler Warren
1026	Colston Loveland
944	Emeka Egbuka
908	J.J. McCarthy
1031	Kyle Williams
1033	Dylan Sampson
981	Jalen Coker
271	J.K. Dobbins"""

    faab_dict = {}
    lines = faab_data.strip().split('\n')
    
    for line in lines:
        if line.strip():
            parts = line.split('\t', 1)
            if len(parts) == 2:
                faab_id = int(parts[0])
                player_name = parts[1].strip()
                faab_dict[faab_id] = player_name
    
    print(f"Loaded {len(faab_dict)} FAAB players with IDs")
    return faab_dict

def get_sleeper_players():
    """
    Get all NFL players from Sleeper API
    
    Returns:
        dict: Sleeper player data (sleeper_id -> player_info)
    """
    url = "https://api.sleeper.app/v1/players/nfl"
    
    try:
        print("Fetching all Sleeper NFL players...")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Sleeper players: {e}")
        return {}

def normalize_name(name):
    """
    Normalize a player name for comparison
    
    Args:
        name (str): Player name to normalize
    
    Returns:
        str: Normalized name
    """
    if not name:
        return ""
    
    # Convert to lowercase
    normalized = name.lower()
    
    # Remove common suffixes and prefixes
    suffixes_to_remove = [' jr.', ' jr', ' sr.', ' sr', ' ii', ' iii', ' iv', ' v']
    for suffix in suffixes_to_remove:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)]
    
    # Replace common abbreviations and variations
    replacements = {
        # Periods in initials
        '.': '',
        # Common name variations
        'kenneth': 'ken',
        'kenneth walker iii': 'ken walker iii',
        'ceedee': 'cd',
        'dj': 'dj',
        'd.j.': 'dj',
        'aj': 'aj',
        'a.j.': 'aj',
        'cj': 'cj',
        'c.j.': 'cj',
        'tj': 'tj',
        't.j.': 'tj',
        'jj': 'jj',
        'j.j.': 'jj',
        'kj': 'kj',
        'k.j.': 'kj',
        'rj': 'rj',
        'r.j.': 'rj',
        'pj': 'pj',
        'p.j.': 'pj',
        # Common contractions
        "d'andre": "dandre",
        "de'von": "devon",
        "ja'marr": "jamarr",
        "ja'lynn": "jalynn",
        "ja'tavion": "jatavion",
        "ka'imi": "kaimi",
        "ke'shawn": "keshawn",
        "n'keal": "nkeal",
        "o'cyrus": "ocyrus",
        # Team abbreviations
        " d/st": "",
        " dst": "",
        # Roman numerals and variations
        " ii": "",
        " iii": "",
        " iv": "",
        " v": "",
        " 2nd": "",
        " 3rd": "",
        # Special cases
        "isiah": "isaiah",  # Common spelling variation
        "melvin gordon iii": "melvin gordon",
        "ronald jones ii": "ronald jones",
        "mecole hardman jr": "mecole hardman",
        "marvin jones jr": "marvin jones",
        "ken walker iii": "kenneth walker",
        "patrick mahomes ii": "patrick mahomes"
    }
    
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    # Remove extra whitespace
    normalized = ' '.join(normalized.split())
    
    return normalized

def similarity_score(name1, name2):
    """
    Calculate similarity between two names
    
    Args:
        name1 (str): First name
        name2 (str): Second name
    
    Returns:
        float: Similarity score between 0 and 1
    """
    return SequenceMatcher(None, name1, name2).ratio()

def interactive_fuzzy_matching(faab_name, faab_id, potential_matches):
    """
    Interactively confirm fuzzy matches with user
    
    Args:
        faab_name (str): FAAB player name
        faab_id (int): FAAB player ID
        potential_matches (list): List of potential Sleeper matches
    
    Returns:
        dict or None: Confirmed match or None if rejected
    """
    print(f"\nFAAB ID {faab_id}: '{faab_name}'")
    print("Potential matches:")
    
    for i, match in enumerate(potential_matches, 1):
        print(f"  {i}. {match['full_name']} ({match['position']}, {match['team']}) - Score: {match['score']:.3f}")
    
    while True:
        response = input("Select match (1-{}) or 'n' to skip: ".format(len(potential_matches))).strip().lower()
        
        if response == 'n':
            return None
        
        try:
            choice = int(response) - 1
            if 0 <= choice < len(potential_matches):
                selected = potential_matches[choice]
                return {
                    'faab_id': faab_id,
                    'faab_name': faab_name,
                    'sleeper_id': selected['sleeper_id'],
                    'sleeper_name': selected['full_name'],
                    'position': selected['position'],
                    'team': selected['team'],
                    'active': selected['active'],
                    'confidence': 'USER_CONFIRMED',
                    'similarity_score': selected['score']
                }
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Enter a number or 'n'.")

def find_sleeper_matches_interactive(faab_dict, sleeper_data, threshold=0.8, interactive_threshold=0.95):
    """
    Find matches between FAAB and Sleeper players with interactive confirmation
    
    Args:
        faab_dict (dict): FAAB ID -> player name mapping
        sleeper_data (dict): Sleeper player data
        threshold (float): Minimum similarity score for fuzzy matches
        interactive_threshold (float): Score below which to ask user for confirmation
    
    Returns:
        tuple: (exact_matches, confirmed_matches, unmatched)
    """
    exact_matches = []
    confirmed_matches = []
    unmatched = []
    
    print("Creating normalized Sleeper name lookup...")
    sleeper_lookup = {}
    for sleeper_id, player_info in sleeper_data.items():
        full_name = player_info.get('full_name', '')
        if full_name:
            normalized = normalize_name(full_name)
            sleeper_lookup[normalized] = {
                'sleeper_id': sleeper_id,
                'full_name': full_name,
                'position': player_info.get('position', ''),
                'team': player_info.get('team', ''),
                'active': player_info.get('active', False)
            }
    
    print(f"Processing {len(faab_dict)} FAAB players...")
    
    fuzzy_matches_needing_review = []
    
    for faab_id, faab_name in faab_dict.items():
        normalized_faab = normalize_name(faab_name)
        
        # Skip team defenses
        if 'd/st' in faab_name.lower() or faab_name.endswith('D/ST'):
            unmatched.append({
                'faab_id': faab_id,
                'faab_name': faab_name,
                'reason': 'Team defense - no Sleeper equivalent'
            })
            continue
        
        # Try exact match first
        if normalized_faab in sleeper_lookup:
            match_info = sleeper_lookup[normalized_faab]
            exact_matches.append({
                'faab_id': faab_id,
                'faab_name': faab_name,
                'sleeper_id': match_info['sleeper_id'],
                'sleeper_name': match_info['full_name'],
                'position': match_info['position'],
                'team': match_info['team'],
                'active': match_info['active'],
                'confidence': 'EXACT',
                'similarity_score': 1.0
            })
            continue
        
        # Find potential fuzzy matches
        potential_matches = []
        
        for norm_sleeper, sleeper_info in sleeper_lookup.items():
            score = similarity_score(normalized_faab, norm_sleeper)
            
            if score >= threshold:
                potential_matches.append({
                    'sleeper_id': sleeper_info['sleeper_id'],
                    'full_name': sleeper_info['full_name'],
                    'position': sleeper_info['position'],
                    'team': sleeper_info['team'],
                    'active': sleeper_info['active'],
                    'score': score
                })
        
        # Sort by score (best first)
        potential_matches.sort(key=lambda x: x['score'], reverse=True)
        
        if potential_matches:
            best_match = potential_matches[0]
            
            # Auto-confirm high-confidence matches
            if best_match['score'] >= interactive_threshold:
                confirmed_matches.append({
                    'faab_id': faab_id,
                    'faab_name': faab_name,
                    'sleeper_id': best_match['sleeper_id'],
                    'sleeper_name': best_match['full_name'],
                    'position': best_match['position'],
                    'team': best_match['team'],
                    'active': best_match['active'],
                    'confidence': 'AUTO_CONFIRMED',
                    'similarity_score': best_match['score']
                })
            else:
                # Store for interactive review
                fuzzy_matches_needing_review.append({
                    'faab_id': faab_id,
                    'faab_name': faab_name,
                    'potential_matches': potential_matches[:3]  # Top 3 matches
                })
        else:
            unmatched.append({
                'faab_id': faab_id,
                'faab_name': faab_name,
                'reason': 'No suitable match found'
            })
    
    # Interactive review phase
    if fuzzy_matches_needing_review:
        print(f"\n{len(fuzzy_matches_needing_review)} matches need your confirmation...")
        print("For each match, select the correct player or 'n' to skip.")
        
        for review_item in fuzzy_matches_needing_review:
            confirmed_match = interactive_fuzzy_matching(
                review_item['faab_name'],
                review_item['faab_id'],
                review_item['potential_matches']
            )
            
            if confirmed_match:
                confirmed_matches.append(confirmed_match)
            else:
                unmatched.append({
                    'faab_id': review_item['faab_id'],
                    'faab_name': review_item['faab_name'],
                    'reason': 'User declined suggested matches'
                })
    
    return exact_matches, confirmed_matches, unmatched

def create_id_mapping_csv(exact_matches, confirmed_matches, unmatched, output_file='faab_sleeper_id_mapping.csv'):
    """
    Create a CSV file with ID mappings
    
    Args:
        exact_matches (list): Exact matches
        confirmed_matches (list): User-confirmed matches
        unmatched (list): Unmatched players
        output_file (str): Output CSV filename
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['faab_id', 'faab_name', 'sleeper_id', 'sleeper_name', 
                     'position', 'team', 'active', 'confidence', 'similarity_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Write exact matches
        for match in exact_matches:
            writer.writerow({
                'faab_id': match['faab_id'],
                'faab_name': match['faab_name'],
                'sleeper_id': match['sleeper_id'],
                'sleeper_name': match['sleeper_name'],
                'position': match['position'],
                'team': match['team'],
                'active': match['active'],
                'confidence': match['confidence'],
                'similarity_score': match['similarity_score']
            })
        
        # Write confirmed matches
        for match in confirmed_matches:
            writer.writerow({
                'faab_id': match['faab_id'],
                'faab_name': match['faab_name'],
                'sleeper_id': match['sleeper_id'],
                'sleeper_name': match['sleeper_name'],
                'position': match['position'],
                'team': match['team'],
                'active': match['active'],
                'confidence': match['confidence'],
                'similarity_score': match['similarity_score']
            })
        
        # Write unmatched
        for item in unmatched:
            writer.writerow({
                'faab_id': item['faab_id'],
                'faab_name': item['faab_name'],
                'sleeper_id': '',
                'sleeper_name': '',
                'position': '',
                'team': '',
                'active': '',
                'confidence': 'NONE',
                'similarity_score': 0.0
            })

def create_json_mapping(exact_matches, confirmed_matches, output_file='faab_sleeper_mapping.json'):
    """
    Create a JSON mapping for easy programmatic use
    
    Args:
        exact_matches (list): Exact matches
        confirmed_matches (list): Confirmed matches
        output_file (str): Output JSON filename
    """
    mapping = {}
    
    # Add exact matches
    for match in exact_matches:
        mapping[match['faab_id']] = match['sleeper_id']
    
    # Add confirmed matches
    for match in confirmed_matches:
        mapping[match['faab_id']] = match['sleeper_id']
    
    with open(output_file, 'w') as jsonfile:
        json.dump(mapping, jsonfile, indent=2)
    
    print(f"Created JSON mapping with {len(mapping)} verified mappings")

def display_mapping_results(exact_matches, confirmed_matches, unmatched):
    """
    Display mapping results summary
    
    Args:
        exact_matches (list): Exact matches
        confirmed_matches (list): Confirmed matches
        unmatched (list): Unmatched players
    """
    total = len(exact_matches) + len(confirmed_matches) + len(unmatched)
    
    print(f"\nFAAB to Sleeper ID Mapping Results")
    print("=" * 50)
    print(f"Total FAAB players: {total}")
    print(f"Exact matches: {len(exact_matches)} ({len(exact_matches)/total*100:.1f}%)")
    print(f"User confirmed matches: {len(confirmed_matches)} ({len(confirmed_matches)/total*100:.1f}%)")
    print(f"Unmatched: {len(unmatched)} ({len(unmatched)/total*100:.1f}%)")
    print(f"Total successful mappings: {len(exact_matches) + len(confirmed_matches)} ({(len(exact_matches) + len(confirmed_matches))/total*100:.1f}%)")
    
    if exact_matches:
        print(f"\nSample exact matches:")
        for match in exact_matches[:10]:
            print(f"  FAAB {match['faab_id']}: {match['faab_name']} -> {match['sleeper_id']} ({match['sleeper_name']})")
        if len(exact_matches) > 10:
            print(f"  ... and {len(exact_matches)-10} more")
    
    if confirmed_matches:
        auto_confirmed = [m for m in confirmed_matches if m['confidence'] == 'AUTO_CONFIRMED']
        user_confirmed = [m for m in confirmed_matches if m['confidence'] == 'USER_CONFIRMED']
        
        if auto_confirmed:
            print(f"\nAuto-confirmed high-confidence matches: {len(auto_confirmed)}")
            for match in auto_confirmed[:5]:
                print(f"  FAAB {match['faab_id']}: {match['faab_name']} -> {match['sleeper_name']} ({match['similarity_score']:.3f})")
        
        if user_confirmed:
            print(f"\nUser-confirmed matches: {len(user_confirmed)}")
            for match in user_confirmed[:5]:
                print(f"  FAAB {match['faab_id']}: {match['faab_name']} -> {match['sleeper_name']}")
    
    if unmatched:
        print(f"\nUnmatched players:")
        for item in unmatched[:10]:
            print(f"  FAAB {item['faab_id']}: {item['faab_name']} ({item['reason']})")
        if len(unmatched) > 10:
            print(f"  ... and {len(unmatched)-10} more")

def main():
    """
    Main function to create FAAB to Sleeper ID mappings with interactive confirmation
    """
    print("FAAB to Sleeper ID Mapping Tool (Interactive)")
    print("=" * 45)
    
    # Load FAAB data
    faab_dict = load_faab_data_with_ids()
    
    if not faab_dict:
        print("Failed to load FAAB data")
        return
    
    # Get Sleeper data
    sleeper_data = get_sleeper_players()
    
    if not sleeper_data:
        print("Failed to fetch Sleeper data")
        return
    
    print(f"Loaded {len(sleeper_data)} Sleeper players")
    
    # Get user preferences
    threshold = 0.8
    interactive_threshold = 0.95
    
    user_threshold = input(f"Minimum similarity threshold ({threshold}): ").strip()
    if user_threshold:
        try:
            threshold = float(user_threshold)
        except ValueError:
            print(f"Invalid threshold, using {threshold}")
    
    user_interactive = input(f"Auto-confirm threshold ({interactive_threshold}): ").strip()
    if user_interactive:
        try:
            interactive_threshold = float(user_interactive)
        except ValueError:
            print(f"Invalid threshold, using {interactive_threshold}")
    
    print(f"\nUsing thresholds: minimum={threshold}, auto-confirm={interactive_threshold}")
    print("Matches with scores between these values will require your confirmation.")
    
    # Perform matching
    print("\nMatching players...")
    exact_matches, confirmed_matches, unmatched = find_sleeper_matches_interactive(
        faab_dict, sleeper_data, threshold, interactive_threshold
    )
    
    # Display results
    display_mapping_results(exact_matches, confirmed_matches, unmatched)
    
    # Save results
    csv_file = 'faab_sleeper_id_mapping.csv'
    json_file = 'faab_sleeper_mapping.json'
    
    print(f"\nSaving results...")
    create_id_mapping_csv(exact_matches, confirmed_matches, unmatched, csv_file)
    create_json_mapping(exact_matches, confirmed_matches, json_file)
    
    print(f"\nFiles created:")
    print(f"  {csv_file} - Complete mapping results")
    print(f"  {json_file} - Ready-to-use ID mappings")
    
    print(f"\nMapping Summary:")
    total_mapped = len(exact_matches) + len(confirmed_matches)
    total_players = len(faab_dict)
    print(f"  Successfully mapped: {total_mapped}/{total_players} ({total_mapped/total_players*100:.1f}%)")
    print(f"  Ready for FAAB analysis!")
    
    # Sample usage code
    print(f"\nSample usage in your FAAB analysis:")
    print(f"```python")
    print(f"import json")
    print(f"with open('{json_file}', 'r') as f:")
    print(f"    id_mapping = json.load(f)")
    print(f"sleeper_id = id_mapping.get(str(faab_id))  # Convert faab_id to string")
    print(f"```")

if __name__ == "__main__":
    main()