from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from tqdm import tqdm
import allfname as fn

class callback(CallbackAny2Vec):
    """Callback to print loss after each epoch."""

    def __init__(self):
        self.epoch = 0
        self.loss_to_be_subed = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        loss_now = loss - self.loss_to_be_subed
        self.loss_to_be_subed = loss
        print('Loss after epoch {}: {}'.format(self.epoch, loss_now))
        self.epoch += 1

def main():
    filename = fn.allfname()

    for i in filename:
        print('model 생성')
        corpus = [sent.strip().split(" ") for sent in tqdm(open(i+".txt", 'r', encoding='utf-8').readlines())]

        print("학습 중")
        # model = Word2Vec(corpus, size=100, workers=4, sg=1, compute_loss=True, iter=1, callbacks=[callback()])
        model = Word2Vec(corpus, size=20, min_count=1)
        model.wv.save_word2vec_format(i+".vec")

if __name__ == "__main__":
    main()
    print('완료')
