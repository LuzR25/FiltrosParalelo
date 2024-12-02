# FiltrosParalelo
Este repositorio contiene el código en Python para aplicar 6 filtros diferentes a imágenes usando el paralelismo, presentado como proyecto final para la asignatura Programación Paralela.

Los integrantes del equipo son:
- Christopher Arturo Rajón Polanco
- Luz Rocío García Peña

## Descripción del proyecto
Este programa aplica procesa imágenes y les aplica filtros haciendo uso del paralelismo. Permite:
- Cargar imágenes al programa desde el dispositivo (con paralelismo).
- Aplicar 9 diferentes filtros a las imágenes, que son los siguientes: Canny, GaussianBlur, Laplacian, Sobel, Mean, Median, UnsharpMask, Rotate, SobelWithOrientation.
- Medir el uso del CPU y el tiempo de procesamiento de las imágenes.
- Ver en grande una imagen al hacer clic en ella. Esto aplica tanto para la imagen original como la modificada.
- Guardar imágenes haciendo clic a la letra 'g' en el teclado luego de haber dado clic a la imagen para verla en grande.

## SpeedUp y Eficiencia

<table style="width:100%; border-collapse: collapse; text-align: center; vertical-align: middle;">
  <thead>
    <tr>
      <th rowspan="2">Procesadores</th>
      <th colspan="9">Tiempo (s) para n=82 imágenes</th>
    </tr>
    <tr>
      <th>Canny</th>
      <th>GaussianBlur</th>
      <th>Laplacian</th>
      <th>Sobel</th>
      <th>Mean</th>
      <th>Median</th>
      <th>UnsharpMask</th>
      <th>Rotate</th>
      <th>SobelWithOrientation</th>
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
      <td>1.33</td>
      <td>1.63</td>
      <td>2.97</td>
    </tr>
    <tr>
      <td>2</td>
      <td>0.38</td>
      <td>0.78</td>
      <td>0.5</td>
      <td>1.09</td>
      <td>0.42</td>
      <td>6.04</td>
      <td>0.41</td>
      <td>0.95</td>
      <td>1.49</td>
    </tr>
    <tr>
      <td>4</td>
      <td>0.32</td>
      <td>0.7</td>
      <td>0.44</td>
      <td>0.92</td>
      <td>0.25</td>
      <td>5.09</td>
      <td>0.33</td>
      <td>0.86</td>
      <td>1.40</td>
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
UnsharpMask = $1.33 \div 0.33 = 4.03$  
Rotate = $1.63 \div 0.86 = 1.89$  
SobelWithOrientation = $2.97 \div 1.40 = 2.12$  

### Eficiencia
Canny = $4.125 \div 4 = 1.03$  
GaussianBlur = $2.2 \div 4 = 0.55$  
Laplacian = $3.909 \div 4 = 0.97$  
Sobel = $2.75 \div 4 = 0.68$  
Mean = $5.52 \div 4 = 1.38$  
Median = $2.009 \div 4 = 0.502$  
UnsharpMask = $4.03 \div 4 = 1.007$  
Rotate = $1.89 \div 4 = 0.47$  
SobelWithOrientation = $2.12 \div 4 = 0.53$  


