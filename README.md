### how to test testwork?
``` sh
#[setup env]:
sudo docker build . -t testwork -f ./Dockerfile
sudo docker run --name stand -d -it testwork

#[terminal1]:
sudo docker exec stand ganache-cli

#[terminal2]:
sudo docker exec -w /teststand/ stand truffle migration --network development
sudo docker attach stand
# execute into docker shell
python3 front.py <address stakingCoin> <private key owner stakingCoin>
```
