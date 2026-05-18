$port = 3000
$root = $PSScriptRoot
$url  = "http://localhost:$port/"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()
Write-Host "Flapy Brett server running at $url"
Write-Host "Press Ctrl+C to stop."

$mimeTypes = @{
  '.html' = 'text/html; charset=utf-8'
  '.js'   = 'application/javascript'
  '.css'  = 'text/css'
  '.png'  = 'image/png'
  '.jpg'  = 'image/jpeg'
  '.ico'  = 'image/x-icon'
  '.json' = 'application/json'
  '.woff2'= 'font/woff2'
}

while ($listener.IsListening) {
  try {
    $ctx  = $listener.GetContext()
    $req  = $ctx.Request
    $resp = $ctx.Response

    $localPath = $req.Url.LocalPath
    if ($localPath -eq '/' -or $localPath -eq '') { $localPath = '/index.html' }
    $filePath = Join-Path $root ($localPath.TrimStart('/'))

    if (Test-Path $filePath -PathType Leaf) {
      $ext  = [System.IO.Path]::GetExtension($filePath)
      $mime = if ($mimeTypes.ContainsKey($ext)) { $mimeTypes[$ext] } else { 'application/octet-stream' }
      $bytes = [System.IO.File]::ReadAllBytes($filePath)
      $resp.ContentType   = $mime
      $resp.ContentLength64 = $bytes.Length
      $resp.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $resp.StatusCode = 404
    }
    $resp.OutputStream.Close()
  } catch {}
}
