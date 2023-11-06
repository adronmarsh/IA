### 1. En la práctica se eliminan los atributos "Name", "Investigator or Source", "pdf", "href formula", "href", "original order". ¿Por qué crees que no se tienen en cuenta? ¿Crees que se podría sacar algún tipo de información de alguno de estos atributos? ¿Por qué?

<p>Creo que estos atributos no se tienen en cuenta ya que no son útiles a la hora de trabajar con los datos. No aportan ningún tipo de información relevante y por tanto ocupan columnas en nuestro dataset.</p>

### 2. ¿Por qué sacamos el mes y el día de “Case Number” y no de “Date”?

<p>Ambos atributos, "Case Number" y "Date" tienen la misma información pero en distinto formato y en este caso el formato de "Case "Number" es mucho más cómodo para poder extraer los datos.</p>

### 3. En el caso de ds_USA[‘Day’] y ds_USA[‘Month’], el valor 0 se corresponde con datos que no se conocen, ¿cómo utilizarías un algoritmo para inferir estos datos?


### 4. La variable ds_USA[‘Area’] contiene un valor nulo. En la práctica se ha optado por eliminar el registro. ¿Se podría haber rellenado con la media, la mediana o la moda? Razona la respuesta y escribe el comando correspondiente.

<p> En este caso, el procedimiento más correcto hubiera sido rellenar el valor nulo con la moda. Esto no afectaría en gran medida a la conclusión final y tendríamos un dato más que aportar. </p>

```copyable
ds_USA.drop(ds_USA[ds_USA['Area'].isna()].index, inplace = np.mean(de_USA['Area]))
```

### 5. ¿En la práctica aparecen outliers?, explícalo.

### 6. ¿Crees que el dataset está balanceado? Explícalo.

### 7. En la práctica, ¿qué normalizaciones de datos aparecen?

### 8. Al aplicar el método de la Varianza aparecen magnitudes muy diferentes, ¿a qué crees que es debido?

### 9. ¿Con qué atributos nos quedaremos si aplicamos Correlación? Explica la respuesta

### 10.  En Backward Elimination, ¿hay algún error en el código? Explícalo

### 11. ¿Qué es la discretización y el 1 hot encoding? Pon un ejemplo para ambos casos aplicado a la práctica. 
 
### 12. ¿Qué diferencias hay entre PCA1 y PCA2? ¿Con qué variables nos quedaríamos? 
