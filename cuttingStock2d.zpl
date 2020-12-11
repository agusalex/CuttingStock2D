###Input###
set posibilidades := {read "rects.txt" as "<1n,2n,3n,4n>"};
set posters_cant := {read "posters_cant.txt" as "<1n,2n,3n>"};

#do print posibilidades;
###Variables###
var x[<i,j,k,m> in posibilidades] binary;

###Funcion Objetivo###
maximize espacioCubierto: sum<i,j,k,m> in posibilidades : x[i,j,k,m] * (k) * (m);

###Restricciones###								
subto noSuperposicion: forall<i,j,v,w> in posibilidades: 
							forall<k,m,y,z> in posibilidades:
								if (i!=k and v!=y) or (i==k and v!=y) or (i!=k and v==y) or (j!=m and w!=z) or (j==m and w!=z) or (j!=m and w==z)
									then if (i+v>k and i<k+y and j+w>m and j<m+z)
											then (x[i,j,v,w]+x[k,m,y,z])<= 1 
										 end 
									end;
									
subto cantidad: forall<w,h,u> in posters_cant: sum<i,j,k,m> in posibilidades with((k == w and m == h) or (k == h and m == w)): x[i,j,k,m] <= u;		