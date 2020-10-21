import os
import allfname as fn

def main():
    filename = fn.allfname()

    for i in filename:
        os.system('python -m gensim.scripts.word2vec2tensor --input '+i+'.vec --output '+i)

if __name__ == "__main__":
    main()
    print('완료')
