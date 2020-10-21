from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pandas as pd
from gensim.models import KeyedVectors
import allfname as fn
import plotly
import plotly.graph_objects as go

# 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처
# font_location = "c:/Windows/fonts/malgun.ttf"
# font_name = font_manager.FontProperties(fname=font_location).get_name()
# matplotlib.rc('font', family=font_name)

font_location = "c:/Windows/fonts/HMFMMUEX.TTC"
font_name = font_manager.FontProperties(fname=font_location).get_name()
font = {'family' : font_name,
        'weight' : 'bold',
        'size'   : 15}
# matplotlib.rc('font', **font)


mpl.rcParams['axes.unicode_minus'] = False
# plt.rc('font', family=font_name)
plt.rc('font', **font)

def html(filename, vocabs, xs, ys):
    text=[]
    for i,v in enumerate(vocabs):
        text.append(v)

    fig = go.Figure(data=go.Scatter(x=xs,
                                    y=ys,
                                    mode='markers+text',
                                    text=text))

    fig.update_layout(title=filename, font=dict(family=font_name, size=18))
    # fig.show()

    plotly.offline.plot(
    fig, filename=filename+"_pca"+'.html'
    )


def show_tsne(filename,  X_show, vocab_show):
    tsne = TSNE(n_components=2)
    X = tsne.fit_transform(X_show)
    df = pd.DataFrame(X, index=vocab_show, columns=['x', 'y'])
    fig = plt.figure()
    fig.set_size_inches(30, 20)
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])

    for word, pos in df.iterrows():
        ax.annotate(word, pos, fontsize=18)

    plt.xlabel("t-SNE 특성 0")
    plt.ylabel("t-SNE 특성 1")
    plt.savefig(filename+"_tsne"+'.png', dpi=300)
    # plt.show()

def show_pca(filename,  X_show, vocab_show):
    # PCA 모델을 생성합니다
    pca = PCA(n_components=2)
    pca.fit(X_show)
    # 처음 두 개의 주성분으로 숫자 데이터를 변환합니다
    x_pca = pca.transform(X_show)
    plt.figure(figsize=(30, 20))
    plt.xlim(x_pca[:, 0].min(), x_pca[:, 0].max())
    plt.ylim(x_pca[:, 1].min(), x_pca[:, 1].max())

    for i in range(len(X_show)):
        plt.text(x_pca[i, 0], x_pca[i, 1], str(vocab_show[i]), fontdict={'weight': 'bold', 'size': 18})

    plt.xlabel("첫 번째 주성분")
    plt.ylabel("두 번째 주성분")
    plt.savefig(filename+"_pca"+'.png', dpi=300)
    # plt.show()


def main():
    filename = fn.allfname()
    # filename = ['군산청년몰']

    for i in filename:
        model_name = i +'.vec'  # 'word2vec'
        model = KeyedVectors.load_word2vec_format(model_name)
        vocab = list(model.wv.vocab)

        X = model[vocab]
        # sz개의 단어에 대해서만 시각화
        sz = 20
        X_show = X[:sz,:]
        vocab_show = vocab[:sz]

        html(i, vocab, X_show, vocab_show)

        show_tsne(i, X_show, vocab_show)
        show_pca(i,  X_show, vocab_show)

if __name__ == "__main__":
    main()
    print('완료')
