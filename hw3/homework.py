import copy
import time
from collections import defaultdict


def convertToPredicate(string):
    pred = []
    if string[0] == '~': pred.append('~')
    else: pred.append('')
    pred.extend(string.replace('~', '').replace('(', ',').replace(')', '').split(','))
    return pred


def convertVar(sentence, idx):
    var = defaultdict(str)
    for pred in sentence:
        for i, obj in enumerate(pred[2:]):
            if obj[0].islower():
                if var[obj] == '':
                    var[obj] = 'v' + str(idx)
                    pred[i+2] = var[obj]
                    idx += 1
                else: pred[i+2] = var[obj]
    return sentence, idx


def unify(kbPredVar, queryPredVar, convert):
    if convert == None:
        return None
    elif kbPredVar == queryPredVar:
        return convert
    elif kbPredVar.islower():
        if kbPredVar in convert:
            return unify(convert[kbPredVar], queryPredVar, convert)
        elif queryPredVar in convert:
            return unify(kbPredVar, convert[queryPredVar], convert)
        else:
            convert[kbPredVar] = queryPredVar
            return convert
    elif queryPredVar.islower():
        if queryPredVar in convert:
            return unify(convert[queryPredVar], kbPredVar, convert)
        elif kbPredVar in convert:
            return unify(queryPredVar, convert[kbPredVar], convert)
        else:
            convert[queryPredVar] = kbPredVar
            return convert
    else:
        return None


def resolution(kb, querySentence):
    sentencePairs = []
    for kbSenetnce in kb:
        for kbPred in kbSenetnce:
            for queryPred in querySentence:
                if kbPred[0] != queryPred[0] and kbPred[1] == queryPred[1]:
                    sentencePairs.append((kbSenetnce, querySentence))
    for sentencePairs in sentencePairs:
        kbSenetnce, querySentence = sentencePairs[0], sentencePairs[1]
        Sentences = []
        for i, kbPred in enumerate(kbSenetnce):
            for j, queryPred in enumerate(querySentence):
                if kbPred[0] != queryPred[0] and kbPred[1] == queryPred[1]:
                    newKbSenetnce = copy.deepcopy(kbSenetnce)
                    newQuerySentence = copy.deepcopy(querySentence)
                    newKbSenetnce, kbSentenceIdx = convertVar(newKbSenetnce, 1)
                    newQuerySentence = convertVar(newQuerySentence, kbSentenceIdx + 1)[0]
                    convert = {}
                    for k in range(2, len(newKbSenetnce[i])):
                        convert = unify(newKbSenetnce[i][k], newQuerySentence[j][k], convert)
                    if convert != None:
                        newSentence = []
                        sentence1 = copy.deepcopy(newKbSenetnce)
                        sentence2 = copy.deepcopy(newQuerySentence)
                        sentence1.remove(sentence1[i])
                        # if queryDict[str(sentence2[j])] == 1:
                            # print(str(sentence2[j]))
                            # print(queryDict)
                            # return False
                        # queryDict[str(sentence2[j])] = 1
                        sentence2.remove(sentence2[j])
                        newSentence.extend(sentence1)
                        newSentence.extend(sentence2)
                        if newSentence != []:
                            for a, pred in enumerate(newSentence):
                                for b, var in enumerate(pred[2:]):
                                    if var in convert:
                                        newSentence[a][b+2] = convert[var]
                            newSentence = convertVar(newSentence, 1)[0]
                            newSentence.sort(key=lambda x: x[0] + x[1])
                            # print("new",newSentence)
                            # print("kbS",newKbSenetnce)
                            Sentences.append(newSentence)
                        else:
                            newSentence = None
                            Sentences.append(newSentence)
                            for c in Sentences:
                                if c == None:
                                    return True
        if time.time() - startTime > 5: return False
        for s in Sentences:
            if s not in kb:
                kb.append(s)
                if resolution(kb, s) == True: return True

# read input file
f = open("input.txt", "r")
lines = f.readlines()
nQuery = int(lines[0])
queries = [convertToPredicate(query.strip()) for query in lines[1:nQuery+1]]
nKB = lines[nQuery+1]
origin_kb = []
# build knowledge base
for line in lines[nQuery+2:]:
    # a => b convert to [~a|b]
    replaceLine = line.strip().replace('&', '|').replace('=>', '|')
    orPredList = replaceLine.split(' | ')
    if "=>" in line:
        for i in range(len(orPredList)):
            if i != len(orPredList) - 1:
                if orPredList[i][0] != '~': orPredList[i] = '~' + orPredList[i]
                else: orPredList[i] = orPredList[i][1:]
    origin_kb.append(orPredList)
origin_kb.sort(key=lambda x: len(x))
for i in range(len(origin_kb)):
    originSentence = [convertToPredicate(pred) for pred in origin_kb[i]]
    origin_kb[i] = convertVar(originSentence, 1)[0]
    origin_kb[i].sort(key=lambda x: x[0] + x[1])
# write output file
f = open("output.txt", "w")
for query in queries:
    startTime = time.time()
    queryDict = defaultdict(int)
    kb = copy.deepcopy(origin_kb)
    if query[0] == '~': query[0] = ''
    else: query[0] = '~'
    if resolution(kb, [query]): f.write("TRUE\n")
    else: f.write("FALSE\n")
