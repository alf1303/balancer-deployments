import { Task, TaskRunOptions } from '@src';

export default async (task: Task, { force, from }: TaskRunOptions = {}): Promise<void> => {

  const wunit = await task.deployAndVerify('WUNIT0', [], from, force);
  console.log("Deployed WUNIT:", wunit.address);
};
