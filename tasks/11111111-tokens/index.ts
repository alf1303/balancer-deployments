import { Task, TaskRunOptions } from '@src';

export default async (task: Task, { force, from }: TaskRunOptions = {}): Promise<void> => {
  const Test_args = ["Test_token1", "Test1", "355000000000000000000000"];
  const Test = await task.deployAndVerify('CustomToken', Test_args, from, force);
  console.log("Deployed Test:", Test.address);
};
