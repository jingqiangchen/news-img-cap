import common
import os, re
import argparse

def train(mode="TI-PG", coverage="False", cov_type=0, batch_size=10, gpu=1, corpus="dailymail"):
    
    if gpu is None:
        gpu=1
        
    exp_name = mode
    pointer_image="True"
    use_image="True"
    article="article"
    max_enc_steps=400
    
    if coverage == "True":
        exp_name=exp_name+"-COV"
        if cov_type>0:
            exp_name=exp_name+str(cov_type)
    
    if mode=="TI-PG":
        coverage = "False"
        pointer_gen = "True"
    elif mode=="TI-PG2":
        coverage = "False"
        pointer_gen = "True"
        pointer_image="False"
    elif mode=="TI-PGC":
        coverage = "True"
        pointer_gen = "True"
    elif mode=="TI-G":
        coverage = "False"
        pointer_gen = "False"
        
    elif mode=="T-PG":
        coverage = "False"
        pointer_gen = "True"
        pointer_image="False"
        use_image="False"
    elif mode=="T-G":
        coverage = "False"
        pointer_gen = "False"
        pointer_image="False"
        use_image="False"
        
    elif mode=="TI-PG-50A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=50
        article="article_50"
    elif mode=="TI-PG-100A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=100
        article="article_100"
    elif mode=="TI-PG-200A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=200
        article="article_200"
    elif mode=="TI-PG-400A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=400
        article="article_400"
        
    elif mode=="TI-PG-50":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=50
    elif mode=="TI-PG-100":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=100
    elif mode=="TI-PG-200":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=200
 
    if corpus=="dailymail":
      common.path_chunked=common.path_corpus + "/chunked"
      common.path_chunked_train=common.path_chunked+"/train-2"
      common.path_chunked_dev=common.path_chunked+"/dev-2"
      common.path_chunked_test=common.path_chunked+"/test-2"
    elif corpus=="bbc":
      common.path_chunked=common.path_corpus + "/chunked-bbc"
      common.path_chunked_train=common.path_chunked+"/train-2"
      common.path_chunked_dev=common.path_chunked+"/dev-2"
      common.path_chunked_test=common.path_chunked+"/test-2"
    
    data_path=common.path_chunked_train+"/*"
 
    os.system('''
        export CUDA_VISIBLE_DEVICES=%d
            
        python -m run_summarization \
              --data_path="%s" \
              --exp_name=%s \
              --batch_size=%d \
              --use_image=%s \
              --pointer_gen=%s \
              --pointer_image=%s \
              --coverage=%s \
              --article=%s \
              --max_enc_steps=%d \
              --coverage=%s \
              --cov_type=%d \
              --corpus=%s 
    ''' % (gpu, data_path, exp_name, batch_size, use_image, pointer_gen, pointer_image, coverage, article, max_enc_steps, coverage, cov_type, corpus))
    

def beam_search(mode="TI-PG", coverage="False", cov_type=0, beam_size=4, gpu=1, is_batch=False, corpus="dailymail"):
    
    if gpu is None:
        gpu=1
        
    exp_name = mode
    pointer_image="True"
    use_image="True"
    article="article"
    max_enc_steps=400
    
    if coverage == "True":
        exp_name=exp_name+"-COV"
        if cov_type>0:
            exp_name=exp_name+str(cov_type)
    
    if mode=="TI-PG":
        coverage = "False"
        pointer_gen = "True"
    elif mode=="TI-PG2":
        coverage = "False"
        pointer_gen = "True"
        pointer_image="False"
    elif mode=="TI-PGC":
        coverage = "True"
        pointer_gen = "True"
    elif mode=="TI-G":
        coverage = "False"
        pointer_gen = "False"
        pointer_image="False"
        
    elif mode=="T-PG":
        coverage = "False"
        pointer_gen = "True"
        pointer_image="False"
        use_image="False"
    elif mode=="T-G":
        coverage = "False"
        pointer_gen = "False"
        pointer_image="False"
        use_image="False"
        
    elif mode=="TI-PG-50A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=50
        article="article_50"
    elif mode=="TI-PG-100A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=100
        article="article_100"
    elif mode=="TI-PG-200A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=200
        article="article_200"
    elif mode=="TI-PG-400A":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=400
        article="article_400"
        
    elif mode=="TI-PG-50":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=50
    elif mode=="TI-PG-100":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=100
    elif mode=="TI-PG-200":
        coverage = "False"
        pointer_gen = "True"
        max_enc_steps=200
        
    if corpus=="dailymail":
      common.path_chunked=common.path_corpus + "/chunked"
      common.path_chunked_train=common.path_chunked+"/train-2"
      common.path_chunked_dev=common.path_chunked+"/dev-2"
      common.path_chunked_test=common.path_chunked+"/test-2"
    elif corpus=="bbc":
      common.path_chunked=common.path_corpus + "/chunked-bbc"
      common.path_chunked_train=common.path_chunked+"/train-2"
      common.path_chunked_dev=common.path_chunked+"/dev-2"
      common.path_chunked_test=common.path_chunked+"/test-2"
    elif corpus=="example":
      common.path_chunked=common.path_corpus + "/chunked"
      common.path_chunked_train=common.path_chunked+"/example-1"
      common.path_chunked_dev=common.path_chunked+"/example-1"
      common.path_chunked_test=common.path_chunked+"/example-1"
    
    data_path=common.path_chunked_test+"/*"
    
    path_ckpt = common.path_log_root + "/" + exp_name + "/train/checkpoint"
    
    if is_batch:
        os.system("cp '%s' '%s'" % (path_ckpt, path_ckpt+"-bak"))
    
    min_ckpt=100000
    max_ckpt=400000
    cur_ckpt=100000
    new_first_line=""
    sign=True
    while True and sign: 
        sign=False
        if is_batch and cur_ckpt>=min_ckpt and cur_ckpt<=max_ckpt :
            with open(path_ckpt) as file:
                lines=file.readlines()
                lines=lines[1:]
                
                for line in lines:
                    line=line.strip("\n").strip("\"")
                    items=line.split("-")
                    if int(items[-1])>=cur_ckpt:
                        cur_ckpt=int(items[-1])+1
                        new_first_line="model_checkpoint_path:"+line.split(":")[-1]+"\""
                        sign=True
                        print(line)
                        break
            
            if sign:
                with open(path_ckpt, "w") as file:
                    file.write(new_first_line+"\n")
                    for line in lines:
                        line=line.strip("\n")
                        file.write(line+"\n")
        
        os.system('''
                export CUDA_VISIBLE_DEVICES=%d
                
                python -m run_summarization \
                      --mode=decode \
                      --single_pass=True \
                      --data_path="%s" \
                      --exp_name=%s \
                      --use_image=%s \
                      --pointer_gen=%s \
                      --pointer_image=%s \
                      --beam_size=%d \
                      --coverage=%s \
                      --article="%s" \
                      --max_enc_steps=%d \
                      --coverage=%s \
                      --cov_type=%d \
                      --corpus=%s 
            ''' % (gpu, data_path, exp_name, use_image, pointer_gen, pointer_image, beam_size, coverage, article, max_enc_steps, coverage, cov_type, corpus))
        
        if not is_batch:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='img-cap args')
    parser.add_argument('--action', choices=['train', 'beam-search', 'beam-search-batch'], default='train')
    parser.add_argument('--mode', choices=['TI-PG', 'TI-G', 'TI-PG2', 'T-PG', 'T-G', 'T-PGC', 
                                           'TI-PG-50A', 'TI-PG-100A', 'TI-PG-200A', 'TI-PG-400A',
                                           'TI-PG-50', 'TI-PG-100', 'TI-PG-200'], default="TI-PG")
    parser.add_argument('--batch_size', type=int, default=10)
    parser.add_argument('--beam_size', type=int, default=4)
    parser.add_argument('--gpu', type=int, default=1)
    parser.add_argument('--coverage', choices=['True', 'False'], default='False')
    parser.add_argument('--cov_type', type=int, default=0)
    parser.add_argument('--corpus', choices=['dailymail', 'bbc', 'example'], default='dailymail')
    
    
    args = parser.parse_args()
    if args.action == 'train':
        while True:
            train(mode=args.mode, cov_type=args.cov_type, coverage=args.coverage, batch_size=args.batch_size, gpu=args.gpu, corpus=args.corpus)
    elif args.action == 'beam-search':
        beam_search(mode=args.mode, cov_type=args.cov_type, coverage=args.coverage, beam_size=args.beam_size, gpu=args.gpu, corpus=args.corpus)
    elif args.action == 'beam-search-batch':
        beam_search(mode=args.mode, cov_type=args.cov_type, coverage=args.coverage, beam_size=args.beam_size, gpu=args.gpu, is_batch=True, corpus=args.corpus)





