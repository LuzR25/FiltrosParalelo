# FiltrosParalelo
Este repositorio contiene el código en Python para aplicar 6 filtros diferentes a imágenes usando el paralelismo, presentado como proyecto final para la asignatura Programación Paralela.

Los integrantes del equipo son:
- Christopher Arturo Rajón Polanco
- Luz Rocío García Peña

## Descripción del proyecto
Haciendo uso del paralelismo, se seleccionan imágenes del propio dispositivo del usuario y se cargan en la vista. El usuario puede elegir cualquiera de los 6 filtros disponibles para aplicarlo a todas las imágenes que haya seleccionado. Una vez aplicado el filtro, el usuario puede dar clic a la imagen modificada para verla en grande y notar con mayor detalle el cambio realizado al aplicar el filtro y también puede abrir en grande la imagen original si lo desea.

## Tabla de SpeedUp y Eficiencia

<table style="width:100%; border-collapse: collapse; text-align: center; vertical-align: middle;">
  <thead>
    <tr>
      <th rowspan="2">Procesadores</th>
      <th colspan="6">Tiempo (s) para n=82 imágenes</th>
    </tr>
    <tr>
      <th>Canny</th>
      <th>GaussianBlur</th>
      <th>Laplacian</th>
      <th>Sobel</th>
      <th>Mean</th>
      <th>Median</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td> 					
      <td>1.32</td>
      <td>1.54</td>
      <td>1.72</td>
      <td>2.53</td>
      <td>1.38</td>
      <td>10.23</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.38</td>
      <td>0.78</td>
      <td>0.5</td>
      <td>1.09</td>
      <td>0.42</td>
      <td>6.04</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.32</td>
      <td>0.7</td>
      <td>0.44</td>
      <td>0.92</td>
      <td>0.25</td>
      <td>5.09</td>
    </tr>
  </tbody>
</table>


###SpeedUp
Canny = $$ \frac{1.32}{0.32} = 4.12 $$ 
GaussianBlur = $$ \frac{1.54}{0.7} = 2.2 $$
Laplacian = $$ \frac{1.72}{0.44} = 3.909 $$ 
Sobel = $$ \frac{2.53}{0.92} = 2.75 $$ 
Mean = $$ \frac{1.38}{0.25} = 5.52 $$ 
Median = $$ \frac{10.23}{5.09} = 2.009 $$ 

  
