 lambda = lambda(HPS) +[-alpha*Tr*(b+cTr-2c*Ts)] +[alpha*(b-2c*Ts)]*T + [c*alpha]*T2
shortening: replace alpha=0.7836, Tr= 296.7, Ts=61.97 and set:

fx =-0.7836*296.7*(b+c*296.7-2*c*61.97)
gx =0.7836*(b-2*c*61.97)
hx = c*0.7836

with a,b,c is the parameters from eq. S2 in form: E= a+bT+cT^2
lambda = lambda(HPS) +fx +gx*T +hx*T2
---------------------------------------
a=-22.657
b=0.15379
c=-0.00025597
lambda(H)= lambda(HPS) -25.474060537497937 + 0.14536949272248*T - 0.000200578092*T2
--------------------------------------
a=-23.364
b= 0.15876
c=-0.00026696
lambda(A) = lamda(HPS) - 26.18813544485645 + 0.15033132675264*T  - 0.000209189856*T2 
--------------------------------------
a= 2.1607
b=-0.015064
c=0.000026
lambda(O) = lamda(HPS) + 2.4579836352288 -0.014329254383999998*T + 0.0000203736*T2
--------------------------------------
a= 10.475
b= 0.071482
c= 0.0001201
lambda(P) = lambda(HPS) -21.443043354801116 + 0.044349257181599995*T +0.00009411036*T2 (inconsistent)
--------------------------------------
a= 8.5997
b=-0.057676
c= 0.000093317
lambda(C) = lambda(HPS) + 9.661189715316128 -0.05425780315672799*T +0.0000731232012*T2