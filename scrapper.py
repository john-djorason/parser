
import parser.lawyer as lawly_lawyer

from enum import Enum
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import requests
import json
import datetime
import html


class LawlyParserType(Enum):
    """Possible connection types"""

    API = 1
    Scrapper = 2
    JSON = 3


class LawlyScrapperSource(Enum):
    """Active sources"""

    FreeLawyer_Input = 1
    FreeLawyer_Output = 2
    ERAU_Input = 3
    ERAU_Output = 4
    ERN_Input = 5
    ERN_Output = 6
    Atty_Input = 7
    Atty_Output = 8
    LawyerUA_Input = 9
    LawyerUA_Output = 10
    Protocol_Input = 11
    Protocol_Output = 12
    NotaryKiev_Input = 13
    NotaryKiev_Output = 14
    NotaryUA_Input = 15
    NotaryUA_Output = 16
    Jurliga_Input = 17
    Jurliga_Output = 18
    ValidLawyers = 19
    ERAU_Site = 20
    NotaryKievUA_Input = 21
    NotaryKievUA_Output = 22
    Notary2gis_Input = 23
    Notary2gis_Output = 24
    Leegl_Input = 25
    Leegl_Output = 26
    Czech_Input = 27
    Czech_Output = 28
    Poland_Input = 29
    Poland_Output = 30

    @classmethod
    def to_string(cls, val):
        if val == cls.FreeLawyer_Input:
            return 'https://www.freelawyer.ua'
        elif val == cls.FreeLawyer_Output:
            return 'db'
        elif val == cls.ERAU_Input:
            return 'https://api.conp.com.ua/api/v1.0/attorney'
        elif val == cls.ERAU_Output:
            return 'db'
        else:
            return ''

    @classmethod
    def lawyer_list_cat(cls, val):
        if val == cls.FreeLawyer_Input:
            return 'freelawyers'
        elif val == cls.FreeLawyer_Output:
            return 'output_data'
        elif val == cls.ERAU_Input:
            return 'search'
        elif val == cls.ERAU_Output:
            return 'output_data'
        elif val == cls.ERN_Input:
            return 'search'
        elif val == cls.ERN_Output:
            return 'output_data'
        elif val == cls.Atty_Input:
            return 'list'
        elif val == cls.Atty_Output:
            return 'output_data'
        elif val == cls.LawyerUA_Input:
            return 'search'
        elif val == cls.LawyerUA_Output:
            return 'output_data'
        elif val == cls.Protocol_Input:
            return 'yuridicheskiy_katalog'
        elif val == cls.Protocol_Output:
            return 'output_data'
        elif val == cls.NotaryKiev_Input:
            return 'reestr-notariusov-kieva'
        elif val == cls.NotaryKiev_Output:
            return 'output_data'
        elif val == cls.NotaryKievUA_Input:
            return 'spisok'
        elif val == cls.NotaryKievUA_Output:
            return 'output_data'
        elif val == cls.Notary2gis_Input:
            return 'kyiv/search/%D0%9D%D0%BE%D1%82%D0%B0%D1%80%D0%B8%D1%83%D1%81%D1%8B%20%2F%20%D0%9D%D0%BE%D1%82%D0%B0%D1%80%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%BE%D0%BD%D1%82%D0%BE%D1%80%D1%8B/rubricId/343'
        elif val == cls.Notary2gis_Output:
            return 'output_data'
        elif val == cls.NotaryUA_Input:
            return '?list'
        elif val == cls.NotaryUA_Output:
            return 'output_data'
        elif val == cls.Jurliga_Input:
            # return 'perelik-spetsialistiv'
            return 'perel%D1%96k-spets%D1%96al%D1%96st%D1%96v'
        elif val == cls.Jurliga_Output:
            return 'output_data'
        elif val == cls.Leegl_Input:
            return 'lawyers'
        elif val == cls.Leegl_Output:
            return 'output_data'
        elif val == cls.ValidLawyers:
            return 'lawyers_db'
        elif val == cls.ERAU_Site:
            return ''
        elif val == cls.Czech_Input:
            return 'Home/SearchResult?pageSize=50&page='
        elif val == cls.Czech_Output:
            return 'output_data'
        elif val == cls.Poland_Input:
            return 'list/strona/'
        elif val == cls.Poland_Output:
            return 'output_data'
        else:
            return r'output_data\europe\poland'

    @classmethod
    def lawyer_profile_cat(cls, val):
        if val == cls.FreeLawyer_Input:
            return 'user'
        elif val == cls.FreeLawyer_Output:
            return 'freelawyer.json'
        elif val == cls.ERAU_Input:
            return ''
        elif val == cls.ERAU_Output:
            return 'attorneys.json'
        elif val == cls.ERN_Input:
            return ''
        elif val == cls.ERN_Output:
            return 'notaries.json'
        elif val == cls.Atty_Input:
            return 'i'
        elif val == cls.Atty_Output:
            return 'atty.json'
        elif val == cls.LawyerUA_Input:
            return '?ID='
        elif val == cls.LawyerUA_Output:
            return 'lawyerua.json'
        elif val == cls.Protocol_Input:
            return 'cabinet'
        elif val == cls.Protocol_Output:
            return 'protocol.json'
        elif val == cls.NotaryKiev_Input:
            return ''
        elif val == cls.NotaryKiev_Output:
            return 'notarykeiv.json'
        elif val == cls.NotaryKievUA_Input:
            return 'notarius'
        elif val == cls.NotaryKievUA_Output:
            return 'notarykeivua.json'
        elif val == cls.Notary2gis_Input:
            return 'firm'
        elif val == cls.Notary2gis_Output:
            return 'notary2gis.json'
        elif val == cls.NotaryUA_Input:
            return ''
        elif val == cls.NotaryUA_Output:
            return 'notaryua.json'
        elif val == cls.Jurliga_Input:
            return ''
        elif val == cls.Jurliga_Output:
            return 'jurliga.json'
        elif val == cls.Leegl_Input:
            return ''
        elif val == cls.Leegl_Output:
            return 'leegl.json'
        elif val == cls.ValidLawyers:
            return 'lawyers_db.json'
        elif val == cls.ERAU_Site:
            return 'profile'
        elif val == cls.Czech_Input:
            return 'Contact/Details'
        elif val == cls.Czech_Output:
            return 'czech.json'
        elif val == cls.Poland_Input:
            return ''
        elif val == cls.Poland_Output:
            return 'poland.json'
        else:
            return ''


class LawlyParser:
    _connection = None
    _type = None
    _input_source = None
    _output_source = None

    def __init__(self, parser_type, input_source=None, output_source=None):
        self._type = parser_type
        self._input_source = input_source
        self._output_source = output_source

    def _connect(self, url):
        """Connects to an external source"""

    def _get_data(self, url):
        """Returns lawyer's json data"""

        return None

    def _get_lawyer(self, lawyer_type, lawyer_id='') -> lawly_lawyer.Lawyer:
        """Returns Lawyer class object"""

        return lawly_lawyer.Lawyer()

    def _convert_lawyer(self, json_data):
        """Converts lawyer's json data into Lawyer class object"""

        return None

    def get_lawyers(self, lawyer_type):
        """Returns Lawyers"""

        return []

    def save_json(self, lawyers, postfix=''):
        dir_name = LawlyScrapperSource.to_string(self._output_source)
        cat_name = LawlyScrapperSource.lawyer_list_cat(self._output_source)
        file_name = LawlyScrapperSource.lawyer_profile_cat(self._output_source)
        if postfix:
            file_name = file_name.replace('.json', '_'.join(['', postfix, '.json']))
        path = '\\'.join([dir_name, cat_name, file_name])

        lawyer_items = []
        for lawyer in lawyers:
            lawyer_dict = lawyer.to_dict()
            lawyer_items.append(lawyer_dict)

        output_data = dict()
        output_data['lawyers'] = lawyer_items
        with open(path, 'w', encoding='utf-8') as outfile:
            json.dump(output_data, outfile, indent=4, ensure_ascii=False)

    @property
    def type(self):
        return self._type

    @staticmethod
    def get_json_key(json_data, key):
        if not isinstance(key, str):
            return ''

        if json_data is None or key is None:
            return ''

        try:
            result = json_data[key]
        except KeyError as e:
            result = ''
        except TypeError as e:
            result = ''

        return result


class LawlyAPI(LawlyParser):
    _token = ''

    def __init__(self):
        super().__init__(LawlyParserType.API)
        self._set_token()

    def _set_token(self):
        if self._token:
            curr_token = self._token.replace(' ', '')

            host = 'https://api.conp.com.ua/api/v1.0/user/token'
            headers = {'Authorization': curr_token}
            try:
                response = requests.get(host, headers=headers)
            except requests.exceptions.InvalidHeader as e:
                self._token = ''
                self._set_token()
                return

            token = response.text
            if token == '{}':
                token = self._token
        else:
            host = 'https://api.conp.com.ua/api/v1.0/user/login'
            data = {'email': 'djoras@ukr.net', 'password': 'lookatmem8s'}
            response = requests.post(host, data=data)
            token = response.text

        token = token.replace('"', '')
        token = token.replace(' ', '')
        self._token = token

    def _connect(self, url):
        self._connection = None
        headers = {'Authorization': self.token}

        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            return

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return

        self._connection = response

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        data_str = self._connection.text
        data = json.loads(data_str)

        return data

    @property
    def token(self):
        self._set_token()

        return self._token


class LawlyAPIERAU(LawlyAPI):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.ERAU_Input
        self._output_source = LawlyScrapperSource.ERAU_Output

    def _get_lawyer(self, lawyer_type, lawyer_id=''):
        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = 'https://api.conp.com.ua/api/v1.0/attorney/{}'.format(lawyer_id)
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return None

        lawyer_data = self._get_data(url)
        lawyer = self._convert_lawyer(lawyer_data)

        return lawyer

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])
        if not url:
            return lawyers

        all_attorneys = []
        holders = self._get_holders()
        for holder in holders:
            holder_arr = [holder]
            attorneys = self._get_attorneys_by_holders(url, holder_arr)
            if attorneys:
                # self.save_json(attorneys, holder)
                for attorney in attorneys:
                    all_attorneys.append(attorney)

        self.save_json(all_attorneys)

        return lawyers

    def _get_holders(self):
        # holders = [
        #     'Рада адвокатів Автономної Республіки Крим',
        #     'Рада адвокатів Вінницької області',
        #     'Рада адвокатів Волинської області',
        #     'Рада адвокатів Дніпропетровської області',
        #     'Рада адвокатів Донецької області',
        #     'Рада адвокатів Житомирської області',
        #     'Рада адвокатів Закарпатської області',
        #     'Рада адвокатів Запорізької області',
        #     'Рада адвокатів Івано-Франківської області',
        #     'Рада адвокатів Кіровоградської області',
        #     'Рада адвокатів Луганської області',
        #     'Рада адвокатів Львівської області',
        #     'Рада адвокатів Миколаївської області',
        #     'Рада адвокатів Одеської області',
        #     'Рада адвокатів Полтавської області',
        #     'Рада адвокатів Рівненської області',
        #     'Рада адвокатів Сумської області',
        #     'Рада адвокатів Тернопільської області',
        #     'Рада адвокатів Харківської області',
        #     'Рада адвокатів Херсонської області',
        #     'Рада адвокатів Хмельницької області',
        #     'Рада адвокатів Київської області',
        #     'Рада адвокатів Черкаської області',
        #     'Рада адвокатів Чернівецької області',
        #     'Рада адвокатів Чернігівської області',
        #     'Рада адвокатів міста Києва',
        #     'Рада адвокатів міста Севастополя'
        # ]

        holders = []

        main_cat = LawlyScrapperSource.to_string(self._output_source)
        input_cat = 'input_data'
        holders_file = 'holders.txt'
        full_path = '\\'.join([main_cat, input_cat, holders_file])
        with open(full_path, 'r') as f:
            for line in f.readlines():
                holder = line.replace(',', '')
                holder = holder.replace('"', '')
                holder = holder.replace('\n', '')
                if holder:
                    holders.append(holder)

        return holders

    def _get_attorneys_by_holders(self, url, holders, offset=0):
        lawyers = []

        res = self._get_attorneys_json_data(url, holders, offset)
        lawyers_total = LawlyParser.get_json_key(res, 'total')
        lawyers_count = int(lawyers_total if lawyers_total else 0)
        if not lawyers_count:
            return lawyers

        page_count = lawyers_count // 10
        for page in range(page_count):
            print('processing page: ', str(page + 1), '/', str(page_count))

            data = self._get_attorneys_json_data(url, holders, page)
            lawyers_items = LawlyParser.get_json_key(data, 'items')
            if not lawyers_items:
                continue

            for item in lawyers_items:
                lawyer_id = LawlyParser.get_json_key(item, 'id')
                if not lawyer_id:
                    continue

                lawyer = self._get_lawyer(lawly_lawyer.LawyerType.Attorney, lawyer_id)
                if lawyer is not None:
                    lawyer.update('description', holders[0])
                    lawyers.append(lawyer)

        return lawyers

    def _get_attorneys_json_data(self, url, holders, offset=0):
        headers = {'Authorization': self.token}
        data = {
            'query': '',
            'defaultOperator': 'or',
            'filter': {
                'accountHolder': {
                    'list': holders,
                    'operator': 'or'
                }
            },
            'sort': {},
            'searchIndex': 'attorney',
            'from': offset,
            'aggregation': False
        }

        try:
            response = requests.post(url=url, json=data, headers=headers)
            res = response.json()
        except requests.exceptions.InvalidHeader as e:
            res = ''

        return res

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Attorney
        id_str = LawlyParser.get_json_key(json_data, 'id')
        lawyer_id = int((id_str if id_str else 0))

        person = LawlyParser.get_json_key(json_data, 'person')
        first_name = LawlyParser.get_json_key(person, 'givenName')
        last_name = LawlyParser.get_json_key(person, 'familyName')
        middle_name = LawlyParser.get_json_key(person, 'additionalName')
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = LawlyParser.get_json_key(person, 'sex')

        gov_url = 'https://erau.unba.org.ua/profile/' + str(lawyer_id)
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificateNumber')
        cert_date = LawlyParser.get_json_key(json_data, 'certificateDate')
        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        workplace = LawlyParser.get_json_key(json_data, 'workplace')
        country = LawlyParser.get_json_key(workplace, 'countryName')
        area = LawlyParser.get_json_key(workplace, 'region')
        # area = area.replace(' область', '')
        region = LawlyParser.get_json_key(workplace, 'district')
        # region = region.replace(' район', '')
        town = LawlyParser.get_json_key(workplace, 'locality')
        # town = town.replace('місто ', '')
        street = LawlyParser.get_json_key(workplace, 'streetAddress')
        street_type = ''
        street_number = LawlyParser.get_json_key(workplace, 'streetNumber')
        apartment_type = ''
        apartment_number = 0
        postal_code = LawlyParser.get_json_key(workplace, 'postalCode')
        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set()
        phones = set(LawlyParser.get_json_key(json_data, 'phone'))

        email_arr = LawlyParser.get_json_key(json_data, 'email')
        email = ''
        if email_arr:
            email = email_arr[0]

        status = None
        avatar = None

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyAPIERN(LawlyAPI):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.ERN_Input
        self._output_source = LawlyScrapperSource.ERN_Output

    def _get_lawyer(self, lawyer_type, lawyer_id=''):
        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = 'https://api.conp.com.ua/api/v1.0/notary/{}'.format(lawyer_id)

        if not url:
            return None

        lawyer_data = self._get_data(url)
        lawyer = self._convert_lawyer(lawyer_data)

        return lawyer

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])
        if not url:
            return lawyers

        res = self._get_notaries_json_data(url)
        lawyers_total = LawlyParser.get_json_key(res, 'total')
        lawyers_count = int(lawyers_total if lawyers_total else 0)
        if not lawyers_count:
            return lawyers

        page_count = lawyers_count // 10
        for page in range(page_count):
            print('processing page: ', str(page + 1), ' / ', str(page_count))

            data = self._get_notaries_json_data(url, page)
            lawyers_items = LawlyParser.get_json_key(data, 'items')
            if not lawyers_items:
                continue

            for item in lawyers_items:
                lawyer_id = LawlyParser.get_json_key(item, 'certificateNumber')
                if not lawyer_id:
                    continue

                lawyer = self._get_lawyer(lawly_lawyer.LawyerType.Notary, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

        return lawyers

    def _get_notaries_json_data(self, url, offset=0):
        headers = {'Authorization': self.token}
        data = {
            'query': '',
            'defaultOperator': 'or',
            'filter': {},
            'sort': {},
            'searchIndex': 'attorney',
            'from': offset,
            'aggregation': False
        }

        response = requests.post(url=url, json=data, headers=headers)
        res = response.json()

        return res

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Notary
        lawyer_id = LawlyParser.get_json_key(json_data, 'certificateNumber')
        person = LawlyParser.get_json_key(json_data, 'person')
        first_name = LawlyParser.get_json_key(person, 'givenName')
        last_name = LawlyParser.get_json_key(person, 'familyName')
        middle_name = LawlyParser.get_json_key(person, 'additionalName')
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = LawlyParser.get_json_key(person, 'sex')

        gov_url = 'https://ern.minjust.gov.ua/' + str(lawyer_id)
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificateNumber')
        cert_date = None
        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        address = LawlyParser.get_json_key(json_data, 'address')
        country = LawlyParser.get_json_key(address, 'countryName')
        area = LawlyParser.get_json_key(address, 'region')
        # area = area.replace(' область', '')
        region = LawlyParser.get_json_key(address, 'district')
        # region = region.replace(' район', '')
        town = LawlyParser.get_json_key(address, 'locality')
        # town = town.replace('місто ', '')
        street = LawlyParser.get_json_key(address, 'streetAddress')
        street_type = ''
        street_number = LawlyParser.get_json_key(address, 'streetNumber')
        apartment_type = ''
        apartment_number = 0
        postal_code = LawlyParser.get_json_key(address, 'postalCode')
        new_address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set([])

        phones_arr = []
        full_address = LawlyParser.get_json_key(address, 'source')
        parts = full_address.split(',')
        if parts:
            phone = parts[-1]
            phones_arr.append(phone)
        phones = set(phones_arr)
        email = ''
        status = None
        avatar = None

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=new_address,
            description=description,
            specializations=specializations,
            phones=phones,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapper(LawlyParser):
    def __init__(self):
        super().__init__(LawlyParserType.Scrapper)

    def _connect(self, url):
        self._connection = None

        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
            request = Request(url, headers=headers)
            html = urlopen(request)
        except HTTPError as e:
            return

        if html is None:
            return

        self._connection = html
        self._soup_wrapper()

    def _soup_wrapper(self):
        connection = self._connection

        try:
            soup = BeautifulSoup(connection.read(), features='html.parser')
            title = soup.body.h1
        except AttributeError as e:
            soup = None

        self._connection = soup

    def _get_lawyer(self, lawyer_type, lawyer_id=''):
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            if lawyer_id.find('http') >= 0:
                url = lawyer_id
            else:
                url = LawlyScrapperSource.to_string(self._input_source)
                user_cat = LawlyScrapperSource.lawyer_profile_cat(self._input_source)
                url = '/'.join([url, user_cat, lawyer_id])
        else:
            return None

        if not url:
            return None

        lawyer_data = self._get_data(url)
        if lawyer_data is None:
            return None

        lawyer = self._convert_lawyer(lawyer_data)

        return lawyer

    def _get_page_count(self):
        """Returns count of lawyer list pages in the site"""

        return 0


class LawlyScrapperFreeLawyer(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.FreeLawyer_Input
        self._output_source = LawlyScrapperSource.FreeLawyer_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = ''
        for person in self._connection.find_all('div', {'class': 'fl-wrapper'}):
            script = person.script
            if script is None:
                continue

            script_text = script.contents
            script_text = script_text[0]
            script_text = script_text.replace('\r', '')
            script_text = script_text.replace('\t', '')
            script_text = script_text.replace('\n', '')
            try:
                json_data = json.loads(script_text)
            except json.decoder.JSONDecodeError as e:
                json_data = ''

        if json_data == '':
            return None

        specs = []
        for spec_list in self._connection.find_all('ul', {'class': 'lawyer-areas'}):
            for spec in spec_list.find_all('li'):
                spec_name = spec.a.text
                if spec_name:
                    specs.append(spec_name)

        json_data['specializations'] = specs

        education = ''
        for edu_element in self._connection.find_all('br', {'class': ['d-none', 'd-sm-block']}):
            edu_text = edu_element.next_element.replace('\n', '').strip()
            if edu_text:
                education = edu_text
                break

        json_data['education'] = education

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        page_count = self._get_page_count()
        for page_num in range(1, page_count + 1):
            print('processing page #', str(page_num))

            if page_num == 1:
                new_url = url
            else:
                new_url = '/'.join([url, str(page_num)])

            self._connect(new_url)
            if self._connection is None:
                continue

            lawyer_ids = []
            for person in self._connection.find_all('div', {'itemtype': 'https://schema.org/Person'}):
                lawyer_link = person.find('div', {'class': ['fl-lawyer__pic', 'js-lawyer-quick-preview']}).a
                lawyer_url = lawyer_link['href']
                lawyer_id = lawyer_url.replace('/user/', '')
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

            for lawyer_id in lawyer_ids:
                lawyer = self._get_lawyer(lawyer_type, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

        return lawyers

    def _get_page_count(self):
        count = 0

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])

        self._connect(url)
        if self._connection is None:
            return count

        max_count = 0
        for max_lawyers in self._connection.find_all('div', {'class': 'fl-paginations__count-page'}):
            max_str = max_lawyers.text
            max_str = max_str.replace('1-20', '')
            max_str = max_str.replace('юристов из', '')
            max_str = max_str.strip()
            try:
                max_count = int(max_str)
            except TypeError as e:
                max_count = 0
            break
        count = max_count // 20
        tail = max_count - count * 20
        count = count + 1 if tail else 0

        return count

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        if LawlyParser.get_json_key(json_data, 'jobTitle') == 'Адвокат':
            lawyer_type = lawly_lawyer.LawyerType.Attorney

        url = LawlyParser.get_json_key(json_data, 'url')
        lawyer_id = url.replace('https://www.freelawyer.ua/user/', '')

        full_name = json_data['name']
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[0]
            last_name = name_arr[2]
            middle_name = name_arr[1]
        else:
            first_name = name_arr[0]
            last_name = name_arr[1]
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = url
        cert_type = lawly_lawyer.VerificationType.Diploma
        cert_number = LawlyParser.get_json_key(json_data, 'education')
        cert_date = None
        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        address = LawlyParser.get_json_key(json_data, 'address')
        country = LawlyParser.get_json_key(address, 'addressCountry')
        area = ''
        region = ''
        town = LawlyParser.get_json_key(address, 'addressLocality')
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''
        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = LawlyParser.get_json_key(json_data, 'description')
        specializations = set(LawlyParser.get_json_key(json_data, 'specializations'))

        phones = set([])
        email = ''
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/images/xuser_male.png.pagespeed.ic.rHI-9n-lSV.webp') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperAtty(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Atty_Input
        self._output_source = LawlyScrapperSource.Atty_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}
        id_str = url.replace('http://atty.com.ua/i/', '')
        if id_str:
            json_data['id'] = id_str

        for card in self._connection.find_all('section', {'class': 'show_vizitka'}):
            for photo in card.find_all('div', {'class': 'photo'}):
                link = photo.div.a
                if link is None:
                    break

                link_url = link['href']
                if link_url:
                    link_url = 'http://atty.com.ua' + link_url
                json_data['image'] = link_url
                break

            for main_block in card.find_all('div', {'class': 'main_container'}):
                for info in main_block.find_all('div', {'class': 'main_info'}):
                    for title in info.find_all('div', {'class': 'fsize4'}):
                        job_title = title.next
                        json_data['job_title'] = job_title.strip()
                        break

                    for name in info.find_all('div', {'class': 'fsize7'}):
                        name_str = name.text
                        json_data['name'] = name_str.strip()
                        break

                    for cert in info.find_all('div', {'class': 'fcolor4'}):
                        cert_str = cert.text
                        json_data['certificate'] = cert_str.strip()
                        break
                    break

                for contacts in main_block.find_all('div', {'class': 'contacts'}):
                    for contact in contacts.find_all('div', {'class': 'show_contact'}):
                        for location_img in contact.find_all('i', {'class': 'icon3-location'}):
                            location = location_img.parent.text
                            json_data['address'] = location.strip()
                            break

                        for phone_img in contact.find_all('i', {'class': 'icon3-phone'}):
                            phone = phone_img.parent.text
                            json_data['phones'] = phone.strip()
                            break

                        for post_img in contact.find_all('i', {'class': 'icon3-post'}):
                            email = post_img.parent.text
                            json_data['email'] = email.strip()
                            break
                    break
                break
            break

        for tabs in self._connection.find_all('div', {'class': ['show_tab', 'tab-content']}):
            for tab_descr in tabs.find_all('div', {'id': 'descr'}):
                description = tab_descr.text
                json_data['description'] = description.strip()
                break

            specializations = []
            for tab_price in tabs.find_all('div', {'id': 'price'}):
                for price in tab_price.find_all('div', {'class': ['show_price', 'container30']}):
                    spec_str = price.div.text
                    spec = spec_str.strip()
                    if spec:
                        specializations.append(spec)
                break
            json_data['specializations'] = specializations

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        page_count = self._get_page_count()
        for page_num in range(1, page_count + 1):
            print('processing page #', str(page_num))

            if page_num == 1:
                new_url = url
            else:
                new_url = '/?page='.join([url, str(page_num)])

            self._connect(new_url)
            if self._connection is None:
                continue

            lawyer_ids = []
            for person in self._connection.find_all('div', {'class': ['fsize4', 'container05']}):
                lawyer_link = person.a
                lawyer_url = lawyer_link['href']
                lawyer_id = lawyer_url.replace('/i/', '')
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

            for lawyer_id in lawyer_ids:
                lawyer = self._get_lawyer(lawyer_type, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

        return lawyers

    def _get_page_count(self):
        count = 0

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])

        self._connect(url)
        if self._connection is None:
            return count

        last_page = None
        for page in self._connection.find_all('span', {'class': 'page'}):
            last_page = page

        if last_page is None:
            return count

        count_str = last_page.text.strip()
        count = int(count_str)

        return count

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        job_title = LawlyParser.get_json_key(json_data, 'job_title')
        if job_title.find('Адвокат') >= 0:
            lawyer_type = lawly_lawyer.LawyerType.Attorney

        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_str = LawlyParser.get_json_key(json_data, 'certificate')
        cert_type = None
        cert_number = ''
        cert_date = None
        if cert_str:
            cert_arr = cert_str.split(' ')

            cert_type = lawly_lawyer.VerificationType.License
            cert_type_str = cert_arr[0]
            if cert_type_str == 'ЕГРПОУ':
                cert_type = lawly_lawyer.VerificationType.EDRPOU

            cert_number = cert_arr[1]
            cert_number.replace('№', '')

            full_str = cert_type_str + ' №' + cert_number + ' от '
            cert_date = cert_str.replace(full_str, '')

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = ''
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        if address_str:
            address_arr = address_str.split(', ')
            for part in address_arr:
                if part.find('обл.') >= 0:
                    area = part.replace('обл.', '').strip()
                elif part.find('г.') >= 0:
                    town = part.replace('г.', '').strip()
                elif part.find('ул.') >= 0:
                    street = part.replace('ул.', '').strip()

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = LawlyParser.get_json_key(json_data, 'description')
        specializations = set(LawlyParser.get_json_key(json_data, 'specializations'))

        phones_str = LawlyParser.get_json_key(json_data, 'phones')
        phones_arr_coma = phones_str.split(',')
        phones_arr_semi = phones_str.split(';')
        phones_arr = phones_arr_coma if len(phones_arr_coma) > len(phones_arr_semi) else phones_arr_semi
        phones = set([phone.strip() for phone in phones_arr])

        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/img/show_nophoto_profile.png') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperLawyerUA(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.LawyerUA_Input
        self._output_source = LawlyScrapperSource.LawyerUA_Output

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        page_count = self._get_page_count()
        for page_num in range(1, page_count + 1):
            print('processing page #', str(page_num), '/', str(141))

            if page_num == 1:
                new_url = url
            else:
                new_url = '/?PAGEN_1='.join([url, str(page_num)])

            self._connect(new_url)
            if self._connection is None:
                continue

            for person_data in self._connection.find_all('div', {'class': 'col-sm-6'}):
                lawyer_json = {}

                link = person_data.a
                if link is not None:
                    url_str = link['href']
                    if url:
                        id_str = url_str.replace('/specialists/?ID=', '')
                        lawyer_json['id'] = id_str

                for person in person_data.find_all('div', {'class': 'green-shadow'}):
                    for name_info in person.find_all('div', {'class': 'lawyer-name'}):
                        name_title = name_info.text
                        arr = name_title.split(', ')
                        if arr:
                            lawyer_json['name'] = arr[0]
                            lawyer_json['job_title'] = arr[1]
                        break

                    for img_info in person.find_all('div', {'class': 'img-wrap'}):
                        img_el = img_info.span
                        if img_el is None:
                            break

                        img_str = img_el['style']
                        if img_str:
                            img_str = img_str.replace('background-image: url(', '')
                            img_str = img_str.replace(')', '')
                            lawyer_json['image'] = 'https://lawyer.ua' + img_str
                        break

                    for location in person.find_all('span', {'class': 'location'}):
                        address = location.text
                        if address:
                            lawyer_json['address'] = address
                        break

                    for spec_list in person.find_all('ul', {'class': 'spec_list'}):
                        specializations = []
                        for item in spec_list.find_all('li'):
                            spec = item.text
                            if spec:
                                spec = spec.replace(chr(8212), '')
                                specializations.append(spec)

                        if specializations:
                            lawyer_json['specializations'] = specializations
                        break

                    lawyer = self._convert_lawyer(lawyer_json)
                    if lawyer is not None:
                        lawyers.append(lawyer)
                    break

        return lawyers

    def _get_page_count(self):
        # count = 142
        count = 0

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])

        self._connect(url)
        if self._connection is None:
            return count

        last_page = None
        for page in self._connection.find_all('a', href=lambda x: x and x.startswith('/search/?PAGEN_1=')):
            try:
                page_class_list = page['class']
                page_class = page_class_list[0]
            except KeyError as e:
                page_class = ''
            except IndexError as e:
                page_class = ''

            if not page_class == 'modern-page-next':
                last_page = page

        if last_page is None:
            return 0

        count_str = last_page.text.strip()
        count = int(count_str)

        print(count)
        return count

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        job_title = LawlyParser.get_json_key(json_data, 'job_title')
        if job_title.find('Адвокат') >= 0:
            lawyer_type = lawly_lawyer.LawyerType.Attorney

        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = None
        cert_number = ''
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = ''
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_str = address_str.strip()
        if address_str:
            if address_str.find('область') >= 0:
                area = address_str.replace(' область', '')
            else:
                town = address_str

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set(LawlyParser.get_json_key(json_data, 'specializations'))

        phones = set([])

        email = ''
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/no_avatar.jpg') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperProtocol(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Protocol_Input
        self._output_source = LawlyScrapperSource.Protocol_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}
        for person in self._connection.find_all('div', {'class': 'user-profile'}):
            for id_el in person.find_all('div', {'class': 'user_id'}):
                id_str = id_el.text
                id_str = id_str.replace('ID:', '')
                json_data['id'] = id_str.strip()
                break

            for photo in person.find_all('div', {'class': 'user-profile-photo'}):
                img = photo.img
                if img is None:
                    break

                link_url = img['src']
                if link_url:
                    link_url = 'https://protocol.ua/' + link_url
                json_data['image'] = link_url
                break

            for name_el in person.find_all('div', {'class': 'user-profile__name'}):
                name_str = name_el.text
                json_data['name'] = name_str.strip()
                break

            phones = []
            for contact in person.find_all('a', {'class': 'simple-link-red'}):
                href = contact['href']
                if not href:
                    continue

                value = contact.text.strip()
                if href.find('mailto') >= 0:
                    json_data['email'] = value
                elif href.find('tel') >= 0:
                    phones.append(value)
            json_data['phones'] = phones

            for location in person.find_all('a', {'class': 'event-location__link'}):
                element = location.parent
                if element is None:
                    break

                address = element.text
                address = address.replace('Показать на карте', '')
                json_data['address'] = address.strip()

            specializations = []
            for services in person.find_all('ul', {'class': 'user-profile-services__list'}):
                for service in services.find_all('li'):
                    service_str = service.text
                    service_str = service_str.strip()
                    if service_str:
                        specializations.append(service_str)
            json_data['specializations'] = specializations

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        page_count = self._get_page_count()
        for page_num in range(1, page_count + 1):
            print('processing page #', str(page_num), '/', str(234))

            if page_num == 1:
                new_url = url
            else:
                new_url = '/'.join([url, str(page_num)])

            self._connect(new_url)
            if self._connection is None:
                continue

            lawyer_ids = []
            for person in self._connection.find_all('div', {'class': 'lawyers-col-2'}):
                lawyer_link = person.a
                lawyer_url = lawyer_link['href']
                lawyer_id = lawyer_url.replace('/ru/cabinet/', '')
                lawyer_id = lawyer_id.replace('/', '')
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

            for lawyer_id in lawyer_ids:
                lawyer = self._get_lawyer(lawyer_type, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

        return lawyers

    def _get_page_count(self):
        count = 0

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])

        self._connect(url)
        if self._connection is None:
            return count

        last_page = None
        for page in self._connection.find_all('li', {'class': 'pager-list-item'}):
            last_page = page

        if last_page is None:
            return count

        count_str = last_page.text.strip()
        count = int(count_str)
        print(count)

        return count

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = None
        cert_number = ''
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = ''
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_arr = address_str.split(', ')
        if address_arr:
            area = address_arr[0]
            area = area.replace(' обл.', '')
            if len(address_arr) > 1:
                town = address_arr[1]
            if len(address_arr) > 2:
                street = address_arr[2]
                street = street.replace('вул. ', '')
                street = street.replace('вулиця ', '')
                street = street.replace('ул. ', '')
                street = street.replace('улица ', '')
            if len(address_arr) > 3:
                street_number = address_arr[3]

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set(LawlyParser.get_json_key(json_data, 'specializations'))
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/images/no_avatar.jpg') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperNotaryKiev(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.NotaryKiev_Input
        self._output_source = LawlyScrapperSource.NotaryKiev_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}
        id_str = url.replace('https://notariusy.kiev.ua/', '')
        id_str = id_str.replace('/', '')
        if id_str:
            json_data['id'] = id_str

        for person in self._connection.find_all('div', {'class': 'leftsize'}):
            for detail in person.find_all('div', {'class': 'field-name-body'}):
                for detail_el in detail.find_all('p'):
                    detail_str = detail_el.text
                    if detail_str.find('Номер свидетельства') >= 0:
                        cert = detail_str.replace('Номер свидетельства:', '')
                        json_data['certificate'] = cert.strip()
                    if detail_str.find('E-MAIL:') >= 0:
                        email = detail_str.replace('E-MAIL:', '')
                        json_data['email'] = email.strip()
                break

            # for photo in person.find_all('div', {'class': 'field-type-image'}):
            #     img = photo.img
            #     if img is None:
            #         break
            #
            #     link_url = img['src']
            #     json_data['image'] = link_url
            #     break

            for name_el in person.find_all('div', {'class': 'titleGroup'}):
                name_str = name_el.text
                json_data['name'] = name_str.strip()
                break

            phones = []
            for contact in person.find_all('div', {'class': 'field-name-field-phone'}):
                for phone_el in contact.find_all('div', {'class': 'field-item'}):
                    phone = phone_el.text
                    phones.append(phone.strip())
                    break
                break
            json_data['phones'] = phones

            for district_el in person.find_all('div', {'class': 'field-name-field-district'}):
                district = district_el.span
                if district is None:
                    break

                region = district.text
                json_data['region'] = region.strip()
                break

            for location in person.find_all('div', {'class': 'field-name-field-adress'}):
                for address_el in location.find_all('div', {'class': 'field-item'}):
                    address = address_el.text
                    json_data['address'] = address.strip()
                    break
                break

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        new_url = url

        self._connect(new_url)
        if self._connection is None:
            return lawyers

        lawyer_ids = []
        for font in self._connection.find_all('font'):
            detail_str = font.text
            if not detail_str.find('Нотариус ') >= 0:
                continue

            person = font.font
            if person is None:
                continue

            lawyer_link = person.a
            if lawyer_link is None:
                continue

            lawyer_url = lawyer_link['href']
            lawyer_id = lawyer_url.replace('https://notariusy.kiev.ua/', '')
            if lawyer_id:
                lawyer_ids.append(lawyer_id)

        # lawyer_id = 'dudash-marianna-miroslavovna'
        # lawyer_ids.append(lawyer_id)

        count = 0
        for lawyer_id in lawyer_ids:
            count += 1
            print(count, '/', len(lawyer_ids))

            lawyer = self._get_lawyer(lawyer_type, lawyer_id)
            if lawyer is not None and lawyer.email != '':
                lawyers.append(lawyer)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Notary
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate')
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = LawlyParser.get_json_key(json_data, 'region')
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_arr = address_str.split(',')
        if address_arr:
            town = address_arr[0]
            town = town.replace('г.', '')
            town = town.strip()
            if len(address_arr) > 1:
                street = address_arr[1]
                street = street.replace('ул. ', '')
                street = street.strip()
            if len(address_arr) > 2:
                street_number = address_arr[2]
            if len(address_arr) > 3:
                street_house = address_arr[3]
                if street_house.find('оф.') >= 0:
                    apartment_type = 'оф.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                elif street_house.find('кв.') >= 0:
                    apartment_type = 'кв.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                else:
                    apartment_number = street_house.strip()

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/sites/default/files/notar') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperNotaryKievUA(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.NotaryKievUA_Input
        self._output_source = LawlyScrapperSource.NotaryKievUA_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}
        id_str = url.replace('https://notarius.kiev.ua/notarius', '')
        id_str = id_str.replace('/', '')
        if id_str:
            json_data['id'] = id_str

        for person in self._connection.find_all('div', {'class': 'entry-header-title'}):
            for name_el in person.find_all('h1'):
                name = name_el.text
                json_data['name'] = name.strip()
                break

            for contact_el in person.find_all('div', {'class': 'entry-header-custom-left'}):
                phones = []
                for contact in contact_el.find_all('span', {'class': 'entry-phone'}):
                    for phone_el in contact.find_all('a'):
                        phone = phone_el.text
                        phones.append(phone.strip())
                    break
                json_data['phones'] = phones

                email = ''
                for email_el in contact_el.find_all('span', {'class': 'entry-email'}):
                    email = email_el.text
                    break
                json_data['email'] = email

                break

            for location in person.find_all('span', {'class': 'frontend_address'}):
                address = location.text
                json_data['address'] = address.strip()
                break

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        new_url = url

        self._connect(new_url)
        if self._connection is None:
            return lawyers

        lawyer_ids = []
        for card in self._connection.find_all('div', {'class': 'pt-cv-content-item'}):
            for person in card.find_all('div', {'class': 'pt-cv-ifield'}):
                lawyer_link = person.a
                if lawyer_link is None:
                    continue

                lawyer_url = lawyer_link['href']
                lawyer_id = lawyer_url.replace('https://notarius.kiev.ua/notarius/', '')
                lawyer_id = lawyer_id.replace('/', '')
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

                break

        count = 0
        for lawyer_id in lawyer_ids:
            count += 1
            print(count, '/', len(lawyer_ids))

            lawyer = self._get_lawyer(lawyer_type, lawyer_id)
            if lawyer is not None and lawyer.email != '':
                lawyers.append(lawyer)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Notary
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate')
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = LawlyParser.get_json_key(json_data, 'region')
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_arr = address_str.split(',')
        if address_arr:
            town = address_arr[0]
            town = town.replace('г.', '')
            town = town.strip()
            if len(address_arr) > 1:
                street = address_arr[1]
                street = street.replace('ул. ', '')
                street = street.strip()
            if len(address_arr) > 2:
                street_number = address_arr[2]
            if len(address_arr) > 3:
                street_house = address_arr[3]
                if street_house.find('оф.') >= 0:
                    apartment_type = 'оф.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                elif street_house.find('кв.') >= 0:
                    apartment_type = 'кв.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                else:
                    apartment_number = street_house.strip()

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/sites/default/files/notar') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperNotary2gis(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Notary2gis_Input
        self._output_source = LawlyScrapperSource.Notary2gis_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}
        id_str = url.replace('https://2gis.ua/kyiv/firm/', '')
        id_str = id_str.replace('/', '')
        if id_str:
            json_data['id'] = id_str

        for person in self._connection.find_all('div', {'class': 'entry-header-title'}):
            for name_el in person.find_all('h1'):
                name = name_el.text
                json_data['name'] = name.strip()
                break

            for contact_el in person.find_all('div', {'class': 'entry-header-custom-left'}):
                phones = []
                for contact in contact_el.find_all('span', {'class': 'entry-phone'}):
                    for phone_el in contact.find_all('a'):
                        phone = phone_el.text
                        phones.append(phone.strip())
                    break
                json_data['phones'] = phones

                email = ''
                for email_el in contact_el.find_all('span', {'class': 'entry-email'}):
                    email = email_el.text
                    break
                json_data['email'] = email

                break

            for location in person.find_all('span', {'class': 'frontend_address'}):
                address = location.text
                json_data['address'] = address.strip()
                break

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        new_url = url

        self._connect(new_url)
        if self._connection is None:
            return lawyers

        lawyer_ids = []
        for card in self._connection.find_all('div', {'class': '_121zpzx'}):
            for person in card.find_all('div', {'class': '_1h3cgic'}):
                lawyer_link = person.a
                if lawyer_link is None:
                    continue

                lawyer_url = lawyer_link['href']
                lawyer_id = lawyer_url.replace('kyiv/firm', '')
                lawyer_id = lawyer_id.replace('/', '')
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

                break

        count = 0
        for lawyer_id in lawyer_ids:
            count += 1
            print(count, '/', len(lawyer_ids))

            lawyer = self._get_lawyer(lawyer_type, lawyer_id)
            if lawyer is not None and lawyer.email != '':
                lawyers.append(lawyer)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Notary
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate')
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = LawlyParser.get_json_key(json_data, 'region')
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_arr = address_str.split(',')
        if address_arr:
            town = address_arr[0]
            town = town.replace('г.', '')
            town = town.strip()
            if len(address_arr) > 1:
                street = address_arr[1]
                street = street.replace('ул. ', '')
                street = street.strip()
            if len(address_arr) > 2:
                street_number = address_arr[2]
            if len(address_arr) > 3:
                street_house = address_arr[3]
                if street_house.find('оф.') >= 0:
                    apartment_type = 'оф.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                elif street_house.find('кв.') >= 0:
                    apartment_type = 'кв.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                else:
                    apartment_number = street_house.strip()

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/sites/default/files/notar') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperNotaryUA(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.NotaryUA_Input
        self._output_source = LawlyScrapperSource.NotaryUA_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {'id': url}
        for person in self._connection.find_all('div', {'id': 'InnerWrapper'}):
            for cert_el in person.find_all('div', {'class': 'svidet'}):
                cert_str = cert_el.text
                cert_str = cert_str.replace('Свидетельство о праве на занятие нотариальной деятельностью №', '')
                cert_str = cert_str.replace(' от ', ',')
                cert_arr = cert_str.split(',')
                if cert_arr:
                    json_data['certificate_number'] = cert_arr[0].strip()
                    if len(cert_arr) > 1:
                        json_data['certificate_date'] = cert_arr[1].strip()
                break

            for photo in person.find_all('img', {'class': 'notarius_photo'}):
                link_url = photo['src']
                if link_url:
                    link_url = url + link_url
                json_data['image'] = link_url
                break

            for name_el in person.find_all('h3', {'class': 'n_name'}):
                name_str = name_el.text
                json_data['name'] = name_str.strip()
                break

            for descr_el in person.find_all('h3', {'class': 'text_edit_notar'}):
                descr_str = descr_el.text
                json_data['description'] = descr_str.strip()
                break

            for contacts in person.find_all('table', {'class': 'table_contacts'}):
                for contact in contacts.find_all('tr'):
                    contact_name = contact.th.text
                    contact_value = contact.td.text.strip()
                    if contact_name.find('Тел') >= 0:
                        phones = []
                        phone_arr = contact_value.split('\n')
                        for phone_str in phone_arr:
                            phone = phone_str.strip()
                            if phone:
                                phones.append(phone)
                        json_data['phones'] = phones
                    elif contact_name.find('E-mail') >= 0:
                        json_data['email'] = contact_value
                    elif contact_name.find('Адрес') >= 0:
                        json_data['address'] = contact_value
                break
            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        new_url = url

        self._connect(new_url)
        if self._connection is None:
            return lawyers

        lawyer_ids = []
        for person in self._connection.find_all('div', {'class': 'notarius_card'}):
            for link in person.find_all('a', {'class': 'name'}):
                lawyer_id = link['href']
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

        for lawyer_id in lawyer_ids:
            lawyer = self._get_lawyer(lawyer_type, lawyer_id)
            if lawyer is not None:
                lawyers.append(lawyer)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Notary
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate_number')
        cert_date = LawlyParser.get_json_key(json_data, 'certificate_date')

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = 'Киевская'
        region = ''
        town = 'Киев'
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_arr = address_str.split(', ')
        if address_arr:
            street = address_arr[0]
            street = street.replace('ул. ', '')
            street = street.strip()
            if len(address_arr) > 1:
                street_number = address_arr[1]
            if len(address_arr) > 2:
                street_house = address_arr[2]
                if street_house.find('оф') >= 0:
                    apartment_type = 'оф.'
                    apartment_number = street_house.replace('офис', '').strip()
                    apartment_number = apartment_number.replace('оф.', '').strip()
                elif street_house.find('кв') >= 0:
                    apartment_type = 'кв.'
                    apartment_number = street_house.replace('квартира', '').strip()
                    apartment_number = apartment_number.replace('кв.', '').strip()
                else:
                    apartment_number = street_house.strip()

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = LawlyParser.get_json_key(json_data, 'description')
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/user_site/img/default_img1.jpg') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperJurliga(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Jurliga_Input
        self._output_source = LawlyScrapperSource.Jurliga_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}

        id_str = url.replace('https://jurliga.ligazakon.net/catalog/', '')
        id_str = id_str.replace('/', '')
        json_data['id'] = id_str

        for person in self._connection.find_all('div', {'class': 'catalog_firm_header__top-block'}):
            for photo in person.find_all('div', {'class': 'firm_logo_container'}):
                try:
                    link_url = photo['style']
                except KeyError as e:
                    break

                link_url = link_url.replace('background-image: url(', '')
                link_url = link_url.replace(')', '')
                link_url = link_url.replace(';', '')
                json_data['image'] = link_url
                break

            for name_el in person.find_all(attrs={'class': 'firm_name'}):
                name_str = name_el.text
                json_data['name'] = name_str.strip()
                break

            for type_el in person.find_all(attrs={'class': 'firm_type'}):
                type_str = type_el.text
                json_data['type'] = type_str.strip()
                break
            break

        for about in self._connection.find_all('section', {'class': 'catalog_firm_about'}):
            for descr_el in about.find_all('div', {'class': 'description_text'}):
                descr_str = descr_el.text
                json_data['description'] = descr_str.strip()
                break

            specializations = []
            for spec_el in about.find_all('div', {'class': 'practic_item_title'}):
                spec_str = spec_el.text
                spec_str = spec_str.strip()
                if spec_str:
                    specializations.append(spec_str)
            json_data['specializations'] = specializations
            break

        url_contacts = '/'.join([url, 'kontakty'])
        self._connect(url_contacts)
        if self._connection is None:
            if json_data:
                return json_data
            else:
                return None

        for contacts in self._connection.find_all('div', {'class': 'contacts_section'}):
            for address_block in contacts.find_all('div', {'class': 'adr'}):
                for locality in address_block.find_all('div', {'class': 'locality'}):
                    locality_str = locality.text
                    locality_arr = locality_str.split(',')
                    for loc_item in locality_arr:
                        loc = loc_item.strip()
                        if not loc:
                            continue

                        if loc.find('обл') >= 0:
                            json_data['area'] = loc.replace('обл.', '').strip()
                        else:
                            json_data['town'] = loc

                for street_address in address_block.find_all('div', {'class': 'street-address'}):
                    street_str = street_address.text
                    street_arr = street_str.split(',')
                    for street_item in street_arr:
                        street_new = street_item.strip()
                        if not street_new:
                            continue

                        if street_new.find('район') >= 0 or street_new.find('р-н') >= 0:
                            region = street_new.replace('район', '')
                            region = region.replace('р-н', '')
                            json_data['region'] = region.strip()
                        elif street_new.find('улица') >= 0 or street_new.find('ул.') >= 0:
                            street = street_new.replace('улица', '')
                            street = street.replace('ул.', '')
                            json_data['street'] = street.strip()
                        else:
                            json_data['street_number'] = street_new

            phones = []
            for telephone_block in contacts.find_all('div', {'class': 'telephones_block'}):
                for phone_el in telephone_block.find_all('a', {'class': 'contacts_telephone_item'}):
                    phone_str = phone_el.text
                    phone = phone_str.strip()
                    if phone_str:
                        phones.append(phone)
                break
            json_data['phones'] = phones

            for mail_block in contacts.find_all('div', {'class': 'mail_block'}):
                for email_el in mail_block.find_all('a', {'class': 'contacts_email'}):
                    email_str = email_el.text
                    email = email_str.strip()
                    if email:
                        json_data['email'] = email
                break

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            url = LawlyScrapperSource.to_string(self._input_source)
            lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            url = '/'.join([url, lawyers_cat])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        new_url = url

        self._connect(new_url)
        if self._connection is None:
            return lawyers

        page_count = self._get_page_count()
        for page_num in range(1, page_count + 1):
            print('processing page #', str(page_num), '/', str(page_count + 1))

            if page_num == 1:
                new_url = url
            else:
                new_url = '?page='.join([url, str(page_num)])

            self._connect(new_url)
            if self._connection is None:
                continue

            lawyer_ids = []
            for person in self._connection.find_all('a', {'class': 'firm_name'}):
                lawyer_url = person['href']
                lawyer_id = lawyer_url.replace('/catalog/', '')
                if lawyer_id:
                    lawyer_ids.append(lawyer_id)

            for lawyer_id in lawyer_ids:
                lawyer = self._get_lawyer(lawyer_type, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

        return lawyers

    def _get_page_count(self):
        count = 0

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])

        self._connect(url)
        if self._connection is None:
            return count

        last_page = None
        for page in self._connection.find_all('li', {'class': 'page-item'}):
            page_class_list = page['class']
            if 'arrow' not in page_class_list:
                last_page = page

        if last_page is None:
            return count

        count_str = last_page.text.strip()
        count = int(count_str)
        print(count)

        return count

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        type_str = LawlyParser.get_json_key(json_data, 'type')
        if type_str.find('Адвокат') >= 0:
            lawyer_type = lawly_lawyer.LawyerType.Attorney
        elif type_str.find('Нотар') >= 0:
            lawyer_type = lawly_lawyer.LawyerType.Notary

        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = None
        cert_number = ''
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = LawlyParser.get_json_key(json_data, 'area')
        region = LawlyParser.get_json_key(json_data, 'region')
        town = LawlyParser.get_json_key(json_data, 'town')
        street = LawlyParser.get_json_key(json_data, 'street')
        street_type = ''
        street_number = LawlyParser.get_json_key(json_data, 'street_number')
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = LawlyParser.get_json_key(json_data, 'description')
        specializations = set(LawlyParser.get_json_key(json_data, 'specializations'))
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = None

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/Content/_pics/firm_catalog/pic_') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperERAU(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.ERAU_Site

    def update_lawyer(self, lawyer_obj=None, lawyer_id=''):
        if lawyer_id:
            id_str = lawyer_id
        else:
            id_str = lawyer_obj.id

        id_str = str(id_str)

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_profile_cat(self._input_source)
        url = '/'.join([url, lawyers_cat, id_str])

        self._connect(url)
        if self._connection is None:
            return False

        status = True
        for person in self._connection.find_all('div', {'class': 'termination-advocacy-activities'}):
            status = False
            break

        for stop_block in self._connection.find_all('div', {'class': 'column-right__inner'}):
            stop_str = stop_block.text.lower()
            if stop_str.find('зупинено') >= 0 or stop_str.find('припинено') >= 0:
                status = False
            if stop_str.find('поновлено') >= 0:
                status = True

        success = lawyer_obj.update('status', status)

        return success


class LawlyScrapperLeegl(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Leegl_Input
        self._output_source = LawlyScrapperSource.Leegl_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}
        id_str = url.replace('https://leegl.com.ua/lawyers/', '')
        if id_str:
            json_data['id'] = id_str

        for person in self._connection.find_all('div', {'class': 'profile-general'}):
            for name_el in person.find_all('h1', {'class': 'profile-general__name'}):
                name = name_el.text
                json_data['name'] = name.strip()
                break

            for contact_el in person.find_all('lawyer-contacts'):
                data = contact_el[':contacts']
                contact_data = json.loads(data)

                phones = []
                phone_data = LawlyParser.get_json_key(contact_data, 'phone')
                if phone_data:
                    phones.append(phone_data['value'])

                email = ''
                email_data = LawlyParser.get_json_key(contact_data, 'email')
                if email_data:
                    email = email_data['value']

                if not email:
                    continue

                json_data['phones'] = phones
                json_data['email'] = email

                break

            break

        if not json_data:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        lawyer_ids = []
        with open(r'D:\Projects\lawly\Parser\input_data\leegl_list.txt', 'r') as file:
            lawyer_ids = file.readlines()

        count = 0
        for lawyer_id in lawyer_ids:
            count += 1
            print(count, '/', len(lawyer_ids))

            lawyer_id = lawyer_id.replace('\n', '')
            lawyer = self._get_lawyer(lawyer_type, lawyer_id)
            if lawyer is not None and lawyer.email != '':
                lawyers.append(lawyer)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 3:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = name_arr[2]
        elif len(name_arr) == 2:
            first_name = name_arr[1]
            last_name = name_arr[0]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = ''
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate')
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        country = 'Украина'
        area = ''
        region = LawlyParser.get_json_key(json_data, 'region')
        town = ''
        street = ''
        street_type = ''
        street_number = ''
        apartment_type = ''
        apartment_number = 0
        postal_code = ''

        address_str = LawlyParser.get_json_key(json_data, 'address')
        address_arr = address_str.split(',')
        if address_arr:
            town = address_arr[0]
            town = town.replace('г.', '')
            town = town.strip()
            if len(address_arr) > 1:
                street = address_arr[1]
                street = street.replace('ул. ', '')
                street = street.strip()
            if len(address_arr) > 2:
                street_number = address_arr[2]
            if len(address_arr) > 3:
                street_house = address_arr[3]
                if street_house.find('оф.') >= 0:
                    apartment_type = 'оф.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                elif street_house.find('кв.') >= 0:
                    apartment_type = 'кв.'
                    apartment_number = street_house.replace(apartment_type, '').strip()
                else:
                    apartment_number = street_house.strip()

        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = ''
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = True

        ava_url = LawlyParser.get_json_key(json_data, 'image')
        if ava_url.find('/sites/default/files/notar') != -1:
            ava_url = ''
        avatar = lawly_lawyer.LawyerAvatar(ava_url)

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperCzech(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Czech_Input
        self._output_source = LawlyScrapperSource.Czech_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}

        path = LawlyScrapperSource.to_string(self._input_source)
        lawyers_profile_cat = LawlyScrapperSource.lawyer_profile_cat(self._input_source)
        path = '/'.join([path, lawyers_profile_cat])

        id_str = url.replace(path + '/', '')
        id_str = id_str.replace(id_str + '\n', '')
        if id_str:
            json_data['id'] = id_str

        has_email = False
        for rows in self._connection.find_all('tr'):
            for row in rows:
                try:
                    cells = row.find_all('td')
                except:
                    continue
                for cell in cells:
                    text = cell.text.strip()
                    if text == 'Jméno':
                        value = cell.find_next_sibling('td').text.strip()
                        json_data['name'] = value
                    elif text == 'Evidenční číslo':
                        value = cell.find_next_sibling('td').text.strip()
                        json_data['certificate'] = value
                    elif text == 'email':
                        try:
                            value = cell.findNext('a')['href']
                        except:
                            continue

                        start = value.find('mailto:')
                        value = value[start + 8:]
                        value = value.replace('\\', '')
                        value = value.replace('+', '')
                        value = value.replace('\'', '')
                        json_data['email'] = value
                        has_email = True
                    elif text == 'Telefon':
                        value = cell.find_next_sibling('td').text.strip()
                        value = value.replace('+420', '')
                        json_data['phones'] = [value]
            break

        if not json_data or not has_email:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_profile_cat(self._input_source)
        url = '/'.join([url, lawyers_cat])
        if not url:
            return lawyers

        with open(r'D:\Projects\lawly\Parser\input_data\europe\czech.txt', 'r', encoding='utf-8') as f:
            ids = f.readlines()
            ind = 0
            total = len(ids)
            for lawyer_id in ids:
                lawyer_id = lawyer_id.replace('\n', '')
                lawyer = self._get_lawyer(lawyer_type, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

                ind += 1
                if ind % 100 == 0:
                    print(ind, '-', total)
                if ind == 1000:
                    break

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Attorney
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 4:
            first_name = name_arr[0] + ' ' + name_arr[1] + ' ' + name_arr[2]
            last_name = name_arr[3]
            middle_name = ''
        elif len(name_arr) == 3:
            first_name = name_arr[0] + ' ' + name_arr[1]
            last_name = name_arr[2]
            middle_name = ''
        elif len(name_arr) == 2:
            first_name = name_arr[0]
            last_name = name_arr[1]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = lawyer_id
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate')
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        address = None
        description = ''
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = True
        avatar = None

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyScrapperPoland(LawlyScrapper):
    def __init__(self):
        super().__init__()
        self._input_source = LawlyScrapperSource.Poland_Input
        self._output_source = LawlyScrapperSource.Poland_Output

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        json_data = {}

        path = LawlyScrapperSource.to_string(self._input_source)
        lawyers_profile_cat = LawlyScrapperSource.lawyer_profile_cat(self._input_source)
        path = '/'.join([path, lawyers_profile_cat])

        id_str = url.replace(path + '/', '')
        if id_str:
            json_data['id'] = id_str

        has_email = False
        section = self._connection.find_all('section')[0]

        name = section.findNext('h2').text.strip()
        json_data['name'] = name

        cert = section.findNext('h3').text.strip()
        cert = cert.replace(')', '')
        start = cert.find('Adw/')
        cert = cert[start + 4:]
        json_data['certificate'] = cert

        rows = section.findNext('div')
        for row in rows:
            cell = row.findNext('span')
            text = cell.text.strip()
            if text == 'Email:':
                div = cell.find_next_sibling('div')
                value = div['data-ea'] + '@' + div['data-eb']
                json_data['email'] = value
                has_email = True
            elif text == 'Komórkowy:':
                value = cell.find_next_sibling('div').text.strip()
                value = value.replace('+48', '')
                value = value.replace('-', '')
                json_data['phones'] = [value]

        if not json_data or not has_email:
            return None

        return json_data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        path = LawlyScrapperSource.to_string(self._input_source)
        lawyers_cat = LawlyScrapperSource.lawyer_list_cat(self._input_source)
        url = '/'.join([path, lawyers_cat])
        if not url:
            return lawyers

        done = 0
        for ind in range(10):
            number = done + ind + 1
            new_url = url + str(number)

            self._connect(new_url)
            if self._connection is None:
                return lawyers

            lawyer_ids = []
            for links in self._connection.find_all('td', {'class': 'icon_link'}):
                for link in links:
                    lawyer_id = link['href']
                    lawyer_id = lawyer_id.replace(path + '/', '')
                    if lawyer_id:
                        lawyer_ids.append(lawyer_id)

            for lawyer_id in lawyer_ids:
                lawyer = self._get_lawyer(lawyer_type, lawyer_id)
                if lawyer is not None:
                    lawyers.append(lawyer)

            print(number)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_type = lawly_lawyer.LawyerType.Attorney
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        full_name = LawlyParser.get_json_key(json_data, 'name')
        name_arr = full_name.split(' ')
        if len(name_arr) == 4:
            first_name = name_arr[0] + ' ' + name_arr[1] + ' ' + name_arr[2]
            last_name = name_arr[3]
            middle_name = ''
        elif len(name_arr) == 3:
            first_name = name_arr[0] + ' ' + name_arr[1]
            last_name = name_arr[2]
            middle_name = ''
        elif len(name_arr) == 2:
            first_name = name_arr[0]
            last_name = name_arr[1]
            middle_name = ''
        else:
            first_name = full_name
            last_name = ''
            middle_name = ''
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = ''

        gov_url = lawyer_id
        cert_type = lawly_lawyer.VerificationType.License
        cert_number = LawlyParser.get_json_key(json_data, 'certificate')
        cert_date = None

        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        address = None
        description = ''
        specializations = set([])
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = True
        avatar = None

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer


class LawlyJSON(LawlyParser):
    def __init__(self, json_input):
        super().__init__(LawlyParserType.JSON)
        self._input_source = json_input
        self._output_source = json_input

    def _connect(self, url):
        self._connection = None

        try:
            with open(url, 'r', encoding='utf-8') as f:
                pass
        except FileNotFoundError as e:
            return

        self._connection = url

    def _get_data(self, url):
        self._connect(url)
        if self._connection is None:
            return None

        with open(self._connection, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def get_lawyers(self, lawyer_type):
        lawyers = []

        url = ''
        if lawyer_type == lawly_lawyer.LawyerType.Lawyer:
            dir_name = LawlyScrapperSource.to_string(self._input_source)
            cat_name = LawlyScrapperSource.lawyer_list_cat(self._input_source)
            file_name = LawlyScrapperSource.lawyer_profile_cat(self._input_source)
            url = '\\'.join([dir_name, cat_name, file_name])
        elif lawyer_type == lawly_lawyer.LawyerType.Attorney:
            url = ''
        elif lawyer_type == lawly_lawyer.LawyerType.Notary:
            url = ''

        if not url:
            return lawyers

        lawyers_json = self._get_data(url)
        items = LawlyParser.get_json_key(lawyers_json, 'lawyers')
        if not items:
            return lawyers

        count = 0
        for item in items:
            count += 1
            # print('processing lawyer #', str(count))

            lawyer = self._convert_lawyer(item)
            lawyers.append(lawyer)

        return lawyers

    def _convert_lawyer(self, json_data):
        lawyer_id = LawlyParser.get_json_key(json_data, 'id')

        lawyer_type = lawly_lawyer.LawyerType.Lawyer
        type_str = LawlyParser.get_json_key(json_data, 'type')
        if type_str:
            lawyer_type = lawly_lawyer.LawyerType.from_string(type_str)

        first_name = LawlyParser.get_json_key(json_data, 'first_name')
        last_name = LawlyParser.get_json_key(json_data, 'last_name')
        middle_name = LawlyParser.get_json_key(json_data, 'middle_name')
        lawyer_name = lawly_lawyer.LawyerName(first_name, last_name, middle_name)

        gender = LawlyParser.get_json_key(json_data, 'gender')

        gov_url = LawlyParser.get_json_key(json_data, 'gov_url')
        cert_type_str = LawlyParser.get_json_key(json_data, 'cert_type')
        cert_type = lawly_lawyer.VerificationType.from_string(cert_type_str)
        cert_number = LawlyParser.get_json_key(json_data, 'cert_number')
        cert_date_str = LawlyParser.get_json_key(json_data, 'cert_date')
        cert_date = datetime.datetime.strptime(cert_date_str, '%m/%d/%y %H:%M:%S') if cert_date_str else None
        lawyer_verification = lawly_lawyer.LawyerVerification(
            cert_type=cert_type,
            cert_number=cert_number,
            cert_date=cert_date,
            gov_url=gov_url
        )

        address = LawlyParser.get_json_key(json_data, 'address')
        country = LawlyParser.get_json_key(address, 'addressCountry')
        area = LawlyParser.get_json_key(address, 'area')
        region = LawlyParser.get_json_key(address, 'region')
        town = LawlyParser.get_json_key(address, 'town')
        street = LawlyParser.get_json_key(address, 'full_street')
        street_type = LawlyParser.get_json_key(address, 'street_type')
        street_number = LawlyParser.get_json_key(address, 'street_number')
        apartment_type = LawlyParser.get_json_key(address, 'apartment_type')
        apartment_number = str(LawlyParser.get_json_key(address, 'apartment_number'))
        postal_code = LawlyParser.get_json_key(address, 'postal_code')
        address = lawly_lawyer.LawyerAddress(
            country=country,
            area=area,
            region=region,
            town=town,
            street=street,
            street_type=street_type,
            street_number=street_number,
            apartment_type=apartment_type,
            apartment_number=apartment_number,
            postal_code=postal_code
        )

        description = LawlyParser.get_json_key(json_data, 'description')
        specializations = set(LawlyParser.get_json_key(json_data, 'specializations'))
        phones = set(LawlyParser.get_json_key(json_data, 'phones'))
        email = LawlyParser.get_json_key(json_data, 'email')
        status = LawlyParser.get_json_key(json_data, 'status')

        ava_dict = LawlyParser.get_json_key(json_data, 'avatar')
        ava_data = LawlyParser.get_json_key(ava_dict, 'base64')
        ava_name = LawlyParser.get_json_key(ava_dict, 'name')
        ava_extension = LawlyParser.get_json_key(ava_dict, 'extension')
        avatar = lawly_lawyer.LawyerAvatar(
            data=ava_data,
            name=ava_name,
            extension=ava_extension
        )

        lawyer = lawly_lawyer.Lawyer(
            lawyer_id=lawyer_id,
            lawyer_type=lawyer_type,
            name=lawyer_name,
            gender=gender,
            verification=lawyer_verification,
            address=address,
            phones=phones,
            description=description,
            specializations=specializations,
            email=email,
            status=status,
            avatar=avatar
        )

        return lawyer
