import { BalancerSDK, BalancerSdkConfig, Network } from '@balancer-labs/sdk';

const config: BalancerSdkConfig = {
  network: Network.SEPOLIA,
  rpcUrl: `https://rpc.sepolia.org`,
};
const balancer = new BalancerSDK(config);

async function ggg() {
    const poolId = "B433AECEE4D39BA915ED76BD2130EA0F1B615856000100000000000000000092"
    const pool = await balancer.pools.find(poolId);
    console.log(pool);
}

ggg()