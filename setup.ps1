python -m venv Venv
echo "Sanal ortam oluşturuldu."

$sourcePath = "$env:LOCALAPPDATA\RaspberryPIYapayZeka"
$destinationPath = ".\API"

.\Venv\Scripts\Activate.ps1
echo "Paketler yükleniyor..."
Start-Sleep -Seconds 1

.\Venv\Scripts\pip install -r requirements.txt
.\Venv\Scripts\pip install audioop-lts
echo "Paketler yüklendi."

echo "Kurulum tamamlandı."
deactivate