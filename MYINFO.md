yarn extract-artifacts --id 11111111-tokens

network config:  ~/.hardhat/networks.json, hardhat.config.ts

0) Deploy WETH: yarn hardhat deploy --id 00001111-wunit0 --network gnosis --force
1) Deploy tokens: 
   yarn hardhat deploy --id 11111111-tokens --network gnosis --force
2) add tokens to /home/rex/projects/other/balancer-deployments/tasks/00000000-tokens/output/gnosis.json

For verification check net config in bottom of hardhat.config.ts and ~/.hardhat/networks.json
3) deploy authorizers and vault:
set proper admin address in actual network section in tasks/authorizer/input.ts
yarn hardhat deploy --id 20210418-authorizer --network gnosis --force
yarn hardhat deploy --id 20210418-vault --network gnosis --force
** if ProtocolFeeCollectors is not verified, then after few minutes set proper addresses in 00001122-protocol_verify/index.ts and run 'yarn hardhat deploy --id 00001122-protocol_verify --network gnosis --force'
yarn hardhat deploy --id 20220325-authorizer-adaptor --network gnosis --force
yarn hardhat deploy --id 20221124-authorizer-adaptor-entrypoint --network gnosis --force
yarn hardhat deploy --id 20230414-authorizer-wrapper --network gnosis --force

4) Set vault's authorizer to authorizer-wrapper address:
   - get proper action (role) id by calling Vault's method getActionId('0x058a628f') where '0x058a628f' is method identificator for setAuthorizer   method
   - call grantRole method on Authorizer contract, using action_id and address of admin account
   - call setAuthorizer method on Vault's contract from admin account

Deploying WeightedPool:
1) yarn hardhat deploy --id 20220725-protocol-fee-percentages-provider --network gnosis --force
2) yarn hardhat deploy --id 20230320-weighted-pool-v4 --network gnosis --force

Deploying ManagedPool:
1) yarn hardhat deploy --id 20220725-protocol-fee-percentages-provider --network gnosis --force
2) yarn hardhat deploy --id 20230411-managed-pool-v2 --network gnosis --force


Run node:
docker run -p 8545:8545 -p 8546:8546 --mount type=bind,source=/home/rex/evm/testnodedata,target=/var/lib/besu hyperledger/besu:latest --miner-enabled --miner-coinbase fe3b557e8fb62b89f4916b721be55ceb828dbd73 --rpc-http-enabled --rpc-ws-enabled --data-path=/var/lib/besu --genesis-file=/var/lib/besu/dev.json  --host-allowlist=*

Run explorer sirato:
NODE_ENDPOINT=http://172.16.239.1:8545 docker-compose up
docker-compose down -v --> stop explorer and remove chain data

deployments settings (network and account) ~/.hardhat/networks.json

NOTES:
1) Sometimes Vault contract can fail with INSUFFICIENT_GAS Error. Then set runs option in optimizer in hardhat.config.ts to 200 or higher
