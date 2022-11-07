FROM ubuntu:22.04
RUN echo "[*] prepare enviroment" && sleep 3 &&  apt-get update && apt-get install python3 python3-pip nodejs npm -y
RUN npm install -g truffle && npm install -g ganache-cli
RUN pip3 install web3
RUN mkdir /teststand
COPY front/ /teststand
COPY stakingToken/ /teststand
WORKDIR /teststand
RUN npm install @openzeppelin/contracts
RUN echo "[+] enviroment complete init"
