import model
import nltk

def check(body):
	try:
		toBePredicted = [0 for i in range(21)]
		toBePredicted[0] = len(body)
		w = len(body.split(' '))
		toBePredicted[1] = w/float(toBePredicted[0])
		toBePredicted[2] = body.count('account') + body.count('Account')
		toBePredicted[3] = body.count('access') + body.count('Access')
		toBePredicted[4] = body.count('bank') + body.count('Bank')
		toBePredicted[5] = body.count('credit') + body.count('Credit')
		toBePredicted[6] = body.count('click') + body.count('Click')
		toBePredicted[7] = body.count('identity') + body.count('Identity')
		toBePredicted[8] = body.count('inconvenience') + body.count('Inconvenience')
		toBePredicted[9] = body.count('information') + body.count('Information')
		toBePredicted[10] = body.count('limited') + body.count('Limited')
		toBePredicted[11] = body.count('minutes') + body.count('Minutes')
		toBePredicted[12] = body.count('password') + body.count('Password')
		toBePredicted[13] = body.count('recently') + body.count('Recently')
		toBePredicted[14] = body.count('risk') + body.count('Risk')
		toBePredicted[15] = body.count('social') + body.count('Social')
		toBePredicted[16] = body.count('security') + body.count('Security')
		toBePredicted[17] = body.count('service') + body.count('Service')
		toBePredicted[18] = body.count('suspended') + body.count('Suspended')
		text = nltk.word_tokenize(body)
		pos_tagged = nltk.pos_tag(text)
		nouns = filter(lambda x:x[1]=='VB' or x[1]=='VBD' or x[1]=='VBG' or x[1]=='VBN' or x[1]=='VBP' or x[1]=='VBZ',pos_tagged)
		toBePredicted[19] = len(list(nouns))
		toBePredicted[20] = len(set(body))
		result = model.classifier.predict([toBePredicted])[0]
		return result
	except:
		return 0