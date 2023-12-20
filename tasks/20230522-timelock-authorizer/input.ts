import { Task, TaskMode } from '@src';
import { DelayData, RoleData } from './input/types';

const Authorizer = new Task('20210418-authorizer', TaskMode.READ_ONLY);
const AuthorizerAdaptorEntrypoint = new Task('20221124-authorizer-adaptor-entrypoint', TaskMode.READ_ONLY);

export type TimelockAuthorizerDeployment = {
  Authorizer: string;
  AuthorizerAdaptorEntrypoint: string;
  Root: string;
  RootTransferDelay: number;
  getRoles: () => Promise<RoleData[]>;
  Granters: RoleData[];
  Revokers: RoleData[];
  ExecuteDelays: DelayData[];
  GrantDelays: DelayData[];
};

/* eslint-disable @typescript-eslint/no-explicit-any */
export type TimelockAuthorizerDeploymentInputType = {
  Authorizer: Task;
  AuthorizerAdaptorEntrypoint: Task;
  networks: string[];
  [key: string]: any; // index signature
};
/* eslint-enable @typescript-eslint/no-explicit-any */

const input: TimelockAuthorizerDeploymentInputType = {
  Authorizer,
  AuthorizerAdaptorEntrypoint,
  networks: ['sepolia'],
};

// Include input files for each network inside global inputs.
input.networks.forEach((network) => {
  input[network] = require(`./input/${network}.ts`);
});

export default input;
