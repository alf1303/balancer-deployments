import { Task, TaskRunOptions } from '@src';

export default async (task: Task, { force, from }: TaskRunOptions = {}): Promise<void> => {

  const feeCollector = "0xbe3d08ab6D1b451841308755C0cA283b94B83324"; // ProtocolFeesCollector address
  const feeCollectorArgs = ["0x858547402B702CDF3320efc99A7DC7ED5c29836A"]; // See ProtocolFeesCollector constructor # VAULT address
  await task.verify('ProtocolFeesCollector', feeCollector, feeCollectorArgs);
};
