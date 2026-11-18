$salida = 'C:\tmp\lista_sz.txt'

# ejecuta el programa en C en el directorio actual
& .\lista_size.exe
if ($LASTEXITCODE -ne 0) { # equialente a $? de POSIX en Bash
    Write-Error "lista_size.exe ha fallado ($LASTEXITCODE)"
    exit 1
}

# comprobamos que se haya creado el archivo de salida
if (-not (Test-Path $salida)) {
    Write-Error "no existe $salida"
    exit 1
}

// inicializo variables, no es necesario en scripts de shell pero siempre es
// mas seguro y como PowerShell permite castear, lo aprovecho tambien
$total = 0
$n = 0
$minNombre = '';
$minTam = [uint64]::MaxValue
$maxNombre = '';
$maxTam = [uint64]0
 
foreach ($linea in Get-Content $salida) {
    if (-not $linea) { continue }
 
    # en Windows ':' no puede ir en un nombre de fichero y asi parseo mas facil
    $nombre, $tam = $linea -split ':'
    $tam = [uint64]$tam
 
    $total += $tam
    $n++
 
    if ($tam -lt $minTam) { $minTam = $tam; $minNombre = $nombre }
    if ($tam -ge $maxTam) { $maxTam = $tam; $maxNombre = $nombre }
}
 
if ($n -eq 0) {
    "No hay ficheros en el directorio"
    exit 0
}
 
"Tamano Total:        $total bytes"
"Mas pequeno:  $minNombre ($minTam bytes)"
"Mas grande:   $maxNombre ($maxTam bytes)"
