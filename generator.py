import random 
def get_num():
	codes = {
	0:"!",
	1:"a",
	2:"b",
	3:"c",
	4:"d",
	5:"e",
	6:"f",
	7:"g",
	8:"h",
	9:"i",
	10:"j",
	11:"k",
	12:"l",
	13:"m",
	14:"n",
	15:"o",
	16:"p",
	17:"q",
	18:"r",
	19:"s",
	20:"t",
	21:"u",
	22:"v",
	23:"w",
	24:"x",
	25:"y",
	26:"z",
	27:"1",
	28:"2",
	29:"3",
	30:"4",
	31:"5",
	32:"6",
	33:"7",
	34:"8",
	35:"9",
	36:"?",
	37:"-",
	38:"&",
	39:"="
	}
	num = random.randrange(0,39)
	num1 = random.randrange(0,39)
	num2 = random.randrange(0,39)
	num3 = random.randrange(0,39)
	num4 = random.randrange(0,39)
	code = f"{codes[num]}{codes[num1]}{codes[num2]}{codes[num3]}{codes[num4]}"
	return(code)
print(get_num())

