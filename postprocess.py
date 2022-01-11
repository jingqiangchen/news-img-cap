import common
import os, re
import argparse
import numpy as np
from meteor import Meteor 
meteor = Meteor()

path_results=common.path_corpus+"/results-pg"

models=["T-G", "TI-G", "TI-G-COV", "TI-G-COV3", "TI-PG", "TI-PG2", "TI-PG2-COV", 
        "TI-PG-COV", "TI-PG-COV3", "T-PG", "T-PG-COV", 
        "TI-PG-50", "TI-PG-50A", "TI-PG-100", "TI-PG-100A", "TI-PG-200", "TI-PG-200A", "TI-PG-400A"]
#models=["T-G", "TI-G", "TI-G-COV", "TI-G-COV3", "TI-PG", "TI-PG2", "TI-PG2-COV", 
#        "TI-PG-COV", "TI-PG-COV3", "T-PG", "T-PG-COV"]
#models=["TI-PG-50", "TI-PG-50A", "TI-PG-100", "TI-PG-100A", "TI-PG-200", "TI-PG-200A", "TI-PG-400A"]
models=["TI-PG", "TI-PG-COV", "TI-PG-COV3", "TI-PG2", "TI-PG2-COV"]

def re_calc(corpus="dailymail", model_base=common.model_base): 
    def re_calc_one(io_dir):
        files=os.listdir(io_dir)
        files=sorted(files)
        files=files[::-1]
        sign=0
        for file_name in files:
            if len(file_name) >6 :
                continue 
            if sign==0: 
                sign+=1
                continue
            
            r_file=open(io_dir+"/"+file_name)
            w_file=open(io_dir+"/"+file_name+"-meteor","w")
            sign=""
            num=0
            total_meteor_score_unk=0.
            total_meteor_score_rep=0.
            for line in r_file.readlines():
                line=line.strip("\n")
                ma=re.match("^\[?(\d+)\]?$",line)
                w_file.write(line+"\n")
                if ma:
                    record_no=ma.group(0)
                    sign=""
                    target_summary=""
                    unk_summary=""
                    rep_summary=""
                    num+=1
                    print("["+record_no+"]")
                elif line=="------------------unk---summary----------------":
                    sign="unk-summary"
                elif line=="------------------rep---summary----------------":
                    sign="rep-summary"
                elif line=="------------------target---summary----------------":
                    sign="target-summary"
                elif line=="-------------------full---unk---------------":
                    sign=""
                    meteor_score = meteor._score(unk_summary, [target_summary]) * 100 
                    total_meteor_score_unk += meteor_score
                    w_file.write("%.2f\n" % (meteor_score))
                    w_file.write("%.2f\n" % (total_meteor_score_unk/num))
                elif line=="-------------------full---rep---------------":
                    sign=""
                    meteor_score = meteor._score(rep_summary, [target_summary]) * 100
                    total_meteor_score_rep += meteor_score
                    w_file.write("%.2f\n" % (meteor_score))
                    w_file.write("%.2f\n" % (total_meteor_score_rep/num))
                else:
                    if sign=="unk-summary":
                        unk_summary=line
                    elif sign=="rep-summary":
                        rep_summary=line
                    elif sign=="target-summary":
                        target_summary=line
            r_file.close()
            w_file.close()
    
    for model in models:
        io_dir=common.path_corpus+"/"+model_base+"/"+model+"/decode-"+corpus

        re_calc_one(io_dir)
    

def accumulate(corpus="dailymail", model_base=common.model_base):
    
    def accumulate_one(dir_name):
        file_names=os.listdir(common.path_corpus+"/"+model_base+"/"+dir_name+"/decode-"+corpus)
        file_names=sorted(file_names)
        file_names=file_names[::-1]
        
        out_dir=path_results+"/accumulate/" + corpus
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        w_file=open(out_dir+"/"+dir_name, "w")
        sign=0
        for file_name in file_names:
            if not file_name.endswith("-meteor"):
                continue
            if sign==0:
                sign+=1
                continue
            
            result1=""
            result2=""
            r_file=open(common.path_corpus + "/" + model_base + "/" + dir_name + "/decode-" + corpus + "/" + file_name)
            lines=r_file.readlines()
            lines=lines[::-1]
            print(dir_name+"/"+file_name)
            sign="correct"
            index=0
            for i in range(len(lines)):
                line=lines[i].strip("\n")
                if line=="ERROR!":
                    sign="error"
                    continue
                if re.match("^\[(\d+)\]$",line):
                    sign="correct"
                    index=0
                    continue
                if sign=="error":
                    continue
                
                if index==1:
                    items=line.split("\t")
                    result1=("%.2f %.2f %.2f" % (float(items[0])*100, float(items[1])*100, float(items[2])*100))
                elif index==3:
                    items=line.split("\t")
                    result1=("%.2f %.2f %.2f" % (float(items[0])*100, float(items[1])*100, float(items[2])*100))+"|"+result1
                elif index==5:
                    items=line.split("\t")
                    result1=("%.2f %.2f %.2f" % (float(items[0])*100, float(items[1])*100, float(items[2])*100))+"|"+result1
                elif index==7:
                    items=line.split("\t")
                    result1=items[0]+" "+items[1]+" "+items[2]+" "+items[3]+" "+items[4]+"|"+result1
                elif index==9:
                    result1=line+" | "+result1
                elif index==12:
                    items=line.split("\t")
                    result2=("%.2f %.2f %.2f" % (float(items[0])*100, float(items[1])*100, float(items[2])*100))
                elif index==14:
                    items=line.split("\t")
                    result2=("%.2f %.2f %.2f" % (float(items[0])*100, float(items[1])*100, float(items[2])*100))+"|"+result2
                elif index==16:
                    items=line.split("\t")
                    result2=("%.2f %.2f %.2f" % (float(items[0])*100, float(items[1])*100, float(items[2])*100))+"|"+result2
                elif index==18:
                    items=line.split("\t")
                    result2=items[0]+" "+items[1]+" "+items[2]+" "+items[3]+" "+items[4]+"|"+result2
                elif index==20:
                    result2=line+" | "+result2
                    break
                index+=1
            r_file.close()
            w_file.write(file_name.split(".")[0].split("-")[0]+": ")
            w_file.write(result1+" ||| "+result2+"\n")
        w_file.close()
        
    def accumulate_two():
        file_names=os.listdir(path_results+"/accumulate/" + corpus)
        file_names.sort()
        w_file_bleu=open(path_results+"/"+corpus+"-bleu.txt", "w")
        w_file_meteor=open(path_results+"/"+corpus+"-meteor.txt", "w")
        w_file_rouge_l=open(path_results+"/"+corpus+"-rouge-l.txt", "w")
        for file_name in file_names:
            r_file=open(path_results+"/accumulate/"+corpus+"/"+file_name)
            lines=r_file.readlines()
            max_i_bleu=0
            max_i_meteor=0
            max_i_rouge_l=0
            max_bleu=-1
            max_meteor=-1
            max_rouge_l=-1
            for i in range(len(lines)):
                line=lines[i].strip("\n")
                print(file_name+":"+line)
                value_bleu=float(line.split("|||")[0].split("|")[1].strip(" ").split(" ")[0])
                value_meteor=float(line.split("|||")[0].split("|")[0].strip(" ").split(":")[1].strip(" "))
                value_rouge_l=float(line.split("|||")[0].split("|")[-1].strip(" ").split(" ")[-1])
                if value_bleu>max_bleu:
                    max_bleu=value_bleu
                    max_i_bleu=i
                if value_meteor>max_meteor:
                    max_meteor=value_meteor
                    max_i_meteor=i
                if value_rouge_l>max_rouge_l:
                    max_rouge_l=value_rouge_l
                    max_i_rouge_l=i
            w_file_bleu.write(file_name+"-"+lines[max_i_bleu])
            w_file_meteor.write(file_name+"-"+lines[max_i_meteor])
            w_file_rouge_l.write(file_name+"-"+lines[max_i_rouge_l])
            r_file.close()
        w_file_bleu.close()
        w_file_meteor.close()
        w_file_rouge_l.close()
    
    
    for file_dir in models:
        accumulate_one(file_dir)
    
    accumulate_two()


def bbc(gpu=1):
    os.system(''' python main.py --mode T-G --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-G --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-G --action beam-search-batch --gpu %d --coverage True --cov_type 0 --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-G --action beam-search-batch --gpu %d --coverage True --cov_type 3 --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG2 --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG2 --action beam-search-batch --gpu %d --coverage True --cov_type 0 --corpus bbc''' % gpu)
    
    os.system(''' python main.py --mode TI-PG-50 --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG-50A --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG-100 --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG-100A --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG-200 --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG-200A --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG-400A --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    
    os.system(''' python main.py --mode TI-PG --action beam-search-batch --gpu %d --coverage True --cov_type 0 --corpus bbc''' % gpu)
    os.system(''' python main.py --mode TI-PG --action beam-search-batch --gpu %d --coverage True --cov_type 3 --corpus bbc''' % gpu)
    os.system(''' python main.py --mode T-PG --action beam-search-batch --gpu %d --corpus bbc''' % gpu)
    os.system(''' python main.py --mode T-PG --action beam-search-batch --gpu %d --coverage True --cov_type 0 --corpus bbc''' % gpu)


def statistic():
    meta_file_names=[common.path_train_file, common.path_dev_file, common.path_test_file]
    text_len=0.
    cap_len=0.
    text_count=0.
    for meta_file_name in meta_file_names:
        meta_file=open(meta_file_name)
        
        for file_name in meta_file.readlines():
            file=open(common.path_story_texts+"/"+file_name.strip("\n").split("-")[0])
            text_len+=len(file.read().replace("\n", " ").split(" "))
            file.close()
            
            file=open(common.path_captions+"/"+file_name.strip("\n"))
            cap_len+=len(file.read().replace("\n", "").split(" "))
            file.close()
            
            text_count+=1
            
        meta_file.close()
    print(text_len/text_count)
    print(cap_len/text_count)
    print("dailymail:text_len: %f" % (text_len/text_count)) 
    print("dailymail:cap_len: %f" % (cap_len/text_count))
    
    text_len=0.
    cap_len=0.
    text_count=0.
    meta_file=open(common.path_test_file)
    for file_name in meta_file.readlines():
        file=open(common.path_story_texts+"/"+file_name.strip("\n"))
        text_len+=len(file.read().replace("\n", " ").split(" "))
        file.close()
            
        file=open(common.path_captions+"/"+file_name.strip("\n"))
        cap_len+=len(file.read().replace("\n", "").split(" "))
        file.close()
        text_count+=1
        
    meta_file.close()
    print(text_len/text_count)
    print(cap_len/text_count)
    print("bbc:text_len: %f" % (text_len/text_count))
    print("bbc:cap_len: %f" % (cap_len/text_count))
    

def visualparts2words(corpus):
    if corpus=="dailymail":
        test_file=open(common.path_corpus+"/tests")
    else:
        test_file=open(common.path_corpus+"/tests-bbc")
    txt_file_names=[line.strip("\n") for line in test_file.readlines()]
    test_file.close()
    
    def done(score_file_path, source_file_dir):
        
        r_file=open(score_file_path)
        print(score_file_path)
        w_file=open(score_file_path+"-out","w")
        print(score_file_path+"-out")
        while True:
            line= r_file.readline()
            if line=="":
                break
            line=line.strip("\n")
            ma=re.match("^\[(\d+)\]$",line)
            if ma:
                w_file.write(line+"\n")
                record_no=ma.group(1)
                row_index=-1
                arrays=[]
                
                txt_file=open(source_file_dir+"/"+txt_file_names[int(record_no)-1])
                txt=txt_file.read()
                txt=txt.strip("\n")
                txt=txt.split(" ")
                txt_file.close()
            elif row_index==-1:
                items=line.split(" ")
                row=int(items[0])
                col=int(items[1])
                row_index=0
            else:
                items=line.split(" ")
                array=[float(item) for item in items]
                arrays.append(array)
                row_index+=1
                if row_index==row:
                    arrays=np.array(arrays)
                    max_values=arrays.max(axis=0)
                    indices = np.where(arrays==max_values)
                    #print(arrays)
                    #print(max_values)
                    #print(indices)
                    ts = zip(indices[0], indices[1])
                    ts = sorted(ts, key=lambda ts: ts[1])
                    for row_index, col_index in ts:
                        if col_index>0 and col_index % 14 == 0:
                            w_file.write("\n")
                        w_file.write(str(row_index)+" ")
                    w_file.write("\n")
                        
                    for row_index, col_index in ts:
                        if col_index>0 and col_index % 14 == 0:
                            w_file.write("\n")
                        w_file.write(txt[row_index]+" ")
                    w_file.write("\n")
                    
        r_file.close()
        w_file.close()
        
    for model in models:
        if model in ["T-G", "TI-G", "TI-G-COV", "TI-G-COV3", "TI-PG", "TI-PG2", "TI-PG2-COV", "TI-PG-COV", "TI-PG-COV3", "T-PG", "T-PG-COV"]:
            source_file_dir=common.path_corpus+"/story-texts-1-flat"
        elif model in ["TI-PG-400A"]:
            source_file_dir=common.path_corpus+"/story-texts-400-flat"
        elif model in ["TI-PG-200A"]:
            source_file_dir=common.path_corpus+"/story-texts-200-flat"
        elif model in ["TI-PG-100A"]:
            source_file_dir=common.path_corpus+"/story-texts-100-flat"
        elif model in ["TI-PG-50A"]:
            source_file_dir=common.path_corpus+"/story-texts-50-flat"
        
        decode_dir=common.path_log_root+"/"+model+"/decode-"+corpus
        file_names=os.listdir(decode_dir)
        file_names=sorted(file_names)[::-1]
        sign=0
        for file_name in file_names:
            if file_name.endswith("-txt-img"):
                if sign>0:
                    done(decode_dir+"/"+file_name, source_file_dir)
                sign+=1


def evaluate_visualparts2words(corpus):
    if corpus=="dailymail":
        test_file=open(common.path_corpus+"/tests")
    else:
        test_file=open(common.path_corpus+"/tests-bbc")
    txt_file_names=[line.strip("\n") for line in test_file.readlines()]
    test_file.close()
    
    def done1(score_file_path, caption_file_dir, result_file):
        
        r_file=open(score_file_path)
        print(score_file_path)
        w_file=open(score_file_path+"-2","w")
        print(score_file_path+"-out")
        result_file=open(result_file,"w")
        
        total=0
        total_count=0
        count=0
        
        for line in r_file.readlines():
            #line= r_file.readline()
            line=line.strip("\n")
            ma=re.match("^\[(\d+)\]$",line)
            if ma:
                w_file.write(line+"\n")
                record_no=ma.group(1)
                row_index=-1
                arrays=[]
                
                txt_file=open(caption_file_dir+"/"+txt_file_names[int(record_no)-1])
                txt=txt_file.read()
                txt=txt.strip("\n")
                txt=txt.split(" ")
                txt_file.close()
                
                w_file.write(record_no)
                
                captions=set(txt)
                vwords=set([])
                
                row_index=0
                count+=1
            else:
                row_index+=1
                if row_index>14:
                    items=line.split(" ")
                    vwords.update(set(items))
                    #print(arrays)
                    #print(max_values)
                    #print(indices)
                    if row_index==28:
                        common_words=vwords-(vwords-captions)
                        prec=float(len(common_words))/len(captions)
                        total+=prec
                        total_count+=len(vwords)
                        w_file.write(" ".join([str(item) for item in common_words]))
                        w_file.write("\n")
                        w_file.write("%.4f\n" % (prec))
                        w_file.write("%.4f\n" % (1.0*total_count/count))
                        w_file.write("%.4f\n" % (total/count))
                    
        r_file.close()
        w_file.close()
        
    for model in models:
        caption_file_dir=common.path_captions
        
        decode_dir=common.path_log_root+"/"+model+"/decode-"+corpus
        result_dir=common.path_corpus+"/results-pg/img-txt-rela"
        file_names=os.listdir(decode_dir)
        file_names=sorted(file_names)[::-1]
        sign=0
        for file_name in file_names:
            if file_name.endswith("-txt-img-out"):
                if sign>0:
                    done1(decode_dir+"/"+file_name, caption_file_dir, result_dir+"/"+file_name)
                sign+=1


def attentions(corpus):
    models=["TI-G", "TI-G-COV", "TI-G-COV3", "TI-PG", "TI-PG2", "TI-PG2-COV", 
        "TI-PG-COV", "TI-PG-COV3"]
    
    if corpus=="dailymail":
        test_file=open(common.path_corpus+"/tests")
    else:
        test_file=open(common.path_corpus+"/tests-bbc")
    txt_file_names=[line.strip("\n") for line in test_file.readlines()]
    test_file.close()
    
    def done(score_file_path, source_file_dir):
        all_text_att=0.
        all_img_att=0.
        
        r_file=open(score_file_path)
        print(score_file_path)
        w_file=open(score_file_path+"-out","w")
        print(score_file_path+"-out")
        record_no=0
        line_no=0
        print(score_file_path)
        while True:
            line= r_file.readline()
            if line=="":
                break
            line_no+=1
            line=line.strip("\n")
            items=line.split(" ")
            if len(items)==2:
                record_no+=1
                w_file.write("[%d]\n" % record_no)
                w_file.write(line+"\n")
                
                row=int(items[0])
                col=int(items[1])
                row_index=0
                arrays=[]
                
                txt_file=open(source_file_dir+"/"+txt_file_names[int(record_no)-1])
                print(record_no, row, col)
                txt=txt_file.read()
                txt=txt.strip("\n")
                txt=txt.split(" ")
                txt_file.close()
            else:
                if len(items)!=col:
                    print(line_no)
                    print(len(items))
                    print(line)
                    print(items)
                array=[float(item) for item in items]
                arrays.append(array)
                row_index+=1
                del array
                    
                if row_index==row:
                    arrays=np.array(arrays)
                    #if record_no=="5069":
                        
                    #print(np.shape(arrays))
                    img_att_arrays=arrays[:, :196]
                    text_att_arrays=arrays[:, 196:]
                    
                    #print(text_att_arrays)
                    max_text_atts=text_att_arrays.max(axis=1)
                    text_indices = np.where(np.transpose(text_att_arrays, [1, 0])==max_text_atts)
                    #print(max_text_atts)
                    #print(text_indices)
                    #print(arrays)
                    #print(max_values)
                    #print(indices)
                        
                    sum_text_att=text_att_arrays.sum()
                    sum_img_att=img_att_arrays.sum()
                    att=sum_img_att+sum_text_att
                    sum_text_att=sum_text_att/att
                    sum_img_att=sum_img_att/att
                        
                    w_file.write("%.6f %.6f\n" % (sum_img_att, sum_text_att))
                        
                    all_text_att+=sum_text_att
                    all_img_att+=sum_img_att
                    att=all_text_att+all_img_att
                    w_file.write("%.6f %.6f\n" % (all_img_att/att, all_text_att/att))
                        
                    text_ts=zip(text_indices[1], text_indices[0])
                    text_ts = sorted(text_ts, key=lambda text_ts: text_ts[0])
                    for row_index, col_index in text_ts:
                        w_file.write(str(col_index)+" ")
                    w_file.write("\n")
                            
                    for row_index, col_index in text_ts:
                        w_file.write(txt[col_index]+" ")
                    w_file.write("\n")
                        
                    del arrays
            
        r_file.close()
        w_file.close()
        
    for model in models:
        if model in ["T-G", "TI-G", "TI-G-COV", "TI-G-COV3", "TI-PG", "TI-PG2", "TI-PG2-COV", "TI-PG-COV", "TI-PG-COV3", "T-PG", "T-PG-COV"]:
            source_file_dir=common.path_corpus+"/story-texts-1-flat"
        elif model in ["TI-PG-400A"]:
            source_file_dir=common.path_corpus+"/story-texts-400-flat"
        elif model in ["TI-PG-200A"]:
            source_file_dir=common.path_corpus+"/story-texts-200-flat"
        elif model in ["TI-PG-100A"]:
            source_file_dir=common.path_corpus+"/story-texts-100-flat"
        elif model in ["TI-PG-50A"]:
            source_file_dir=common.path_corpus+"/story-texts-50-flat"
        
        decode_dir=common.path_log_root+"/"+model+"/decode-"+corpus
        file_names=os.listdir(decode_dir)
        file_names=sorted(file_names)[::-1]
        sign=0
        for file_name in file_names:
            if file_name.endswith("-attn"):
                if sign>0:
                    done(decode_dir+"/"+file_name, source_file_dir)
                sign+=1


def evaluate_attentions(corpus):
    if corpus=="dailymail":
        test_file=open(common.path_corpus+"/tests")
    else:
        test_file=open(common.path_corpus+"/tests-bbc")
    txt_file_names=[line.strip("\n") for line in test_file.readlines()]
    test_file.close()
    
    def done1(score_file_path, caption_file_dir, result_file):
        
        r_file=open(score_file_path)
        print(score_file_path)
        w_file=open(score_file_path+"-2","w")
        print(score_file_path+"-out")
        result_file=open(result_file,"w")
        
        total=0
        total_count=0
        count=0
        
        for line in r_file.readlines():
            #line= r_file.readline()
            line=line.strip("\n")
            ma=re.match("^\[(\d+)\]$",line)
            if ma:
                w_file.write(line+"\n")
                record_no=ma.group(1)
                row_index=-1
                arrays=[]
                
                txt_file=open(caption_file_dir+"/"+txt_file_names[int(record_no)-1])
                txt=txt_file.read()
                txt=txt.strip("\n")
                txt=txt.split(" ")
                txt_file.close()
                
                w_file.write(record_no)
                
                captions=set(txt)
                vwords=set([])
                
                row_index=0
                count+=1
            else:
                row_index+=1
                if row_index>14:
                    items=line.split(" ")
                    vwords.update(set(items))
                    #print(arrays)
                    #print(max_values)
                    #print(indices)
                    if row_index==28:
                        common_words=vwords-(vwords-captions)
                        prec=float(len(common_words))/len(captions)
                        total+=prec
                        total_count+=len(vwords)
                        w_file.write(" ".join([str(item) for item in common_words]))
                        w_file.write("\n")
                        w_file.write("%.4f\n" % (prec))
                        w_file.write("%.4f\n" % (1.0*total_count/count))
                        w_file.write("%.4f\n" % (total/count))
                    
        r_file.close()
        w_file.close()
        
    for model in models:
        caption_file_dir=common.path_captions
        
        decode_dir=common.path_log_root+"/"+model+"/decode-"+corpus
        result_dir=common.path_corpus+"/results-pg/img-txt-rela"
        file_names=os.listdir(decode_dir)
        file_names=sorted(file_names)[::-1]
        sign=0
        for file_name in file_names:
            if file_name.endswith("-txt-img-out"):
                if sign>0:
                    done1(decode_dir+"/"+file_name, caption_file_dir, result_dir+"/"+file_name)
                sign+=1


def pointer2words(corpus):
    if corpus=="dailymail":
        test_file=open(common.path_corpus+"/tests")
    else:
        test_file=open(common.path_corpus+"/tests-bbc")
    txt_file_names=[line.strip("\n") for line in test_file.readlines()]
    test_file.close()
    
    def done(score_file_path, source_file_dir):
        all_text_att=0.
        all_img_att=0.
        
        r_file=open(score_file_path)
        print(score_file_path)
        w_file=open(score_file_path+"-out","w")
        print(score_file_path+"-out")
        record_no=0
        line_no=0
        print(score_file_path)
        while True:
            line= r_file.readline()
            if line=="":
                break
            line_no+=1
            line=line.strip("\n")
            items=line.split(" ")
            if len(items)==2:
                record_no+=1
                w_file.write("[%d]\n" % record_no)
                w_file.write(line+"\n")
                
                row=int(items[0])
                col=int(items[1])
                row_index=0
                arrays=[]
                
                txt_file=open(source_file_dir+"/"+txt_file_names[int(record_no)-1])
                print(record_no, row, col)
                txt=txt_file.read()
                txt=txt.strip("\n")
                txt=txt.split(" ")
                txt_file.close()
            else:
                if len(items)!=col:
                    print(line_no)
                    print(len(items))
                    print(line)
                    print(items)
                
                array=[float(item) for item in items]
                arrays.append(array)
                row_index+=1
                del array
                    
                if row_index==row:
                    arrays=np.array(arrays)
                    
                    max_atts=arrays.max(axis=1)
                    indices = np.where(np.transpose(arrays, [1, 0])==max_atts)
                        
                    ts=zip(indices[1], indices[0])
                    ts = sorted(ts, key=lambda ts: ts[0])
                    for row_index, col_index in ts:
                        w_file.write(str(col_index)+" ")
                    w_file.write("\n")
                            
                    for row_index, col_index in ts:
                        w_file.write(txt[col_index]+" ")
                    w_file.write("\n")
                        
                    del arrays
            
        r_file.close()
        w_file.close()
        
    for model in models:
        if model in ["T-G", "TI-G", "TI-G-COV", "TI-G-COV3", "TI-PG", "TI-PG2", "TI-PG2-COV", "TI-PG-COV", "TI-PG-COV3", "T-PG", "T-PG-COV"]:
            source_file_dir=common.path_corpus+"/story-texts-1-flat"
        elif model in ["TI-PG-400A"]:
            source_file_dir=common.path_corpus+"/story-texts-400-flat"
        elif model in ["TI-PG-200A"]:
            source_file_dir=common.path_corpus+"/story-texts-200-flat"
        elif model in ["TI-PG-100A"]:
            source_file_dir=common.path_corpus+"/story-texts-100-flat"
        elif model in ["TI-PG-50A"]:
            source_file_dir=common.path_corpus+"/story-texts-50-flat"
        
        decode_dir=common.path_log_root+"/"+model+"/decode-"+corpus
        file_names=os.listdir(decode_dir)
        file_names=sorted(file_names)[::-1]
        sign=0
        for file_name in file_names:
            if file_name.endswith("-pointer"):
                if sign>0:
                    done(decode_dir+"/"+file_name, source_file_dir)
                sign+=1


def case_study():
    
    def example_hex():
        example_origin=open(common.path_corpus+"/example1")
        example_out=open(common.path_corpus+"/example1-test", "w")
        for line in example_origin:
            line=line.strip("\n")
            example_out.write(common.Hashhex(line)+"-0\n")
        example_out.close()
        example_origin.close()
    
    #example_hex()
    
    def attention_distribution():
        path_example=common.path_log_root+"/TI-PG/decode-example"
        path_example_out=path_results+"/example1/attentions"
        file_names=os.listdir(path_example)
        file_names=sorted(file_names)[::-1]
        score_file_names=[]
        sign=0
        for file_name in file_names:
            if file_name.endswith("-attn"):
                if sign>0:
                    score_file_names.append(file_name)
                sign+=1
        for file_name in score_file_names:
            all_text_att=0.
            all_img_att=0.
            
            r_file=open(path_example+"/"+file_name)
            print(file_name)
            w_file=open(path_example_out+"/"+file_name,"w")
            
            record_no=0
            line_no=0
            while True:
                line= r_file.readline()
                if line=="":
                    break
                line_no+=1
                line=line.strip("\n")
                items=line.split(" ")
                if len(items)==2:
                    record_no+=1
                    w_file.write("[%d]\n" % record_no)
                    w_file.write(line+"\n")
                    
                    row=int(items[0])
                    col=int(items[1])
                    row_index=0
                    arrays=[]
                else:
                    if len(items)!=col:
                        print(line_no)
                        print(len(items))
                        print(line)
                        print(items)
                    array=[float(item) for item in items]
                    array=np.array(array)
                    img_att_array=array[:196]
                    text_att_array=array[196:]
                    img_att_sum=text_att_array.sum()
                    text_att_sum=text_att_array.sum()
                    w_file.write("%.10f %.10f\n" % (1-text_att_sum, text_att_sum))
                    arrays.append(array)
                    row_index+=1
                    del array
                        
                    if row_index==row:
                        arrays=np.array(arrays)
                        img_att_arrays=arrays[:, :196]
                        text_att_arrays=arrays[:, 196:]
                            
                        sum_text_att=text_att_arrays.sum()
                        sum_img_att=img_att_arrays.sum()
                        att=sum_img_att+sum_text_att
                        sum_text_att=sum_text_att/att
                        sum_img_att=1-sum_text_att
                            
                        w_file.write("%.6f %.6f\n" % (sum_img_att, sum_text_att))
                            
                        del arrays
                
            r_file.close()
            w_file.close()
    
    def pointer_distribution():
        path_example=common.path_log_root+"/TI-PG/decode-example"
        path_example_out=path_results+"/example1/pointers"
        source_file_dir=common.path_corpus+"/story-texts-1-flat"
        test_file=open(common.path_corpus+"/example1-test")
        txt_file_names=[line.strip("\n") for line in test_file.readlines()]
        test_file.close()
        
        file_names=os.listdir(path_example)
        file_names=sorted(file_names)[::-1]
        attn_file_names=[]
        ptr_file_names=[]
        sign1=0
        sign2=0
        for file_name in file_names:
            if file_name.endswith("-attn"):
                if sign1>0:
                    attn_file_names.append(file_name)
                sign1+=1
                
            if file_name.endswith("-pointer"):
                if sign2>0:
                    ptr_file_names.append(file_name)
                sign2+=1
        
        for att_file_name, ptr_file_name in zip(attn_file_names, ptr_file_names):
            
            r_file_att=open(path_example+"/"+att_file_name)
            r_file_ptr=open(path_example+"/"+ptr_file_name)
            print(att_file_name, ptr_file_name)
            w_file=open(path_example_out+"/"+att_file_name,"w")
            
            record_no=0
            line_no=0
            while True:
                line_att= r_file_att.readline()
                line_ptr=r_file_ptr.readline()
                if line_att=="" or line_ptr=="":
                    break
                line_no+=1
                line_att=line_att.strip("\n")
                line_ptr=line_ptr.strip("\n")
                items_att=line_att.split(" ")
                items_ptr=line_ptr.split(" ")
                #print(line_ptr)
                if len(items_att)==2:
                    record_no+=1
                    w_file.write("[%d]\n" % record_no)
                    
                    row=int(items_att[0])
                    col=int(items_att[1])
                    print("%d %d\n" % (row, col))
                    row_index=0
                    arrays_att=[]
                    arrays_ptr=[]
                    
                    txt_file=open(source_file_dir+"/"+txt_file_names[int(record_no)-1])
                    print(record_no, row, col)
                    txt=txt_file.read()
                    txt=txt.strip("\n")
                    txt=txt.split(" ")
                    txt_file.close()
                else:
                    array_att=[float(item) for item in items_att]
                    array_att=np.array(array_att)
                    img_att_array=array_att[:196]
                    text_att_array=array_att[196:]
                    arrays_att.append(text_att_array)
                    del array_att
                    
                    array_ptr=[float(item) for item in items_ptr]
                    array_ptr=np.array(array_ptr)
                    arrays_ptr.append(array_ptr)
                    del array_ptr
                    
                    row_index+=1
                        
                    if row_index==row:
                        arrays_att=np.array(arrays_att)
                        arrays_ptr=np.array(arrays_ptr)
                        
                        sum_arrays_att=np.sum(arrays_att,0)
                        print(np.shape(arrays_ptr))
                        sum_arrays_ptr=np.sum(arrays_ptr,0)
                        
                        sum_arrays=sum_arrays_ptr-sum_arrays_att
                        sum_arrays=sum_arrays/row
                        sum_arrays=np.sort(sum_arrays)
                        ix, = np.unravel_index(sum_arrays.argsort(axis=0), dims=sum_arrays.shape)
                        ix=ix[::-1]
                        for index in ix:
                            w_file.write("%f"%(sum_arrays[index]*1000))
                            w_file.write("\t")
                        w_file.write("\n")
                        for index in ix:
                            w_file.write(txt[index])
                            w_file.write("\t")
                        #sum_arrays=sum_arrays[::-1]*1000
                        #str_sum_arrays=" ".join(["%.20f" % (item) for item in sum_arrays])
                            
                        #w_file.write("%s\n" % str_sum_arrays)
                        w_file.write("%f\n" % np.sum(sum_arrays))
                
            r_file_att.close()
            r_file_ptr.close()
            w_file.close()
    
    #attention_distribution()
    pointer_distribution()


def test():
    #print(common.Hashhex("""http://web.archive.org/web/20130411214317id_/http://www.dailymail.co.uk/sciencetech/article-2306283/The-Rhino-DNA-database-cut-poaching.html"""))
    a=np.array([1.,8.,3.,4.])
    ix, = np.unravel_index(a.argsort(axis=0), dims=a.shape)
    print(ix)

if __name__ == '__main__':
    #re_calc("dailymail")
    #re_calc("bbc")
    #accumulate("dailymail")
    #accumulate("bbc")
    #bbc(100, 1)
    #statistic()
    #test()
    #visualparts2words("dailymail")
    #visualparts2words("bbc")
    #evaluate_visualparts2words("dailymail")
    #attentions("bbc")
    #pointer2words("dailymail")
    #bbc()
    case_study()





