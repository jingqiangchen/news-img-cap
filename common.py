
import hashlib

path_base="/home/test/img-cap"

path_lib = path_base + "/libs"
path_meteor= path_lib + "/meteor-master/meteor-1.5.jar"

path_corpus=path_base + "/dailymail"
path_story_texts=path_corpus + "/story-texts-1-flat"
path_captions=path_corpus + "/captions"
path_image_features_split=path_corpus + "/image-features-split"

path_vocab = path_corpus + "/vocab-tkde"
path_embedding = path_corpus + "/vocab_embedding_tkde"

path_train_file=path_corpus + "/trains"
path_dev_file=path_corpus + "/devs"
path_test_file=path_corpus + "/tests-bbc"
path_example_file=path_corpus + "/example1-test"

path_chunked=path_corpus + "/chunked"
path_chunked_train=path_chunked+"/train-2"
path_chunked_dev=path_chunked+"/dev-2"
path_chunked_test=path_chunked+"/test-2"
path_chunked_example1=path_chunked+"/example1"

path_log_root = path_corpus + "/abs-models-pg"

model_base = "abs-models-pg"

def Hashhex(s):
    h = hashlib.sha1()
    h.update(s)
    return h.hexdigest()