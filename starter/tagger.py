# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
import pandas as pd


def normalize(df):
    for col in df.columns:
        df[col] = df[col]/sum(df[col])
    return df


def build_tables(input):
    words = input.split("\n")

    #print(words[:6])

    em = {}
    trans = {}
    tags = ['Start']
    prev_tag = tags[-1]

    for line in words:
        if ":" not in line:
            continue
        col = line.index(":")

        # gets curr tag
        tag = line[col+2:]

        if prev_tag not in trans:
            trans[prev_tag] = {}
        if tag not in trans[prev_tag]:
            trans[prev_tag][tag] = 0
        trans[prev_tag][tag] += 1

        # to get all unique tags
        if tag not in tags:
            tags.append(tag)

        # gets curr word
        word = line[:col-1]

        # for each word, increments the appropriate tag
        if word not in em:
            em[word]= {}
        if tag not in em[word]:
            em[word][tag] = 0
        em[word][tag] += 1

        prev_tag = tag

    em_df = pd.DataFrame(em).transpose()
    em_df = em_df.fillna(0)
    em_df = normalize(em_df)

    trans_df = pd.DataFrame(trans).transpose()
    trans_df = normalize(trans_df)
    return em_df, trans_df, tags


def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    print(training_list, test_file, output_file)


    # INPUT
    input = ""

    for file in training_list:
        f = open(file, "r")
        input += f.read()

    em_df, trans_df, tags = build_tables(input)
    #print(em_df.head(10))



    # TEST get words
    input = ""
    f = open(test_file, "r")
    input += f.read()
    words = input.split("\n")

    # OUTPUT
    f = open(output_file, "w")


    # em_df = em_df.transpose()
    # trans_df = trans_df.transpose()
    # d = dict(em_df.idxmax())
    # t = dict(trans_df.idxmax())

    prev_tag = 'PUN'
    for word in words:
        p = {}
        for i in tags:

            p[i] = em_df.loc[word, i] * trans_df.loc[prev_tag, i]
            if p[i] == 0:
                p[i] = 1/(len(tags)**2)

            # if word in t and word in d:
            #     if em_df[word].max() > trans_df[word].max():
            #         tag = d[word]
            #     else:
            #         tag = t[word]
            # else:
            #     if word in d:
            #         tag = d[word]
            #     elif word in t:
            #         tag = t[word]
            #     else:
            #         tag = tags[-1]

        tag = max(p, key=p.get)

        prev_tag = tag
        s = word + " : " + tag + "\n"
        f.write(s)
    f.close()

    #print(get_results(test_file, output_file))

    return


if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)


    #tag(['../training-test/training1.txt', '../training-test/training2.txt'], '../training-test/test1.txt', 'o.txt')

