import math

# --- osnovna struktura podataka i funkcije za podrsku

class point:
    
    def __init__(self,x,y):
        self.x=x
        self.y=y

def line(p1,p2,n):
    # p1 - starting point
    # p2 - ending point
    # n - number of points along the line including the end points

    x1=p1.x
    y1=p1.y
    x2=p2.x
    y2=p2.y
    
    data_x=[]
    data_y=[]
    
    dx=x2-x1
    dy=y2-y1

    for i in range (1,n+1):
        xi=x1+dx/(n-1)*(i-1)
        yi=y1+dy/(n-1)*(i-1)
        
        data_x.append(xi)
        data_y.append(yi)

    return data_x, data_y

def wedge(p1,p2,pm,n):
    # p1 - starting point
    # p2 - ending point
    # pm - midpoint
    # n - number of points along one piece of line including the end point and the midpoint
    #     total number of points along the wedge is 2n-1

    x1=p1.x
    y1=p1.y
    x2=p2.x
    y2=p2.y
    xm=pm.x
    ym=pm.y    
    
    data_x=[]
    data_y=[]
    
    dx=xm-x1
    dy=ym-y1

    for i in range (1,n+1):
        xi=x1+dx/(n-1)*(i-1)
        yi=y1+dy/(n-1)*(i-1)
        
        data_x.append(xi)
        data_y.append(yi)

    dx=x2-xm
    dy=y2-ym        

    for i in range (n+1,2*n):
        xi=xm+dx/(n-1)*(i-n)
        yi=ym+dy/(n-1)*(i-n)
        
        data_x.append(xi)
        data_y.append(yi)
        

    return data_x, data_y


def arc(p1,p2,pc,n):
    # p1 - starting point
    # p2 - ending point
    # pc - center point      
    # n - number of points along the arc including the end points
    #
    # the arc is drawn from the point p1 to the point p2 following
    # counter-clockwise direction (positive rotational direction)
    # if this direction is not desired, the points p1 and p2
    # should be swapped when calling this function
    
    x1=p1.x
    y1=p1.y
    x2=p2.x
    y2=p2.y
    xc=pc.x
    yc=pc.y
    
    data_x=[]
    data_y=[]

    r=math.sqrt((x1-xc)**2+(y1-yc)**2)
    
    dx1=x1-xc
    dy1=y1-yc    
    phi1=math.acos(dx1/r)
    if dy1<0: phi1=-phi1
    
    dx2=x2-xc
    dy2=y2-yc    
    phi2=math.acos(dx2/r)
    if dy2<0: phi2=-phi2

    if phi2<phi1: phi2=phi2+2*math.pi
    
    for i in range (1,n+1):
        phi_i=phi1+(phi2-phi1)/(n-1)*(i-1)
        xi=xc+r*math.cos(phi_i)
        yi=yc+r*math.sin(phi_i)
        
        data_x.append(xi)
        data_y.append(yi)

    return data_x, data_y

# --- glavni dio programa

# vrhovi bloka i pomocne tacke (centri lukova, ukoliko ih ima)
P1=point(0,0)
P2=point(10,0)
P3=point(10,10)
P4=point(0,10)

C1=point(5,5)


# granicne linije
bl1_x, bl1_y=arc(P1,P2, C1, 11)
bl2_x, bl2_y=arc(P2,P3, C1, 11)
bl3_x, bl3_y=arc(P3,P4, C1, 11)
bl4_x, bl4_y=arc(P4,P1, C1, 11)

#reverse_line=[True, False, False, True]
reverse_line=[False, False, True, True]
# linearna transfinitna interpolacija unutar granicnih linija

# provjera da li naspramne stranice imaju isti broj tačaka
if len(bl1_x) != len(bl3_x) or len(bl2_x) != len(bl4_x):
    print (" naspramne stranice nemaju jednak broj tačaka")
    quit()
    
# sparivanje tacaka na naspramnim linijama, ovisno o orijentaciji linije 
if reverse_line[0]:
    bl1_x.reverse()
    bl1_y.reverse()

if reverse_line[1]:
    bl2_x.reverse()
    bl2_y.reverse()

if reverse_line[2]:
    bl3_x.reverse()
    bl3_y.reverse()    

if reverse_line[3]:
    bl4_x.reverse()
    bl4_y.reverse()

# interpolacija
    
eta_line_x=[]
eta_line_y=[]
xi_line_x=[]
xi_line_y=[]                                

for i in range (0,len(bl1_x)):
    datax=[]
    datay=[]
    for j in range (0,len(bl2_x)):
        xi=i/(len(bl1_x)-1)
        eta=j/(len(bl2_x)-1)
        
        x=(1-xi)*bl4_x[j]+xi*bl2_x[j]+\
           (1-eta)*bl1_x[i]+eta*bl3_x[i]-\
           (1-xi)*(1-eta)*bl1_x[0]-xi*(1-eta)*bl1_x[len(bl1_x)-1]-\
           (1-xi)*eta*bl3_x[0]-xi*eta*bl3_x[len(bl3_x)-1]

        y=(1-xi)*bl4_y[j]+xi*bl2_y[j]+\
           (1-eta)*bl1_y[i]+eta*bl3_y[i]-\
           (1-xi)*(1-eta)*bl1_y[0]-xi*(1-eta)*bl1_y[len(bl1_x)-1]-\
           (1-xi)*eta*bl3_y[0]-xi*eta*bl3_y[len(bl3_x)-1]

        datax.append(x)
        datay.append(y)
                
    eta_line_x.append(datax)
    eta_line_y.append(datay)

    # transpose the matrix data for the grid lines along xi direction
    xi_line_x=[*zip(*eta_line_x)]
    xi_line_y=[*zip(*eta_line_y)]  
            
# --- graficki prikaz
import matplotlib.pyplot as plt     
slika = plt.figure(figsize=(6,6))   
dijagram=plt.subplot(1,1,1)         

l1 = plt.plot(bl1_x, bl1_y, c='r', ls='-', lw=3, marker='None', markersize=3, markerfacecolor='k',label="$south$")
l2 = plt.plot(bl2_x, bl2_y, c='g', ls='-', lw=3, marker='None', markersize=3, markerfacecolor='k',label="$east$")
l3 = plt.plot(bl3_x, bl3_y, c='b', ls='-', lw=3, marker='None', markersize=3, markerfacecolor='k',label="$north$")
l4 = plt.plot(bl4_x, bl4_y, c='m', ls='-', lw=3, marker='None', markersize=3, markerfacecolor='k',label="$west$")
for i in range (0,len(bl1_x)):
    plt.plot(eta_line_x[i-1], eta_line_y[i-1], c='grey', ls='-', lw=1, marker='o', markersize=1, markerfacecolor='grey',label="$mesh$")
for i in range (0,len(bl2_x)):
    plt.plot(xi_line_x[i-1], xi_line_y[i-1], c='grey', ls='-', lw=1, marker='o', markersize=1, markerfacecolor='grey',label="$mesh$")    

lx = plt.xlabel("$x$",fontsize=16)
ly = plt.ylabel("$y$",fontsize=16)
plt.xticks(fontsize=12, rotation=0, ha='center', va='top')
plt.yticks(fontsize=12, rotation=0, ha='right', va='center')
plt.xlim(-5,15)
plt.ylim(-5,15)
#plt.legend(loc="lower left", frameon=True, borderpad=1, framealpha=1, edgecolor="inherit", prop={'size': 12}, handlelength=4)
plt.axhline(y=0, color='grey', lw=0.5)
plt.axvline(x=0, color='grey', lw=0.5)

plt.savefig('3.png')
plt.show()

"""
# Writing to a file
file1 = open('myfile.txt', 'w')
file1.writelines((L))
file1.close()
 
# Using readline()
file1 = open('myfile.txt', 'r')
count = 0
 
while True:
    count += 1
 
    # Get next line from file
    line = file1.readline()
 
    # if line is empty
    # end of file is reached
    if not line:
        break
    print("Line{}: {}".format(count, line.strip()))
 
file1.close()
"""
