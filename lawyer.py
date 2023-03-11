
from enum import Enum
import requests
import base64


class Lawyer:
    _id = ''
    _type = None
    _name = None
    _gender = None
    _verification = None
    _address = None
    _description = ''
    _specializations = ()
    _phones = []
    _email = ''
    _status = None
    _avatar = None

    def __init__(
            self,
            lawyer_id='',
            lawyer_type=None,
            name=None,
            gender=None,
            verification=None,
            address=None,
            description='',
            specializations=(),
            phones=(),
            email='',
            status=None,
            avatar=None
    ):
        self._id = lawyer_id
        self._type = lawyer_type
        self._name = name
        if isinstance(gender, str):
            self._gender = LawyerGender.from_string(gender)
        else:
            self._gender = gender
        self._verification = verification
        self._address = address
        self._description = description
        self._specializations = list(specializations)
        self._unified_phones(phones)
        self._unified_email(email)
        self._status = status
        self._avatar = avatar

    def __str__(self):
        header_str = ' '.join([LawyerType.to_string(self.type), self.id])
        body_str = '\n'.join(
            ['\tПІБ: ' + str(self.name),
             '\tСтать: ' + str(LawyerGender.to_string(self.gender)),
             '\tСвідоцтво: ' + str(self.verification),
             '\tАдреса: ' + str(self.address),
             '\tОпис: ' + str(self.description),
             '\tСпеціалізації: ' + str(self.specializations),
             '\tТелефони: ' + str(self.phones),
             '\tПошта: ' + self.email,
             '\tСтатус: ' + ('N/A' if self.status is None else ('Працює' if self.status else 'Зупинено')),
             '\tФото: ' + ('+' if self.avatar else '-')]
        )
        res = '\n'.join([header_str, body_str])

        return res

    def __bool__(self):
        bool_arr = [
            self.type is None,
            self.name is None or not self.name,
            self.address is None or not self.address,
            not self.phones and not self.email
        ]

        if any(bool_arr):
            return False
        else:
            return True

    def __eq__(self, other):
        bool_arr = [
            # self.verification == other.verification,
            self.name == other.name,
            self.check_contacts(other)
        ]

        if any(bool_arr):
            return True
        else:
            return False

    def to_dict(self):
        data = dict()
        data['id'] = self.id
        data['type'] = LawyerType.to_string(self.type)
        data['first_name'] = self.name.first_name
        data['last_name'] = self.name.last_name
        data['middle_name'] = self.name.middle_name
        data['description'] = self.description
        data['email'] = self.email
        data['phones'] = self.phones
        data['address'] = self.address.to_dict() if self.address else None
        data['specializations'] = self.specializations
        data['avatar'] = self.avatar.to_dict() if self.avatar else None
        data['status'] = self.status

        return data

    def check_contacts(self, other):
        # check emails
        curr_email = self.email
        other_email = other.email
        if curr_email and other_email and curr_email == other_email:
            return True

        # check phones
        curr_phones = self.phones
        other_phones = other.phones

        check = False
        for phone in curr_phones:
            if phone in other_phones:
                check = True
                break

        return check

    def merge(self, other):
        lawyer_id = self.id
        if not lawyer_id:
            lawyer_id = other.id

        lawyer_type = self.type
        if lawyer_type == LawyerType.Lawyer:
            if other.type == LawyerType.Attorney or other.type == LawyerType.Notary:
                lawyer_type = other.type
        elif lawyer_type is None:
            lawyer_type = LawyerType.Lawyer

        new_first = self.name.first_name
        if not new_first:
            new_first = other.name.first_name
        new_last = self.name.last_name
        if not new_last:
            new_last = other.name.last_name
        new_middle = self.name.middle_name
        if not new_middle:
            new_middle = other.name.middle_name
        name = LawyerName(new_first, new_last, new_middle)

        gender = self.gender
        if other.gender == LawyerGender.Male or other.gender == LawyerGender.Female:
            gender = other.type
        if gender is None:
            gender = LawyerGender.Another

        ver_type = self.verification.certificate.type
        if not ver_type:
            ver_type = other.verification.certificate.type
        ver_num = self.verification.certificate.number
        if not ver_num:
            ver_num = other.verification.certificate.number
        ver_date = self.verification.certificate.date
        if not ver_date:
            ver_date = other.verification.certificate.date
        if ver_num:
            if self.type == LawyerType.Attorney or self.type == LawyerType.Notary:
                ver_type = VerificationType.License
        verification = LawyerVerification(ver_type, ver_num, ver_date)

        adr_country = self.address.country
        if not adr_country:
            adr_country = other.address.country
        adr_area = self.address.area
        if not adr_area:
            adr_area = other.address.area
        adr_region = self.address.region
        if not adr_region:
            adr_region = other.address.region
        adr_town = self.address.town
        if not adr_town:
            adr_town = other.address.town
        adr_street = self.address.street
        if not adr_street:
            adr_street = other.address.street
        adr_street_type = self.address.street_type
        if not adr_street_type:
            adr_street_type = other.address.street_type
        adr_street_number = self.address.street_number
        if not adr_street_number:
            adr_street_number = other.address.street_number
        adr_apartment_type = self.address.apartment_type
        if not adr_apartment_type:
            adr_apartment_type = other.address.apartment_type
        adr_apartment_number = self.address.apartment_number
        if not adr_apartment_number or adr_apartment_number == '0':
            if other.address.apartment_number == '0':
                adr_apartment_number = ''
            else:
                adr_apartment_number = other.address.apartment_number
        adr_postal_code = self.address.postal_code
        if not adr_postal_code:
            adr_postal_code = other.address.postal_code
        new_address = LawyerAddress(
            country=adr_country,
            area=adr_area,
            region=adr_region,
            town=adr_town,
            street=adr_street,
            street_type=adr_street_type,
            street_number=adr_street_number,
            apartment_type=adr_apartment_type,
            apartment_number=adr_apartment_number,
            postal_code=adr_postal_code
        )

        description = self.description.strip()
        if other.description:
            joiner = ''
            if description:
                joiner = '. '
                if description[-1] == '.':
                    joiner = ' '
            description = description + joiner + other.description.strip()

        specializations = []
        for spec in self.specializations:
            new_spec = spec.strip()
            if not new_spec:
                continue
            if new_spec in specializations:
                continue
            specializations.append(spec)
        for spec in other.specializations:
            new_spec = spec.strip()
            if not new_spec:
                continue
            if new_spec in specializations:
                continue
            specializations.append(spec)
        specializations = set(specializations)

        phones = []
        curr_phones = self.phones
        other_phones = other.phones
        for phone in curr_phones:
            if phone not in phones:
                phones.append(phone)
        for phone in other_phones:
            if phone not in phones:
                phones.append(phone)
        phones = set(phones)

        email = self.email
        if not email:
            email = other.email

        status = self.status
        if status is None:
            status = other.status

        avatar = self.avatar
        if not avatar:
            avatar = other.avatar

        new_lawyer = Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=name,
            gender=gender,
            verification=verification,
            address=new_address,
            description=description,
            specializations=specializations,
            phones=phones,
            email=email,
            status=status,
            avatar=avatar
        )

        return new_lawyer

    def update(self, attr, value):
        if not isinstance(attr, str):
            return False

        inner_attr = '_' + attr
        try:
            self.__setattr__(inner_attr, value)
        except KeyError as e:
            return False

        return True

    def _unified_phones(self, phones):
        curr_phones = []
        for phone in phones:
            if phone is None or not phone:
                continue

            new_phone = phone.replace('-', '')
            new_phone = new_phone.replace('+', '')
            new_phone = new_phone.replace('(', '')
            new_phone = new_phone.replace(')', '')
            new_phone = new_phone.replace(' ', '')
            if new_phone.find('38') == 0:
                new_phone = new_phone[2:len(new_phone)]
            if new_phone.find('8') == 0:
                new_phone = new_phone[1:len(new_phone)]
            if new_phone.find('0') == 0:
                new_phone = new_phone[1:len(new_phone)]

            if new_phone:
                curr_phones.append(new_phone)

        self._phones = curr_phones

    def _unified_email(self, email):
        new_email = email.replace(' ', '')
        new_email = new_email.replace(',', '')
        new_email = new_email.replace(':', '')
        new_email = new_email.replace(';', '')
        new_email = new_email.replace('#', '')
        new_email = new_email.replace('%', '')
        new_email = new_email.replace('?', '')
        new_email = new_email.replace('^', '')
        new_email = new_email.replace('(', '')
        new_email = new_email.replace(')', '')

        self._email = new_email

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def gender(self):
        return self._gender

    @property
    def verification(self):
        return self._verification

    @property
    def address(self):
        return self._address

    @property
    def description(self):
        return self._description

    @property
    def specializations(self):
        return self._specializations

    @property
    def phones(self):
        return self._phones

    @property
    def email(self):
        return self._email

    @property
    def status(self):
        curr_status = self._status
        # if self.type == LawyerType.Lawyer:
        #     curr_status = None

        return curr_status

    @property
    def avatar(self):
        return self._avatar


class LawyerType(Enum):
    """Possible lawyer types"""

    Lawyer = 1
    Attorney = 2
    Notary = 3

    @classmethod
    def to_string(cls, val):
        if val == cls.Lawyer:
            # return 'Юрист'
            return 1
        elif val == cls.Attorney:
            # return 'Адвокат'
            return 2
        elif val == cls.Notary:
            # return 'Нотаріус'
            return 4
        else:
            # return ''
            return 0

    @classmethod
    def from_string(cls, val):
        # if val == 'Юрист':
        if val == 1:
            return cls.Lawyer
        # elif val == 'Адвокат':
        elif val == 2:
            return cls.Attorney
        # elif val == 'Нотаріус':
        elif val == 4:
            return cls.Notary
        else:
            return None


class LawyerGender(Enum):
    """Possible gender types"""

    Male = 1
    Female = 2
    Another = 3

    @classmethod
    def to_string(cls, val):
        if val == cls.Male:
            return 'чоловік'
        elif val == cls.Female:
            return 'жінка'
        elif val == cls.Another:
            return 'N/A'
        else:
            return ''

    @classmethod
    def from_string(cls, val):
        if val == 'чоловік':
            return LawyerGender.Male
        elif val == 'жінка':
            return LawyerGender.Female
        else:
            return LawyerGender.Another


class LawyerName:
    _first_name = ''
    _last_name = ''
    _middle_name = ''

    def __init__(self, first_name, last_name, middle_name=''):
        self._first_name = first_name
        self._last_name = last_name
        self._middle_name = middle_name

    def __str__(self):
        arr_name = [self.last_name, self.first_name]
        if self.middle_name:
            arr_name.append(self.middle_name)

        res = ' '.join(arr_name)

        return res

    def __bool__(self):
        bool_arr = [
            not self.first_name,
            not self.last_name,
            not self.middle_name
        ]

        if all(bool_arr):
            return False
        else:
            return True

    def __eq__(self, other):
        curr_first_name = self.first_name.lower().strip()
        curr_last_name = self.last_name.lower().strip()
        curr_middle_name = self.middle_name.lower().strip()

        other_first_name = other.first_name.lower().strip()
        other_last_name = other.last_name.lower().strip()
        other_middle_name = other.middle_name.lower().strip()

        check_curr_last = [
            curr_last_name and other_first_name and curr_last_name == other_first_name,
            curr_last_name and other_last_name and curr_last_name == other_last_name,
            curr_last_name and other_middle_name and curr_last_name == other_middle_name
        ]

        check_other_last = [
            other_last_name and curr_first_name and other_last_name == curr_first_name,
            other_last_name and curr_last_name and other_last_name == curr_last_name,
            other_last_name and curr_middle_name and other_last_name == curr_middle_name
        ]

        check_last = [
            any(check_curr_last),
            any(check_other_last)
        ]

        check_curr_first = [
            curr_first_name and other_first_name and curr_first_name == other_first_name,
            curr_first_name and other_middle_name and curr_first_name == other_middle_name
        ]

        check_other_first = [
            other_first_name and curr_first_name and other_first_name == curr_first_name,
            other_first_name and curr_middle_name and other_first_name == curr_middle_name
        ]

        check_first = [
            any(check_curr_first),
            any(check_other_first)
        ]

        bool_arr = [
            any(check_last),
            any(check_first)
        ]

        return all(bool_arr)

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def middle_name(self):
        return self._middle_name

    def full_name(self):
        return str(self)

    def short_name(self):
        arr_name = [self.first_name, self.last_name[0] + '.']
        if self.middle_name:
            arr_name.append(self.middle_name[0] + '.')

        res = ' '.join(arr_name)

        return res


class LawyerAddress:
    _country = ''
    _area = ''
    _region = ''
    _town = ''
    _street = ''
    _street_type = ''
    _street_number = ''
    _apartment_type = ''
    _apartment_number = ''
    _postal_code = ''
    _full_street = ''

    def __init__(
            self,
            country,
            area,
            region,
            town,
            street,
            street_type,
            street_number,
            apartment_type='',
            apartment_number='',
            postal_code=''
    ):
        self._country = country
        self._area = area
        self._region = region
        self._town = town
        self._full_street = street

        street_type_parse, street_name_parse, street_number_parse = self._parse_street(street)

        self._street = street_name_parse

        if street_type:
            self._street_type = street_type
        else:
            self._street_type = street_type_parse

        if street_number:
            self._street_number = street_number
        else:
            self._street_number = street_number_parse

        self._apartment_type = apartment_type
        self._apartment_number = apartment_number
        self._postal_code = postal_code

    def __str__(self):
        address_arr = []
        if self.postal_code:
            address_arr.append(self.postal_code)

        if self.country:
            address_arr.append(self.country)

        if self.area:
            address_arr.append(self.area + ' обл.')

        if self.region:
            address_arr.append(self.region + ' р-н')

        if self.town:
            address_arr.append('м. ' + self.town)

        if self.street:
            street_type = 'вул.'
            if self.street_type:
                street_type = self.street_type
            address_arr.append(street_type + ' ' + self.street)

            if self.street_number:
                address_arr.append(self.street_number)

        if self.apartment_number and self.apartment_number != '0':
            apartment_type = 'кв.'
            if self.apartment_type:
                apartment_type = self.apartment_type
            address_arr.append(apartment_type + ' ' + self.apartment_number)

        address = ', '.join(address_arr)

        return address

    def __bool__(self):
        bool_arr = [
            not self.area,
            not self.region,
            not self.town,
            not self.street
        ]

        if all(bool_arr):
            return False
        else:
            return True

    def to_dict(self):
        data = dict()
        # data['country'] = self.country
        data['area'] = self.area
        data['region'] = self.region
        data['town'] = self.town
        data['street'] = self.street
        data['street_type'] = self.street_type
        data['street_number'] = self.street_number
        data['full_street'] = self.full_street
        # data['apartment_type'] = self.apartment_type
        # data['apartment_number'] = self.apartment_number
        # data['postal_code'] = self.postal_code

        return data

    @property
    def country(self):
        return self._country

    @property
    def area(self):
        return self._area

    @property
    def region(self):
        return self._region

    @property
    def town(self):
        return self._town

    @property
    def street(self):
        return self._street

    @property
    def street_type(self):
        return self._street_type

    @property
    def street_number(self):
        return self._street_number

    @property
    def apartment_type(self):
        return self._apartment_type

    @property
    def apartment_number(self):
        return self._apartment_number

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def full_street(self):
        return self._full_street

    def full_address(self):
        return str(self)

    @staticmethod
    def _parse_street(street):
        street_type = ''
        street_name = ''
        street_number = ''

        if 'площа' in street:
            street_type = 'пл.'
            street_name = street.replace('площа', '')
            street_name = ' '.join(street_name.split())
        elif 'вулиця' in street:
            street_type = 'вул.'
            street_name = street.replace('вулиця', '')
            street_name = ' '.join(street_name.split())
        elif 'провулок' in street:
            street_type = 'пров.'
            street_name = street.replace('провулок', '')
            street_name = ' '.join(street_name.split())
        elif 'проспект' in street:
            street_type = 'п-т.'
            street_name = street.replace('проспект', '')
            street_name = ' '.join(street_name.split())
        elif 'мікро район' in street:
            street_type = 'мк.р-н'
            street_name = street.replace('мікро район', '')
            street_name = ' '.join(street_name.split())
        elif 'набережна' in street:
            street_type = 'наб.'
            street_name = street.replace('набережна', '')
            street_name = ' '.join(street_name.split())
        elif 'Майдан' in street:
            street_type = 'Майдан'
            street_name = street.replace('Майдан', '')
            street_name = ' '.join(street_name.split())
        elif 'узвіз' in street:
            street_type = 'уз.'
            street_name = street.replace('узвіз', '')
            street_name = ' '.join(street_name.split())
        elif 'шосе' in street:
            street_type = 'шосе'
            street_name = street.replace('шосе', '')
            street_name = ' '.join(street_name.split())
        elif 'бульвар' in street:
            street_type = 'б-р.'
            street_name = street.replace('бульвар', '')
            street_name = ' '.join(street_name.split())
        elif 'Проїзд' in street:
            street_type = 'Проїзд'
            street_name = street.replace('Проїзд', '')
            street_name = ' '.join(street_name.split())
        elif street:
            street_type = 'вул.'
            street_name = street.strip()

        arr = street_name.split(',')
        if arr:
            street_name = arr[0]
            if len(arr) > 1:
                street_number = arr[1]
                street_number = street_number.replace(' ', '')

        return street_type, street_name, street_number


class VerificationType(Enum):
    """Possible verification types"""

    Diploma = 1
    License = 2
    EDRPOU = 3

    @classmethod
    def from_string(cls, val):
        if val == 'Диплом':
            return cls.Diploma
        elif val == 'Ліцензія':
            return cls.License
        elif val == 'ЄРДПОУ':
            return cls.EDRPOU
        else:
            return None


class LawyerVerification:
    _gov_url = ''
    _certificate = None

    def __init__(self, cert_type, cert_number, cert_date, gov_url=''):
        self._url = gov_url
        self._certificate = LawyerCertificate(cert_type, cert_number, cert_date)

    def __str__(self):
        res = str(self.certificate)
        if self.gov_url:
            res = res + ' (' + self.gov_url + ')'

        return res

    def __bool__(self):
        if self.certificate:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.certificate == other.certificate

    @property
    def certificate(self):
        return self._certificate

    @property
    def gov_url(self):
        return self._gov_url


class LawyerCertificate:
    _type = None
    _number = ''
    _date = None

    def __init__(self, cert_type, cert_number, cert_date):
        self._type = cert_type
        self._number = cert_number
        self._date = cert_date

    def __str__(self):
        res = ''
        if self.number:
            res = self.number

        if self.date is not None:
            res = res + ', ' + str(self.date)

        return res

    def __bool__(self):
        if self.type == VerificationType.Diploma and self.number:
            return True
        else:
            return False

    def __eq__(self, other):
        if not self.number or not other.number:
            return False

        bool_arr = [
            self.number == other.number,
            self.type == other.type
        ]

        return all(bool_arr)

    @property
    def type(self):
        return self._type

    @property
    def number(self):
        return self._number

    @property
    def date(self):
        return self._date


class LawyerAvatar:
    _data = ''
    _name = ''
    _extension = ''

    def __init__(self, url='', data='', name='', extension=''):
        if url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
            b64_data = base64.b64encode(requests.get(url, headers=headers).content)
            str_data = str(b64_data).replace('b\'', '')
            self._data = str_data
            self._name, self._extension = self._parse_url(url)
        else:
            self._data = data
            self._name = name
            self._extension = extension

    def __bool__(self):
        if self.data:
            return True
        else:
            return False

    @property
    def data(self):
        curr_data = self._data
        if curr_data and curr_data[-1] == '\'':
            curr_data = curr_data[:-1]

        return curr_data

    @property
    def name(self):
        return self._name

    @property
    def extension(self):
        return self._extension

    def to_dict(self):
        dict_ava = {
            'base64': self.data,
            'name': self.name,
            'extension': self.extension
        }

        return dict_ava

    @staticmethod
    def _parse_url(url):
        name = ''
        ext = ''

        img_arr = url.split('/')
        if img_arr:
            img_file = img_arr[-1]
            sep_name = img_file.split('.')
            if len(sep_name) > 1:
                name = sep_name[0]
                ext = sep_name[1]

        return name, ext
