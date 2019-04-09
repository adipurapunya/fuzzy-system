import sys

temperature_fuzzy_set = ['Cold', 'Cool', 'Normal', 'Warm', 'Hot'] # input value degree celcius
humidity_fuzzy_set = ['Dry', 'Moist', 'Wet'] # input value percentage of humidity

sprinkler_duration_fuzzy_set = ['Short', 'Medium', 'Long'] # output, how long we have to sprinkler our plant ?


def main():
    print('')
    print('Input Of Fuzzyfication')
    print('')
    print('Please input temperature value (celcius) : ', end = '', flush=True)
    temperature = int(sys.stdin.readline())

    print('Please input percentage humidity (%) : ', end='', flush=True)
    humidity = int(sys.stdin.readline())

    rules = parse_kb_file('rule.kb')

    tmp = temperatureFunction(temperature)
    hum = humidityFunction(humidity)

    print('Output Of Fuzzyfication')
    print(tmp)
    print(hum)
    print('')

    inf = inferred(tmp, hum,  rules) # inference Process

    result_rule_min = []

    for dt in inf:
        print(dt[0][0][0][1], dt[0][0][0][2], dt[0][0][1][1], dt[0][0][1][2], dt[1])
        minimum = min(dt[0][0][0][2], dt[0][0][1][2])
        result_rule_min.append([dt[1],minimum])
    print('')

    print(result_rule_min)

    result_rule_max = {}
    for data in result_rule_min:
        if data[0] in result_rule_max:
            result_rule_max[data[0]].add(data[1])
        else:
            result_rule_max[data[0]] = set([data[1]])

    output_inference = []
    for key, value in result_rule_max.items():
        output_inference.append([key,max(value)])

    print('')
    print('Output Inference is', output_inference)
    print('')

    print('Deffuzzyfication')
    finalValue = defuzzyfication(output_inference)

    print('Minutes', finalValue)


def defuzzyfication(input):

    result = float(0)

    x1_short = 0
    x2_short = 28
    coefisien_short = float(0)

    x1_medium = 20
    x2_medium = 48
    coefisien_medium = float(0)

    x1_long = 40
    x2_long = 90
    coefisien_long = float(0)

    _short_numerator = float(0)    #pembilang
    _medium_numerator = float(0) #pembilang
    _long_numerator = float(0) #pembilang

    _short_denominator = float(0) #penyebut
    _medium_denominator = float(0) #penyebut
    _long_denominator = float(0) #penyebut

    for data in input:
        if data[0] == 'Short':
            coefisien_short = data[1]
        if data[0] == 'Medium':
            coefisien_medium = data[1]
        if data[0] == 'Long':
            coefisien_long = data[1]

    if coefisien_short != float(0) and coefisien_medium != float(0) and coefisien_long == float(0):
        x_start_short = x1_short
        x_end_short = x1_medium + 1 # should be plus 1

        x_start_medium = x2_short
        x_end_medium = x1_long + 1 # should be plus 1

        for i in range(x_start_short, x_end_short):
            _short_numerator += i * coefisien_short
            _short_denominator += coefisien_short

        for i in range(x_start_medium, x_end_medium):
            _medium_numerator += i * coefisien_medium
            _medium_denominator += coefisien_medium

        result = (_medium_numerator + _short_numerator) / (_medium_denominator + _short_denominator)

        #======================

    if coefisien_short == float(0) and coefisien_medium != float(0) and coefisien_long != float(0):

        x_start_medium = x2_short
        x_end_medium = x1_long + 1  # should be plus 1

        x_start_long = x2_medium
        x_end_long = x2_long + 1  # should be plus 1

        for i in range(x_start_medium, x_end_medium):
            _medium_numerator += i * coefisien_medium
            _medium_denominator += coefisien_medium

        for i in range(x_start_long, x_end_long):
            _long_numerator += i * coefisien_long
            _long_denominator += coefisien_long

        result = (_medium_numerator + _long_numerator) / (_medium_denominator + _long_denominator)

            # ======================

    if coefisien_short != float(0) and coefisien_medium != float(0) and coefisien_long != float(0):

        x_start_short = x1_short
        x_end_short = x1_medium + 1  # should be plus 1

        x_start_medium = x2_short
        x_end_medium = x1_long + 1  # should be plus 1

        x_start_long = x2_medium
        x_end_long = x2_long + 1  # should be plus 1

        for i in range(x_start_short, x_end_short):
            _short_numerator += i * coefisien_short
            _short_denominator += coefisien_short

        for i in range(x_start_medium, x_end_medium):
            _medium_numerator += i * coefisien_medium
            _medium_denominator += coefisien_medium

        for i in range(x_start_long, x_end_long):
            _long_numerator += i * coefisien_long
            _long_denominator += coefisien_long

        result = (_short_numerator + _medium_numerator + _long_numerator) / (_short_numerator + _medium_denominator + _long_denominator)

    if coefisien_short != float(0) and coefisien_medium == float(0) and coefisien_long == float(0):
        x_start_short = x1_short
        x_end_short = x1_medium + 1  # should be plus 1

        for i in range(x_start_short, x_end_short):
            _short_numerator += i * coefisien_short
            _short_denominator += coefisien_short

        result = (_short_numerator) / (_short_denominator)

        #=====

    if coefisien_short == float(0) and coefisien_medium != float(0) and coefisien_long == float(0):
        x_start_medium = x2_short
        x_end_medium = x1_long + 1  # should be plus 1

        for i in range(x_start_medium, x_end_medium):
            _medium_numerator += i * coefisien_medium
            _medium_denominator += coefisien_medium

        result = (_medium_numerator) / (_medium_denominator)

    #=====

    if coefisien_short == float(0) and coefisien_medium == float(0) and coefisien_long != float(0):
        x_start_long = x2_medium
        x_end_long = x2_long + 1  # should be plus 1

        for i in range(x_start_long, x_end_long):
            _long_numerator += i * coefisien_long
            _long_denominator += coefisien_long

        result = (_long_numerator)/(_long_denominator)


    return result




def inferred(fuzzification_temp, fuzzification_hum, fuzzyfication_rule):
    agenda = []
    possibility = []

    for dt in fuzzification_temp:
        agenda.append(dt)
    for dt in fuzzification_hum:
        agenda.append(dt)

    while agenda:
        item = agenda.pop(0)
        for rule in fuzzyfication_rule:
            for j, premise in enumerate(rule[0]):
                if premise == item[0]:
                    rule[0][j] = [True, rule[0][j], item[1]]
            if check_hypothesis(rule[0]):
                conclusion = rule[1]
                possibility.append(rule)
                agenda.append(conclusion)
                rule[0] = [rule[0],'processed']

    return possibility

def check_hypothesis(hypothesis):
    for entry in hypothesis:
        if entry[0] != True:
            return False
    return True

def temperatureFunction(input):
    linguistik_temperature = []
    if input >= -10 and input <=3:
        linguistik_temperature.append(temperature_fuzzy_set[0]) #Cold
    if input >= 0 and input <=15:
        linguistik_temperature.append(temperature_fuzzy_set[1]) #Cool
    if input >= 12 and input <=27:
        linguistik_temperature.append(temperature_fuzzy_set[2]) #Normal
    if input >= 24 and input <=39:
        linguistik_temperature.append(temperature_fuzzy_set[3]) #Warm
    if input >= 36 and input <=50:
        linguistik_temperature.append(temperature_fuzzy_set[4]) #Hot

    #=========================

    value_temp = []

    if len(linguistik_temperature) > 1:
        if linguistik_temperature[0] == temperature_fuzzy_set[0] and linguistik_temperature[1] == temperature_fuzzy_set[1]: # Between Cold and Cool
            #Cold
            cold = -(input - 3) / (3 - 0)
            value_temp.append([linguistik_temperature[0],cold])
            #Cool
            cool = (input - 0) / (3 - 0)
            value_temp.append([linguistik_temperature[1], cool])
        elif linguistik_temperature[0] == temperature_fuzzy_set[1] and linguistik_temperature[1] == temperature_fuzzy_set[2]: # Between Cool and Normal
            #Cool
            cool = -(input - 15) / (15-12)
            value_temp.append([linguistik_temperature[0],cool])
            #Normal
            normal = (input - 12) / (15-12)
            value_temp.append([linguistik_temperature[1],normal])
        elif linguistik_temperature[0] == temperature_fuzzy_set[2] and linguistik_temperature[1] == temperature_fuzzy_set[3]: # Between Normal and Warm
            #Normal
            normal = -(input - 27) / (27-24)
            value_temp.append([linguistik_temperature[0],normal])
            #Warm
            warm = (input - 24) / (27-24)
            value_temp.append([linguistik_temperature[1],warm])
        elif linguistik_temperature[0] == temperature_fuzzy_set[3] and linguistik_temperature[1] == temperature_fuzzy_set[4]: # Between Warm and Hot
            #Warm
            warm = -(input - 39) / (39-36)
            value_temp.append([linguistik_temperature[0],warm])
            #Hot
            hot = (input - 36) / (39-36)
            value_temp.append([linguistik_temperature[1],hot])
    else:
        value_temp.append([linguistik_temperature[0],1])


    return value_temp

def humidityFunction(input):
    linguistik_humidity = []
    if input >=0 and input <=20:
        linguistik_humidity.append(humidity_fuzzy_set[0]) # Dry
    if input >=10 and input <=50:
        linguistik_humidity.append(humidity_fuzzy_set[1]) # Moist
    if input >=40 and input <=70:
        linguistik_humidity.append(humidity_fuzzy_set[2]) # Wet

    #==========================
    value_hum = []
    if len(linguistik_humidity)>1:
        if linguistik_humidity[0] == humidity_fuzzy_set[0] and linguistik_humidity[1] == humidity_fuzzy_set[1] : #Between Dry and Moist
            #Dry
            dry = -(input - 20) / (20 - 10)
            value_hum.append([linguistik_humidity[0],dry])
            #Moist
            moist = (input - 10) / (20 - 10)
            value_hum.append([linguistik_humidity[1],moist])
        elif linguistik_humidity[0] == humidity_fuzzy_set[1] and linguistik_humidity[1] == humidity_fuzzy_set[2] : #Between Moist and Wet
            #Moist
            moist = -(input - 50) / (50 - 40)
            value_hum.append([linguistik_humidity[0],moist])
            #Wet
            wet = (input - 40) / (50 - 40)
            value_hum.append([linguistik_humidity[1],wet])
    else:
        value_hum.append([linguistik_humidity[0],1])

    return value_hum


def parse_kb_file(filename):
    kb_file = open(filename, 'rU')        # 'rU' is smart about line-endings
    kb_rules = []                         # to hold the list of rules

    for line in kb_file:                  # read the non-commented lines
        if not line.startswith('#') and line != '\n':
            kb_rules.append(split_and_build_literals(line.strip()))

    kb_file.close()
    return kb_rules

def split_and_build_literals(line):
    rules = []
    # Split the line of literals
    literals = line.split(' ')
    hypothesis = []
    while len(literals) > 1:
        hypothesis.append(literals.pop(0))
    rules.append(hypothesis)
    rules.append(literals.pop(0))
    return rules


if __name__ == '__main__':
    main()