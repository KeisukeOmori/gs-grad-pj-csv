from flask import Flask, request, render_template, jsonify
from flask import redirect
from flask import url_for
import requests
import json

import pandas as pd
import spacy
import os
#nlp = spacy.load('en_core_web_sm')
nlp = spacy.load
import re
from collections import Counter
import codecs
import csv

import matplotlib.pyplot as plt
from wordcloud import WordCloud

import random
from datetime import datetime
import string

app = Flask(__name__)

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def main():
    props = {'title': 'BIOgrabber', 'msg': 'Welcome to Index Page.'}
    html = render_template('index.html', props=props)
    return html

def search():
    renderpage = render_template("search.html")
    return renderpage

@app.route("/result", methods=['POST'])
def result():
    with codecs.open("static/bigdata_all_g.csv", 'r', 'utf-8', 'ignore') as f:
        df1 = pd.read_csv(f, dtype='object')
    idlist = pd.Series.tolist(df1.PMID)

    item = request.form['item']
    url_f    = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term='
    url_b    = '&retmax=500&retmode=json'
    url      = url_f + item + url_b
    get_url  = requests.get(url)
    get_json = get_url.json()
    pmids = get_json['esearchresult']['idlist']
    
    cloudid = set(pmids) & set(idlist)
    matchid = df1[df1['PMID'].isin(cloudid)]

    gene= ''.join(map(str,matchid.Match_gene))
    gene_trim = gene.replace("'", "").replace(",","").replace("[","").replace("]","").replace("AR","")
    
    stop_words = ['year','of','in','the','to','doing', 'am', 'between', 'of', 'same', 'she', 'to', "don't", "they're",
                    "we've", "she'll", "we'll", 'does', "you'll", "aren't", 'are', "we're",
                    'cannot', "haven't", 'into', 'yourselves', "didn't", 'during', 'her', 'how',
                    'all', 'should', 'herself', 'by', 'against', 'own', 'further', 'be',
                    'myself', 'about', 'me', 'them', "you're", 'off', 'ought', 'under', 'has',"he's", "she's", 'itself', "i'd", 'there', 'if', "wasn't", 'those', 'our',
                    'otherwise', 'did', 'above', 'however', 'was', 'com', 'ourselves', "i've",'your', "why's", 'else', 'yourself', 'his', 'most', "when's", 'why', 'this',
                    'once', "it's", "i'm", 'ever', "shouldn't", 'an', 'while', 'whom', "you've","i'll", 'k', "they've", 'what', "he'd", "hasn't", "couldn't", 'had', 'i',
                    "you'd", 'but', 'himself', 'could', "how's", 'so', 'hers', 'we', "weren't",'the', 'they', 'yours', 'just', 'nor', 'then', 'few', "shan't", 'r', 'too',
                    "mustn't", 'would', 'can', 'ours', 'such', 'very', "won't", 'were', 'in','only', 'below', 'any', 'as', 'here', 'again', "they'll", "can't", "let's",
                    'him', 'have', 'theirs', 'it', 'you', 'which', 'been', 'on', 'over', 'more','some', "here's", 'themselves', 'where', 'is', "we'd", 'shall', 'with',
                    'like', 'being', 'my', 'since', 'that', 'until', 'who', "wouldn't",'before', 'www', 'out', 'than', 'at', 'do', 'or', 'their', "where's",
                    "they'd", 'http', 'when', "isn't", "he'll", 'from', 'for', 'other',"that's", 'its', 'get', 'both', "hadn't", 'and', 'these', 'up', "what's",
                    'no', 'through', "she'd", 'also', "doesn't", 'not', "there's", 'a', 'he','because', 'down', 'after', "who's", 'having', 'each','','BP','department','various',
                    'de','doi','conflict','sCollection','Author','Cassell','stage','jkcvhl','cell','protein','Cultivated','St','Russia','Institute','pii','ND','released','Capacity',
                    'National','expression','expressed','University','Key','Medicine','Wang','Laboratory','State','colonization','China','Xining','age','Qinghai','Animal','communities','Zhang',
                    'Science','Laboratory','s41598','abundance','significantly','lambs','genes','Italy','mediate','Basic','Bari','Organs','Medical','information','Dec','sequence','Microcirculation','heritable','control',
                    'factors','refer','changes','Epub','process','term','Ribatti','vascular','regulated','Sciences','states','Different','angiogenic','factors','print','article','makes','due',
                    'analyze','events','mechanisms','cells','processes','aim','aberrations','PMID','Innsbruck','Zoology Center','molecular','Biosciences','weight','Technikerstrasse','uibk','low',
                    'pathway','Physics','Clinical','weight','Taiwan','patients','Taipei','Hospital','anti','City','showed','College','results','treatment','landscape','Shanghai','High','promote','distant','associated','poor',
                    'USA','small','Texas','significant','showed','College','United','America','Minnesota','increased','phenotype','mice','Istanbul','Nightingale Abide','statistically','Turkey','evaluation','utility','prognostic','London','UK',
                    'survival',"1'","2'","3'","depart'","pmid'","4'",'ahead',"print'",'Liverpool','Unit','severe','case','infection','Broadgreen','Hospitals','Royal','Health','identified','Infectious','West','England','UK','Tropical','adults','Trust',
                    'Sciences','two','features','North','comparison','Johnston','Research','Sciences','Biology','Copyright','Center','review','response','Published Elsevier','Electronic','address','therapy','School','non','System','Center','Cellular','effect','disease','immune',
                    'therapies','specific','study','role','studies','based','role','important','shown','activity','patient','targeting','Division','CONCLUSION','response','efficacy','METHOD','PMCID','analysis','compared','development','novel',
                    'trial','human','METHODS','group','composition','effects','level','Technology','diseases','potential','microbioal','including','species',
                    'IV','GC','HR','MS','SR','CP','HP','CS','PI3','HCC','MB','ZO','HL']

    wordcloud = WordCloud(
        stopwords = set(stop_words),
        width=1000, height=1000,
        mode="RGB")

    wordcloud.generate(gene_trim)
    plt.figure(figsize=(12,12), facecolor='k')
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.imshow(wordcloud)
    plt.axis('off')
    save_dir = "static/img/"
    
    dt_now = datetime.now().strftime("%Y%m%d%H%M%S") + random_str(5)
    save_path = os.path.join(save_dir, dt_now + ".png")
    plt.savefig(save_path)
    props = {'title': 'Step-by-Step Flask - hello', 'msg': 'What you ask for.',
             'item': item, 'url': url, 'pmids':pmids,'save_path':save_path}

    html = render_template('result.html', props=props)
    return html

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('main'))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    #port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    #app.run(debug=True)