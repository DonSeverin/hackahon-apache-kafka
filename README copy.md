To Run use:
 docker compose up -d

if in wsl and getting permission error:
    sudo groupadd docker
    sudo usermod -aG docker $USER

 Then use uv sync

 Start listening with transport_consumper.py
 Start api retrieval with transport_producer.py