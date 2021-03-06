from datetime import datetime

def check_family_dates_before_current(_families):
    for k, v in _families.items():
        if v.married != 'N/A':
            if not is_date_before_current(v.married):
                print('ERROR: FAMILY: US01: ' + v.famid + ': Marriage ' +
                    v.married + ' occurs in the future')
        if v.divorced != 'N/A':
            if not is_date_before_current(v.divorced):
                print('ERROR: FAMILY: US01: ' + v.famid + ': Divorce ' +
                    v.divorced + ' occurs in the future')
    return True

def check_individual_dates_before_current(_individuals):
    for k, v in _individuals.items():
        if v.birthday != 'N/A':
            if not is_date_before_current(v.birthday):
                print('ERROR: INDIVIDUAL: US01: ' + v.indiid + ': Birthday ' +
                    v.birthday + ' occurs in the future')
        if v.death != 'N/A':
            if not is_date_before_current(v.death):
                print('ERROR: INDIVIDUAL: US01: ' + v.indiid + ': Death ' +
                    v.death + ' occurs in the future')
    return True

def check_individual_age_less_than_150(_individuals):
    for k, v in _individuals.items():
        birth_date = datetime.strptime(v.birthday, '%d %b %Y')
        death_date = datetime.now()
        if v.death != 'N/A':
            death_date = datetime.strptime(v.death, '%d %b %Y')
        _age = calculate_dates_range(birth_date, death_date)
        if _age > 150:
            print('ERROR: INDIVIDUAL: US07: ' + v.indiid +
                ': More than 150 years old - Birth date ' + v.birthday)
    return True

def check_family_male_last_names(_families, _individuals):
    for k, v in _families.items():
        family_last_name = _individuals[v.husbandid].name.split('/')[1]
        for i in v.children:
            if _individuals[i].gender == 'M' and _individuals[i].name.split('/')[1] != family_last_name:
                print('ERROR: INDIVIDUAL: US16: ' + _individuals[i].indiid +
                    ': has last name: ' + _individuals[i].name.split('/')[1] +
                    ' diffrent than the family last name: ' + family_last_name)
    return True

def check_gender_role(_families, _individuals):
    for k, v in _families.items():
        if _individuals[v.husbandid].gender != 'M':
            print('ERROR: FAMILY: US21: ' + v.famid + ': Husband gender is not M.')
        if _individuals[v.wifeid].gender != 'F':
            print('ERROR: FAMILY: US21: ' + v.famid + ': Wife gender is not F.')
    return True

def is_date_before_current(_date_string):
    _date = datetime.strptime(_date_string, '%d %b %Y')
    return _date < datetime.now()

def calculate_dates_range(_from, _to):
    '''Takes two dates and return the reange between the two dates as int'''
    return (abs((_from - _to).days))/365

def check_corresponding_entries(_families, _individuals):
    for k, v in _individuals.items():
        if v.spouse != 'N/A':
            found_spouse = False
            for i, m in _families.items():
                if m.famid == v.spouse and (v.indiid == m.husbandid or v.indiid == m.wifeid):
                    found_spouse = True
                    break
            if not found_spouse:
                print('ERROR: INDIVIDUAL: US26: ' + v.indiid + ': Spouse has no corresponding entries in the family records.')
        if v.child != 'N/A':
            found_child = False
            for i, m in _families.items():
                if m.famid == v.child:
                    for c in m.children:
                        if c == v.indiid:
                            found_spouse = True
                            break
                        else:
                            continue
                        break
            if not found_child:
                print('ERROR: INDIVIDUAL: US26: ' + v.indiid + ': Child has no corresponding entries in the family records.')
    for k, v in _families.items():
        if v.husbandid not in _individuals:
            print('ERROR: FAMILY: US26: ' + v.famid + ': Husband ' + v.husbandid + ' has no corresponding entries for in the individuals records.')
        if v.wifeid not in _individuals:
            print('ERROR: FAMILY: US26: ' + v.famid + ': Wife ' + v. wifeid + ' has no corresponding entries for in the individuals records.')
        for c in v.children:
            if c not in _individuals:
                print('ERROR: FAMILY: US26: ' + v.famid + ': Child ' + v. wifeid + ' has no corresponding entries for in the individuals records.')

def check_duplicate(_individuals):
    x = 0
    indi_list = []

    for v in _individuals.itervalues():
        indi_list.append(v)

    while x < len(indi_list):
        y = x + 1
        while y < len(indi_list):
            if indi_list[x].name == indi_list[y].name and indi_list[x].birthday == indi_list[y].birthday :
                print('ERROR: INDIVIDUAL: US23: ' + indi_list[x].indiid +
                ' and ' + indi_list[y].indiid + ' has similar name and birth date')
            y = y + 1;
        x = x + 1;

def check_siblings_less_than_15(_families):
    for k, v in _families.items():
        if len(v.children) > 14:
            print('ERROR: FAMILY: US15: ' + v.famid + ': Has siblings more more than 14 [' + str(len(v.children)) + ' Siblings]')

def calculate_age(birthday):
        if birthday != 'N/A':
            _birthday = datetime.strptime(birthday, '%d %b %Y')
            today = datetime.today()
            return today.year - _birthday.year - ((today.month, today.day) < (_birthday.month, _birthday.day))
        else:
            return 'N/A'
