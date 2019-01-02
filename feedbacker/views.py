import nltk
import string
import numpy as np
import pandas as pd
import seaborn as sns
import wikipedia
import matplotlib.pyplot as plt

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from django.shortcuts import render, redirect
from collections import OrderedDict

####GLOBALS####
is_noun = lambda pos: pos[:2] == 'NN'
documents = []
titles = []
input_doc = ""
document_numbers = []
document_similarities = []
stoplist = set(
    ", & && || : ; < > ] [ { } 's 'S $ # % * - | + ) ( ! ~ ` `` 'u u' inn \u0631\u0627\u062d\u06cc\u0644 \u0634\u0631\u06cc\u0641\u202c @ a /br > < -- . able about above abroad according accordingly across actually adj after afterwards again against ago ahead ain't all allow allows almost alone along alongside already also although always am amid amidst among amongst an and another any anybody anyhow anyone anything anyway anyways anywhere apart appear appreciate appropriate are aren't around as a's aside ask asking associated at available away awfully b back backward backwards be became because become becomes becoming been before beforehand begin behind being believe below beside besides best better between beyond both brief but by c came can cannot cant can't caption cause causes certain certainly changes clearly c'mon co co. com come comes concerning consequently consider considering contain containing contains corresponding could couldn't course c's currently d dare daren't definitely described despite did didn't different directly do does doesn't doing done don't down downwards during e each edu eg eight eighty either else elsewhere end ending enough entirely especially et etc even ever evermore every everybody everyone everything everywhere ex exactly example except f fairly far farther few fewer fifth first five followed following follows for forever former formerly forth forward found four from further furthermore g get gets getting given gives go goes going gone got gotten greetings h had hadn't half happens hardly has hasn't have haven't having he he'd he'll hello help hence her here hereafter hereby herein here's hereupon hers herself he's hi him himself his hither hopefully how howbeit however hundred i i'd ie if ignored i'll i'm immediate in inasmuch inc inc. indeed indicate indicated indicates inner inside insofar instead into inward is isn't it it'd it'll its it's itself i've j just k keep keeps kept know known knows l last lately later latter latterly least less lest let let's like liked likely likewise little look looking looks low lower ltd m made mainly make makes many may maybe mayn't me mean meantime meanwhile merely might mightn't mine minus miss more moreover most mostly mr mrs much must mustn't my myself n name namely nd near nearly necessary need needn't needs neither never neverf neverless nevertheless new next nine ninety no nobody non none nonetheless noone no-one nor normally not nothing notwithstanding novel now nowhere o obviously of off often oh ok okay old on once one ones one's only onto opposite or other others otherwise ought oughtn't our ours ourselves out outside over overall own p particular particularly past per perhaps placed please plus possible presumably probably provided provides q que quite qv r rather rd re really reasonably recent recently regarding regardless regards relatively respectively right round s said same saw say saying says second secondly see seeing seem seemed seeming seems seen self selves sensible sent serious seriously seven several shall shan't she she'd she'll she's should shouldn't since six so some somebody someday somehow someone something sometime sometimes somewhat somewhere soon sorry specified specify specifying still sub such sup sure t take taken taking tell tends th than thank thanks thanx that that'll thats that's that've the their theirs them themselves then thence there thereafter thereby there'd therefore therein there'll there're theres there's thereupon there've these they they'd they'll they're they've thing things think third thirty this thorough thoroughly those though three through throughout thru thus till to together too took toward towards tried tries truly try trying t's twice two u un under underneath undoing unfortunately unless unlike unlikely until unto up upon upwards us use used useful uses using usually v value various versus very via viz vs w want wants was wasn't way we we'd welcome well we'll went were we're weren't we've what whatever what'll what's what've when whence whenever where whereafter whereas whereby wherein where's whereupon wherever whether which whichever while whilst whither who who'd whoever whole who'll whom whomever who's whose why will willing wish with within without wonder won't would wouldn't x y yes yet you you'd you'll your you're yours yourself yourselves you've z zero <br> br".split())

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

currdir = path.dirname(__file__)

currdir = currdir + "/static"


####END GLOBALS###


def index(request):
    return render(request, "landing.html")


def feedback(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        use_top = 6  # use most relevent doc
        count = 0
        both = 0.0
        A_c = 0.0
        B_c = 0.0
        relation = 0.0

        temp_title = title
        temp_title = temp_title.lower()
        text = content
        consepts_in_title = [word for word in nltk.word_tokenize(temp_title) if word not in stoplist]  # removing stop
        text = text.lower()
        # text = filter(lambda x: x in string.printable, text)
        consepts_in_user_provided_doc = [word for word in nltk.word_tokenize(text) if word not in stoplist]
        consepts_in_user_provided_doc = list(OrderedDict.fromkeys(consepts_in_user_provided_doc))

        search = [[0 for i in range(2)] for j in range(use_top)]  # 2D list to save search data

        p = 0
        k = 0
        wordle_text = []
        for ci in consepts_in_user_provided_doc:
            p = p + 1
        print
        "ci count :", p
        for cj in consepts_in_title:
            k = k + 1
        print
        "cj count :", k
        total_conecpts_in_user_doc = p * k
        save_relation = [[0 for i in range(3)] for j in range((p * k))]  # 2D list to save search data
        r_counter = 0

        check = 0
        try:
            title = wikipedia.search(temp_title, 7, True)[0]
            text_1 = get_wiki(title[0])
            text_2 = get_wiki(title[1])
            text_3 = get_wiki(title[2])
            text_4 = get_wiki(title[3])
            text_5 = get_wiki(title[4])
            text_6 = get_wiki(title[5])
            text_7 = get_wiki(title[6])

            text_1 = text_1.lower()
            wiki_concepts_1 = [word for word in nltk.word_tokenize(text_1) if word not in stoplist]
            # print wiki_concepts_1
            text_2 = text_2.lower()
            wiki_concepts_2 = [word for word in nltk.word_tokenize(text_2) if word not in stoplist]
            # print wiki_concepts_2
            text_3 = text_3.lower()
            wiki_concepts_3 = [word for word in nltk.word_tokenize(text_3) if word not in stoplist]

            text_4 = text_4.lower()
            wiki_concepts_4 = [word for word in nltk.word_tokenize(text_4) if word not in stoplist]

            text_5 = text_5.lower()
            wiki_concepts_5 = [word for word in nltk.word_tokenize(text_5) if word not in stoplist]

            text_6 = text_6.lower()
            wiki_concepts_6 = [word for word in nltk.word_tokenize(text_6) if word not in stoplist]

            text_7 = text_7.lower()
            wiki_concepts_7 = [word for word in nltk.word_tokenize(text_7) if word not in stoplist]
            pass  # do nothing
        except Exception as e:
            print(e, " |there is an error while fetching wiki data ++++")
        check = 1

        for ci in consepts_in_user_provided_doc:
            for cj in consepts_in_title:
                for x in range(0, use_top):
                    if x == 3 and check == 0:
                        words = wiki_concepts_1
                    elif x == 4 and check == 0:
                        words = wiki_concepts_2
                    elif x == 5 and check == 0:
                        words = wiki_concepts_3
                    elif x == 6 and check == 0:
                        words = wiki_concepts_4
                    elif x == 7 and check == 0:
                        words = wiki_concepts_5
                    elif x == 8 and check == 0:
                        words = wiki_concepts_6
                    elif x == 9 and check == 0:
                        words = wiki_concepts_7

                    if ci in words:
                        search[count][0] = 1  # ci(A) is found in count file #
                    if cj in words:
                        search[count][1] = 1  # cj(B) is found in count file #
                    count = count + 1
                for x in range(0, (use_top)):
                    if (search[x][0] and search[x][1]) == 1:  # Both Ci(A) and Cj(B) found in x file in the List
                        both = both + 1
                    if search[x][0] == 1:  # Ci(A) found in x file in the List
                        A_c = A_c + 1
                    if search[x][1] == 1:  # Cj(B) found in x file in the List
                        B_c = B_c + 1
                print(search)
                print(both)  # cij - count
                print(A_c)  # ci - count from all files
                print(B_c)  # cj - count from all files
                if A_c == 0:
                    A_c = 1
                if B_c == 0:
                    B_c = 1
                relation = ((both * both) / (A_c * B_c))
        print("Relation  between [", ci, "] and [", cj, "] = ", relation)
        save_relation[r_counter][0] = ci
        save_relation[r_counter][1] = cj
        save_relation[r_counter][2] = relation
        search = [[0 for i in range(2)] for j in range(use_top)]
        count = 0
        both = 0.0
        A_c = 0.0
        B_c = 0.0
        relation = 0.0
        r_counter = r_counter + 1

        save_relation.sort(key=lambda x: x[2], reverse=True)
        count_th = 0
        correlation_th_percentage = 0.4  # only concepts that are grater or == then this ration will appear in correlation map
        concept_map_th_percentage = 0.5  # only concepts that are grater or == then this ration will appear in concept map
        for i in save_relation:
            if i[2] >= concept_map_th_percentage:
                wordle_text.append(i[0])
            if i[2] >= correlation_th_percentage:
                count_th = count_th + 1
        best_relation = [[0 for i in range(3)] for j in range(count_th)]
        temp_th = 0
        best_match = 0
        less_match = 0
        for i in save_relation:
            if i[2] >= correlation_th_percentage:  # use this loop for extracting desired relational data for wordle
                best_relation[temp_th][0] = i[0]
                best_relation[temp_th][1] = i[1]
                best_relation[temp_th][2] = i[2]
                temp_th = temp_th + 1
            if i[2] >= 0.5:  # use this for other calculations
                best_match = best_match + 1
            if 0 < i[2] < 0.5:
                less_match = less_match + 1

        if count_th > 0:
            relations = np.array(best_relation)

            x = np.array(relations[:, 0])
            x = x.astype(str)
            y = np.array(relations[:, 1])
            y = y.astype(str)
            z = np.array(relations[:, 2])
            z = z.astype(float)

            df = pd.DataFrame.from_dict(np.array([x, y, z]).T)
            df.columns = ['Concepts in Provided Document', 'Concepts in Title', 'Z_value']
            df['Z_value'] = pd.to_numeric(df['Z_value'])
            pivotted = df.pivot('Concepts in Title', 'Concepts in Provided Document', 'Z_value')

            plt.figure(figsize=(65, 25))
            ax = plt.subplot(111)

            p = sns.heatmap(pivotted, annot=True, fmt=".1f", linewidths=.5, ax=ax)
            p.set_xticklabels(p.get_xticklabels(), rotation=90)
            p.get_figure().savefig(path.join(currdir, "heatmap.png"))
            plt.close()

            more_related_concepts_percentage = float((float(best_match) / float(total_conecpts_in_user_doc)) * 100)
            less_related_concepts_percentage = float((float(less_match) / float(total_conecpts_in_user_doc)) * 100)
            other_concepts_percentage = float(
                100 - (more_related_concepts_percentage + less_related_concepts_percentage))
            m1 = "{0:.2f}".format(more_related_concepts_percentage), '% \n Most Relevant'
            m1 = ''.join(map(str, m1))
            m2 = "{0:.2f}".format(less_related_concepts_percentage), '% \n Less Relevant'
            m2 = ''.join(map(str, m2))
            m3 = "{0:.2f}".format(other_concepts_percentage), '% \n Other'
            m3 = ''.join(map(str, m3))

            df = pd.DataFrame({'Concepts Distribution': [float("{0:.2f}".format(more_related_concepts_percentage)),
                                                         float("{0:.2f}".format(less_related_concepts_percentage)),
                                                         float("{0:.2f}".format(other_concepts_percentage))], },
                              index=[m1, m2, m3])
            p = df.plot.pie(y='Concepts Distribution', figsize=(6, 6), colors=['cadetblue', 'skyblue', 'lightcoral'])
            p.get_figure().savefig(path.join(currdir, "pi_chart.png"))
            plt.close()
            # ----------------------------------------------------
        else:
            img = Image.new('RGB', (800, 1280), (255, 255, 255))
            img.save(path.join(currdir, "heatmap.png"), "PNG")
            img.save(path.join(currdir, "pi_chart.png"), "PNG")

        wordle_text = " ".join(wordle_text)

        if wordle_text == "" or wordle_text == " ":
            create_wordcloud("N0 Concept Concept Concept Concept Found Found Found  ")
        else:
            create_wordcloud(wordle_text)

        return render(request, "feedback.html")
    else:
        return redirect('dashboard:landing')


def create_wordcloud(text):
    # create numpy araay for wordcloud mask image
    mask = np.array(Image.open(path.join(currdir, "cloud.png")))
    # create set of stopwords
    stopwords = set(STOPWORDS)
    # create wordcloud object
    wc = WordCloud(background_color="white",
                   max_words=200,
                   mask=mask,
                   stopwords=stopwords)
    # generate wordcloud
    wc.generate(text)
    # save wordcloud
    wc.to_file(path.join(currdir, "wordle.png"))


def get_wiki(query):
    # get wikipedia page for selected title
    page = wikipedia.page(query)
    return page.content
