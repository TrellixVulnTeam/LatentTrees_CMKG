import torch

from tensorboardX import SummaryWriter

class MonitorTree():

    def __init__(self, pruning, logdir=None):

        super(MonitorTree, self).__init__()

        self.writer = SummaryWriter(logdir)
        self.pruning = pruning

    def write(self, model, it, report_tree=False, **metrics):

        if report_tree and self.pruning:

            self.writer.add_scalars('variables/eta_group', 
                {"linf": torch.norm(model.latent_tree.eta, p=float('inf')),
                 "l1": torch.norm(model.latent_tree.eta, p=1), 
                 "l0": torch.norm(torch.clamp(model.latent_tree.eta, 0, 1), p=0),
                 # "eta": model.latent_tree.eta,
                 }, it)

            self.writer.add_scalars('variables/d_group', 
                { 
                 "l0": torch.norm(torch.clamp(model.latent_tree.d, 0, 1), p=0),
                 # "d": model.latent_tree.d,
                 }, it)

        for key, item in metrics.items():
            self.writer.add_scalars(key, item, it)
        # self.writer.add_graph(model, x)

    def close(self, logfile="./monitor_scalars.json"):
        self.writer.export_scalars_to_json(logfile)
        self.writer.close()

