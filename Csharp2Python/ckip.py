import ckip_classic.client



class ckip_parser():
    def __init__(self):
        self.model = ckip_classic.client.CkipParserClient(username='danchang11', password='to26292661')
        self.model_v = ckip_classic.__version__

    def parse(self,sentence:str):
        ann = self.model(sentence)
        return ann



