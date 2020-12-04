###Input###
#set cantidades := {read "cantidades.txt" as "<1n>"};
set posibilidades := {read "rects.txt" as "<1n,2n,3n,4n>"};


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
									
#subto noSobrepasarAncho: forall<i,j,k,m> in posibilidades: 
		#						(i+k) * x[i,j,k,m] <= maxAncho;
								
#subto noSobrepasarAlto: forall<i,j,k,m> in posibilidades: 
		#						(j+m) * x[i,j,k,m] <= maxAlto;

