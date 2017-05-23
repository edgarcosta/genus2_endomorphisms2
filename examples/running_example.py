import sys
sys.path.append(".");
import heuristic_endomorphisms
import misc
import AJ
AJ.load_gp();
import InvertAJglobal
import bound_rosati
import newton_lift


from sage.all import CDF, ComplexField, I, Matrix, NumberField, QQ, PolynomialRing
from sage.all import ceil, gp, latex, set_random_seed, sqrt, vector


digits= 600
prec = 2000
QQx = PolynomialRing(QQ, 'x');
g = QQx([-1, 5, -8, 4, -1, 1])
print "y^2 = %s" % latex(g)
End = heuristic_endomorphisms.EndomorphismData(g, prec = digits)
CClow = ComplexField(16);
CCap = ComplexField(prec);
K = End.field_of_definition()
alpha = Matrix([[0,sqrt(2)],[sqrt(2), 0]])
alphas =[misc.convert_magma_matrix_to_sage(elt, K).transpose() for elt in End.geometric_representations()[0]]
alphas_geo =[misc.convert_magma_matrix_to_sage(elt, QQ).transpose()  for elt in End.geometric_representations()[2]]
alpha_magma = -(2*alphas[2] -(alphas[0]  + alphas[1]))
alpha_geo = -(2*alphas_geo[2] -(alphas_geo[0]  + alphas_geo[1]))
#print alpha_magma
print "M = %s" % latex(alpha)
alpha_CCap = alpha.change_ring(CCap)
print "\quad"
print "R = %s" % latex(alpha_geo)
Pi = End.period_matrix().transpose()
print "%% M Pi = Pi R ? %s" % (CClow(vector((Pi * alpha_geo - alpha_CCap* Pi).list()).norm()),)
print "%% sqrt(2) = %s" % (CClow(alpha_CCap[0,1]),)


#Deals with odd degree f
P = (2, 5)
assert P[1] ** 2 == g(P[0])
P_CCap = vector(CCap, P)
print "P = %s %% = %s " % (latex(P), vector(CClow, P))
print "P_0 = (%s, 0)" % (gp.polroots(g)[1],)
G = g.parent()(list(reversed(g.padded_list(7))))
x0, y0 = P_CCap;
v = 1/x0;
w = CCap(y0/(x0**3));
# 0 = AJ.AJ1_digits( G, (0,0), digits)
total = (0 - vector(CCap, AJ.AJ1_digits( G, (v,w), digits)) ).list();
total.reverse();
#ajP = \int_\inf ^P w_i
ajP = vector(CCap, total);
alphaP_an = vector(CCap, alpha_CCap * ajP)
print "b \\approx %s" % (latex(Matrix(CClow, ajP).transpose()))

prec=1994
import random
seed = 1
random.seed(seed)
set_random_seed(seed)
iaj = InvertAJglobal.InvertAJglobal(g, prec, False);
iaj.iajlocal.verbose = False
alphaP_div = iaj.invertAJ(alphaP_an, 10)

# depend on the seed!
Q = [(0.92243522256797054577629117628229042518574238306341704170203175092270707227816998411395599908402249895914861534693791913080427164188899810012069026640523462795339825093582226073343897039584625785673316272757394685982835882981672465662244612518627522638207366142261482138934683891621770945132619254697256223390001553134170763910152191778429300612971398345045003989170038311417168072223420338848340378512477846630243172211002412980326650314835877533490404036038989478901890620713042636848583196595852236427192106576168759006274861003671571102162719192205560019357638678465362845479258411366601897318967 + 0.85210532320381637818164854946799802337216580035730277317797972699742947578822634743820407011445317758869504800574958833696044695025678721256093693509713467170323978784872600534253966180144771561185774507573906936322135676752758374410734403151344588425655507835282065295633256023275166596883572750095937492673108222963661783909606188119970338808130041396623186036860670357152774740777893579079349512634755817878394528330858114004013148662660353757028502905103711908258963860991825465608477595848881655653417165860887295637214805914673390528093026292262504085548578732343472957196705457718320008336686*I, 1.1033050840624623828608287950555330582001849055926803990401309724995572376253675857278362572759177931038366722553944618509419572425134957829825565655803002521066648937069664830895384379620639045223771193918614384438867795565549384507930605396759788913166407464682180638667594328947683382366562692229019303779518222553841972635353028513272985313631792909280598442030941869003897664498493223793238753483273396806747708579030682627274904737537730259381831755788993545100794825386890659138662874125198323093021008845544444041605669212832475819439021527763620748673706078922565650698638436184969645995722 - 1.9091990655519686705174349377911538278070146721163296424228791895832840544534667073017495777402218215901035597593087349109104963079729296687739152709728227002734659605370299296115813706526139801007709680132516776072585013956888211088455868874978728077574399779710359342089569036564406347732450252114150755151548594363575438578992327141138667441089862631197905489087388828456737925669601743120088566696361699820294296354092073337495737657676310194208712167007287714331373787159639452624891905357717384441186225189286332362676392793048719458559834450947969207351127809905292605844927701874386424725836*I), (0.32570156675768474031801190510414413898004598582118332718323530238702999004916442960534704936399334153758641653638600410117642787837179179806723893993146005529946603491867453471554162955827805366204769356304050617326148527371904481819215743532254223992656216246418054401316780329949616286258084140198500770361897200005821001130526706732342534146218415178701569451376372702180048399945902841685535249808903275035733873700253150023780497711449960879034090708546555355015110275385600164312702686794411556161169085485665661987905275254305199997492813965247610532806770457484779703468375089400601009211225 + 0.95918809360580248623467188859651855153901527806118305128581821266163955575037729560674829716679565076230535399332544064903898358844446111219664268787455649873906844821608487299394383242274830709137977461756605458639798048802140202880325913040387244378516565562052201724430181227779195165513224695038925854246821189023930028046849509831285072343859010810631202841634687176032289978624604300379303329620320916718290178319774250035032863286418210969080193927806065948614937085604775585081765996840356078761044244148417832283246413190567829898013830718288652943975081690852511630030186489215257064757379*I, 2.1465005412568922038267896543990820412161517962937560408992601362607383246559395820859009735151698951211504198847273295155521129758228506063463970658868788126712484812525764277040316561869328748424591590671065606214736763550602928557383274013683238141359256613286579868783015055456942079067021401997356954947211478201712973126604857447732359166285432041527468650995462899650926018495469687616420892603874945166684205623716610213649034161457924826343547171338505845100843489556746194175976576685063630427936101416614275727653282426415230503589106111280332679238991512388420111633504901305928685209370 - 0.36446735684652377260216259757438173408191269815647644500492445383829625528142546263942836129811869549988396026243859029464789341700521609321838971255092308863535670245511714997917337850457333164445956233669544004858875800391553804269005324192006172356844198222136358236920847336415234241316009093456470156118251644301740509226057465275720565608880152940717262669939922923622230822198403936943791336489241879047601378101198050566801148946297168711472830153658061744780335139538010071187342421175188350663785044496635479571787093470364953805105998832586031517391917433746506736368618218011753371151743*I)]
B = [(0.91626983664478729649940401520377346249089903887404916145380247881467567126658529045695432539424897975936428306412819693481869369576108731846476141171407825183869405450075905546816389093635267749884285379842088368745934235999950764179838475502117891299898622214869119390778676615531058989926087907722353318815878141127203382945178035816879310097012441763160551991070642917198749820669545190097461199000071556170689743930191615592587616510557612092143682088264048021581268284609959754043205819973833037550309604126891820543591155677058108552123610873527908068252370466122121841994750395785639489154682 + 0.84830156844739259942358356719902217745531995763276330780056766100571942352392518278057754653489299230650136391957927421341270504943277517551158398053639530664277907222104440875373286325800091916500864158798872961307293812238616342618325960507267339488453753960814397004739951334176397276676582904473919509957026611756382845702810072196503211340879726490464109884422575135751093702873800793930734580757091801891668227482244882203919916745149413452446381740569416592218369583648811694367857505859985295544786208240501329076317964591718479032489036017790656971466702581577913290954019002202046552092585*I, 1.1041386601114886129463120693388694654819702583425504733851976545242396487322714500485582997084097540514201452488794313224960618607427726666849132815824481073123416753554279157137921518428530073042304074734909032457962920976553908409964261682308419755963088127511072106915710194356667164375790642442981708388952171372292571189373438240615305970500233407644509087502504724537891872952637300428346774035406754241065494728210499531525519752574780037630505050293100712512745310784026740464768515228956896220145116373346686263140328186207144842455321638730963255275894060562032725244351436980661323901899 - 1.8835498881839247297217814393967551744586746481059617749356302218893155847638437197279645966791913494782841534419547383598444252291207002684784254808758001647142017179102638452868392688173229151005321979866918817754151668497332336210420540491590480757502009980657034427153862998505797842088917724521163260022799781259933097435018805605860282267985875018585713168080501599712251850942594947032134782345123803627463383484502406039688102074326619489563222568482753282957318587554568074865524828906963056706749583854296128952005170680354824439497980429816303888971841334633841585682529044307047619082200*I), (0.33113745527798769205491384483083340772393126185510042222415312130352343226071900311090253989803482645451625005083059793125946386487840398160290945979644321173449179017860588651906639553092419078958167508157601570425335870606223990836917119316713007314494565442588151419206906318173283959841016165172107053599854809845183903507325963276688783693086654068679280195192872969134666960818301294512344205211118332853872108899947876662184349091238559513828886150078770622995069262373951193045996554971983588105869793216453569371614867447981895067522620899423869249276221048965214668030771239380268414405364 + 0.96556351931596358719280081056412566661115888697930206139562912805202455636066010694849526432347645213480589422194831787034622444055069626011152941259370963139970903100557515369406879177939704472633687684020857916961649589511052800159715358251214459758127060128350836804118724789218504936504933266479496203594684533573149941930789690498955876321559504821698083241923288544485746412661193774955354027615552781305115388191708247601813788116577264790838636848167049498408476807905459530081991970203953865629270539061749045290704300853575428650923445244277745593635418586990939578660458505057407887992166*I, 2.1590120112597952629120072478370149224652668705791539878606694299716981935094178406376867216583521455626029226952381780855397435184736819927982484930193506183796326256413449264282507132099931893822337668618877167585519827755958373386258624865812554201243718715122560221802764525224185509464973650108710196683568324744071893557617781957730946478679810233680278208955143941921636821465236517672380957679184282440800278897334439379544279461504164384762520417698502356001654019714375495562179917706587729202781031960069643076086626169280662823725616798684082366009996161157683949629855187870473317626220 - 0.38348313836550168461031235896843263365835754005058434504335880708901057256544228978750737970841869712726208935733429844617804578026550860413342703221708508572256114739951403586603371753603682505872963953237395506130402053355862451903048269096104875713795773017057015190058685063185540196376065917736112508822301014258116921941745330626303771744562591123361656696510785490576040426318034864055067527832010565300441931933398945467843740260232248661750960192543818065509976880171630959680058306683688055538838273676603896815630212640112759253079374019885447578986328216547603043942840641284485004983769*I)]


for j, M in enumerate([Q, B]):
    if j == 0:
        name = "Q"
    else:
        print "\\\\"
        name = "O"
    for i, row in enumerate(Matrix(M).rows()):
        # CDF gets rid of obvious zeros
        print "%s_%d &\\approx %s\\\\" % (name, i+1, latex(vector(CClow,vector(CDF, row))))
print "."


name = "P"
for i, row in enumerate(alphaP_div.coordinates()):
    print "%s_%d &\\approx %s\\\\" % (name, i+1, latex(vector(CClow, vector(CDF, row))))
print "."

algx_poly = [QQ(-3)/4, QQ(3)/2, 1];
print "%% x coordinates satisfy: "
print latex(QQx(algx_poly))
print "%% = %s" % (vector(CClow, vector(CDF, alphaP_div.x_coordinates())),)


P1 = ((3 - I * sqrt(3))/4, (QQ(-5)/16) *( sqrt(2) + I * sqrt(6)));
P2 = ((3 + I * sqrt(3))/4,  (QQ(-5)/16) *( sqrt(2) - I * sqrt(6)));
print "P1 &= %s \\\\%% = %s" % (latex(P1), vector(CDF, P1))
print "P2 &= %s \\\\%% = %s" % (latex(P2), vector(CDF, P2))
diff = vector(CClow, (Matrix(CCap, [P1, P2]) - Matrix(CCap, alphaP_div.coordinates())).list()).norm()
print "%% embedding agrees? %s" % diff

L = (alpha[1,0].minpoly()*P1[0].minpoly()).splitting_field('b', simplify_all = True)
L_poly = PolynomialRing(L, "xL");
xL = L_poly.gen();
M = NumberField(xL, "c")
P_M = vector(M, [misc.NF_embedding_algdep(CCap(elt), M) for elt in P])
P_L = vector(L, [misc.NF_embedding_algdep(CCap(elt), L) for elt in P])
P1_M = vector(M, [misc.NF_embedding_algdep(CCap(elt), M) for elt in P1])
P2_M = vector(M, [misc.NF_embedding_algdep(CCap(elt), M) for elt in P2])
alpha_M = Matrix(M, [ vector(M, [misc.NF_embedding_algdep(CCap(elt), M) for elt in row]) for row in alpha.rows() ])
alpha_L = Matrix(L, [ vector(L, [misc.NF_embedding_algdep(CCap(elt), L) for elt in row]) for row in alpha.rows() ])


rosati = bound_rosati.bound_rosati(alpha_geo);

trace_and_norm = newton_lift.trace_and_norm_ladic(L, M, P_M, P1_M, P2_M, g, alpha_M, rosati, primes = ceil(prec * L.degree()/61));
print "%% trace and norm in terms of x"
print map(QQx, trace_and_norm)

QQt = PolynomialRing(QQ, 't')
t = QQt.gen()
sub = t + P[0];
print "%% trace and norm in terms of t = x + %s, i.e, x = %s + t" % (P[0], -P[0])
print "x_1(t) + x_2(t) = \\frac{%s}{%s}" % (latex(QQt(trace_and_norm[0])(sub)), latex(QQt(trace_and_norm[1])(sub)))
print "x_1(t)x_2(t) = \\frac{%s}{%s}" % (latex(QQt(trace_and_norm[2])(sub)), latex(QQt(trace_and_norm[3])(sub)))
print "%% use Mathematica to deduce the series expansion for x_1 and x_2"


import verify_algebraically
verified = verify_algebraically.verify_algebraically(g, P_L, alpha_L/2, trace_and_norm, True)