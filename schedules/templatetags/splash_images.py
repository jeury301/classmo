from django import template

register = template.Library() 

@register.filter
def get_credit(dictionary,key):
	return dictionary.get(key)

@register.filter
def get_transition_info(dictionary):
	"""
	n=number of images
    a=image visible duration in seconds a=8
    b=image crossfade duration in seconds b=2
    t=total animation duration =(a+b)*n =30, result of a b and n
	"""
	a=8
	b=2
	n=0
	for image in dictionary:
		n+=1
	if n==1:
		return False
	t=(a+b)*n
	l=t
	"""
	oplist getsvalues based on a, b and t, the ordering matters so it should not be changed
	"""
	oplist=[round((a/t)*100,2),round(((a+b)/t)*100,2),round(100-(b/t*100),2)]
	image_of_nth=[]
	for i in range(0,n):
		l=l-(a+b)
		image_of_nth.append(l)

	
	trans_info={"a":a,"b":b,"n":n,"t":t,"oplist":oplist,"image_of_nth":image_of_nth}
	return trans_info



		