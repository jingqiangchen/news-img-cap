import sys
import os
import hashlib
import struct
import subprocess
import collections
import numpy as np
import tensorflow as tf
from tensorflow.core.example import example_pb2

import common

dm_single_close_quote = u'\u2019' # unicode
dm_double_close_quote = u'\u201d'
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote, ")"] # acceptable ways to end a sentence

# We use these to separate the summary sentences in the .bin datafiles
SENTENCE_START = '<s>'
SENTENCE_END = '</s>'

path_train_file = common.path_train_file
path_dev_file = common.path_dev_file 
path_test_file = common.path_test_file
path_example1_file=common.path_example_file

path_chunks = common.path_chunked+""

path_story_texts=common.path_story_texts
path_story_texts_50=path_story_texts
path_story_texts_100=path_story_texts
path_story_texts_200=path_story_texts
path_story_texts_400=path_story_texts
path_captions=common.path_captions
path_image_features_split=common.path_image_features_split

VOCAB_SIZE = 40004
CHUNK_SIZE = 1000 # num examples per chunk, for the chunked data


def copy_files():
    with open(common.path_test_file) as file:
        for line in file.readlines():
            line=line.strip("\n")
            os.system("cp '%s' '%s'" % ("/home/test/img-cap/dailymail/story-texts-0/"+line, path_story_texts+"/"+line))


def chunk_file(set_name):
  in_file = path_chunks + '/%s.bin' % set_name
  reader = open(in_file, "rb")
  chunk = 0
  finished = False
  if not os.path.isdir(path_chunks+"/"+set_name):
    os.mkdir(path_chunks+"/"+set_name)
  
  while not finished:
    chunk_fname = os.path.join(path_chunks+"/"+set_name, '%s_%03d.bin' % (set_name, chunk)) # new chunk
    with open(chunk_fname, 'wb') as writer:
      for _ in range(CHUNK_SIZE):
        len_bytes = reader.read(8)
        if not len_bytes:
          finished = True
          break
        str_len = struct.unpack('q', len_bytes)[0]
        example_str = struct.unpack('%ds' % str_len, reader.read(str_len))[0]
        writer.write(struct.pack('q', str_len))
        writer.write(struct.pack('%ds' % str_len, example_str))
      chunk += 1


def chunk_all():
  # Make a dir to hold the chunks
  if not os.path.isdir(path_chunks):
    os.mkdir(path_chunks)
  # Chunk the data
  #for set_name in ['train-2', 'dev-2', 'test-2']:
  for set_name in ['example-1']:
    print ("Splitting %s data into chunks..." % set_name)
    chunk_file(set_name)
  print ("Saved chunked data in %s" % path_chunks)


def read_text_file(text_file):
  lines = []
  with open(text_file, "r") as f:
    for line in f:
      lines.append(line.strip())
  return lines


def hashhex(s):
  """Returns a heximal formated SHA1 hash of the input string."""
  h = hashlib.sha1()
  h.update(s)
  return h.hexdigest()


def get_url_hashes(url_list):
  return [hashhex(url) for url in url_list]


def write_to_bin(path_in_file, path_out_file, makevocab=False):
  """Reads the tokenized .story files corresponding to the urls listed in the url_file and writes them to a out_file."""
  print ("Making bin file for URLs listed in %s..." % path_in_file)
  file_list = read_text_file(path_in_file)
  num_stories = len(file_list)

  with open(path_out_file, 'wb') as writer:
    for idx,s in enumerate(file_list):
      if idx % 1000 == 0:
        print ("Writing story %i of %i; %.2f percent done" % (idx, num_stories, float(idx)*100.0/float(num_stories)))

      # Look in the tokenized story dirs to find the .story file corresponding to this url
      elif os.path.isfile(os.path.join(path_story_texts, s)):
        story_file = os.path.join(path_story_texts, s)
      else:
        print ("Error: Couldn't find tokenized story file %s in either tokenized story directories %s and %s. Was there an error during tokenization?" % (s, path_story_texts))
        # Check again if tokenized stories directories contain correct number of files

      # Get the strings to write to .bin file
      with open(path_story_texts + "/" + s) as file: 
          article = file.read()
      with open(path_captions + "/" + s) as file: 
          caption = file.read()
      image_features = np.fromfile(path_image_features_split + "/" + s.split("-")[0] + "/" + s, np.float32)
      with open(path_story_texts_50 + "/" + s) as file: 
          article_50 = file.read()
      with open(path_story_texts_100 + "/" + s) as file: 
          article_100 = file.read()
      with open(path_story_texts_200 + "/" + s) as file: 
          article_200 = file.read()
      with open(path_story_texts_400 + "/" + s) as file: 
          article_400 = file.read()

      # Write to tf.Example
      tf_example = example_pb2.Example()
      tf_example.features.feature['article'].bytes_list.value.extend([article.encode('utf-8')])
      tf_example.features.feature['caption'].bytes_list.value.extend([caption.encode('utf-8')])
      tf_example.features.feature['image-features'].bytes_list.value.extend([image_features.tobytes()])
      tf_example.features.feature['article_50'].bytes_list.value.extend([article_50.encode('utf-8')])
      tf_example.features.feature['article_100'].bytes_list.value.extend([article_100.encode('utf-8')])
      tf_example.features.feature['article_200'].bytes_list.value.extend([article_200.encode('utf-8')])
      tf_example.features.feature['article_400'].bytes_list.value.extend([article_400.encode('utf-8')])
      tf_example_str = tf_example.SerializeToString()
      str_len = len(tf_example_str)
      writer.write(struct.pack('q', str_len))
      writer.write(struct.pack('%ds' % str_len, tf_example_str))

  print ("Finished writing file %s\n" % path_out_file)


def create_test_vocab():
    with open(common.path_vocab, "w") as file:
        for i in range(40000):
            file.write("word%d\t1\n"%i)

if __name__ == '__main__':
  #copy_files()

  #write_to_bin(path_train_file, os.path.join(path_chunks, "train-2.bin"))
  #write_to_bin(path_dev_file, os.path.join(path_chunks, "dev-2.bin"))
  #write_to_bin(path_test_file, os.path.join(path_chunks, "test-2.bin"))
  
  #write_to_bin(path_example1_file, os.path.join(path_chunks, "example-1.bin"))

  chunk_all()
































