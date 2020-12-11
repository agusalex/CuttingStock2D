###Input###
set posibilidades := {read "rects.txt" as "<1n,2n,3n,4n>"};
param cantA := read "cantidadPosterA.txt" as "1n" use 1;
param cantB := read "cantidadPosterB.txt" as "1n" use 1;
param cantC := read "cantidadPosterC.txt" as "1n" use 1;

set posterA := {read "poster.txt" as "<1n,2n>" use 1};
set posterB := {read "poster.txt" as "<1n,2n>" skip 1 use 1};
set posterC := {read "poster.txt" as "<1n,2n>" skip 2 use 1};

#do print posibilidades;
###Variables###
var x[<i,j,k,m> in posibilidades] binary;

###Funcion Objetivo###
maximize postersInsertados: sum<i,j,k,m> in posibilidades : x[i,j,k,m] * (k) * (m);

###Restricciones###								
subto noSuperposicion: forall<i,j,v,w> in posibilidades: 
							forall<k,m,y,z> in posibilidades:
								if (i!=k and v!=y) or (i==k and v!=y) or (i!=k and v==y) or (j!=m and w!=z) or (j==m and w!=z) or (j!=m and w==z)
									then if (i+v>k and i<k+y and j+w>m and j<m+z)
											then (x[i,j,v,w]+x[k,m,y,z])<= 1 
										 end 
									end;
									
subto cantidadPostersA: forall<w,h> in posterA: sum<i,j,k,m> in posibilidades with((k == w and m == h) or (k == h and m == w)): x[i,j,k,m] == cantA;
							
subto cantidadPostersB: forall<w,h> in posterB: sum<i,j,k,m> in posibilidades with((k == w and m == h) or (k == h and m == w)): x[i,j,k,m] == cantB;
							
subto cantidadPostersC: forall<w,h> in posterC: sum<i,j,k,m> in posibilidades with((k == w and m == h) or (k == h and m == w)): x[i,j,k,m] == cantC;			