###Input###
set posters:={read "posters.txt" as "<1n,2n>"};
set anchoMuro := {read "anchos.txt" as "<1n>"}; #{0, 254};
set altoMuro := {read "altos.txt" as "<1n>"};
set cantidades := {read "cantidades.txt" as "<1n>"};
set posibilidades := anchoMuro cross altoMuro cross posters;
param maxAlto := read "maxAlto.txt" as "1n" use 1;
param maxAncho := read "maxAncho.txt" as "1n" use 1;


###Variables###
var x[<i,j,k,m> in posibilidades] binary;

###Funcion Objetivo###
maximize segmentosInsertados: sum<i,j,k,m> in posibilidades : x[i,j,k,m] * (k) * (m);

###Restricciones###								
subto noSuperposicion: forall<i,j,v,w> in posibilidades: 
							forall<k,m,y,z> in posibilidades:
								if (i!=k and v!=y) or (i==k and v!=y) or (i!=k and v==y) or (j!=m and w!=z) or (j==m and w!=z) or (j!=m and w==z)
									then if (i+v>k and i<k+y and j+w>m and j<m+z)
											then (x[i,j,v,w]+x[k,m,y,z])<= 1 
										 end 
									end;
									
subto noSobrepasarAncho: forall<i,j,k,m> in posibilidades: 
								(i+k) * x[i,j,k,m] <= maxAncho;
								
subto noSobrepasarAlto: forall<i,j,k,m> in posibilidades: 
								(j+m) * x[i,j,k,m] <= maxAlto;

#Tiene que estar esta para limitar la cantidad de posters que pegamos, medio que se contradice con la funcion objetivo pero bueno							
#subto cantidadPosters: forall<i,j,k,m> in posibilidades: cantidades[k*m*x[i,j,k,m]] >= 4;	

