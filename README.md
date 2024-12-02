# FiltrosParalelo
Este repositorio contiene el código en Python para aplicar 6 filtros diferentes a imágenes usando el paralelismo, presentado como proyecto final para la asignatura Programación Paralela.

Los integrantes del equipo son:
- Christopher Arturo Rajón Polanco
- Luz Rocío García Peña

## Descripción del proyecto
Haciendo uso del paralelismo, se seleccionan imágenes del propio dispositivo del usuario y se cargan en la vista. El usuario puede elegir cualquiera de los 6 filtros disponibles para aplicarlo a todas las imágenes que haya seleccionado. Una vez aplicado el filtro, el usuario puede dar clic a la imagen modificada para verla en grande y notar con mayor detalle el cambio realizado al aplicar el filtro y también puede abrir en grande la imagen original si lo desea.

## SpeedUp y Eficiencia

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


### SpeedUp
Canny = $1.32 \div 0.32 = 4.12$  
GaussianBlur = $1.54 \div 0.7 = 2.2$  
Laplacian = $1.72 \div 0.44 = 3.909$  
Sobel = $2.53 \div 0.92 = 2.75$  
Mean = $1.38 \div 0.25 = 5.52$  
Median = $10.23 \div 5.09 = 2.009$

### Eficiencia
Canny = $4.125 \div 4 = 1.03$
GaussianBlur = $2.2 \div 4 = 0.55$
Laplacian = $3.909 \div 4 = 0.97$
Sobel = $2.75 \div 4 = 0.68$
Mean = $5.52 \div 4 = 1.38$
Median = $2.009 \div 4 = 0.502$

