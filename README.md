## `API-Endpoints`
### `POST /kmeans/`

Dieser Endpunkt ermöglicht es Ihnen, k-means-Clustering auf Ihren Daten durchzuführen. Hier sind die verfügbaren Parameter:

-   `file` (Pflicht): Dies ist das Hochladen der JSON- oder CSV-Datei, auf der das Clustering durchgeführt werden soll.
    
-   `k` (Pflicht): Dies ist die Anzahl der Cluster, die Sie erstellen möchten.
    
-   `number_kmeans_runs` (optional): Dies ist die Anzahl der Durchläufe, die der k-means-Algorithmus mit unterschiedlichen Anfangszentrumspositionen ausführen soll. Standardmäßig ist der Wert 10.
    
-   `max_iterations` (optional): Die maximale Anzahl von Iterationen, die der k-means-Algorithmus durchführen soll, bevor er stoppt. Der Standardwert beträgt 300.
    
-   `tolerance` (optional): Dies ist die Höhe der Frobenius-Norm, die unterschritten werden muss, damit der k-means-Algorithmus mit der Iteration stoppt. Der Standardwert beträgt 0.0001.
    
-   `init` (optional): Dies ist die Methode zur Initialisierung der Clusterzentren. Es stehen drei Optionen zur Verfügung:
    
    -   "k-means++" (Standard): Die besten initialen Startzentren automatisch auswählen.
    -   "random": Zufällige Auswahl der Startpunkte.
    -   "centroids": Verwenden Sie die bereitgestellten Anfangszentren (in Form eines JSON-Strings).
-   `algorithm` (optional): Dies ist der Algorithmus, der für k-means verwendet werden soll. Es stehen vier Optionen zur Verfügung:
    
    -   "lloyd" (Standard): Der Standardk-means-Algorithmus.
    -   "elkan": Eine effizientere Version des k-means-Algorithmus.
    -   "auto" (veraltet): Eine veraltete Option, die den Algorithmus automatisch auswählt.
    -   "full" (veraltet): Eine veraltete Option, die den Standardalgorithmus auswählt.
-   `centroids` (optional): Dies ist ein JSON-String, der die Anfangszentren für die Cluster angibt. Diese Option wird nur verwendet, wenn `init` auf "centroids" gesetzt ist.
    
-   `normalization` (optional): Dies ist eine Zeichenfolge, die die Normalisierung der Daten angibt. Es stehen zwei Optionen zur Verfügung:
    
    -   "min-max": Min-Max-Normalisierung.
    -   "z": Z-Transformation.

### `POST /elbow/`

Dieser Endpunkt ermöglicht es Ihnen, die optimale Anzahl von Clustern mithilfe der Elbow-Methode zu ermitteln. Die Parameter sind weitgehend identisch mit denen des `POST /kmeans/`-Endpunkts, mit Ausnahme von `k`, da hier ein Bereich von `k_min` bis `k_max` angegeben wird, für den die Elbow-Methode durchgeführt wird. Hier sind die verfügbaren Parameter:

-   `file` (Pflicht): Die hochzuladende JSON- oder CSV-Datei.
    
-   `k_min` (Pflicht): Die niedrigste Anzahl von Clustern, die für die Elbow-Methode getestet werden sollen.
    
-   `k_max` (Pflicht): Die höchste Anzahl von Clustern, die für die Elbow-Methode getestet werden sollen.
    

Die übrigen Parameter wie `number_kmeans_runs`, `max_iterations`, `tolerance`, `init`, `algorithm`, `centroids` und `normalization` sind ebenfalls verfügbar und wirken sich auf die Durchführung der Elbow-Methode aus.

### `GET /kmeans/status/{task_id}`

Dieser Endpunkt ermöglicht es Ihnen, den aktuellen Status eines k-means-Clustering-Tasks anhand der angegebenen `task_id` abzurufen. Hier sind die Details:

-   `task_id` (Pflicht): Dies ist die eindeutige ID des Clustering-Tasks, den Sie überwachen möchten.
    
-   Antwort: Die API gibt den aktuellen Status des Tasks zurück, der eine der folgenden Werte sein kann:
    
    -   `"processing"`: Der Task wird noch verarbeitet.
    -   `"completed"`: Der Task wurde erfolgreich abgeschlossen und die Ergebnisse sind verfügbar.
    -   `"Bad Request"`: Ein Fehler ist aufgetreten, und im Feld `detail` wird eine Fehlermeldung angezeigt.

### `GET /kmeans/result/{task_id}`

Dieser Endpunkt ermöglicht es Ihnen, die Ergebnisse eines abgeschlossenen k-means-Clustering-Tasks anhand der angegebenen `task_id` abzurufen. Hier sind die Details:

-   `task_id` (Pflicht): Dies ist die eindeutige ID des Clustering-Tasks, dessen Ergebnisse Sie abrufen möchten.
    
-   Antwort: Die API gibt die Ergebnisse des Tasks zurück, die entweder ein JSON-String oder eine Fehlermeldung sein können:
    
    -   Wenn der Task erfolgreich abgeschlossen wurde, gibt die API die Ergebnisse im JSON-Format zurück.
    -   Wenn ein Fehler aufgetreten ist, gibt die API eine Fehlermeldung zurück, die im Feld `detail` enthalten ist.

Die `GET`-Methoden dienen dazu, den Status eines laufenden oder abgeschlossenen Tasks abzurufen sowie die Ergebnisse eines abgeschlossenen Tasks abzurufen. Sie können diese Methoden verwenden, um den Fortschritt Ihrer Clustering-Aufgaben zu überwachen und die Ergebnisse abzurufen, sobald sie verfügbar sind.

Bitte beachten Sie, dass die `task_id` eindeutig ist und jedem Task zugeordnet wird, den Sie über die `POST`-Methoden erstellen. Sie sollten die `task_id` speichern, um später auf den Status und die Ergebnisse des jeweiligen Tasks zugreifen zu können.