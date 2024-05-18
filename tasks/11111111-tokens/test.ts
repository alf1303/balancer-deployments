import { Task, TaskRunOptions } from '@src';

export default async (task: Task, { force, from }: TaskRunOptions = {}): Promise<void> => {
  // const pz_args = ["Puzzle Token", "PUZZLE", "355000000000000000000000"];
  const weth_args = ["Wrapped Ether", "WETH", "355000000000000000000000"];
  // const swopfi_args = ["Swopfi Token", "SWOP", "355000000000000000000000"];
  // const wx_args = ["WX Token", "WX", "355000000000000000000000"];
  const usdt_args = ["USDT Token", "USDT", "900000000000000000000000"];
  const usdc_args = ["USDC Token", "USDC", "900000000000000000000000"];
  const boba_args = ["Boba Token", "ptBOBA", "900000000000000000000000"];
  const eagle_args = ["Eagle Token", "ptEAGLE", "900000000000000000000000"];
  // const pz = await task.deployAndVerify('CustomToken', pz_args, from, force);
  // console.log("Deployed Puzzle:", pz.address);
  const weth = await task.deployAndVerify('CustomToken', weth_args, from, force);
  console.log("Deployed WETH:", weth.address);
  // const swopfi = await task.deployAndVerify('CustomToken', swopfi_args, from, force);
  // console.log("Deployed SWOPFI:", swopfi.address);
  // const wx = await task.deployAndVerify('CustomToken', wx_args, from, force);
  // console.log("Deployed WX:", wx.address);
  const usdt = await task.deployAndVerify('CustomToken', usdt_args, from, force);
  console.log("Deployed USDT:", usdt.address);
  const usdc = await task.deployAndVerify('CustomToken', usdc_args, from, force);
  console.log("Deployed USDC:", usdc.address);
  const boba = await task.deployAndVerify('CustomToken', boba_args, from, force);
  console.log("Deployed BOBA:", boba.address);
  const eagle = await task.deployAndVerify('CustomToken', eagle_args, from, force);
  console.log("Deployed EAGLE:", eagle.address);
};
